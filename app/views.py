from flask import request, jsonify
from flask.views import MethodView

from errors import ApiError
from crud import create_item, get_item, patch_item, delete_item
from auth import hash_password, check_password, check_auth
from schema import validate, Register, Login, PatchUser
from models import get_session_maker, Owner, Token

Session = get_session_maker()


def register():
    owner_data = validate(Register, request.json)
    with Session() as session:
        owner_data["password"] = hash_password(owner_data["password"])
        owner = create_item(session, Owner, **owner_data)
        return jsonify({"id": owner.id})


def login():
    login_data = validate(Login, request.json)
    with Session() as session:
        owner = session.query(Owner).filter(Owner.email == login_data["email"]).first()
        if owner is None or not check_password(owner.password, login_data["password"]):
            raise ApiError(401, "Invalid user or password")

        token = Token(user=owner)
        session.add(token)
        session.commit()
        return jsonify({"token": token.id})


class OwnerView(MethodView):
    def get(self, owner_id):
        with Session() as session:
            owner = get_item(session, Owner, owner_id)
            return jsonify(
                {"id": owner_id, "email": owner.email, "created_at": owner.created_at.isoformat()}
            )

    def patch(self, owner_id):
        with Session() as session:
            patch_data = validate(PatchUser, request.json)
            if "password" in patch_data:
                patch_data["password"] = hash_password(patch_data["password"])

            token = check_auth(session)
            owner = get_item(session, Owner, owner_id)
            if token.user_id != owner_id:
                raise ApiError(403, "user has no acsess")
            owner = patch_item(session, owner, **patch_data)

            return jsonify(
                {"id": owner.id,
                 "email": owner.email,
                 "created_at": owner.created_at.isoformat(),
                 }
            )

    def delete(self, owner_id: int):
        with Session() as session:
            owner = get_item(session, Owner, owner_id)
            token = check_auth(session)
            if token.owner_id != owner.id:
                raise ApiError(403, "user has no acsess")

            delete_item(session, owner)

            return {"deleted": True}
