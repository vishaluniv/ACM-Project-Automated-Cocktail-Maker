import mysql.connector

host='localhost' 
user='root' 
passwd='rootbar'
database='bartending'


db = mysql.connector.connect(host=host, user=user, password=passwd, database=database)

mycursor = db.cursor()
print(db)
print(mycursor)


def previous(prev_drinks):

    prev_drink = []
    for drink in prev_drinks[0]:
        prev_drink.append(drink)
    return prev_drink

def prev_drink(username):
    con = mysql.connector.connect(host=host, user=user, password=passwd, database=database)
    mycursor=con.cursor()
    mycursor.execute("SELECT drinks FROM customers WHERE username=%s", (username,))
    row=mycursor.fetchone()

    return previous(row)


def signUp(username, password, conpass):
    if username == "" or password == "" or conpass=="":
        ## label will be changed or message box will appear with error code
        return 0
    elif password != conpass:
        return 1
        ##one more error, pass and confirm pass should be the same
    else:
        con = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        mycursor=con.cursor()
        query=("SELECT * FROM customers WHERE username=%s")
        value=(username,)
        mycursor.execute(query, value)
        row=mycursor.fetchone()
        if row!=None:
            #an error that the user already exists
            return 2
        else:
            #new user has been added.
            mycursor.execute("INSERT INTO customers(username, password, drinks) VALUES(%s,%s,%s)", (username, password, "0"))
            
        con.commit()
        myresult=mycursor.fetchall()
        for x in myresult:
            print(x)
        con.close()
        return 3
        ##at this point new user has been added, and we simply inform the user on the GUI

def login(username, password):
    print(username, password)
    if username == "" or password == "":
        ## label will be changed or message box will appear with error code
        return 0
       ##one more error, pass and confirm pass should be the same
    else:
        con = mysql.connector.connect(host=host, user=user, password=passwd, database=database)
        mycursor=con.cursor()
        mycursor.execute("SELECT * FROM customers WHERE username=%s and password=%s", (username, password))
        row=mycursor.fetchone()
        if row==None:
            ##the username or password is wrong
            return 1
         
        con.commit()
        myresult=mycursor.fetchall()
        for x in myresult:
            print(x)
        con.close()
        return 2




