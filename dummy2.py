from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([p.serialize() for p in products])

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    product_ids = data.get('product_ids', [])

    # Intentional mistake: Not handling the case when a product isn't found
    products = [Product.query.get(product_id) for product_id in product_ids]
    total = sum(product.price for product in products if product) # Intentional mistake: should handle None product
    return jsonify({"message": "Checkout successful", "total": total})

@app.before_first_request
def setup():
    db.create_all()
    if not Product.query.first():
        db.session.add_all([
            Product(name="Laptop", price=1000.0),
            Product(name="Phone", price=500.0),
            Product(name="Headphones", price=100.0)
        ])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)