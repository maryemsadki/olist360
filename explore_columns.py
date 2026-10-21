
from sqlalchemy import text
from database import engine


def explore_columns():
    query = text("""
        SELECT
            TABLE_SCHEMA,
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'olist'
        ORDER BY TABLE_NAME, ORDINAL_POSITION;
    """)

    with engine.connect() as connection:
        results = connection.execute(query)

        current_table = None

        print("\n===== STRUCTURE DES TABLES OLISTDW =====\n")

        for row in results:
            table_name = f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}"

            if table_name != current_table:
                current_table = table_name
                print(f"\n--- {table_name} ---")

            print(
                f"  {row.COLUMN_NAME} | "
                f"{row.DATA_TYPE} | "
                f"Nullable: {row.IS_NULLABLE}"
            )


if __name__ == "__main__":
    explore_columns()
