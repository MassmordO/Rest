import os
import time
import MailValid
import AdminWindow
import ClientWindow
import Main
from Main import UserCRUD
import Models
from Models import User
main = UserCRUD
def regmenu():
    users = main.Getusers()
    for i in users: usersdict=i.to_dict()
    os.system("cls")
    try:
        operation = int(input("Добро пожаловать! \n"
                "Выберите функцию: \n"
                "1 - Авторизация\n"
                "2 - Регистрация\n"
                "3 - Выход\n"))
        match operation:
            case 1:
                signInMail = input("Введите почту: ")
                signInPass = input("Введите проль: ")
                isReg = False
                isAdmin=False
                for i in users:
                    usd = i.to_dict()
                    if(signInMail==usd['email'] and signInPass==usd['password']): 
                        isReg=True
                        if(usd['isAdmin']==True): 
                            isAdmin=True
                            idadm = i.id
                            break
                        else: 
                            isAdmin=False
                            usid = i.id
                            break
                    else: isReg=False
                if(isReg==True): 
                    print("Вы авторизованы")
                    if(isAdmin):
                        AdminWindow.adminWindow(idadm)
                    else:
                        ClientWindow.customerWindow(usid)
                else: 
                    print("Введены неверные данные\n")
                    time.sleep(2)
                    regmenu()
            case 2:
                signUpEmail = input("Введите почту: ")
                if(not MailValid.isValid(signUpEmail)):
                    print("Введены неверные данные\n")
                    time.sleep(2)
                    regmenu()
                for i in users:
                    usdr = i.to_dict()
                    if(signUpEmail==usdr['email']):
                        print("Данная почта уже зарегестрирована\n")
                        time.sleep(2)
                        regmenu()
                signUpPass = input("Введите пароль: ")
                if(len(signUpPass)<5):
                    print("Введены неверные данные\n")
                    time.sleep(2)
                    regmenu()
                realcode = MailValid.sendMail(signUpEmail)
                code = int(input("Введите код с почты: "))
                if(not MailValid.match(code,realcode)):
                    print("Введены неверные данные\n")
                    time.sleep(2)
                    regmenu()
                user = User(signUpEmail,signUpPass,False,500,0)
                main.Usersadd(user)
                regmenu()
                users = main.Getusers()
                usersdict.clear()
                for i in users: usersdict=i.to_dict()
            case 3:
                exit()
            case _:
                regmenu()
    except (KeyboardInterrupt, ValueError):
        print("Введены неверные данные\n")
        time.sleep(2)
        regmenu()

regmenu()
