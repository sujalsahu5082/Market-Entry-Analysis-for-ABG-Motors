import os
import json
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
from sklearn.impute import SimpleImputer

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Cache for analytical results to avoid recomputing on every request
CACHE = {}

def load_and_prepare_data():
    print("Loading datasets...")
    # Read files
    in_df = pd.read_excel('IN_Data.xlsx')
    jp_df = pd.read_excel('JPN_Data.xlsx')
    
    # Handle infinite values
    in_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    jp_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Drop rows with NaN in essential columns
    in_df.dropna(subset=['CURR_AGE', 'GENDER', 'ANN_INCOME'], inplace=True)
    jp_df.dropna(subset=['CURR_AGE', 'GENDER', 'ANN_INCOME', 'AGE_CAR', 'PURCHASE'], inplace=True)
    
    # Standardize Gender mapping
    gender_map = {'Male': 0, 'Female': 1, 'M': 0, 'F': 1}
    jp_df['GENDER'] = jp_df['GENDER'].map(gender_map)
    in_df['GENDER'] = in_df['GENDER'].map(gender_map)
    
    # Fill remaining NaNs if any
    jp_df['GENDER'] = jp_df['GENDER'].fillna(0)
    in_df['GENDER'] = in_df['GENDER'].fillna(0)
    
    return jp_df, in_df

