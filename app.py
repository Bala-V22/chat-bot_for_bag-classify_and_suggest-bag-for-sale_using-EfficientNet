from flask import Flask,render_template,request, jsonify
from email.mime.text import MIMEText
import math, random
import smtplib
import pymysql
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from otp import OTP
import cv2 
import os
from werkzeug.utils import secure_filename
from detect import main
from requests import get
from bs4 import BeautifulSoup
import glob
from tensorflow.keras.models import load_model


model_path="classifier-chatbot-97.35.h5"
print (' Model is being loaded- this will take about 10 seconds')
model=load_model(model_path)

app= Flask(__name__)


save_otp=[]
semail=[]
spassword=[]
# search_product=[]
# input_product=[]
b_mail=[]
# prizes=[]


def mail(mail,otp):

    msg="Your Otp is: {}".format(otp)   
    print(msg)    
    msg = MIMEText(msg)

    SMTP_USERNAME = 'pythonfabhost2021@gmail.com'
    SMTP_PASSWORD = 'frqrvtpbohkqfoxk'
    SMTP_PORT = 587
    SMTP_SERVER = 'smtp.gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    # text = msg.as_string()
    server.sendmail("pythonfabhost2021@gmail.com",mail, msg.as_string())
    print("successfully")
    server.quit()

con=pymysql.connect(db='chat',host='localhost',user='root',password='jillabala',autocommit=True)
cur =con.cursor()

def bill_mail(user_mail,msg):
    # msg="Hello Sir/Mam recently you select one product our shop that bill amount is ₹2000"   
    print(msg)    
    msg = MIMEText(msg)

    SMTP_USERNAME = 'pythonfabhost2021@gmail.com'
    SMTP_PASSWORD = 'frqrvtpbohkqfoxk'
    SMTP_PORT = 587
    SMTP_SERVER = 'smtp.gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    # text = msg.as_string()
    server.sendmail("pythonfabhost2021@gmail.com",user_mail, msg.as_string())
    print("successfully")
    server.quit()

def user(email,password):
    # con=pymysql.connect(db='chat',host='localhost',user='root',password='jillabala',autocommit=True)
    # cur =con.cursor()
    while True:
        cur.execute("SELECT * FROM users WHERE mail_id ='"+ email +"'")
        results = cur.fetchall()
        print(results)
        break   
    
    if len(results)==0:   
        sql="INSERT INTO users(mail_id,password) VALUES(%s,%s)"
        val=(email,password)
        cur.execute(sql,val)
    else:
        pass    

def other(sentence):
    r1 = random.randint(1, 3)
    sug_product= "/products/{0}/{1}.jpg".format(sentence,r1)
    print(sug_product)
    return sug_product

def price():
    list1 = [2999, 1453, 2099, 2599, 1998, 3555]
    prize=random.choice(list1)
    return prize

# @app.route('/')
# def index():
#     return render_template("reg.html")

@app.route('/')
def index():
    return render_template("chat.html")    

@app.route("/ask", methods=['POST'])
def ask():

    message = str(request.form['messageText'])
    bot_response=database(message)

    # bot_response =  bot.get_response(message)                                                                                
    # reply = "i need some product"
    # bot_response=reply
    print(bot_response)

    while True:

        if message == ("bye"):

            bot_response='Hope to see you soon'

            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})

        # elif message == ("hi"):

        #     bot_response='hi buddy'     
        #     print(bot_response)
        #     funs=0
        #     return render_template('chat.html')
        
        elif bot_response:

            bot_response = str(bot_response)      
            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})

            break

        else:
        
            try:
                url  = "https://en.wikipedia.org/wiki/"+ message
                page = get(url).text
                soup = BeautifulSoup(page,"html.parser")
                p    = soup.find_all("p")
                return jsonify({'status':'OK','answer':p[1].text})

            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'
            
                print(bot_response)
                return jsonify({'status':'OK','answer':bot_response})    

