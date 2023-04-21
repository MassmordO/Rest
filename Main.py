import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import Models
from Models import Dish
from Models import User
cred = credentials.Certificate("shaverma-f9e8a-fa9031890ade.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class UserCRUD:
    def Usersadd(user):
        collection = db.collection('Users') 
        res = collection.document().set(user.user_return())
        return res

    def GetUserByEmail(email):
        collection = db.collection('Users')
        res = collection.where('email','==',email).get()
        return res

    def Getusers():
        collection = db.collection('Users')
        res = collection.get()
        return res
    
    def GetUsersByID(userid):
        collection = db.collection('Users').document(userid)
        res = collection.get()
        return res
    
    def UpdateUser(userid,user):
        collection = db.collection('Users').document(userid)
        res = collection.update(user.user_return())
        return res

    def Deleteuser(userid):
        collection = db.collectiom('Users').document(userid)
        res = collection.delete()
        return res
    
    def GetAdmin():
        collection = db.collection("Users")
        res = collection.where('isAdmin','==',True)
        return res

class DishCRUD:
    def DishAdd(dish):
        collection = db.collection('Dish') 
        collection.document().set(dish.dish_return())


    def GetDishes():
        collection = db.collection('Dish')
        res = collection.get()
        return res
    
    def GetDishByID(dishid):
        collection = db.collection('Dish').document(dishid)
        res = collection.get()
        return res
    
    def UpdateDish(dishid,dish):
        collection = db.collection('Dish').document(dishid)
        res = collection.update(dish.dish_return())
        return res

    def DeleteDish(dishid):
        collection = db.collectiom('Dish').document(dishid)
        res = collection.delete()
        return res


class IngridientCRUD:
    def IngridientAdd(ingridient):
        collection = db.collection('Ingridient') 
        collection.document().set(ingridient.ing_return())

    def GetIngByName(name):
        collection = db.collection('Ingridient')
        res = collection.where('name','==',name).get()
        return res
    
    def GetIngridients():
        collection = db.collection('Ingridient')
        res = collection.get()
        return res
    
    def GetIngridientByID(ingridientid):
        collection = db.collection('Ingridient').document(ingridientid)
        res = collection.get()
        return res
    
    def UpdateIngridient(ingridientid,ingridient):
        collection = db.collection('Ingridient').document(ingridientid)
        res = collection.update(ingridient.ing_return())
        return res

    def DeleteIngridient(ingridientid):
        collection = db.collectiom('Ingridient').document(ingridientid)
        res = collection.delete()
        return res


class OrderCRUD:
    def OrderAdd(order):
        collection = db.collection('Order') 
        res = collection.add(order.order_return())
        return res[1].id

    def GetOrders():
        collection = db.collection('Order')
        res = collection.get()
        return res
    
    def GetOrdersByEmail(email):
        collection = db.collection('Order')
        res = collection.where('userEmail','==',email).get()
        return res
    
    def GetOrderByID(orderid):
        collection = db.collection('Order').document(orderid)
        res = collection.get()
        return res
    
    def UpdateOrder(ordrid,order):
        collection = db.collection('Order').document(ordrid)
        res = collection.update(order.order_return())
        return res

    def DeleteOrder(orderid):
        collection = db.collectiom('Order').document(orderid)
        res = collection.delete()
        return res

        
class OrderCompositionCRUD:
    def OrderCompositionAdd(ordercomp):
        collection = db.collection('OrderComposition') 
        res = collection.add(ordercomp.orderComposition_return())
        return res[1].id

    def GetOrderCompositions():
        collection = db.collection('OrderComposition')
        res = collection.get()
        return res
    
    def GetOrderCompositionByID(ordercompid):
        collection = db.collection('OrderComposition').document(ordercompid)
        res = collection.get()
        return res
    
    def UpdateOrderComposition(ordercompid,ordercomp):
        collection = db.collection('OrderComposition').document(ordercompid)
        res = collection.update(ordercomp.orderComposition_return())
        return res

    def DeleteOrderComposition(ordercompid):
        collection = db.collectiom('OrderComposition').document(ordercompid)
        res = collection.delete()
        return res
    
class IngidientCompositionCRUD:
    def IngidientCompositionAdd(ingcomp):
        collection = db.collection('IngidientComposition') 
        collection.document().set(ingcomp.ingredientComposition_return())

    def GetIngidientCompositions():
        collection = db.collection('IngidientComposition')
        res = collection.get()
        return res
    
    def GetIngidientCompositionByID(ingcompid):
        collection = db.collection('IngidientComposition').document(ingcompid)
        res = collection.get()
        return res
    
    def UpdateIngidientComposition(ingcompid,ingcomp):
        collection = db.collection('IngidientComposition').document(ingcompid)
        res = collection.update(ingcomp.ingredientComposition_return())
        return res

    def DeleteIngidientComposition(ingcompid):
        collection = db.collectiom('IngidientComposition').document(ingcompid)
        res = collection.delete()
        return res
