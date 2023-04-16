class User:
    def __init__(self, email,password,isAdmin,balance,loyalty):
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        self.balance = balance
        self.loyalty = loyalty
        
    def user_return(self):
        return self.__dict__
    
    
class Dish:
    def __init__(self, name,price):
        self.name=name
        self.price=price
        
    def dish_return(self):
        return self.__dict__
    
class Ingridient:
    def __init__(self,name,price,countInWarehouse,common):
        self.name=name
        self.price=price
        self.countInWarehouse = countInWarehouse
        self.common = common
        
    def ing_return(self):
        return self.__dict__
    
class Order:
    def __init__(self,number,userEmail,creationTime,price,pig,userKnows):
        self.userEmail=userEmail
        self.number=number
        self.creationTime=creationTime
        self.price=price
        self.pig=pig
        self.userKnows=userKnows
        
    def order_return(self):
        return self.__dict__
    
class OrderComposition:
    def __init__(self,number,orderNumber,dishName,dishCount):
        self.number=number
        self.orderNumber = orderNumber
        self.dishName=dishName
        self.dishCount=dishCount
        
    def orderComposition_return(self):
        return self.__dict__
    
class IngridientComposition:
    def __init__(self,number,orderCompositionNumber,ingredientName,ingredientCount):
        self.number=number
        self.orderCompositionNumber = orderCompositionNumber
        self.ingredientName = ingredientName
        self.ingredientCount=ingredientCount
        
    def ingredientComposition_return(self):
        return self.__dict__
