import re
import smtplib
import random
regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
def isValid(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False
    
def sendMail(email):
     smtpEmail = "udrive00@mail.ru"
     smtpObj = smtplib.SMTP("smtp.mail.ru", 587)
     smtpObj.starttls()
     smtpObj.login(smtpEmail, "zcyWmDRBPMLPRr45Hsrm")
     code = random.randint(100000, 999999)
     smtpObj.sendmail(smtpEmail, email, f"Your code: {code}")
     smtpObj.quit()
     return code

def match(usercode,code):
    if (code==usercode):
        return True
    else: return False