@app.route("/login",methods=["post"] )
def reg():
    if request.method=="POST":
        global email
        global password
        email=request.form["email"]
        password=request.form["password"]
        otp=OTP()
        save_otp.append(otp)
        print(save_otp)
        # semail.append(email)
        # spassword.append(password)
        mail(email,otp)
        return render_template("otp.html")   

@app.route("/login_2",methods=["post"] )
def regs():
    if request.method=="POST":
        global email
        global password
        email=request.form["email"]
        password=request.form["password"]
        otp=OTP()
        save_otp.append(otp)
        print(save_otp)
        semail.append(email)
        spassword.append(password)
        mail(email,otp)
        return render_template("log_otp.html") 

@app.route("/verify",methods=["post"])
def otp():
    rgotp=request.form["otp"]
    if rgotp==save_otp[0]:
        user(email,password)
        msg="Login Now"
        msg2="Your Register Successfully"
        del save_otp[0]
        return render_template("reg.html", msg=msg,msg2=msg2)
    else:
        msg="Something Wrong"  
        msg2="OTP or password Something Wrong"
        return render_template("reg.html", msg=msg,msg2=msg2)  

@app.route("/log_verify",methods=["post"])
def otp_2():
    rgotp=request.form["otp"]
    if rgotp==save_otp[0]:
        del save_otp[0]
        print(semail[0])
        print(spassword[0])
        cur.execute('SELECT * FROM users WHERE mail_id = %s AND password = %s', (semail[0], spassword[0]))
        account = cur.fetchone()
        if account:
            b_mail.append(email)
            return render_template("chat.html")
        else:
            msg="Something Wrong"  
            return render_template("reg.html", msg=msg)
    else:
        msg="Something Wrong"  
        return render_template("reg.html", msg=msg)          
 
# @app.route("/ask", methods=['POST'])
# def ask():

#     message = str(request.form['messageText'])
#     bot_response=database(message)

#     # bot_response =  bot.get_response(message)                                                                                
#     # reply = "i need some product"
#     # bot_response=reply
#     print(bot_response)

#     while True:

#         if message == ("bye"):

#             bot_response='Hope to see you soon'

#             print(bot_response)
#             return jsonify({'status':'OK','answer':bot_response})
 
#         elif bot_response:

#             bot_response = str(bot_response)      
#             print(bot_response)
#             return jsonify({'status':'OK','answer':bot_response})

#             break

#         else:
        
#             try:
#                 url  = "https://en.wikipedia.org/wiki/"+ message
#                 page = get(url).text
#                 soup = BeautifulSoup(page,"html.parser")
#                 p    = soup.find_all("p")
#                 return jsonify({'status':'OK','answer':p[1].text})

#             except IndexError as error:

#                 bot_response = 'Sorry i have no idea about that.'
            
#                 print(bot_response)
#                 return jsonify({'status':'OK','answer':bot_response})    

def database(userText):
    try:
        con=pymysql.connect(db='chat',host='localhost',user='root',password='jillabala',autocommit=True)
        cur =con.cursor()    
        cur.execute("SELECT * FROM msg WHERE person ='"+ userText +"'")
        results = cur.fetchall()
        for i in results:
            print(i)
        print(i[2])
        # final=[i]
        data = i[2]
    # datas=tuple(data)
        return data
    except:
        data=0
        return data

def store(change,passed):
    con=pymysql.connect(db='chat',host='localhost',user='root',password='jillabala',autocommit=True)
    cur =con.cursor() 
    cur.execute("update storage set "+ change +" ='" + passed +"' where stand='standard'")

def fetch():   
    cur.execute("SELECT * FROM storage WHERE stand = 'standard'")
    results = cur.fetchall() 
    for i in results:
        pass
    print(i)
    return i 

def delete():
    files = glob.glob('storage/*')
    for f in files:
        os.remove(f)   

