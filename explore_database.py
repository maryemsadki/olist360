
from sqlalchemy import text
from database import engine


def explore_tables():
    query = text("""
        SELECT
            TABLE_SCHEMA,
            TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_SCHEMA, TABLE_NAME;
    """)

    with engine.connect() as connection:
        results = connection.execute(query)

        print("\n===== TABLES DE LA BASE OlistDW =====\n")

        for row in results:
            print(f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}")


if __name__ == "__main__":
    explore_tables()
