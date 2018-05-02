import flask
from parking import api_find_bays

application = flask.Flask(__name__)


# basic json api
@application.route('/api/v1/bays', methods=['GET'], strict_slashes=False)
def find_bays():
    return flask.jsonify(api_find_bays(flask.request.args.to_dict()))


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
