from flask import Blueprint, jsonify, request


api = Blueprint('api', __name__)


@api.route('/user/<int:id>')
def user(id):
    from ..models import User, Role, Vacation, Illness

    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        vacation = Vacation.query.filter_by(user_id=id).all()
        illness = Illness.query.filter_by(user_id=id).all()
        role = Role.query.filter_by(id=user.roles_id).first()
        full_name = user.full_name
        return jsonify({
            "full_name": full_name,
            "role": str(role),
            "vacation_request": str(vacation),
            "illness_cases": str(illness),
        })
