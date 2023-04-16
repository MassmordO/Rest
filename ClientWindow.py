import os
import time
import random
import Loyalti
from Main import UserCRUD
from Main import OrderCRUD
from Models import User
import CreateOrder
def customerWindow(customerId):
    os.system("cls")
    user = UserCRUD.GetUsersByID(customerId)
    userdict = user.to_dict()

    # установка случайного баланса, если он пустой
    if (userdict['balance'] == 0):
        userupdt = User(userdict['email'],userdict['password'],False,{random.randint(1000, 5000)},userdict['loyalty'])
        UserCRUD.UpdateUser(customerId,userupdt)
        user = UserCRUD.GetUsersByID(customerId)
        userdict = user.to_dict()

    print(f"Добро пожаловать! Ваш баланс: {userdict['balance']}")
    try:
        operation = int(input("Выберите функцию\n"
        "1 - Заказать блюдо\n"
        "2 - История покупок\n"
        "3 - Карта лояльности\n"
        "4 - Выйти из аккаунта\n"))

        match(operation):
            case 1:
                CreateOrder.order(customerId)

                customerWindow(customerId)
            case 2:
                userOrders = OrderCRUD.GetOrdersByEmail(userdict['email'])
                for i in userOrders: userOrdersDict = i.to_dict()
                if (userOrders != None):
                    if (len(userOrders)<=0):
                        print("У вас не было заказов")
                    else:
                        for order in userOrders:
                            userOrdersDict= order.to_dict()
                            print(f"{userOrdersDict['creationTime']}: {userOrdersDict['price']} руб. Свинина: {'была' if userOrdersDict['pig'] == True else 'не была'} {'и вы видели это' if userOrdersDict['userKnows'] else ''}")
                input("Выйти на главную")
                customerWindow(customerId)
            case 3:
                print(f"Ваша программа лояльности: {Loyalti.get_loyalty(str(userdict['loyalty']))}, скидка: {userdict['loyalty']}%\n")
                input("Выйти на главную")
                customerWindow(customerId)
            case 4:
                return
            case _:
                print("Неверная операция")
    except (KeyboardInterrupt, ValueError):
        print("Введены неверные данные")
        time.sleep(2)
        customerWindow(customerId)