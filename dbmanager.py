# DB execution statements
import psycopg2
import pandas as pd


def connect():
    """

    Parameters
    ----------
    user : {'admin', 'user-view'}
        connect to the db as either the admin (global permission) or view-only user (SELECT permissions).
        Default to 'admin'

    Returns
    -------
    conn
        a persisting psycopg2 connection object
    curs
        a persisting psycopg2 connection object's cursor
    """

    psql = 'socgenhackathondb.c7bxriukwua5.ap-southeast-1.rds.amazonaws.com'
    psql_port = 5432
    psql_username = 'root'
    psql_password = 'hackathon'
    psql_db = 'tentakka'

    try:
        params = {
            'database': psql_db,
            'user': psql_username,
            'password': psql_password,
            'host': psql,
            'port': psql_port
        }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()

        return conn, curs

    except Exception as e:
        print("Couldn't connect to database")
        print(e)


def disconnect(connection, cursor):
    if connection is not None:
        cursor.close()
        connection.commit()
        connection.close()


def insert_query(df, table: str, schema: str):
    """
    This function runs the input template query
    'INSERT INTO schema.table_name([col1, col2]) VALUES (val1, val2), (val3,val4)'

    Arguments
        schema: the schema name
        table: the table name
        df: the pandas.DataFrame object that contains the data,
            Note that the column names have to be the same as the columns names in the Database table

    Example
        schema = 'test'
        table = 'strategy_holdings'
        df = pd.DataFrame(data=data, columns=['col1', 'col2'])
    """
    connection, cursor = connect()

    columns = tuple(df.columns.values.tolist())
    values = [tuple(i) for i in df.values.tolist()]

    records_list_template = ','.join(['%s'] * len(values))
    insert_query = 'INSERT INTO {}.{} {} VALUES {}'.format(schema, table, columns, records_list_template).replace("'",
                                                                                                                  "")
    query = "WITH rows AS (%s RETURNING 1) SELECT count(*) FROM rows;" % (insert_query)

    query = cursor.mogrify(query)

    try:
        cursor.execute(query, values)

        print("INSERTED %d ROWS INTO %s.%s..." % (cursor.fetchall()[0][0], schema.upper(), table.upper()))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cursor.execute("rollback;")
    finally:
        disconnect(connection, cursor)


def select_all(schema, table):
    connection, cursor = connect()

    select_query = 'SELECT * FROM {}.{};'.format(schema, table).replace("'", "")
    query = cursor.mogrify(select_query)

    try:
        cursor.execute(query)
        colnames = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(cursor.fetchall(), columns=colnames)

        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cursor.execute("rollback;")
    finally:
        disconnect(connection, cursor)


def select_where(schema, table, column, condition, parameter):
    connection, cursor = connect()

    select_where_query = 'SELECT * FROM {}.{} WHERE {} {} \'{}\''.format(schema,
                                                                         table,
                                                                         column.replace("'", ""),
                                                                         condition.replace("'", ""),
                                                                         parameter)
    query = cursor.mogrify(select_where_query)

    try:
        cursor.execute(query)
        colnames = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(cursor.fetchall(), columns=colnames)

        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cursor.execute("rollback;")
    finally:
        disconnect(connection, cursor)


conn, curs = connect()