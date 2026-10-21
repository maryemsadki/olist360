
from sqlalchemy import text
from database import engine


TABLES = [
    "DimCustomer",
    "DimDate",
    "DimProduct",
    "DimSeller",
    "FactDelivery",
    "FactSales",
    "ML_ChurnRisk",
    "ML_CustomerSegments",
    "ML_DeliveryPredictions",
    "ML_ModelComparison",
    "ML_Recommendations",
    "ML_SalesForecast",
]


def explore_data():
    with engine.connect() as connection:

        for table in TABLES:
            query = text(
                f"SELECT COUNT_BIG(*) "
                f"FROM [olist].[{table}]"
            )

            count = connection.execute(query).scalar_one()

            print(f"{table}: {count} lignes")


if __name__ == "__main__":
    explore_data()
