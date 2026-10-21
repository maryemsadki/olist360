import pandas as pd
import numpy as np
import os
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Connexion à la base
engine = create_engine(
    "mssql+pyodbc://@DESKTOP-7FSHKDT\\SQLEXPRESS/OlistDW"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# 2. Chargement des données
df = pd.read_sql("SELECT * FROM olist.vw_ML_Orders", engine)
df['PurchaseDate'] = pd.to_datetime(df['PurchaseDate'])
print("Données chargées :", df.shape)

# 3. Nettoyage
d = df.dropna(subset=['DeliveryDays']).copy()
d = d[(d['DeliveryDays'] > 0) & (d['DeliveryDays'] < 100)]
d['SameState'] = (d['CustomerState'] == d['SellerState']).astype(int)
print("Après nettoyage :", d.shape)

# 4. Préparation features / cible
features = ['Weight','Length','Height','Width','FreightValue','Price',
            'NbItems','OrderMonth','SameState','CustomerState','SellerState','Category']
X = pd.get_dummies(d[features], columns=['CustomerState','SellerState','Category'], drop_first=True)
y = d['DeliveryDays']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Entraînement des 3 modèles
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1),
    'XGBoost': XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.05, random_state=42)
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    results.append([name, mae, rmse, r2])
    print(f"{name} -> MAE={mae:.2f}  RMSE={rmse:.2f}  R2={r2:.3f}")

results_df = pd.DataFrame(results, columns=['Model','MAE','RMSE','R2'])

# 6. Choisir automatiquement le meilleur (le plus petit MAE)
best_name = results_df.loc[results_df['MAE'].idxmin(), 'Model']
best_model = models[best_name]
print(f"\nMeilleur modèle : {best_name}")

# 7. Sauvegarder le modèle entraîné
os.makedirs('../backend/models', exist_ok=True)
joblib.dump(best_model, '../backend/models/delivery_model.pkl')
joblib.dump(list(X.columns), '../backend/models/delivery_model_columns.pkl')
print("Modèle sauvegardé dans backend/models/")

# 8. Exporter aussi les prédictions et la comparaison vers SQL
d['PredictedDeliveryDays'] = best_model.predict(X)
output = d[['OrderID','DeliveryDays','PredictedDeliveryDays']]
output.columns = ['OrderID','ActualDeliveryDays','PredictedDeliveryDays']
output.to_sql('ML_DeliveryPredictions', engine, schema='olist', if_exists='replace', index=False)
results_df.to_sql('ML_ModelComparison', engine, schema='olist', if_exists='replace', index=False)
print("Résultats exportés vers SQL.")