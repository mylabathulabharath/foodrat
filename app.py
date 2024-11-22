from flask import Flask,render_template,request,redirect
import sqlite3
import bcrypt
app=Flask(__name__)

def create_connection():
    conn=sqlite3.connect("users.db")
    return conn

def create_table():
    conn=create_connection()
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS newuser(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)')
    conn.commit()
    conn.close()



@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form['username']
        password=request.form['password']
        conn=create_connection()
        cur=conn.cursor()
        cur.execute('''INSERT INTO newuser(username,password) VALUES(?,?)''',(name,password))
        conn.commit()
        conn.close()
        return redirect('/feedback')
    else:
        return render_template('registration.html')


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        conn=create_connection()
        print(username,password)
        cur=conn.cursor()
        cur.execute('SELECT * FROM newuser WHERE username=? and password=?',(username,password))
        user=cur.fetchone()
        if user:
            return redirect('/feedback')
        return redirect('/register')
    return render_template('login.html')
    


@app.route("/feedback")
def fedback():
    return render_template("feedback.html") 

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/admin')
def admin():
    conn= create_connection()
    cur=conn.cursor()
    cur.execute('SELECT * FROM newuser')
    data=cur.fetchall()
    return render_template('admin.html',users=data)


if __name__=="__main__":
    create_connection()
    create_table()
    app.run(debug=True)
