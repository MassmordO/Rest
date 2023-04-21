import os
import time
import Loyalti
from Main import UserCRUD
from Main import OrderCRUD
from Main import IngridientCRUD
from Models import User
from Models import Ingridient
def adminWindow(adminId):
    os.system("cls")
    admin = UserCRUD.GetUsersByID(adminId)
    admdict = admin.to_dict()

    users = UserCRUD.Getusers()

    print(f"Добро пожаловать, администратор. Ваш баланс: {admdict['balance']}")
    try:
        operation = int(input("Выберите функцию\n"
        "1 - Заказать ингридиент\n"
        "2 - История покупок пользователей\n"
        "3 - Карты лояльности пользователей\n"
        "4 - Выйти из аккаунта\n"))

        match operation:
            case 1:
                supply(adminId)

                adminWindow(adminId)
            case 2:
                for i in users:
                    us = i.to_dict()
                    print( us['email'])

                try:
                    mailInput = int(input("Введите почту пользователя: "))

                    
                    userOrders = OrderCRUD.GetOrdersByEmail(mailInput)

                    if (userOrders != None):
                        if (len(userOrders) <= 0):
                            print("У пользователя не было заказов")
                        else:
                            for order in userOrders:
                                orderdict = order.to_dict()
                                print(f"{orderdict['creationTime']}: {orderdict['price']} руб. Свинина: {'была' if orderdict['Pig']== 1 else 'не была'} {'и пользователь видел это' if orderdict['userKnows']==1 else ''}")
                    else:
                        print("Указанная почта не существует в системе!")
                    input("Выйти на главную")
                    adminWindow(adminId)
                except (ValueError, KeyboardInterrupt, IndexError):
                    print("Неверно выбран пользователь")
                    time.sleep(2)
                    adminWindow(adminId)
                
            case 3:
                for i in users:
                    us = i.to_dict()
                    print( us['email'])
                try:
                    mailInput = int(input("Выберите пользователя: "))
                    user = UserCRUD.GetUserByEmail(mailInput)
                    for i in user:
                        usdict = i.to_dict()

                    if (user != None):
                        print(f"Программа лояльности пользователя ({usdict['email']}): {Loyalti.get_loyalty(user['loyalty'])}, скидка: {user['loyalty']}%\n")
                    else:
                        print("Указанная почта не существует в системе!")
                    input("Выйти на главную")
                    adminWindow(adminId)
                except (ValueError, KeyboardInterrupt, IndexError):
                    print("Неверно выбран пользователь")
                    time.sleep(2)
                    adminWindow(adminId)
                
            case 4:
                return
            case _:
                print("Неверная операция")
    except (ValueError, KeyboardInterrupt):
        print("Введены неверные данные")
        time.sleep(2)
        adminWindow(adminId)
        
        
        
def supply(adminId):
    admin = UserCRUD.GetUsersByID(adminId)
    admdict = admin.to_dict()
    adminbalance = int(admdict['balance'])
    ingridients = IngridientCRUD.GetIngridients()

    if (ingridients == None or len(ingridients) <= 0):
        print("Ошибка получения списка ингридиентов")
        
    else:
        for i in ingridients:
            ingdict = i.to_dict()
            print(f" {ingdict['name']} - {ingdict['price']} руб. На складе: {ingdict['CountInWarehouse']} шт.")

        try:
            idIngridient = input("Выберите ингредиент для поставки: \n")

            try:
                ingridient = IngridientCRUD.GetIngByName(idIngridient)
                for i in ingridient:
                    ingid=i.id
                    ingridientdict = i.to_dict()
                if ingridient == None:
                    raise IndexError

                count = int(input("Введите кол-во выбранного ингридиента: "))
                cost = int(ingridientdict['price'])*count

                confirm = input(f"Поставка {ingridientdict['name']} в количестве {count} шт. - {cost} Рублей\n"
                        "Подтвердить заказ?\n").lower()

                if confirm == 'y' or confirm == 'д':
                    adminbalance -= cost
                    if adminbalance >= 0:
                        updateadm = User(admdict['email'],admdict['password'],admdict['isAdmin'],adminbalance,admdict['loyalty'])
                        UserCRUD.UpdateUser(adminId,updateadm)
                        updateing = Ingridient(ingridientdict['name'],ingridientdict['price'],count,ingridientdict['comon'])
                        IngridientCRUD.UpdateIngridient(ingid,updateing)

                        print("Заказ выполнен!")
                    else:
                        print("Недостаточно средств на счету.")

                    time.sleep(2)
                    return
                elif confirm == "n" or confirm == "н":
                    print("Отмена заказа...")
                    time.sleep(2)
                    return
            except IndexError:
                print("Ингредиента с таким названием нет!")    
                time.sleep(2)    
                return       

        except ValueError:
            print("Введены неверные данные")
            time.sleep(2)
            return