import pymysql

def exists (table_name,  **kwargs):
    status = []
    try:
        db = pymysql.connect(host="dev.satyukt.com", user="shiyaam", password="Devwrite@123", db = "fms_app")
        cursor = db.cursor()
        
        # Start building the query
        sql_query = f"SELECT EXISTS(SELECT 1 FROM {table_name}"
        
        # Check if there are any conditions passed in kwargs
        if kwargs:
            conditions = []
            for key, value in kwargs.items():
                # If the key is 'date', apply DATE() function to the column to ignore time
                if key.lower() == 'date':
                    conditions.append(f"DATE({key}) = %s")  # Use the DATE() function for the date column
                else:
                    conditions.append(f"`{key}` = %s")
            sql_query += " WHERE " + " AND ".join(conditions) + ")"
        
        # Prepare the values tuple
        values = tuple(kwargs.values())
        # print("sql_query:",sql_query, "val: ",values )
        # Execute the query
        cursor.execute(sql_query, values)
        status = cursor.fetchall()[0][0]
        
    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])
    finally:
        cursor.close()
        db.close()
    return status


# exists("user_credentials", user_id=20656,isAdmin=1)
# exists("polygonStore",id=98405,active=1)
#print(exists("user_registration",mobile_no=9976334386))


# FETCH Function
import pymysql
def fetch(table_name, columns="*", limit=None, offset=None, order_by=None, **kwargs):
    fetch_data = []
    try:
        db = pymysql.connect(host="dev.satyukt.com", user="shiyaam", password="Devwrite@123", db = "fms_app")
        cursor = db.cursor()
        
        # Prepare the SELECT clause
        if isinstance(columns, str) and columns == "*":
            select_clause = "*"
        elif isinstance(columns, list):
            select_clause = ', '.join([f"`{col}`" for col in columns])
        else:
            select_clause = columns
            
        # Prepare the WHERE clause
        sql_query = f"SELECT {select_clause} FROM {table_name}"
        values = []
        if kwargs:
            conditions = []
            values = []
            for key, value in kwargs.items():
                if isinstance(value, (list, tuple)):  # Handle IN condition
                    placeholders = ', '.join(['%s'] * len(value))  # Creates '%s, %s, %s'
                    conditions.append(f"`{key}` IN ({placeholders})")
                    values.extend(value)  # Ensure all values are passed correctly
                elif key.lower() == 'date':  # Handle DATE conditions
                    conditions.append(f"DATE({key}) = %s")
                    values.append(value)
                else:
                    conditions.append(f"`{key}` = %s")
                    values.append(value)

            sql_query += " WHERE " + " AND ".join(conditions)
        
        if order_by is not None:
            sql_query += f" ORDER BY {order_by}"
            
        if limit is not None:
            sql_query += f" LIMIT {limit}"
            if offset is not None:
                sql_query += f" OFFSET {offset}"
                
        # Execute the query
        cursor.execute(sql_query, values)
        fetch_data = cursor.fetchall()
    
    except pymysql.MySQLError as e:
        fetch_data = [0, f"Database error: {e.args[1]}"]
    except Exception as e:
        fetch_data = [0, f"Error: {str(e)}"]
    finally:    
        cursor.close()
        db.close()
    
    return fetch_data



# from datetime import datetime
# today_for_api_hits = datetime.today().date()
# print(fetch("api_hits", columns=["count", "date"], referral_code = 329, date = str("2025-04-30")))

# farmer = fetch("polygonStore", columns=["polyinfo"])
# print(fetch("polygonStore", columns=["polyinfo","clientID"],id = "113860")[0])

# t = fetch("polygonStore",columns=["area"],clientID=17663)
#t = fetch("polygonStore",columns=["area"], id=17663)
# total_sum = sum(x[0] for x in t)
# print(total_sum)


def insert(table_name, **kwargs):
    status = []
    try:
        # db = pymysql.connect(host="micro.satyukt.com", user="readuser", password="Secret@123", db="dummy_api")
        db = pymysql.connect(host="dev.satyukt.com", user="shiyaam", password="Devwrite@123", db = "fms_app")
        cursor = db.cursor()

        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s' for _ in kwargs])
        values = tuple(kwargs.values())

        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            cursor.execute(sql_query, values)
            db.commit()
            if table_name == "polygonStore":
                inserted_id = cursor.lastrowid
                status.append([inserted_id, "successfully inserted"])
            else:
                status.append([1, "successfully inserted"])
        except pymysql.MySQLError as e:
            db.rollback()
            if e.args[0] == 1062:  # MySQL error code for duplicate entry
                status.append([0, "Value already exists"])
            else:
                status.append([0, f"MySQL error: {e.args[1]}"])
        finally:
            cursor.close()
            db.close()
            
    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])
        
    return status

# dbs.insert("api_hits", user_id=user_id,farm_id=farm_id,API_name=API_name,Time=datetime.now())[0]
# insert("polygonStore",)

# update("table",{"Conditon_to_chec":VALUE}, SET_value= VALUE)
import pymysql
def update(table_name, conditions, **kwargs):
    status = []
    try:
        # db = pymysql.connect(host="micro.satyukt.com", user="readuser", password="Secret@123", db="dummy_api")
        db = pymysql.connect(host="dev.satyukt.com", user="shiyaam", password="Devwrite@123", db = "fms_app")
        cursor = db.cursor()

        set_clause = ', '.join([f"{key} = %s" for key in kwargs])
        values = list(kwargs.values())

        condition_clause = ' AND '.join([f"{key} = %s" for key in conditions])
        condition_values = list(conditions.values())

        all_values = values + condition_values

        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"
        # print("sql_query:",sql_query, all_values)

        try:
            cursor.execute(sql_query, all_values)
            db.commit()
            if cursor.rowcount > 0:
                status.append([1, "Updated successfully"])
            else:
                status.append([0, "No rows matched the condition"])
        except pymysql.MySQLError as e:
            db.rollback()
            status.append([0, f"MySQL error: {e.args[1]}"])
        finally:
            cursor.close()
            db.close()

    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])

    return status

import pymysql
def delete(table_name, **conditions):
    status = []
    try:
        db = pymysql.connect(host="dev.satyukt.com", user="shiyaam", password="Devwrite@123", db="fms_app")
        cursor = db.cursor()

        # Build the WHERE clause from conditions
        condition_clause = ' AND '.join([f"{key} = %s" for key in conditions])
        condition_values = list(conditions.values())

        sql_query = f"DELETE FROM {table_name} WHERE {condition_clause}"

        try:
            cursor.execute(sql_query, condition_values)
            db.commit()
            if cursor.rowcount > 0:
                status.append([1, "Deleted successfully"])
            else:
                status.append([0, "No rows matched the condition"])
        except pymysql.MySQLError as e:
            db.rollback()
            status.append([0, f"MySQL error: {e.args[1]}"])
        finally:
            cursor.close()
            db.close()

    except pymysql.MySQLError as e:
        status.append([0, f"Database error: {e.args[1]}"])
    except Exception as e:
        status.append([0, f"Error: {str(e)}"])

    return status

# t = update("7015_vendor_payment",{"clientID":74980},validity=0)[0]
# update("api_hits",{"referral_code":329,"Date(date)":"2025-04-30"}, count=53)