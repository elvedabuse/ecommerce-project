from flask import Flask, render_template, request, redirect, url_for, session
from recommender.item_based_recommender import ItemBasedRecommender
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger
from flasgger import swag_from

from flask import jsonify, Response
import csv
import json
import random
from datetime import datetime
import xmltodict
import dicttoxml


app = Flask(__name__)
app.secret_key = 'cok-gizli-bir-anahtar'
swagger = Swagger(app)

API_KEY = "123456"

# API Key kontrolü - Sadece API endpoint'lerinde çalışır
@app.before_request
def require_api_key():
    api_endpoints = [
        'get_products_api',
        'orders_api',
        # Eğer başka API endpoint varsa buraya ekle
    ]
    if request.endpoint in api_endpoints:
        token = request.headers.get('X-API-KEY')
        if token != API_KEY:
            return jsonify({"error": "Unauthorized - Invalid or missing API key"}), 401

# datetime'i Jinja'ya global olarak ekle
app.jinja_env.globals.update(datetime=datetime)

USERS_FILE = 'users.json'
ORDERS_FILE = 'orders.json'

# ==========================
# Kullanıcı Veri İşlemleri
# ==========================
def load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

def load_orders():
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)

# ==========================
# Ürün Veri Yükleme
# ==========================
def load_products_from_csv(path):
    products = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = {
                "id": int(row['product_id']),
                "name": row['product_name'],
                "department_id": int(row['department_id']),
                "aisle_id": int(row['aisle_id']),
                "price": 10.0,
                "description": "Ürün açıklaması yok.",
                "image": "default.jpg"
            }
            products.append(product)
    return products

products = load_products_from_csv('recommender/products_demo.csv')

# ==========================
# Öneri Sistemi Kurulumu
# ==========================
recommender = ItemBasedRecommender(
    'recommender/products_demo.csv',
    'recommender/processed_data.pkl'
)
recommender.load_and_prepare_data()
recommender.calculate_similarity()

# ==========================
# Kullanıcı Yönetimi
# ==========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if any(u['username'] == username for u in users):
            return "Bu kullanıcı adı zaten var."

        hashed_pw = generate_password_hash(password)
        users.append({'username': username, 'password': hashed_pw})
        save_users(users)
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        user = next((u for u in users if u['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['cart'] = {}
            return redirect(url_for('index'))
        else:
            return "Geçersiz kullanıcı adı veya şifre."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==========================
# Ürün ve Sepet Sayfaları
# ==========================
@app.route('/')
def index():
    cart = session.get('cart', {})
    total_quantity = sum(cart.values())
    return render_template('index.html', products=products, total_quantity=total_quantity, current_department=0)

@app.route('/category/<int:department_id>')
def filter_by_department(department_id):
    filtered_products = [p for p in products if p['department_id'] == department_id]
    cart = session.get('cart', {})
    total_quantity = sum(cart.values())
    return render_template('index.html',
                           products=filtered_products,
                           total_quantity=total_quantity,
                           current_department=department_id)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        session['cart'] = cart
    return redirect(url_for('cart_view'))

@app.route('/cart')
def cart_view():
    cart = session.get('cart', {})
    products_in_cart = []
    total_price = 0

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            products_in_cart.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })

    recommendations = []
    if products_in_cart:
        first_product_id = products_in_cart[0]['product']['id']
        raw_recs = recommender.get_similar_products(first_product_id, top_n=5)
        for rec in raw_recs:
            prod = next((p for p in products if p['id'] == rec['product_id']), None)
            if prod:
                recommendations.append({
                    'product_id': prod['id'],
                    'product_name': prod['name'],
                    'price': prod.get('price', 0.0),
                    'description': prod.get('description', 'Ürün açıklaması yok.'),
                    'image': prod.get('image', 'default.jpg'),
                    'similarity': rec.get('similarity', 0.0)
                })

    if not recommendations:
        fallback_products = random.sample(products, min(5, len(products)))
        recommendations = [{
            'product_id': p['id'],
            'product_name': p['name'],
            'price': p.get('price', 0.0),
            'description': p.get('description', 'Ürün açıklaması yok.'),
            'image': p.get('image', 'default.jpg'),
            'similarity': 0.0
        } for p in fallback_products]

    return render_template('cart.html',
                           cart=products_in_cart,
                           total_price=total_price,
                           recommendations=recommendations)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Ürün bulunamadı.", 404
    return render_template('product_detail.html', product=product)

# ==========================
# API: Ürün Listesi JSON & XML
# ==========================
@app.route('/api/v1/products', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Ürünleri JSON veya XML formatında döner',
            'examples': {
                'application/json': [
                    {
                        "id": 1,
                        "name": "Chocolate Sandwich Cookies",
                        "department_id": 1,
                        "aisle_id": 1,
                        "price": 10.0,
                        "description": "Ürün açıklaması yok.",
                        "image": "default.jpg"
                    }
                ],
                'application/xml': "<Products><product><id>1</id><name>Chocolate Sandwich Cookies</name>...</product></Products>"
            }
        }
    }
})
def get_products_api():
    accept = request.headers.get('Accept', '')
    if 'application/xml' in accept:
        xml_data = dicttoxml.dicttoxml({'product': products}, custom_root='Products', attr_type=False)
        return Response(xml_data, mimetype='application/xml')
    else:
        return jsonify(products)
