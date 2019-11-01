import mysql.connector

# TODO: Fill in code where you see TODO

class OrderDB:
    """Application for querying an order database"""
    
    def connect(self):
        """Makes a connection to the database and returns connection to caller"""
        try:
            print("Connecting to database.")
            # TODO: Fill in your connection information
            self.cnx = mysql.connector.connect(user='cphillip', password='55712319', host='cosc304.ok.ubc.ca', database='db_cphillip')
            return self.cnx
        except mysql.connector.Error as err:  
            print(err)       
            
    def init(self):
        """Creates and initializes the database"""
        fileName = "order.ddl"

        try:
            cursor = self.cnx.cursor()
            with open(fileName, "r") as infile:
                st = infile.read()
                commands = st.split(";")
                for line in commands:                   
                    # print(line.strip("\n"))
                    line = line.strip()
                    if line == "":  # Skip blank lines
                        continue 
                        
                    cursor.execute(line)
            
            cursor.close()
            self.cnx.commit()            
        except mysql.connector.Error as err:  
            print(err)
               
    def close(self):
        try:
            print("Closing database connection.")
            self.cnx.close()
        except mysql.connector.Error as err:  
            print(err)   
            
    def listAllCustomers(self):
        """ Returns a String with all the customers in the order database.  
            Format:
                CustomerId, CustomerName
                00000, A. Anderson 

            Return:
                String containing customers"""
        
        print("Executing list all customers.")
        
        output = "CustomerId, CustomerName"
        query = "SELECT CustomerId, CustomerName FROM Customer"
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute(query)
        # TODO: Execute query and build output string
        for(CustomerId, CustomerName) in cursor:
        	output+= "\n {}, {}".format(CustomerId, CustomerName)
        return output        

    def listCustomerOrders(self, customerId):
        """ Returns a String with all the orders for a given customer id.
     
            Note: May need to use getDate(). You should not retrieve all values as Strings.

            Format:
                OrderId, OrderDate, CustomerId, EmployeeId, Total
                01001, 2002-11-08, 00001, E0000, 1610.59
                
            Returns:
                String containing orders
        """
        output = "CustomerId, OrderDate, CustomerId, EmployeeId, Total"
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute("SELECT OrderId, OrderDate, CustomerId, EmployeeId, Total FROM Orders WHERE CustomerId = {};".format(customerId))
        # TODO: Similar to listAllCustomers(), execute query and store results in a string and return the string
        for(CustomerId, OrderDate, CustomerId, EmployeeId, Total)in cursor:
        	output += "\n {} {} {} {} {}".format(OrderId, OrderDate, CustomerId, EmployeeId, Total)
        cursor.close()
        return output  
    
    def listLineItemsForOrder(self, orderId):
        """Returns a cursor with all line items for a given order id."""
        cursor = self.cnx.cursor(buffered = True)
        query = "SELECT * FROM OrderedProduct WHERE OrderId = {};".format(orderId)
        cursor.execute(query)
        # TODO: Execute the query and return a cursor
        return cursor
    
    def computeOrderTotal(self, orderId):
        """Returns a cursor with a row containing the computed order total from the lineitems (named as orderTotal) for a given order id.
             Note: Do NOT just return the Orders.Total value."""
     
        # TODO: Execute the query and return a cursor
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('SELECT SUM(Total) as orderTotal FROM Orders GROUP BY OrderId HAVING OrderId = {};'.format(orderId))
        return cursor
    
    def addCustomer(self, customerId, customerName):
        """Inserts a customer into the database"""
        cursor = self.cnx.cursor(buffered = True)
        query = 'INSERT INTO Customer VALUES ("{}", "{}");'.format(customerId, customerName)
        cursor.execute(query)
        cursor.close()
        self.cnx.commit()
        # TODO: Execute statement. Make sure to commit
        return

    def deleteCustomer(self, customerId):
        """Deletes a customer from the database"""
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('DELETE FROM Customer WHERE CustomerId = "{}";'.format(customerId))
        cursor.close()
        self.cnx.commit()
        # TODO: Execute statement. Make sure to commit
        return   
    
    def updateCustomer(self, customerId, customerName):
        """Updates a customer in the database"""
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('UPDATE Customer SET CustomerName = "{}" WHERE CustomerId = "{}";'.format(customerName, customerId))
        cursor.close()
        self.cnx.commit()
        # TODO: Execute statement. Make sure to commit
        return  
        
    def newOrder(self, orderId, customerId, orderDate, employeeId):
        """Inserts an order into the database"""
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('INSERT INTO Orders VALUES ("{}", "{}", "{}", "{}", NULL);'.format(orderId, orderDate, customerId, employeeId))
        cursor.close()
        self.cnx.commit()
        # TODO: Execute statement. Make sure to commit
        return     
        
    def newLineItem(self, orderId, proudctId, quantity, price):
        """Inserts a lineitem into the database"""
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('INSERT INTO OrderedProduct VALUES ("{}", "{}", "{}", "{}");'.format(orderId, proudctId, quantity, price))
        #cursor.execute('SELECT SUM(Price) FROM OrderedProduct ORDER BY OrderId HAVING OrderId = {}'.format(orderId))
        #total = 0
        #for tot in cursor:
        #    total = tot
        #updateOrderTotal(orderId, tot)
        #cursor.close()
        #self.cnx.commit()
        # TODO: Execute statement. Make sure to commit
        return
        
    def updateOrderTotal(self, orderId, total):
        """Updates an order total in the database"""
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('UPDATE Orders SET Total = "{}" WHERE OrderId = "{}";'.format(total, orderId))
        cursor.close()
        self.cnx.commit()
        # TODO: Execute statement. Make sure to commit
        return  

    def query1(self):
        """Returns the list of products that have not been in any order. Hint: Left join can be used instead of a subquery."""
        print("\nExecuting query #1.")
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('SELECT ProductName FROM Product WHERE ProductId NOT IN(SELECT ProductId FROM OrderedProduct);')
        # TODO: Execute the query and return a cursor
        return cursor

    def query2(self):
        """Returns the order ids and total amount where the order total does not equal the sum of quantity*price for all ordered products in the order."""
        
        print("\nExecuting query #2.")
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('SELECT Orders.OrderID,Orders.Total FROM Orders, (SELECT SUM(quantity * Price ) as tot, OrderId FROM OrderedProduct GROUP BY OrderId) as b WHERE Orders.Total <> b.tot AND Orders.OrderId = b.OrderId GROUP BY Orders.OrderId')
        # TODO: Execute the query and return a cursor  SELECT sum(quantity * Price ) FROM OrderedProduct WHERE OrderId = {}
        return cursor  

    def query3(self):
        """Return for each customer their id, name and average total order amount for orders starting on January 1, 2015 (inclusive). Only show customers that have placed at least 2 orders.
            Format:
                CustomerId, CustomerName, avgTotal
                00001, B. Brown, 489.952000
        """
        
        print("\nExecuting query #3.")
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute('SELECT C.CustomerID,C.CustomerName,AVG(O.total) as AverageTotal FROM Customer as C JOIN (SELECT * FROM Orders WHERE OrderDate > "2015-01-01") as O ON C.CustomerId = O.CustomerId GROUP BY C.CustomerId Having count(OrderId)>1;')
        # TODO: Execute the query and return a cursor
        return cursor  
    
    def query4(self):
        """ Return the employees who have had at least 2 distinct orders where some product on the order had quantity >= 5.
            Format:
                EmployeeId, EmployeeName, orderCount                
        """
        
        print("\nExecuting query #4.")
        cursor = self.cnx.cursor(buffered = True)
        cursor.execute("SELECT E.EmployeeId, E.EmployeeName, count(E.EmployeeId) as NumberOfOrders from Employee E right join (select EmployeeId from Orders O join (select OrderId from OrderedProduct op where Quantity >= 5 group by op.OrderId) op on op.OrderId=O.OrderId) X on X.EmployeeId=E.EmployeeId group by E.EmployeeId having count(E.EmployeeId) > 1")
        

        # TODO: Execute the query and return a cursor
        return cursor
    
    # Do NOT change anything below here
    def resultSetToString(self, cursor, maxrows):
        output = ""
        cols = cursor.column_names
        output += "Total columns: "+str(len(cols))+"\n"
        output += str(cols[0])
        for i in range(1,len(cols)):
            output += ", "+str(cols[i])
        for row in cursor:
            output += "\n"+str(row[0])
            for i in range(1,len(cols)):
                output += ", "+str(row[i])
        output += "\nTotal results: "+str(cursor.rowcount)
        return output
                
# Main execution for testing
orderDB = OrderDB()
orderDB.connect()
orderDB.init()

print(orderDB.listAllCustomers())
print(orderDB.listCustomerOrders("00001"))
orderDB.listLineItemsForOrder("01000")
orderDB.computeOrderTotal("01000")
orderDB.addCustomer("11111", "Fred Smith")
orderDB.updateCustomer("11111", "Freddy Smithers")
orderDB.newOrder("22222", "11111", "2015-10-31", "E0001")
orderDB.newLineItem("22222", "P0005", 5, "3.10")
orderDB.newLineItem("22222", "P0007", 5, "2.25")
orderDB.newLineItem("22222", "P0008", 5, "2.50")
orderDB.deleteCustomer("11111")
orderDB.deleteCustomer("00001")

# Queries
# Re-initialize all data
orderDB.init()
print(orderDB.resultSetToString(orderDB.query1(), 100))
print(orderDB.resultSetToString(orderDB.query2(), 100))
print(orderDB.resultSetToString(orderDB.query3(), 100))
print(orderDB.resultSetToString(orderDB.query4(), 100))
        
orderDB.close()
