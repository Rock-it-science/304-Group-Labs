import mysql.connector
try:
    cnx = mysql.connector.connect(user='cphillip', password='55712319', host='cosc304.ok.ubc.ca', database='workson')
    cursor = cnx.cursor()
    query = "SELECT ename, salary FROM emp"                
    cursor.execute(query)
    for (ename, salary) in cursor:
        print(ename, salary)
    cursor.close()
except mysql.connector.Error as err:  
    print(err)
finally:
    cnx.close()