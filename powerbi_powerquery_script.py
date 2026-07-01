# Python Script for Power BI - Power Query Editor
# Paste this script inside Power Query -> Transform -> Run Python Script.
# Note: Ensure you have pandas, numpy, and scikit-learn installed in your Power BI Python path.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

# 'dataset' contains the input table from the previous Power Query step (Indian dataset)
df_indian = dataset.copy()

# Load JPN training dataset (Specify the absolute path if necessary)
# Example: jp_df = pd.read_excel('C:/Users/Sujal Sahu/Downloads/Market-Entry-Analysis-for-ABG-Motors-in-India---CAPSTONE-PROJECT--main/JPN_Data.xlsx')
try:
    jp_df = pd.read_excel('JPN_Data.xlsx')
except Exception:
    # Fallback to local workspace absolute path
    import os
    workspace_path = r'c:\Users\Sujal Sahu\Downloads\Market-Entry-Analysis-for-ABG-Motors-in-India---CAPSTONE-PROJECT--main'
    jp_df = pd.read_excel(os.path.join(workspace_path, 'JPN_Data.xlsx'))

# Handle NaNs and infinite values
jp_df.replace([np.inf, -np.inf], np.nan, inplace=True)
df_indian.replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop rows where essential columns are missing in training data
jp_df.dropna(subset=['CURR_AGE', 'GENDER', 'ANN_INCOME', 'PURCHASE'], inplace=True)

# Standardize GENDER values
gender_map = {'Male': 0, 'Female': 1, 'M': 0, 'F': 1}
jp_df['GENDER'] = jp_df['GENDER'].map(gender_map).fillna(0)
df_indian['GENDER'] = df_indian['GENDER'].map(gender_map).fillna(0)

# Clean Indian dataset features (fill nulls dynamically using an imputer)
X_train = jp_df[['CURR_AGE', 'GENDER', 'ANN_INCOME']]
y_train = jp_df['PURCHASE']

imputer = SimpleImputer(strategy='mean')
X_train_imp = imputer.fit_transform(X_train)

# Fit models
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_imp, y_train)

dt = DecisionTreeClassifier(max_depth=10, min_samples_leaf=4, min_samples_split=10, random_state=42)
dt.fit(X_train_imp, y_train)

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train_imp, y_train)

# Select features from Indian dataset and run prediction
X_ind = df_indian[['CURR_AGE', 'GENDER', 'ANN_INCOME']]
X_ind_imp = imputer.transform(X_ind)

df_indian['LR_PREDICTION'] = lr.predict(X_ind_imp)
df_indian['LR_PROBABILITY'] = lr.predict_proba(X_ind_imp)[:, 1]

df_indian['DT_PREDICTION'] = dt.predict(X_ind_imp)
df_indian['DT_PROBABILITY'] = dt.predict_proba(X_ind_imp)[:, 1]

df_indian['RF_PREDICTION'] = rf.predict(X_ind_imp)
df_indian['RF_PROBABILITY'] = rf.predict_proba(X_ind_imp)[:, 1]

# Reassign table back to variable 'dataset' for Power BI output
dataset = df_indian
