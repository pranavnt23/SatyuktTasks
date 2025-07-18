import pymysql

DB_CONFIG = {
    "host": "3.14.103.172",
    "user": "readuser",
    "password": "Secret@123",
    "db": "dummy_api"
}

def exists(table_name, **kwargs):
    status = []
    db = cursor = None
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()

        sql_query = f"SELECT EXISTS(SELECT 1 FROM {table_name}"
        if kwargs:
            conditions = []
            for key in kwargs:
                if key.lower() == 'date':
                    conditions.append(f"DATE({key}) = %s")
                else:
                    conditions.append(f"`{key}` = %s")
            sql_query += " WHERE " + " AND ".join(conditions) + ")"

        values = tuple(kwargs.values())
        cursor.execute(sql_query, values)
        status = cursor.fetchone()[0]

    except pymysql.MySQLError as e:
        status = [0, f"Database error: {e.args[1]}"]
    except Exception as e:
        status = [0, f"Error: {str(e)}"]
    finally:
        if cursor: cursor.close()
        if db: db.close()
    return status


def fetch(table_name, columns="*", limit=None, offset=None, order_by=None, **kwargs):
    fetch_data = []
    db = cursor = None
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()

        if isinstance(columns, list):
            select_clause = ', '.join(f"`{col}`" for col in columns)
        else:
            select_clause = columns

        sql_query = f"SELECT {select_clause} FROM {table_name}"
        values = []

        if kwargs:
            conditions = []
            for key, value in kwargs.items():
                if isinstance(value, (list, tuple)):
                    placeholders = ', '.join(['%s'] * len(value))
                    conditions.append(f"`{key}` IN ({placeholders})")
                    values.extend(value)
                elif key.lower() == 'date':
                    conditions.append(f"DATE({key}) = %s")
                    values.append(value)
                else:
                    conditions.append(f"`{key}` = %s")
                    values.append(value)
            sql_query += " WHERE " + " AND ".join(conditions)

        if order_by:
            sql_query += f" ORDER BY {order_by}"
        if limit is not None:
            sql_query += f" LIMIT {limit}"
            if offset is not None:
                sql_query += f" OFFSET {offset}"

        cursor.execute(sql_query, values)
        fetch_data = cursor.fetchall()

    except pymysql.MySQLError as e:
        fetch_data = [0, f"Database error: {e.args[1]}"]
    except Exception as e:
        fetch_data = [0, f"Error: {str(e)}"]
    finally:
        if cursor: cursor.close()
        if db: db.close()
    return fetch_data


def insert(table_name, **kwargs):
    status = []
    db = cursor = None
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()

        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        values = tuple(kwargs.values())

        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            cursor.execute(sql_query, values)
            db.commit()
            if table_name == "polygonStore":
                status.append([cursor.lastrowid, "successfully inserted"])
            else:
                status.append([1, "successfully inserted"])
        except pymysql.MySQLError as e:
            db.rollback()
            if e.args[0] == 1062:
                status.append([0, "Value already exists"])
            else:
                status.append([0, f"MySQL error: {e.args[1]}"] if len(e.args) > 1 else [0, str(e)])

    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])
    finally:
        if cursor: cursor.close()
        if db: db.close()
    return status


def update(table_name, conditions, **kwargs):
    status = []
    db = cursor = None
    try:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()

        set_clause = ', '.join(f"{key} = %s" for key in kwargs)
        where_clause = ' AND '.join(f"{key} = %s" for key in conditions)

        values = list(kwargs.values()) + list(conditions.values())

        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        try:
            cursor.execute(sql_query, values)
            db.commit()
            if cursor.rowcount > 0:
                status.append([1, "Updated successfully"])
            else:
                status.append([0, "No rows matched the condition"])
        except pymysql.MySQLError as e:
            db.rollback()
            status.append([0, f"MySQL error: {e.args[1]}"] if len(e.args) > 1 else [0, str(e)])

    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])
    finally:
        if cursor: cursor.close()
        if db: db.close()
    return status


def delete(table_name, **conditions):
    status = []
    db = cursor = None
    try:
        db = pymysql.connect(
            host="dev.satyukt.com",
            user="shiyaam",
            password="Devwrite@123",
            db="fms_app"
        )
        cursor = db.cursor()

        where_clause = ' AND '.join(f"{key} = %s" for key in conditions)
        values = list(conditions.values())

        sql_query = f"DELETE FROM {table_name} WHERE {where_clause}"

        try:
            cursor.execute(sql_query, values)
            db.commit()
            if cursor.rowcount > 0:
                status.append([1, "Deleted successfully"])
            else:
                status.append([0, "No rows matched the condition"])
        except pymysql.MySQLError as e:
            db.rollback()
            status.append([0, f"MySQL error: {e.args[1]}"] if len(e.args) > 1 else [0, str(e)])

    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])
    finally:
        if cursor: cursor.close()
        if db: db.close()
    return status