def train_models(jp_df, in_df):
    print("Training models...")
    
    # Define models
    models_config = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    }
    
    # --- 1. Train 4-Feature Models (for Japanese data analysis and single customer predictor with AGE_CAR) ---
    X4 = jp_df[['CURR_AGE', 'GENDER', 'ANN_INCOME', 'AGE_CAR']]
    y4 = jp_df['PURCHASE']
    X4_train, X4_test, y4_train, y4_test = train_test_split(X4, y4, test_size=0.2, random_state=42)
    
    imputer4 = SimpleImputer(strategy='mean')
    X4_train_imp = imputer4.fit_transform(X4_train)
    X4_test_imp = imputer4.transform(X4_test)
    
    trained_models_4 = {}
    metrics_4 = {}
    
    for name, model in models_config.items():
        # Copy model to avoid shared state
        clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42) if name == 'Random Forest' else \
              (DecisionTreeClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, random_state=42) if name == 'Decision Tree' else \
               LogisticRegression(max_iter=1000, random_state=42))
        
        clf.fit(X4_train_imp, y4_train)
        y_pred = clf.predict(X4_test_imp)
        
        # Calculate ROC Curve
        if hasattr(clf, "predict_proba"):
            y_prob = clf.predict_proba(X4_test_imp)[:, 1]
        else:
            y_prob = clf.decision_function(X4_test_imp)
            
        fpr, tpr, _ = roc_curve(y4_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        # Feature importances
        importances = {}
        if name == 'Logistic Regression':
            for col, coef in zip(X4.columns, clf.coef_[0]):
                importances[col] = float(abs(coef))
        else:
            for col, imp in zip(X4.columns, clf.feature_importances_):
                importances[col] = float(imp)
                
        # Normalize importances
        total_imp = sum(importances.values())
        if total_imp > 0:
            importances = {k: v / total_imp for k, v in importances.items()}
        
        cm = confusion_matrix(y4_test, y_pred)
        
        trained_models_4[name] = clf
        metrics_4[name] = {
            'accuracy': float(accuracy_score(y4_test, y_pred)),
            'precision': float(precision_score(y4_test, y_pred)),
            'recall': float(recall_score(y4_test, y_pred)),
            'f1': float(f1_score(y4_test, y_pred)),
            'confusion_matrix': cm.tolist(),
            'roc': {'fpr': fpr.tolist()[::20], 'tpr': tpr.tolist()[::20], 'auc': float(roc_auc)}, # Subsample for size
            'feature_importances': importances
        }
        
    # --- 2. Train 3-Feature Models (for predicting on Indian Dataset where AGE_CAR is missing) ---
    X3 = jp_df[['CURR_AGE', 'GENDER', 'ANN_INCOME']]
    y3 = jp_df['PURCHASE']
    X3_train, X3_test, y3_train, y3_test = train_test_split(X3, y3, test_size=0.2, random_state=42)
    
    imputer3 = SimpleImputer(strategy='mean')
    X3_train_imp = imputer3.fit_transform(X3_train)
    X3_test_imp = imputer3.transform(X3_test)
    
    trained_models_3 = {}
    metrics_3 = {}
    
    for name, model in models_config.items():
        clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42) if name == 'Random Forest' else \
              (DecisionTreeClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, random_state=42) if name == 'Decision Tree' else \
               LogisticRegression(max_iter=1000, random_state=42))
              
        clf.fit(X3_train_imp, y3_train)
        y_pred = clf.predict(X3_test_imp)
        
        if hasattr(clf, "predict_proba"):
            y_prob = clf.predict_proba(X3_test_imp)[:, 1]
        else:
            y_prob = clf.decision_function(X3_test_imp)
            
        fpr, tpr, _ = roc_curve(y3_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        importances = {}
        if name == 'Logistic Regression':
            for col, coef in zip(X3.columns, clf.coef_[0]):
                importances[col] = float(abs(coef))
        else:
            for col, imp in zip(X3.columns, clf.feature_importances_):
                importances[col] = float(imp)
                
        total_imp = sum(importances.values())
        if total_imp > 0:
            importances = {k: v / total_imp for k, v in importances.items()}
            
        cm = confusion_matrix(y3_test, y_pred)
        
        trained_models_3[name] = clf
        metrics_3[name] = {
            'accuracy': float(accuracy_score(y3_test, y_pred)),
            'precision': float(precision_score(y3_test, y_pred)),
            'recall': float(recall_score(y3_test, y_pred)),
            'f1': float(f1_score(y3_test, y_pred)),
            'confusion_matrix': cm.tolist(),
            'roc': {'fpr': fpr.tolist()[::20], 'tpr': tpr.tolist()[::20], 'auc': float(roc_auc)},
            'feature_importances': importances
        }
        
    # --- 3. Run predictions on Indian dataset using 3-feature models ---
    print("Running predictions on Indian dataset...")
    X_indian = in_df[['CURR_AGE', 'GENDER', 'ANN_INCOME']]
    X_indian_imp = imputer3.transform(X_indian)  # use the same imputer trained on Japanese data
    
    indian_predictions = {}
    for name, clf in trained_models_3.items():
        y_pred_ind = clf.predict(X_indian_imp)
        y_prob_ind = clf.predict_proba(X_indian_imp)[:, 1] if hasattr(clf, "predict_proba") else clf.decision_function(X_indian_imp)
        
        indian_predictions[name] = {
            'potential_buyers': int(sum(y_pred_ind)),
            'total_customers': int(len(in_df)),
            'buyer_rate': float(sum(y_pred_ind) / len(in_df)),
            'probabilities': y_prob_ind.tolist()[::50] # Subsample for client-side distribution charts
        }
        
    return trained_models_4, metrics_4, trained_models_3, metrics_3, indian_predictions, imputer4, imputer3

# Prepare directory structure
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Global variables for models and data summary
jp_df_global, in_df_global = load_and_prepare_data()
models4, metrics4, models3, metrics3, ind_preds, imp4, imp3 = train_models(jp_df_global, in_df_global)

# Compute EDA summaries once
def get_eda_data():
    print("Computing EDA statistics...")
    # Age bins
    age_bins = [0, 20, 30, 40, 50, 60, 70, 80]
    age_labels = ['0-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80']
    
    jp_df_global['AGE_GROUP'] = pd.cut(jp_df_global['CURR_AGE'], bins=age_bins, labels=age_labels)
    in_df_global['AGE_GROUP'] = pd.cut(in_df_global['CURR_AGE'], bins=age_bins, labels=age_labels)
    
    # Income bins (normalize or scale to groups)
    # JPN Income has different range than Indian Income. Let's make relative income percentiles
    jp_df_global['INCOME_GROUP'] = pd.qcut(jp_df_global['ANN_INCOME'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    in_df_global['INCOME_GROUP'] = pd.qcut(in_df_global['ANN_INCOME'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    jp_age_purchase = jp_df_global.groupby('AGE_GROUP', observed=False)['PURCHASE'].mean().fillna(0).to_dict()
    jp_income_purchase = jp_df_global.groupby('INCOME_GROUP', observed=False)['PURCHASE'].mean().fillna(0).to_dict()
    
    # Distributions
    jp_age_dist = jp_df_global['AGE_GROUP'].value_counts().sort_index().to_dict()
    in_age_dist = in_df_global['AGE_GROUP'].value_counts().sort_index().to_dict()
    
    # Gender purchase rate
    jp_gender_purchase = jp_df_global.groupby('GENDER', observed=False)['PURCHASE'].mean().to_dict()
    
    # Convert keys to strings
    return {
        'jp_age_purchase': {str(k): float(v) for k, v in jp_age_purchase.items()},
        'jp_income_purchase': {str(k): float(v) for k, v in jp_income_purchase.items()},
        'jp_age_dist': {str(k): int(v) for k, v in jp_age_dist.items()},
        'in_age_dist': {str(k): int(v) for k, v in in_age_dist.items()},
        'jp_gender_purchase': {str(k): float(v) for k, v in jp_gender_purchase.items()},
        'jp_income_mean': float(jp_df_global['ANN_INCOME'].mean()),
        'in_income_mean': float(in_df_global['ANN_INCOME'].mean()),
        'jp_age_mean': float(jp_df_global['CURR_AGE'].mean()),
        'in_age_mean': float(in_df_global['CURR_AGE'].mean()),
        'jp_total_count': int(len(jp_df_global)),
        'in_total_count': int(len(in_df_global))
    }

CACHE['eda'] = get_eda_data()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    return jsonify(CACHE['eda'])

@app.route('/api/models')
def get_model_metrics():
    return jsonify({
        'models_4_features': metrics4,
        'models_3_features': metrics3
    })

@app.route('/api/predict_indian_market')
def get_indian_market_predictions():
    return jsonify(ind_preds)

@app.route('/api/predict', methods=['POST'])
def predict_probability():
    data = request.json
    try:
        age = float(data.get('age'))
        gender = int(data.get('gender'))
        income = float(data.get('income'))
        age_car = data.get('age_car') # Can be None or value
        
        # Decide if using 3-feature or 4-feature model
        res = {}
        if age_car is not None:
            # Predict with 4-feature model
            age_car = float(age_car)
            features = np.array([[age, gender, income, age_car]])
            features_imp = imp4.transform(features)
            
            for name, clf in models4.items():
                prob = clf.predict_proba(features_imp)[0, 1] if hasattr(clf, "predict_proba") else clf.decision_function(features_imp)[0]
                pred = int(clf.predict(features_imp)[0])
                res[name] = {
                    'probability': float(prob),
                    'prediction': pred
                }
        else:
            # Predict with 3-feature model
            features = np.array([[age, gender, income]])
            features_imp = imp3.transform(features)
            
            for name, clf in models3.items():
                prob = clf.predict_proba(features_imp)[0, 1] if hasattr(clf, "predict_proba") else clf.decision_function(features_imp)[0]
                pred = int(clf.predict(features_imp)[0])
                res[name] = {
                    'probability': float(prob),
                    'prediction': pred
                }
        return jsonify({'status': 'success', 'predictions': res})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    print("Starting ABG Motors Market Entry Analysis Server...")
    app.run(host='0.0.0.0', port=5000, debug=False)
