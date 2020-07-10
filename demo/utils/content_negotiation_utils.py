from flask import request


def request_wants_json():
    """Simple method which can be used to negotiate based on the Accept header

    Use it like:

    if request_wants_json():
        return jsonify(...)
    else
        return render_template(...)

    See http://flask.pocoo.org/snippets/45
    """
    best = request.accept_mimetypes.best_match(["application/json", "text/html"])

    return best == "application/json" and request.accept_mimetypes[best] > request.accept_mimetypes["text/html"]
