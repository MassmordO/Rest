import os
import time
import random
from datetime import datetime
from Main import DishCRUD
from Main import IngridientCRUD
from Main import UserCRUD
from Models import Order
from Models import OrderComposition
from Main import OrderCRUD
from Main import OrderCompositionCRUD
from Main import IngidientCompositionCRUD
from Models import IngridientComposition
from Models import Ingridient
from Models import User
dish = DishCRUD.GetDishes()
for i in dish:
    dishdict = i.to_dict()
    dishId = i.id
defaultPrice = dishdict['price']


def order(userId):
    os.system("cls")
    ingridients = IngridientCRUD.GetIngridients()
    orderIngridients = []
    for i in ingridients:
        ingdict = i.to_dict()
        orderIngridients.append([ingdict, 1 if (int(ingdict['countInWarehouse']) and int(ingdict['common'])>0) else 0])
    count = -1

    print(f"Шаурма: {defaultPrice} руб.")

    try:
        count = int(input("Сколько шаурмы желаете заказать?\n"
                          "0 - Выйти на главную\n"))
    except ValueError:
        print("Введены неверные данные")
        time.sleep(2)
        order(userId)

    if count == 0:
        return
    
    if count > 0:
        changingComposition(orderIngridients, userId, count, ingridients)



def changingComposition(orderIngridients, userId, shavermaCount, ingridients):
    while True:
        printComposition(orderIngridients)
        try:
            changeComposition = input("Изменить состав?\n").strip().lower()

            if changeComposition == 'y' or changeComposition == 'д':
                changeOrderComposition(orderIngridients, ingridients)
                
                continue
            elif changeComposition == 'n' or changeComposition == 'н':
                for ing in orderIngridients:
                    ingridient = IngridientCRUD.GetIngByName(ing[0]['name'])
                for i in ingridient:
                    ingredientdict = i.to_dict()
                if ingredientdict['countInWarehouse'] < ing[1]*shavermaCount:
                    print("Некоторых ингридиентов для Вашего заказа не хватает!")
                    input()
                    return
                    
                user = UserCRUD.GetUsersByID(userId)
                userdict = user.to_dict()
                userbalance = userdict['balance']
                totalPrice = calculateOrderPrice(orderIngridients, shavermaCount)

                if userdict['loyalty']> 0:
                    print(f"Ваш заказ стоит {totalPrice} руб.")
                    totalPrice = totalPrice - (totalPrice*(int(userdict['loyalty'])/100))
                    print(f"Но с учётов Вашей карты лояльности, он обойдётся Вам в {totalPrice}")
                    input()
                if userdict['balance'] < totalPrice:
                    print("Недостаточно средств!")
                    input()
                    return

                confirmOrder = input(f"Подтвердить заказ: {shavermaCount} шт. шаурма на {totalPrice} руб.?\n")

                if confirmOrder == 'y' or confirmOrder == 'д':

                    orderContainsPig = False
                    userKnowsAboutPig = False

                    randOneFive = random.randint(1, 6)
                    if randOneFive == 5:
                        orderContainsPig = True
                        randOneFive = random.randint(1, 6)
                        if randOneFive == 5:
                            userKnowsAboutPig = True

                    if userKnowsAboutPig == True:
                        totalPrice = totalPrice - (totalPrice*0.3)

                        print("Приносим изменения за свинину в Вашей шаурме.\nМы предлагаем Вам скидку на Ваш заказ в размере 30%")
                        print(f"Итоговая стоимость заказа: {totalPrice} руб.")
                        input()
                    rand = random.randint(0,100000)
                    orderadd =  Order(rand,userdict['email'],datetime.now(),totalPrice, 1 if orderContainsPig else 0,1 if userKnowsAboutPig else 0)
                    res = OrderCRUD.OrderAdd(orderadd)

                    
                    order = OrderCRUD.GetOrderByID(res)
                    orderCompositionadd = OrderComposition(rand,order.id,dishdict['name'],shavermaCount)
                    rescomp = OrderCompositionCRUD.OrderCompositionAdd(orderCompositionadd)

                    
                    orderComposition = OrderCompositionCRUD.GetOrderCompositionByID(rescomp)

                    for ing in orderIngridients:
                        ingredcomp = IngridientComposition(rand,orderComposition.id,ing[0]['name'],ing[1]*shavermaCount)
                        IngidientCompositionCRUD.IngidientCompositionAdd(ingredcomp)
                        ingredienaforupdate = IngridientCRUD.GetIngByName(ing[0]['name'])
                        for i in ingredienaforupdate:
                            ingid = i.id
                            ingredienaforupdatedict = i.to_dict()
                        countingrid = int(ingredienaforupdatedict['countInWarehouse'])-(ing[1]*shavermaCount)
                        ingupdate = Ingridient(ingredienaforupdatedict['name'],ingredienaforupdatedict['price'],countingrid,ingredienaforupdatedict['common'])
                        IngridientCRUD.UpdateIngridient(ingid,ingupdate)

                    admup = UserCRUD.GetAdmin()
                    for i in admup:
                        admupdict = i.to_dict()
                        idadmup = i.id
                    adm = User(admupdict['email'],admupdict['password'],admupdict['isAdmin'],int(admupdict['balance'])+totalPrice,admupdict['loyalty'])
                    UserCRUD.UpdateUser(idadmup,adm)
                    userup = User(userdict['email'],userdict['password'],userdict['isAdmin'],userbalance-totalPrice,userdict['loyalty'])
                    UserCRUD.UpdateUser(userId,userup)
                    print("Заказ успешно оформлен!")

                    if (totalPrice > 500):
                        userup = User(userdict['email'],userdict['password'],userdict['isAdmin'],userbalance-totalPrice,5)
                        UserCRUD.UpdateUser(userId,userup)
                    elif (totalPrice > 800):
                        userup = User(userdict['email'],userdict['password'],userdict['isAdmin'],userbalance-totalPrice,10)
                        UserCRUD.UpdateUser(userId,userup)
                    elif (totalPrice > 1000):
                        userup = User(userdict['email'],userdict['password'],userdict['isAdmin'],userbalance-totalPrice,20)
                        UserCRUD.UpdateUser(userId,userup)
                    input("На главную")
                    return
                elif confirmOrder == 'n' or confirmOrder == 'н':
                    print("Отменяем заказ...")
                    time.sleep(2)
                    return
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            print("Неверная операция")
            time.sleep(2)
            continue

