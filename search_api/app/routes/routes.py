from flask import request, jsonify
from flask_cors import cross_origin

from search_api.api import db
from search_api.app.models import PaperStore, PaperSchema, ReadingList, ReadingListSchema
from search_api.app.routes import bp


class InvalidRequest(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@bp.errorhandler(InvalidRequest)
def handle_invalid_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.route('/search', methods=['GET'])
def search_paper_metadata():  # put application's code here
    search_term = request.args.get('search_term')

    search_term = search_term.lower()

    if search_term is None:
        return jsonify([])

    # hard limit in place to prevent broad queries from fetching entire database
    # pagination is a clear solution to this. Likely offset+limit pagination.
    # offset + limit pagination can lead to performance slow-downs server side
    # However performance hit from returning 40k records seems to occur within the browser itself when loading + rendering data
    # So I'm not too concerned about server speed limits Offset + limit pagination is easy to implement so it wins as the choice of pagination approach

    # Where this production code. Pagination would be the next API feature to add!!
    results = PaperStore.query.filter(PaperStore.title.like(f"%{search_term}%") |
                                      PaperStore.authors.like(f"%{search_term}%") |
                                      PaperStore.journal.like(f"%{search_term}%") |
                                      PaperStore.abstract.like(f"%{search_term}%")
                                      ).limit(1000).all()

    papers_schema = PaperSchema(many=True)

    return jsonify(papers_schema.dump(results))


@bp.route('/reading_list', methods=['GET'])
def get_reading_list():
    reading_list = ReadingList.query.all()

    reading_list_schema = ReadingListSchema(many=True)

    return jsonify(reading_list_schema.dump(reading_list))


@bp.route('/reading_list', methods=['POST'])
def add_item_to_reading_list():
    reading_list_item = request.get_json()

    if reading_list_item is None:
        raise InvalidRequest(message="Request Body Is Missing One Or More Required Keys")

    for key in ['title', 'paper_url']:
        if key not in reading_list_item.keys():
            raise InvalidRequest(message="Request Body Is Missing One Or More Required Keys")

    new_reading_list_item = ReadingList(title=reading_list_item['title'], paper_url=reading_list_item['paper_url'])
    db.session.add(new_reading_list_item)
    db.session.commit()

    reading_list_schema = ReadingListSchema()

    return jsonify(reading_list_schema.dump(new_reading_list_item))
