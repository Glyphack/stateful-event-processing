from typing import Any, Dict

def create_tables_queries(
    conn,
    conf: Dict[str, Any],
) -> None:
    """ Create db tables with given config """
    cur = conn.cursor()

    schema = ','.join(conf['table_schema'])
    query = (
        f"CREATE TABLE if not exists {conf['table_name']} ("
        f"{schema});"
    )

    print(f'Executing: {query}')
        
    cur.execute(query)
    conn.commit()
