from flask import Blueprint
from Models.user_model import user_model

user = Blueprint('user', __name__)
usrObj = user_model()


@user.route('/')
def user_signup_controller():
    return usrObj.user_signup()