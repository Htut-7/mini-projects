from flask import Flask, jsonify, request, url_for
from flaskext.mysql import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'food_delivery'

mysql = MySQL(app)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT id FROM users WHERE email=%s", (data['email'],))
    if cursor.fetchone():
        return jsonify({"message": "Email already exists"}), 409

    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
        (data['name'], data['email'], generate_password_hash(data['password']), 'user')
    )
    mysql.get_db().commit()
    return jsonify({"message": "Registered successfully"})


# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (data['email'],))
    user = cursor.fetchone()

    if user and check_password_hash(user[3], data['password']):
        return jsonify({
            "message": "Login successful",
            "id": user[0],
            "name": user[1],
            "role": user[4]
        })

    return jsonify({"message": "Invalid credentials"}), 401


# ---------------- FOODS ----------------
@app.route('/foods', methods=['GET'])
def get_foods():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM foods")
    rows = cursor.fetchall()

    foods = []
    for row in rows:
        foods.append({
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "image": url_for('static', filename='images/' + row[3], _external=True)
        })

    return jsonify(foods)


# ---------------- CREATE ORDER ----------------
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data['user_id']
    items = data['items']

    cursor = mysql.get_db().cursor()

    for item in items:
        cursor.execute(
            "INSERT INTO orders (user_id, food_id, quantity, status) VALUES (%s,%s,%s,%s)",
            (user_id, item['id'], item['quantity'], 'pending')
        )

    mysql.get_db().commit()
    return jsonify({"message": "Order placed"})


# ---------------- ADMIN GET ORDERS ----------------
@app.route('/orders', methods=['GET'])
def get_orders():
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT o.id, u.name, f.name, o.quantity, o.status
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN foods f ON o.food_id = f.id
        ORDER BY o.id DESC
    """)

    rows = cursor.fetchall()
    orders = []

    for r in rows:
        orders.append({
            "order_id": r[0],
            "customer": r[1],
            "food": r[2],
            "quantity": r[3],
            "status": r[4]
        })

    return jsonify(orders)


# ---------------- UPDATE ORDER STATUS (ADMIN) ----------------
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    status = data.get('status')

    if status not in ['pending', 'accepted', 'rejected']:
        return jsonify({"message": "Invalid status"}), 400

    cursor = mysql.get_db().cursor()
    cursor.execute(
        "UPDATE orders SET status=%s WHERE id=%s",
        (status, order_id)
    )
    mysql.get_db().commit()

    return jsonify({"message": "Order updated"})

if __name__ == "__main__":
    app.run(debug=True)
