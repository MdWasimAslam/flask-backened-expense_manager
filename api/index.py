from flask import Flask,render_template
from Controllers.user_controller import user
from Controllers.gemini_controller import gemini
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(gemini, url_prefix='/gemini')

@app.route('/')
def home():
    return 'Welcome to the API'


if __name__ == '__main__':
    app.run(debug=True)