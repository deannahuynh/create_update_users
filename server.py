from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/users')
def all_users():
    mysql = connectToMySQL('users')
    users = mysql.query_db("SELECT * FROM users")
    print(users)
    return render_template("/all_users/index.html", users=users)

@app.route('/users/new')
def add_user():
    return render_template('/create_user/create.html')

@app.route('/users/create', methods=['POST'])
def create_user():
    mysql = connectToMySQL('users')
    query = " INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        'fn': request.form['first_name'],
        'ln': request.form['last_name'],
        'em': request.form['email']
    }
    new_user = mysql.query_db(query, data)
    return redirect(f"/users/{new_user}")

@app.route('/users/<id>')
def user_by_id(id):
    mysql = connectToMySQL('users')
    query = ("SELECT * FROM users WHERE id = %(id)s;")
    data = {
        "id": id
    }
    users = mysql.query_db(query, data)
    print(users)
    return render_template('user_id/id.html', id=int(id),users=users[0])

@app.route('/users/<id>/edit')
def edit_user(id):
    mysql = connectToMySQL('users')
    query = "SELECT * FROM users WHERE ID = %(id)s"
    data = {
        "id": id
    }
    users = mysql.query_db(query, data)
    return render_template('update_users/update.html', id=id, users=users[0])

@app.route('/users/<id>/update', methods=['POST'])
def update_user(id):
    mysql = connectToMySQL('users')
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s WHERE ID = %(id)s;"
    data = {
        "id": id,
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "em": request.form['email']
    }
    mysql.query_db(query, data)
    return redirect(f'/users/{id}')

@app.route('/users/<id>/destroy')
def delete_user(id):
    mysql = connectToMySQL('users')
    query = "DELETE FROM users WHERE ID = %(id)s;"
    data = {
        "id": id
    }
    mysql.query_db(query, data)
    return redirect("/users")


    

if __name__ == "__main__":
    app.run(debug=True)