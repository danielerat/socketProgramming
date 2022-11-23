import sqlite3
from tabulate import tabulate


class Database():
    sqliteConnection = sqlite3.connect('Data.db')
    cursor = sqliteConnection.cursor()
    print("1. Request Student/Employee Email\n2. Request Student/Employee Phone\n3. Get All Employee/Students from a department")
    choice=int(input("Choose Your Request Type: "))

    if (choice==1):
        data=input("Enter the first and last name")
        name=list(data.split(" ",1))
        name.append("XXX") if len(name)<2 else ""
        sqlite_select_query = "SELECT depNumber,firstName,lastName,email from people where LOWER(firstName)=LOWER('{}') and lastName like '%{}%' ".format(name[0],name[1])
    
    elif(choice==2):
        data=input("Enter the first and last name")
        name=list(data.split(" ",1))
        name.append("XXX") if len(name)<2 else ""
        sqlite_select_query = "SELECT depNumber,firstName,lastName,phoneNumber from people where LOWER(firstName)=LOWER('{}') and lastName like '%{}%' ".format(name[0],name[1])
    elif(choice==3):
        data = int(input("Enter the department Number: "))
        sqlite_select_query = "SELECT depNumber,firstName,lastName,phoneNumber,email from people where depNumber={};".format(data)

    # print(sqlite_select_query)
    records = cursor.execute(sqlite_select_query).fetchall()
    print()
    print()
    if (choice==3):
        # print("-------------------------------")
        # print("Number Of People Found:  ", len(records))
        # print("Dpt\t Names \tPhone \tEmail")
        # sinner=""
        # for i in records:
        #     sinner+="{}\t{}\t{} \t{}".format(i[0],i[1]+" "+i[2],i[3],i[4])
        print(tabulate(records, tablefmt="grid", showindex="always"))
    else:
        # print("Number Of People Found:  ", len(records))
        # sinner=""
        # for i in records:
        #       sinner+="\nDepartment number: {} \nNames: {}\nData:{}".format(i[0],i[1]+" "+i[2],i[3])
        # print((sinner))

        print(tabulate(records))

# db=sqlite3.connect("Data.db")
# db.row_factory=sqlite3.Row #allo us to access column separately row[id], etc..
# db.execute("drop table if exists people") #remove the table if it already exist and craet  new one 
# db.execute("create table people (depNumber int, firstName text,lastName text,phoneNumber text,email text)")
# db.execute("insert into people values(?,?,?,?,?)",(1,"UWASE","Aline","+250783305114","UWASE@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(2,"MUGENI	","Rebecca","+250783305114","MUGENI@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(2,"SEHIRE ","IRAKOZE BENJAMIN","+250783305114","SEHIRE@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(1,"NDAHAYO ","ERNESTE","+250783305114","NDAHAYO@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(1,"NDIZIHIWE ","RAZARD","+250783305114","NDIZIHIWE@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(1,"TUYISENGE ","Evariste","+250783305114","TUYISENGE@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(2,"FURAHA ","Sylvie","+250783305114","FURAHA@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(1,"NIYOMUGABO","JEAN D'AMOUR","+250783305114","NIYOMUGABO@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(1,"SHEMA ","Diogene","+250783305114","SHEMA@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(2,"ILUNGA","GISA DANIEL","+250783305114","ILUNGA@gmail.com"))
# db.execute("insert into people values(?,?,?,?,?)",(1,"TUYISINGIZE ","Leopord","+250783305114","TUYISINGIZE@gmail.com"))
# db.commit()