def calculateOrderPrice(orderIngridients, tacoCount):
    price = defaultPrice*tacoCount

    for iwc in orderIngridients:
        countOverOne = iwc[1]-1

        if iwc[0]['common']:
            if countOverOne > 0:
                price += countOverOne*iwc[0]['price']
        else:
            if iwc[1] > 0:
                price += iwc[0]['price']*iwc[1]

    return price

def printComposition(orderIngridients):
    print("Текущий состав заказа:")
    for iwc in orderIngridients:
        print(f"{iwc[0]['name']} {iwc[1]} шт. {iwc[0]['price']*iwc[1]} руб.")
        

def changeOrderComposition(orderIngridients, ingridients):
    iwcs = orderIngridients

    ings = ingridients

    ingridient = None
    ingrId = -1

    while ingrId != 0:
        print("Список доступных ингредиентов:")
        for i in range(len(iwcs)):
            if (int(iwcs[i][0]['countInWarehouse']) > 0):
                print(f"{i+1}. {iwcs[i][0]['name']} {iwcs[i][0]['price']} руб.")

        try:
            ingrId = int(input("Выберите ингридиент: \n0 - Назад\n"))

            if ingrId == 0:
                return

            ingridient = iwcs[ingrId-1]
            if ingridient[0]['countInWarehouse'] <= 0:
                raise IndexError

            try:
                ingrOp = -1
                while ingrOp != 0:
                    ingrOp = int(input("1: +1\n2: -1\n0: Хватит\n"))
                    
                    if ingrOp == 0:
                        break

                    match (ingrOp):
                        case 1:
                            ingridientWithCount = findCortege(ingridient, iwcs)

                            availableCount = getIngridientWarehouseCount(ings, ingridientWithCount[0])

                            if availableCount < (ingridientWithCount[1] + 1):
                                print("На складе нет столько!")
                            else:
                                ingridientWithCount[1] += 1
                                print(f"{ingridientWithCount[0]['name']} теперь {ingridientWithCount[1]} шт.")
                        case 2:
                            ingridientWithCount = findCortege(ingridient, iwcs)

                            ingridientWithCount[1] -= 1
                            if ingridientWithCount[1] < 0:
                                ingridientWithCount[1] = 0
                                print("Нельзя сделать меньше 0!")
                            else:
                                print(f"{ingridientWithCount[0]['name']} теперь {ingridientWithCount[1]} шт.")
                            
                    
            except ValueError:
                print("Неверный номер операции!")    
                time.sleep(2)    
                continue
        except (ValueError, IndexError):
            print("Ингредиента с таким номеров нет!")    
            time.sleep(2)    
            continue

    

def findCortege(ingridient, iwcs):
    for i in range(len(iwcs)):
        if ingridient[0]['name'] == iwcs[i][0]['name']:
            return iwcs[i]

    return None

def getIngridientWarehouseCount(ingridients, ingridient):
    for ing in ingridients:
        ingdict = ing.to_dict()
        if ingdict['name'] == ingridient['name']:
            return ingdict['countInWarehouse']
