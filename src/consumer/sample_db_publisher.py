from typing import List
import psycopg2

conn = psycopg2.connect(
    database="sampledb",
    host="localhost",
    user="baeldung",
    password="baeldung",
    port="5432"
)


queries = [
    """CREATE TABLE if not exists sea_vessel_positions (
    id SERIAL PRIMARY KEY,
	MMSI INTEGER,
	Longitude real,
	Latitude real,
	Type char(1));"""
]

def create_tables_queries(
    queries: List[str],
) -> None:
    """ Create given tables with given queries """
    cur = conn.cursor()

    for query in queries:
        print(query)
        
        cur.execute(query)
        conn.commit()

create_tables_queries(queries)

# def create_tables(
#     table_names: List[str],
#     columns_names: List[str],
# ) -> None:
#     """ Create given tables with given columns respectively """
#     cur = conn.cursor()

#     for table, columns in zip(table_names, columns_names):
#         create_table_sql = f"CREATE TABLE if not exists {table} {columns};"
#         print(create_table_sql)
        
#         cur.execute(create_table_sql)
#         conn.commit()

# columns_names = ["(MMSI INTEGER PRIMARY KEY, Longitude real, Latitude real, Type char(1))"]
# table_names = [""]