# ==========================
# Siparişi Tamamlama
# ==========================
@app.route('/checkout', methods=['POST'])
def checkout():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('cart_view'))

    items = []
    total_price = 0

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            items.append({
                "product_id": product_id,
                "name": product['name'],
                "quantity": quantity,
                "price": product['price'],
                "item_total": item_total,
                "image": product.get('image', 'default.jpg')
            })

    order_record = {
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "total_price": total_price,
        "items": items
    }

    orders = load_orders()
    orders.append(order_record)
    save_orders(orders)

    session['cart'] = {}
    return render_template('order_success.html', order=order_record)

# ==========================
# Sipariş API (JSON & XML)
# ==========================
from flask import request, jsonify, Response

API_KEY = "123456"

@app.route('/orders', methods=['GET', 'POST'])
def orders_api():
    token = request.headers.get('X-API-KEY')
    if token != API_KEY:
        return jsonify({"error": "Unauthorized - Invalid or missing API key"}), 401

    if request.method == 'GET':
        orders = load_orders()

        # İsteğe bağlı username sorgu parametresi al
        req_username = request.args.get('username', None)

        if req_username:
            filtered_orders = [order for order in orders if order['username'] == req_username]
        else:
            filtered_orders = orders

        accept = request.headers.get('Accept', '')
        if 'application/xml' in accept:
            xml_data = dicttoxml.dicttoxml(filtered_orders, custom_root='Orders', attr_type=False)
            return Response(xml_data, mimetype='application/xml')
        else:
            return jsonify(filtered_orders)

    elif request.method == 'POST':
        content_type = request.headers.get('Content-Type', '')

        if 'application/xml' in content_type:
            try:
                data = xmltodict.parse(request.data)
                order = data.get('Orders', {}).get('item')
                if order:
                    if not isinstance(order, list):
                        order = [order]
                    orders = load_orders()
                    for o in order:
                        o['total_price'] = float(o['total_price'])
                        for i in o['items']['item']:
                            i['product_id'] = int(i['product_id'])
                            i['quantity'] = int(i['quantity'])
                            i['price'] = float(i['price'])
                            i['item_total'] = float(i['item_total'])
                        orders.append(o)
                    save_orders(orders)
                    return Response("<response>Order added</response>", mimetype='application/xml', status=201)
                else:
                    return Response("<response>Invalid XML format</response>", mimetype='application/xml', status=400)
            except Exception as e:
                return Response(f"<response>Error: {str(e)}</response>", mimetype='application/xml', status=400)

        elif 'application/json' in content_type:
            data = request.json
            if data:
                orders = load_orders()
                orders.append(data)
                save_orders(orders)
                return jsonify({"message": "Order added"}), 201
            else:
                return jsonify({"error": "Invalid JSON"}), 400

        else:
            return jsonify({"error": "Unsupported Content-Type"}), 415

@app.route('/orders_view')
def orders_view():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    orders = load_orders()
    user_orders = [order for order in orders if order['username'] == username]

    return render_template('orders.html', orders=user_orders)

# ==========================
# Ana Uygulama
# ==========================
if __name__ == '__main__':
    app.run(debug=True)
