from flask import Blueprint, request, jsonify
from Models.user_model import user_model
from Models.auth_model import auth_model

user = Blueprint('user', __name__)
usrObj = user_model()
auth = auth_model()


@user.route('/getall', methods=['GET'])
@auth.token_auth()
def user_getall_controller():
    return usrObj.user_getall_model()


@user.route('/addOne', methods=['POST'])
def user_addOne_controller():
    return usrObj.user_addOne_model(request.json)


@user.route('/updateOne', methods=['PUT'])
def user_updateOne_controller():
    return usrObj.user_updateOne_model(request.json)


@user.route('/deleteOne', methods=['DELETE'])
def user_deleteOne_controller():
    return usrObj.user_deleteOne_model(request.json)


@user.route('/getOne/<int:id>', methods=['GET'])
def user_getOne_controller(id):
    print(id)
    return usrObj.user_getOne_model(id)


@user.route('/advUpdateOne/<id>', methods=['PATCH'])
def user_advUpdateOne_controller(id):
    return usrObj.user_advUpdateOne_model(request.json,id)


@user.route('/login', methods=['POST'])
def user_login_controller():
    return usrObj.user_login_model(request.json)