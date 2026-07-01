import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

def main():
    print("Step 1: Loading JPN and IN datasets...")
    jp_df = pd.read_excel('JPN_Data.xlsx')
    in_df = pd.read_excel('IN_Data.xlsx')
    
    # Handle infinite values
    jp_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    in_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Drop rows with missing target or essential inputs in training data
    jp_df.dropna(subset=['CURR_AGE', 'GENDER', 'ANN_INCOME', 'PURCHASE'], inplace=True)
    
    # Keep copy of original index for Indian data to merge predictions safely
    in_df_original = in_df.copy()
    in_df.dropna(subset=['CURR_AGE', 'GENDER', 'ANN_INCOME'], inplace=True)
    
    print(f"Loaded JPN shape: {jp_df.shape}, Loaded IN shape: {in_df.shape}")
    
    # Standardize gender mappings
    gender_map = {'Male': 0, 'Female': 1, 'M': 0, 'F': 1}
    jp_df['GENDER'] = jp_df['GENDER'].map(gender_map).fillna(0)
    in_df['GENDER'] = in_df['GENDER'].map(gender_map).fillna(0)
    
    # Train-test split on JPN dataset using only common columns (3 features)
    X = jp_df[['CURR_AGE', 'GENDER', 'ANN_INCOME']]
    y = jp_df['PURCHASE']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    imputer = SimpleImputer(strategy='mean')
    X_train_imp = imputer.fit_transform(X_train)
    
    # Train models
    print("Step 2: Training classifiers...")
    
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_imp, y_train)
    
    dt = DecisionTreeClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, random_state=42)
    dt.fit(X_train_imp, y_train)
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train_imp, y_train)
    
    print("Classifiers trained successfully.")
    
    # Predict on Indian dataset
    print("Step 3: Predicting buying likelihood on Indian dataset...")
    X_indian = in_df[['CURR_AGE', 'GENDER', 'ANN_INCOME']]
    X_indian_imp = imputer.transform(X_indian)
    
    # Generate columns
    in_df['LR_PREDICTION'] = lr.predict(X_indian_imp)
    in_df['LR_PROBABILITY'] = lr.predict_proba(X_indian_imp)[:, 1]
    
    in_df['DT_PREDICTION'] = dt.predict(X_indian_imp)
    in_df['DT_PROBABILITY'] = dt.predict_proba(X_indian_imp)[:, 1]
    
    in_df['RF_PREDICTION'] = rf.predict(X_indian_imp)
    in_df['RF_PROBABILITY'] = rf.predict_proba(X_indian_imp)[:, 1]
    
    # Merge predictions back into original dataset structure to preserve missing values rows (as NaNs) if needed
    print("Step 4: Merging results and exporting to Excel...")
    final_df = in_df_original.merge(
        in_df[['ID', 'LR_PREDICTION', 'LR_PROBABILITY', 'DT_PREDICTION', 'DT_PROBABILITY', 'RF_PREDICTION', 'RF_PROBABILITY']],
        on='ID',
        how='left'
    )
    
    # Save to Excel
    output_filename = 'cleaned_indian_with_predictions.xlsx'
    final_df.to_excel(output_filename, index=False)
    print(f"Export completed! File saved to '{output_filename}'.")

if __name__ == '__main__':
    main()
