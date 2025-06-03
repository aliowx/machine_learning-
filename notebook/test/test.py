import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, StackingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import logging
import shap
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('../../data/DummyData.csv')



df.head()

df.describe()


df.info()


target_columns = ['steps_goal', 'mvpa_mins_goal']
feature_columns = [col for col in df.columns if col not in target_columns]

feature_columns


X = df[feature_columns]
y = df[target_columns]


numerical_cols = X.select_dtypes(include=['float64', 'int64']).columns
num_imputer = SimpleImputer(strategy='mean')
X[numerical_cols] = num_imputer.fit_transform(X[numerical_cols])



data_clean = df.dropna(subset=target_columns)
X_clean = data_clean[feature_columns]
y_clean = data_clean[target_columns]


scaler = StandardScaler()
X_clean[numerical_cols] = scaler.fit_transform(X_clean[numerical_cols])



numerical_cols

data_clean = df.dropna(subset=['steps_goal', 'mvpa_mins_goal'])


data_clean

data_clean.isna().sum()

variance = data_clean.var(numeric_only=True)
non_zero_variance_cols = variance[variance > 0].index
data_clean = data_clean[non_zero_variance_cols]


correlation_matrix = data_clean.corr()


corr_steps = correlation_matrix['steps_goal'].abs().sort_values(ascending=False)
corr_mvpa = correlation_matrix['mvpa_mins_goal'].abs().sort_values(ascending=False)
corr_mvpa

top_features = pd.concat([corr_steps[1:6], corr_mvpa[1:6]]).index.unique()[:10]
top_features

selected_columns = list(top_features) + ['steps_goal', 'mvpa_mins_goal']
corr_subset = correlation_matrix.loc[selected_columns, selected_columns]
plt.figure(figsize=(10, 8))
sns.heatmap(corr_subset, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Correlation Matrix')
plt.show()


X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.4, random_state=42)

print("Shape of full data:", X_clean.shape)
print("Shape of test set:", X_test.shape)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

models = {
    'Linear Regression': MultiOutputRegressor(LinearRegression()),
    'Ridge Regression': MultiOutputRegressor(Ridge()),
    'Lasso Regression': MultiOutputRegressor(Lasso()),
    'ElasticNet': MultiOutputRegressor(ElasticNet()),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, random_state=42),
    'MLP': MultiOutputRegressor(MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)),
    'K-Nearest Neighbors': MultiOutputRegressor(KNeighborsRegressor())
}
estimators = [
    ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
    ('xgb', XGBRegressor(n_estimators=100, random_state=42)),
    ('gb', GradientBoostingRegressor(n_estimators=100, random_state=42))
]
stacked_model = StackingRegressor(estimators=estimators, final_estimator=LinearRegression())
models['Stacked Ensemble'] = stacked_model



target_specific_results = {}

results = []
for name, model in models.items():
    try:

        model.fit(X_train, y_train)
        

        y_pred = model.predict(X_test)

        rmse_steps = np.sqrt(mean_squared_error(y_test['steps_goal'], y_pred[:, 0]))
        r2_steps = r2_score(y_test['steps_goal'], y_pred[:, 0])
        rmse_mvpa = np.sqrt(mean_squared_error(y_test['mvpa_mins_goal'], y_pred[:, 1]))
        r2_mvpa = r2_score(y_test['mvpa_mins_goal'], y_pred[:, 1])
        
        results.append({
            'Model': name,
            'RMSE_steps_goal': rmse_steps,
            'R2_steps_goal': r2_steps,
            'RMSE_mvpa_mins_goal': rmse_mvpa,
            'R2_mvpa_mins_goal': r2_mvpa
        })
    except Exception as e:
        print(f"Error{name}: {e}")


for target in ['steps_goal', 'mvpa_mins_goal']:
    try:
        rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
        rf_model.fit(X_train, y_train[target])
        y_pred_target = rf_model.predict(X_test)
        
        rmse_target = np.sqrt(mean_squared_error(y_test[target], y_pred_target))
        r2_target = r2_score(y_test[target], y_pred_target)
        
        target_specific_results[target] = {'RMSE': rmse_target, 'R2': r2_target}
    except Exception as e:
        print(f"Target-Specific Model  {target}: {e}")


if results:
    results_df = pd.DataFrame(results)
    print("result the models\n")
    print(results_df)
else:
    print("there isn't any model finish\n")


print("Target-Specific Models:\n")
for target, metrics in target_specific_results.items():
    print(f"{target}: RMSE={metrics['RMSE']:.2f}, R2={metrics['R2']:.2f}")
"""
/home/ali/.cache/pypoetry/virtualenvs/backend-_rtLvpYT-py3.12/lib/python3.12/site-packages/sklearn/linear_model/_coordinate_descent.py:695: ConvergenceWarning: Objective did not converge. You might want to increase the number of iterations, check the scale of the features or consider increasing regularisation. Duality gap: 2.703e+01, tolerance: 1.250e+01
  model = cd_fast.enet_coordinate_descent(
ErrorGradient Boosting: y should be a 1d array, got an array of shape (2, 2) instead.
/home/ali/.cache/pypoetry/virtualenvs/backend-_rtLvpYT-py3.12/lib/python3.12/site-packages/sklearn/neural_network/_multilayer_perceptron.py:691: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (1000) reached and the optimization hasn't converged yet.
  warnings.warn(
/home/ali/.cache/pypoetry/virtualenvs/backend-_rtLvpYT-py3.12/lib/python3.12/site-packages/sklearn/neural_network/_multilayer_perceptron.py:691: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (1000) reached and the optimization hasn't converged yet.
  warnings.warn(
ErrorK-Nearest Neighbors: Expected n_neighbors <= n_samples_fit, but n_neighbors = 5, n_samples_fit = 2, n_samples = 2
ErrorStacked Ensemble: y should be a 1d array, got an array of shape (2, 2) instead.
result the models

               Model  RMSE_steps_goal  R2_steps_goal  RMSE_mvpa_mins_goal  \
0  Linear Regression      1579.406770       0.975055            39.700418   
1   Ridge Regression      1878.058835       0.964729            46.681504   
2   Lasso Regression       135.644039       0.999816           195.242483   
3         ElasticNet      1878.299908       0.964720            47.237489   
4      Random Forest      4964.822379       0.753505           123.136104   
5        Extra Trees       851.207475       0.992754            21.213203   
6            XGBoost       135.057363       0.999818             0.000957   
7                MLP     13693.776912      -0.875195           122.684832   

   R2_mvpa_mins_goal  
0           0.974782  
1           0.965133  
2           0.390086  
3           0.964298  
4           0.757400  
5           0.992800  
6           1.000000  
7           0.759175  
Target-Specific Models:

steps_goal: RMSE=5254.45, R2=0.72
mvpa_mins_goal: RMSE=130.38, R2=0.73"""