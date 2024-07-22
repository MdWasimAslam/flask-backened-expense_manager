from flask import Flask
from Controllers.user_controller import user
from Controllers.products_controller import products


app = Flask(__name__)

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(products, url_prefix='/products')


@app.route('/')
def home():
    return 'Home'


if __name__ == '__main__':
    app.run(debug=True)