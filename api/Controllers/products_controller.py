from flask import Blueprint

products = Blueprint('products', __name__)

@products.route('/')
def productsFunc():
    return 'Products!'