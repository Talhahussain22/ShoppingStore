import sys

import pyodbc
class Items:
    def __init__(self,id,name,price,quantity):
        self.id=id
        self.name=name
        self.price=price
        self.quantity=quantity


class Admin():

    def Add(self):
        id=input("Enter the id of item:")
        name=input("Enter the name of item:")
        price=float(input("Enter the price of item:"))
        quantity=int(input("Enter the quantity of item you want to add:"))
        item=Items(id,name,price,quantity)
        cursor.execute(f"INSERT INTO ITEMS VALUES('{item.id}','{item.name}','{item.price}','{item.quantity}')")
        cursor.commit()
        print("Item is successfully added")

    def update(self):
        id=input("Enter id of item which you want to update:")
        price=float(input("Enter new price of item:"))
        quantity=int(input("Enter the new quantity of item:"))
        try:
            cursor.execute(f"Update ITEMS  SET Item_Price={price}  where Item_Id='{id}'")
            cursor.execute(f"Update ITEMS  SET Quantity={quantity}  where Item_Id='{id}'")
            cursor.commit()
            print("Item is Successfully Updated")
        except:
            print(f'Item with id {id} not exists')

    def delete(self):
        id = input("Enter id of item which you want to Delete:")
        try:
            cursor.execute(f"Delete from ITEMS where Item_Id='{id}'")
            cursor.commit()
            print("Item is successfully deleted")
        except:
            print(f'No item with id {id} ')



class Customer():
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.Bill=0

    def create_account(self):
        cursor.execute(f"INSERT INTO USERS VALUES('{self.username}','{self.password}')")
        cursor.commit()
        print("Account Successfully Created")

    def View_Store(self):
        cursor.execute(f'SELECT Item_name,Item_Price FROM ITEMS')
        items=cursor.fetchall()
        print("ITEM   Price")
        for i in items:

            print(f'{i[0]}   {i[1]}')

    def Buy(self):
        name=input("Enter the name of Item:")
        cursor.execute(f'SELECT Item_name,Quantity,Item_Price,Item_Id from ITEMS')
        info=cursor.fetchall()
        for data in info:
            if name==data[0]:
                quantity = int(input("Enter the quantity:"))
                if quantity>=data[1]:
                    print(f"Insufficient Quantity || Available quantity is {data[1]} ")
                    break
                else:
                    self.Bill+=data[2]*quantity
                    cursor.execute(f"Update ITEMS SET Quantity={data[1]-quantity} where Item_Id='{data[3]}' ")
                    cursor.commit()
                    break
        else:
            print("Item not found")


conncetor = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Admin\OneDrive\Documents\Shoppingstore.accdb'
connect = pyodbc.connect(conncetor)
cursor = connect.cursor()

def main():
    check=input("Admin or User?:").upper()
    if check=='ADMIN':
        username=input("Enter your username:").upper()
        password=int(input("Enter your password:"))
        if username=="ADMIN" and password==123:
            admin = Admin()
            print("Press 1 for ADD item \nPress 2 for Update item \nPress 3 for Delete item ")
            ask=int(input("Press:"))
            if ask==1:
                admin.Add()
            elif ask==2:
                admin.update()
            elif ask==3:
                admin.delete()
            else:
                print("Invalid Key")

    elif check=="USER":
        id=input("Enter your ID:")
        password=int(input("Enter your Password:"))
        cursor.execute(f'SELECT User_name,Password from USERS')
        info=cursor.fetchall()
        for data in info:
            if id==data[0] and password ==data[1]:
                print("_______________________")
                print("WELCOME BACK SIR/MAM")
                print("_______________________")
                user=Customer(id,password)
                ask=input("Do you want to view the item list(Y/N):").upper()
                if ask=="Y":
                    user.View_Store()
                else:
                    print("OK let's move to shopping")
                while True:
                    user.Buy()
                    permission=input("Do you want to buy more items(Y/N):").upper()
                    if permission=="N":
                        break
                print(f'Your Bill is {user.Bill}')
                break
        else:
            while(True):
                print("WRONG USERNAME OR PASSWORD OR IF YOU DONT HAVE ACCOUNT: \nPRESS 1 TO CREATE ACCOUNT \nPRESS 2 TO LOGIN AGAIN \nPress 3 for exists")
                ask=int(input("PRESS:"))
                if ask==2:
                    main()
                    break
                elif ask==1:
                    username = input("Enter Your Username:")
                    password = int(input("Enter Your Password:"))
                    user=Customer(username,password)
                    user.create_account()
                    print("Press 1 for Shopping \nPress other key to  for Exit")
                    inp=int(input("Press:"))
                    if inp==1:
                        main()
                        break
                    else:
                        break
                elif ask==3:
                    sys.exit()
                else:
                    print("Enter valid Key")



main()


