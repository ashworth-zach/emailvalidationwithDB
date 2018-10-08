from flask import Flask, redirect, render_template, request, flash
import pymysql.cursors
import datetime
import re
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mysql = connectToMySQL("emaildb")

app = Flask(__name__)
app.secret_key = "ThisIsSecret!"

@app.route('/')
def index():
    all_emails = mysql.query_db("SELECT * FROM emails")
    return render_template('index.html', email = all_emails)
def display():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('result.html', emails=emails)
@app.route('/process', methods=['POST'])
def submit():
    query='select * from emails where email = %(email)s'
    data={
        'email': request.form['email']
    }
    checkvalid=mysql.query_db(query,data)
    print(checkvalid)
    if len(checkvalid)>0:
        flash('email taken')
        return redirect('/')
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
    else:
        flash("Success!")
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        data = {
             'email': request.form['email']
        }
        # print(request.form['email'])
        mysql.query_db(query, data)
        return display()
    return redirect('/')
@app.route('/delete', methods=['POST'])
def delete():
    id = int(request.form['hidden'])
    query = "DELETE FROM emails WHERE id = {}".format(id)
    mysql.query_db(query)
    return display()
if __name__ == "__main__":
    app.run(debug=True)
