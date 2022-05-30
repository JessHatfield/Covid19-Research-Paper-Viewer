from flask import request, jsonify
from flask_cors import cross_origin

from search_api.app.models import PaperStore, PaperSchema
from search_api.app.routes import bp


@bp.route('/search', methods=['GET'])
def search_paper_metadata():  # put application's code here
    search_term = request.args.get('search_term')

    search_term = search_term.lower()

    if search_term is None:
        return jsonify([])

    results = PaperStore.query.filter(PaperStore.title.like(f"%{search_term}%") |
                                      PaperStore.authors.like(f"%{search_term}%") |
                                      PaperStore.journal.like(f"%{search_term}%") |
                                      PaperStore.abstract.like(f"%{search_term}%")
                                      ).all()

    papers_schema = PaperSchema(many=True)

    return jsonify(papers_schema.dump(results))
