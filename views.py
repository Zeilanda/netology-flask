from typing import Type

from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import Advert, DSN, Base
from schema import validate, CreateAdvertSchema, HttpError, PatchAdvertSchema

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


def get_by_id(item_id: int, orm_model: Type[Advert], session):
    orm_item = session.query(orm_model).get(item_id)
    if orm_item is None:
        raise HttpError(404, "item not found")
    return orm_item


class AdvertView(MethodView):

    def get(self, advert_id: int):
        print("hello")
        with Session() as session:
            advert = get_by_id(advert_id, Advert, session)
            return jsonify(
                {
                    "ad_header": advert.ad_header,
                    "owner": advert.owner,
                    "created_at": advert.created_at.isoformat(),
                }
            )

    def post(self):
        json_data = request.json
        with Session() as session:
            new_advert = Advert(**validate(json_data, CreateAdvertSchema))
            session.add(new_advert)
            session.commit()
            return jsonify({'status': "ok", 'id': new_advert.id})

    def patch(self, advert_id: int):
        data_to_patch = validate(request.json, PatchAdvertSchema)
        with Session() as session:
            advert = get_by_id(advert_id, Advert, session)
            for field, value in data_to_patch.items():
                setattr(advert, field, value)
            session.commit()
            return jsonify({"status": "success"})

    def delete(self, advert_id: int):
        with Session() as session:
            advert = get_by_id(advert_id, Advert, session)
            session.delete(advert)
            session.commit()
            return jsonify({"advert_delete": "success"})


Base.metadata.create_all(engine)
