import json
from app import db
from app.models.bucketlist_models import Bucketlists, Items
from app.bucketlists.bucketlist import decode_token
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource, abort


class BucketlistItems(Resource):
    """
This class contains all the Items resources.
GET: Retrieves the bucketlist item once the bucketlist_id is passed
    Options:
        ?q : This provides a search perimeter
        ?limit: Provides a limit to the items displayed per page.
POST: Adds an item to the bucketlist upon specifying the id

In the case an item is provided in the url:
GET: Retrieves the details of the items
PUT: Updates the item details and lastly,
DELETE: Removes the item from the bucketlist
    """

    def get(self, bucketlist_id):
        """Here we list all bucketlist created by the user"""
        result = {}
        item_list = []
        user_id = decode_token(request)
        bucketlist = Bucketlists.query.filter_by(
            bucketlist_id=bucketlist_id).first()
        if bucketlist is None:
            abort(400, message="Please input the correct ID")
        query_string = request.args.to_dict()
        limit = int(query_string.get('limit', 20))
        page_no = int(query_string.get('page', 1))
        if type(limit) is not int:
            abort(400, message="Limit must be integer")
        if type(page_no) is not int:
            abort(400, message="Page must be integer")

        bucketlist_items = Items.query.filter_by(
            bucketlist_id=bucketlist_id).paginate(
            page_no, limit)
        if not len(bucketlist_items.items):
            abort(400, message="Bucketlist is empty")

        if 'q' in query_string:
            search_result = Items.query.filter(
                Items.name.ilike('%' + query_string['q'] + '%')).paginate(
                page_no, limit)
            if not len(search_result.items):
                abort(
                    400,
                    message="{} does not match any bucketlist item names".format(
                        query_string['q']))
            for item in search_result.items:
                if item.bucketlist.creator.user_id is user_id:
                    if item.bucketlist_id is int(bucketlist_id):
                        result = {
                            "id": item.item_id,
                            "name": item.name,
                            "description": item.description,
                            "completed": item.completed,
                            "date_created": item.date_created,
                            "date_modified": item.date_modified,
                            "bucketlist": item.bucketlist.name,
                            "owner": item.bucketlist.creator.username
                        }
                        item_list.append(result)
            return jsonify(item_list)

        for item in bucketlist_items.items:
            result = {
                "id": item.item_id,
                "name": item.name,
                "description": item.description,
                "completed": item.completed,
                "date_created": item.date_created,
                "date_modified": item.date_modified,
                "bucketlist": item.bucketlist.name,
                "owner": item.bucketlist.creator.username
            }
            item_list.append(result)
        next_page = 'None'
        previous_page = 'None'
        if bucketlist_items.has_next:
            next_page = '{}api/v1/bucketlists/{}/items?limit={}&page={}'.format(
                str(request.url_root),
                str(bucketlist_id),
                str(limit),
                str(page_no + 1))
        if bucketlist_items.has_prev:
            previous_page = '{}api/v1/bucketlists/{}/items?limit={}&page={}'.format(
                str(request.url_root),
                str(bucketlist_id),
                str(limit),
                str(page_no - 1))
        return jsonify({'bucketlist items': item_list,
                        'total pages': bucketlist_items.pages,
                        'previous': previous_page,
                        'next': next_page})

    def post(self, bucketlist_id):
        user_id = decode_token(request)
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(400,
                  message="Kindly make sure you've passed all parameters")
        if not data['item_name']:
            abort(400, message="Name cannot be empty")

        name = data['item_name']
        description = data['item_description']
        completed = False
        if 'completed' in data.keys():
            completed = data['completed']

        item = Items.query.filter_by(
            name=name,
            bucketlist_id=bucketlist_id).first()
        if item:
            abort(400, message="{} bucketlist item already exists".format(
                item.name))
        try:
            new_bucketlist_item = Items(
                name=name,
                description=description,
                completed=completed,
                bucketlist_id=bucketlist_id
            )
            db.session.add(new_bucketlist_item)
            db.session.commit()
            return jsonify({
                'message': "{} bucketlist was succefully created".format(
                    name)})
        except Exception:
            abort(500,
                message="An error occured, Bucket list creation failed")


class OneBucketlistItem(Resource):
    def get(self, bucketlist_id, item_id):
        result = {}
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Provide bucketlist ID to proceed")
        if item_id is None:
            abort(400, message="Provide item ID to proceed")
        single_item = Items.query.filter_by(
            bucketlist_id=bucketlist_id,
            item_id=item_id).first()
        if not single_item:
            abort(400, message="No item matching the id {} in the bucketlist".format(
                item_id))
        result.update({
            single_item.item_id: {
                "name": single_item.name,
                "description": single_item.description,
                "completed": bool(single_item.completed),
                "id": single_item.item_id,
                "date created": single_item.date_created,
                "date modified": single_item.date_modified
            }})
        return jsonify(result)

    def put(self, bucketlist_id, item_id):
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist Id")
        if item_id is None:
            abort(400, message="Missing item id")
        data = json.loads(request.get_data(as_text=True))
        if not data:
            abort(400,
                  message="Please make sure you've passed the right parameters")
        single_item = Items.query.filter_by(
            bucketlist_id=bucketlist_id,
            item_id=item_id).first()

        if not single_item:
            abort(400,
                  message="No bucketlist matching the id {}".format(
                      bucketlist_id))

        try:
            if 'new_item_name' in data.keys():
                single_item.name = data['new_item_name']
            if 'new_item_description' in data.keys():
                single_item.description = data['new_item_description']
            if 'completed' in data.keys():
                if data['completed'].upper() == "TRUE":
                    single_item.completed = True
                elif data['completed'].upper() == "FALSE":
                    single_item.completed = False
                else:
                    abort(400, message='Invalid complete parameters. use True or False.')
                
            single_item.date_modified = datetime.utcnow()
            db.session.add(single_item)
            db.session.commit()
            return jsonify({
                'message': "{} item was updated successfully".format(
                    single_item.name)})
        except Exception:
            abort(500, message="An error occured, Item was not updated")

    def delete(self, bucketlist_id, item_id):
        user_id = decode_token(request)
        if bucketlist_id is None:
            abort(400, message="Missing bucketlist ID")
        if item_id is None:
            abort(400, message="Missing item ID")
        single_item = Items.query.filter_by(
            bucketlist_id=bucketlist_id,
            item_id=item_id).first()
        if not single_item:
            abort(400, message="No item matching the id {}".format(
                item_id))
        try:
            db.session.delete(single_item)
            db.session.commit()
            return jsonify({
                'message': "{} Item deleted successfuly".format(
                    single_item.name)})
        except Exception:
            abort(500, message="An error occured: Item failed to delete")
