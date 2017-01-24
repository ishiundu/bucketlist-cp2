import json
import jwt
from app import db
from app.models.bucketlist_models import Bucketlists, Items
from config import Config
from datetime import datetime
from flask import jsonify, request
from flask_restful import abort, Resource


def decode_token(self):
    """Function to authenticate the token"""
    token = request.headers.get('Authorization')
    if not token:
        abort(401, message="No Authoriztion token")
    try:
        payload = jwt.decode(token, Config.SECRET_KEY)
    except jwt.DecoderError:
        abort(401, message='Token is invalid')
    except jwt.ExpiredSignature:
        abort(401, message='Session expired, please login again')

    return payload['sub']


class Bucketlist(Resource):
    """
This class contains all the Bucketlists Resource.
GET: retrieves all the bucketlist a user has.
?q : Provides a searchparameter
?limit: Provides a limit of how many items can be displayed on a page
POST: Adds a bucketlist.
    """

    def get(self):
        """Here we list all created bucketlists"""
        result = {}
        item_list = []
        bucketlist_list = []
        user_id = decode_token(request)
        query_string = request.args.to_dict()
        # Here we impliment pagination
        limit = int(query_string.get('limit', 20))
        page_no = int(query_string.get('page', 1))
        if type(limit) is not int:
            abort(400, message="Make sure the limit is an integer")
        if type(page_no)is not int:
            abort(400, message="|Make sure the limit is an integer")
        if 'q' in query_string:
            search_result = Bucketlists.query.filter(
                Bucketlists.name.ilike(
                    '%' + query_string['q'] + '%')).filter_by(
                creator_id=user_id).paginate(
                page_no, limit)

            if not len(search_result.items):
                abort(400,
                      message="{} does not match any bucketlist names".format(
                          query_string['q']))

                for bucketlist in search_result.items:
                    if bucketlist.creator_id is user_id:
                        items = Items.query.filter_by(
                            buckelist_id=bucketlist.buckelist_id).all()
                        for item in items:
                            item_list.append({
                                "id": item.item_id,
                                "name": item.name,
                                "description": item.description,
                                "date_created": item.date_created,
                                "date_modified": item.date_modified,
                                "completed": item.completed
                            })
                        result = {
                            "id": bucketlist.buckelist_id,
                            "name": bucketlist.name,
                            "description": bucketlist.description,
                            "date_created": bucketlist.date_created,
                            "date_modified": bucketlist.date_modified,
                            "creator": bucketlist.creator.username
                        }
                    bucketlist_list.append(result)
                return jsonify(bucketlist_list)

            bucketlists = Bucketlists.query.filter_by(creator_id=user_id).paginate(
                page_no, limit)

            if not len(bucketlists.items):
                abort(400, "User doesn't have a bucketlist")
            for bucketlist in bucketlist_list.items:
                item_list = []
                items = Items.query.filter_by(
                    bucketlist_id=bucketlist.bucketlist_id).all()
                for item in items:
                    item_list.append({
                        "id": item.item_id,
                        "name": item.name,
                        "description": item.description,
                        "date_created": item.date_created,
                        "date_modified": item.date_modified,
                        "completed": item.completed
                    })
                result = {
                    "id": bucketlist.bucketlist_id,
                    "name": bucketlist.name,
                    "description": bucketlist.description,
                    "date_created": bucketlist.date_created,
                    "date_modified": item.date_modified,
                    "creator": bucketlist.creator.username
                }
            bucketlist_list.append(result)
        next_page = 'None'
        previous_page = 'None'
        if bucketlists.has_next:
            next_page = "{}api/v1/bucketlists?limit={}&page={}".format(
                str(request.url_root),
                str(limit),
                str(page_no + 1))
        if bucketlists.has_previous:
            previous_page = "{}api/v1/bucketlists?limit={}&page={}".format(
                str(request.url_root),
                str(limit),
                str(page_no - 1))

        return jsonify({
            "bucketlistlists": bucketlist_list,
            "total pages": bucketlists.pages,
            "previous": previous_page,
            "next": next_page
        })

    def post(self):
        user_id = decode_token(request)
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(400,
                  message="Please supply all the parameters")
        name = data['name']
        description = data['description']
        creator_id = user_id

        if not name:
            abort(400, "Name cannot be empty")
            bucketlist = Bucketlists.query.filter_by(
                name=name,
                creator_id=user_id)
        if bucketlist:
            abort(400, "{} bucketlist already exists".format(bucketlist.name))

        try:
            new_bucketlist = Bucketlists(
                name=name,
                description=description,
                date_created=datetime.utcnow(),
                creator_id=creator_id
            )
            db.session.add(new_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist created successfully".format(name)})
        except Exception:
            abort(500, message="Bucketlist not created")


class OneBucketlist(Resource):
    def get(self, bucketlist_id):
        result = {}
        item_list = []
        user_id = decode_token(request)
        single_bucketlist = Bucketlists.query.filter_by(
            creator_id=user_id,
            bucketlist_id=bucketlist_id).first()
        if not single_bucketlist:
            abort(400, messgae="No bucketlist matching the the id {}".format(
                bucketlist_id))
        items = Items.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        for item in items:
            item_list.append({
                "id": item.item_id,
                "name": item.name,
                "description": item.description,
                "date_created": item.date_created,
                "date_modified": item.date_modified,
                "completed": item.completed
            })
        result.update({
            single_bucketlist.bucketlist_id: {
                "name": single_bucketlist.name,
                "description": single_bucketlist.description,
                "items": item_list,
                "date_created": single_bucketlist.date_created,
                "date_modified": item.date_modified,
                "completed": item.completed
            }})
        return jsonify(result)

    def put(self, bucketlist_id):
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(400,
                  message="Please pass the necessary paramateres")
        single_bucketlist = Bucketlists.query.filter_by(
            creator_id=user_id,
            bucketlist_id=bucketlist_id).first()
        if not single_bucketlist:
            abort(400, message="Sorry we can't find a bucketlist matching the id{}".format(
                bucketlist_id))

        try:
            if 'name' in data.keys():
                single_bucketlist.name = data['name']
            if 'description' in data.keys():
                single_bucketlist.description = data['description']
            single_bucketlist.date_modified = datetime.utcnow()
            db.session.add(single_bucketlist)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist updated successfully".format(
                    single_bucketlist.name)})
        except Exception:
            abort(500, message="An error occured, Bucketlist not updated")

    def delete(self, bucketlist_id):
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        single_bucketlist = Bucketlists.query.filter_by(
            creator_id=user_id,
            bucketlist_id=bucketlist_id).first()
        if not single_bucketlist:
            abort(400, message="We can't find the bucketlist matching id{}".format(
                bucketlist_id))

        try:
            items = Items.query.filter_by(
                bucketlist_id=bucketlist_id).all()
            for item in items:
                db.session.delete(item)
                db.session.commit()
                return jsonify({
                    'message': "{} bucketlist was successfuly deleted".format(
                        single_bucketlist.name)})
        except Exception:
            abort(500, message="An Error occured, Bucketlist was not deleted")
