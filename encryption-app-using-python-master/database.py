import mysql.connector
import bcrypt
def dbinsert(firstname,lastname,username,password):
    hashed_password=bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    sql="INSERT INTO member (firstname, lastname, username,password) VALUES (%s, %s, %s, %s)"
    val=(firstname,lastname,username,hashed_password)
    mycursor.execute(sql,val)
    mydb.commit()

def dbvalue(username,password):
    sql="SELECT username,password FROM member WHERE username= '%s'"%(username)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        if x[0]==username and bcrypt.checkpw(password.encode("utf-8"),x[1].encode("utf-8")):
                return True
    else:
        return False
                
mydb = mysql.connector.connect(
  host="localhost",
  username="root",
  password="",
  database="python_project"
)
mycursor = mydb.cursor()