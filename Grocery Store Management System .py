import mysql.connector
from tabulate import tabulate
from datetime import date

#Get the current date
current_date = date.today()

db = mysql.connector.connect(host="localhost", user="root", password="mysql2022")
cursor = db.cursor()

#Create Database 'Grocery_Store'
def create_database():
    try:
        cursor.execute("CREATE DATABASE grocery_store;")
        cursor.execute("USE grocery_store;")

        #Create Table Customer
        cursor.execute("CREATE TABLE CUSTOMER(Name varchar(20), Contact_Number varchar(10) NOT NULL);")
        
        #Create Table Sales
        cursor.execute("CREATE TABLE SALES(Contact_number varchar(10), DATE date, Item_Purchased varchar(30), Quantity int, Cost float);")

        #Create Table Products
        cursor.execute("CREATE TABLE Products(Product_Name varchar(20), Cost float);")
        cursor.execute("INSERT INTO Products VALUES('Cheese', 200);")
        cursor.execute("INSERT INTO Products VALUES('Top Ramen', 100);")
        cursor.execute("INSERT INTO Products VALUES('L´Oréal Hair Gel', 2000);")
        cursor.execute("INSERT INTO Products VALUES('Oreo Biscuits', 135);")
        cursor.execute("INSERT INTO Products VALUES('Dairy Milk Chocolate', 60);")
        cursor.execute("INSERT INTO Products VALUES('Moisturizer', 1000);")
        cursor.execute("INSERT INTO Products VALUES('Shower Gel', 200);")
        cursor.execute("INSERT INTO Products VALUES('Toothpaste', 75);")
        cursor.execute("INSERT INTO Products VALUES('Moisturizer', 1000);")
        db.commit()

        purpose()
    except:
        cursor.execute("USE grocery_store;")
        purpose()
        
#Purpose
def purpose():
    cursor.execute("USE grocery_store")
    print(" ")
    print("*** GROCERY STORE MANAGEMENT SYSTEM ***")
    print(" ")
    print("1. Enter Customer Purchase Details")
    print("2. Show the details of all customers")
    print("3. Show the details of a specific customer")
    print("4. Show the details of all available products")
    print("5. Show the details of a specific product")
    print("6. Show Purchase History")
    print("7. Show the purchase history of a specific customer")
    print("8. Permanently Delete Purchase History")
    print("9. Delete a specific record")
    print(" ")
    choice = int(input("Enter the number corresponding to the action you want to perform: "))
    print(" ")
    if choice==1:
        print("********************************")
        all_products()
        print("********************************")
        print(" ")
        create()
    elif choice==2:
        all_customers()
    elif choice==3:
        customer_details()
    elif choice==4:
        all_products()
    elif choice==5:
        product_details()
    elif choice==6:
        purchase_history()
    elif choice==7:
        customer_purchase_history()
    elif choice==8:
        delete_history()
    elif choice==9:
        delete_record()
    print(" ")

#Enter Customer Purchase Details
def create():
    name = input("Enter the customer name: ")
    contact = input("Enter the Contact Number: ")

    #Enter data into Customer Table
    sql_customer = "INSERT INTO CUSTOMER VALUES(%s, %s);"
    val_customer = (name, contact)
    cursor.execute(sql_customer, val_customer)
    db.commit()

    purchase = "y"
    items_purchased = []
    while purchase=="y":
        item = input("Enter the item name: ")

        try:
            qty = int(input("Enter Quantity: "))
        except ValueError:
            qty = 1
         
        #Fetch the cost of the item
        cursor.execute(f"SELECT COST FROM PRODUCTS WHERE Product_Name='{item}';")
        cost = cursor.fetchall()
        final_cost = cost[0][0] * qty 
        
        #Enter data into SALES Table
        sql_sales = "INSERT INTO SALES VALUES(%s, %s, %s, %s, %s)"
        val_sales = (contact, current_date, item, qty, final_cost)
        cursor.execute(sql_sales, val_sales)
        db.commit()

        purchase = input("Add more items? (y/n): ")
    
    print(" ")
    print("*RECORD ADDED*")
    print(" ")

#Show the details of all customers
def all_customers():
    cursor.execute("SELECT Name, Contact_Number FROM CUSTOMER;")
    result = cursor.fetchall()
    print(" ")
    print(tabulate(result, headers=["Name", "Contact Number"]))

#Show the details of a specific customer
def customer_details():
    customer_name = input("Enter the name of the customer whose details you're looking for: ")
    cursor.execute(f"SELECT Name, Contact_Number FROM CUSTOMER WHERE Name='{customer_name}';")
    result = cursor.fetchall()
    print(" ")
    print(tabulate(result, headers=["Name", "Contact Number"]))

#Show the details of all available products
def all_products():
    cursor.execute("SELECT * FROM PRODUCTS;")
    print("Available Products:")
    print(" ")
    result = cursor.fetchall()
    print(" ")
    print(tabulate(result, headers=["Item", "Cost"]))

#Show the details of a specific product
def product_details():
    product_name = input("Enter the name of the product that you are looking for: ")
    cursor.execute(f"SELECT * FROM PRODUCTS WHERE Product_Name='{product_name}';")
    result = cursor.fetchall()
    print(" ")
    if result != []:
        print(tabulate(result, headers=["Item", "Cost"]))
    else:
        print("Product Not Available")
    
#Show Purchase History
def purchase_history():
    cursor.execute("SELECT * FROM SALES;")
    result = cursor.fetchall()
    print(" ")
    print(tabulate(result, headers=["Contact Number", "Date", "Item Purchased", "Quantity", "Cost"]))

#Show the purchase history of a specific customer
def customer_purchase_history():
    customer_name = input("Enter the name of the customer whose details you're looking for: ")
    cursor.execute(f"SELECT C.Name, C.Contact_Number, S.DATE, S.Item_Purchased, S.Quantity, S.Cost FROM CUSTOMER C, SALES S WHERE C.Contact_Number = S.Contact_Number and C.Name='{customer_name}';")
    result = cursor.fetchall()
    print(" ")
    print(tabulate(result, headers=["Name", "Contact Number", "Date", "Items Purchased", "Quantity", "Cost"]))

#Permanently Delete Purchase History
def delete_history():
    print("*** WARNING: THIS IS GOING TO PERMANENTLY ERASE ALL PURCHASE HISTORY ***")
    print (" ")
    proceed = input("Do you want to proceed? (y/n):")
    print (" ")
    
    cursor.execute("DELETE FROM CUSTOMER;")
    cursor.execute("DELETE FROM SALES;")
    db.commit()
    print("*HISTORY DELETED*")
    
#Delete a specific record
def delete_record():
    contact_info = input("Enter the Contact Number of the record that you want to delete: ")

    cursor.execute(f"DELETE FROM CUSTOMER WHERE Contact_Number='{contact_info}'")
    cursor.execute(f"DELETE FROM SALES WHERE Contact_Number='{contact_info}'")
    db.commit()
    print("*RECORD DELETED*")
    
create_database()