from dataclasses import fields

from flask import request, jsonify
from flask_restful import Resource
from PolygonERP.models.user import User
from PolygonERP.models.database import db
from PolygonERP.utils.auth_utils import is_user_admin, generate_username


class UserListResource(Resource):

    def get(self, user_id):
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append({
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'maiden_name': user.maiden_name,
                'mothers_name': user.mothers_name,
                'pob': user.pob,
                'dob': user.dob,
                'address': user.address,
                'tax_num': user.tax_num,
                'taj_number': user.taj_number,
                'base_pay': user.base_pay,
                'email_address': user.email_address,
                'job_title': user.job_title,
                'is_admin': user.is_admin,

            })
        return jsonify({users_list})

    def post(self):
        data = request.get_json()
        user = User(
        username= generate_username(data.name),
        name= data.name,
        maiden_name= data.maiden_name,
        mothers_name= data.mothers_name,
        pob= data.pob,
        dob= data.dob,
        address= data.address,
        tax_num= data.tax_num,
        taj_number= data.taj_number,
        base_pay= data.base_pay,
        email_address= data.email_address,
        job_title= data.job_title,
        is_admin= is_user_admin(data.is_admin),
        )

        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully', 'id': user.id}, 201