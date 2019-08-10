from flask import Flask, jsonify, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'testusername'
app.config['MYSQL_DATABASE_PASSWORD'] = 'passwordtest'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

# rest api to get all users
@app.route('/api/user')
def get():
    cur = mysql.connect().cursor()
    cur.execute('''select * from users''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(r)

 # rest api to get a single user
@app.route("/api/user/<id>", methods=["GET"])
def user_detail(id):
    cur = mysql.connect().cursor()
    cur.execute('''select * from users where id='''+id)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify(r)

#rest api to create a new user in mysql database
@app.route("/api/user", methods=["POST"])
def user_add():
    print("/api/user POST")
    conn = mysql.connect()
    cur = conn.cursor()
    username=request.json['username']
    password=request.json['password']
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    val = (username, password)
    cur.execute(sql, val)
    conn.commit()
    return jsonify(cur.rowcount.__str__() + " records added ")

#rest api to update a user in mysql database
@app.route("/api/user/<id>", methods=["PUT"])
def user_update(id):
    print("/api/user PUT")
    conn = mysql.connect()
    cur = conn.cursor()
    username=request.json['username']
    password=request.json['password']
    sql = "Update users SET username=%s, password=%s WHERE id=%s"
    val = (username, password, id)
    cur.execute(sql, val)
    conn.commit()
    return jsonify(cur.rowcount.__str__() + " records updated ")

#rest api to delete a user in mysql database
@app.route("/api/user/<id>", methods=["DELETE"])
def user_delete(id):
    print("/api/user PUT")
    conn = mysql.connect()
    cur = conn.cursor()
    sql = "Delete from users WHERE id=%s"
    val = (id)
    cur.execute(sql, val)
    conn.commit()
    return jsonify(cur.rowcount.__str__() + " records deleted ")

    
if __name__ == '__main__':
    app.run()