@app.route("/upload", methods=["post"])
def photo():  
    file=request.files['img']
    files=file.filename
    print(files)
    # input_product.append(files)
    search='input_product'
    store(search,files)
    basepath = os.path.dirname(__file__)
    print(basepath)
    file_path = os.path.join(basepath, 'static', secure_filename(file.filename))
    file.save(file_path)   
    print(file_path)
    # fold='input'
    try:
        sentence=main(files,model)
    except:
        sentence=main(files,model)
        
    search='search_product'
    store(search,sentence)
    # product="\products\{}".format(sentence)
    # print(product)
    img_path=glob.glob("products/{}/*".format(sentence))
    products=len(img_path)
    print(products)
    r1 = random.randint(1, products)
    sug_product= "/products/{0}/{1}.jpg".format(sentence,r1)
    print(sug_product)
    s_file=files
    print(s_file)
    prize=price()
    # prizes.append(prize)
    search='prizes'
    store(search,str(prize))
    search='product'
    store(search,str(r1))
    return render_template('suggest.html',sug= sug_product,product_name=sentence,s_file=files,prize=prize)
     

@app.route("/cam", methods=["post"])
def pic():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'): 
                cv2.imwrite('static/saved_img.jpg', img=frame)
                webcam.release()
            
                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
            
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
    # path="static/saved_img.jpg" 
    name="saved_img.jpg" 
    # input_product.append(name)
    # fold='cam'  
    # sentence=main(name,model)
    
    sentence=main(name,model)
    print(sentence)
    # search_product.append(sentence)
    search='search_product'
    store(search,sentence)
    img_path=glob.glob("products/{}/*".format(sentence))
    print(img_path)
    products=len(img_path)
    print(products)
    r1 = random.randint(1, products)
    sug_product= "/products/{0}/{1}.jpg".format(sentence,r1)
    print(sug_product)
    prize=price()
    # prizes.append(prize)
    search='prizes'
    store(search,str(prize))
    search='product'
    store(search,str(r1))
    return render_template("suggest.html",sug= sug_product,product_name=sentence, s_file=name,prize=prize) 


@app.route('/billing', methods=['post'])
def buy():
    # user_mail=b_mail[0]
    # bill_mail(user_mail)
    # Alert='Check it out'
    # message='Billing Details send in your mail'
    product_number=random.randint(100,999)
    search='product_number'
    store(search,str(product_number))
    return render_template('bill.html',product_number=product_number)


@app.route('/bill', methods=['post'])
def bill_details():
    # search='product_number'
    get_number=fetch()
    prizes=get_number[4]
    pro_number=get_number[5]
    address=request.form['address']
    state=request.form['state']
    pin=request.form['pin']
    num=request.form['num']
    user_mail=request.form['mail']
    links='http://127.0.0.1:5000/your_product'
    msg=(
"""
Your product number: {0}
Your address: {1}
State: {2}
pincode: {3}
num: {4}
Your product prize: {5}
Your Product Link: {6}""".format(pro_number,address,state,pin,num,prizes,links))

    bill_mail(user_mail,msg)
    Alert='Check it out'
    message='Billing Details send in your mail'
    # del prizes
    delete()
    return render_template('chat.html',msg=Alert,msg2=message)


@app.route('/choose', methods=['post'])
def another():
    get_number=fetch()
    sentence=get_number[2]
    name=get_number[3]
    sug_product=other(sentence)
    list3 = [2999, 1453, 2099, 2599, 1998, 3555]
    prize=random.choice(list3)
    search='prizes'
    store(search,str(prize))
    return render_template('suggest.html',sug= sug_product,product_name=sentence, s_file=name,prize=prize)


@app.route('/cancel', methods=['post'])
def can():
    get_number=fetch()
    mg=get_number[3]
    delete()
    # try:
    #     os.remove("storage/{}".format(mg))
    # except:
    #     os.remove("storage/saved_img.jpg")
    return render_template('chat.html')

@app.route('/your_product')
def link():
    value=fetch()
    pro_name=fetch()
    save=fetch()
    path_pic='/products/{}/{}.jpg'.format(pro_name[2],save[6])
    return render_template('link.html',value=value[4],pro_name=pro_name[2],path_pic=path_pic)

if __name__=="__main__":
    app.run(debug=True)    
    