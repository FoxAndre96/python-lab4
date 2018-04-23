import pymysql

if __name__ == "__main__":
    # 1. prepare the SQL query
    sql = "select * from to_do_list"

    # 2. create the connection and connect
    connection = pymysql.connect(user="root", password="passwordserver", host="localhost", database="tasks")

    # 3. get a cursor
    cursor = connection.cursor()
    # 4. execute the query
    cursor.execute(sql)
    # 5. fetch the results from the DB
    result = cursor.fetchall()
    # 6. print the results
    print(result)
    # 7. close the cursor
    cursor.close()

    # 8. close the connection
    connection.close()