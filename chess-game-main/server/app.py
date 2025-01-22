from flask import Flask, request
from flask_cors import CORS
from flask.views import MethodView
import json

from services.find_moves import find_moves

app = Flask(__name__)

class FindMoves(MethodView):
    def post(self):
        data = json.loads(request.data)
        board = data['board']
        selected_player = data['selectedPlayer'].replace('"', '')
        # print (selected_player)
        return json.dumps(find_moves(board, selected_player))

app.add_url_rule('/findmoves', view_func=FindMoves.as_view('findmoves'))

# enables cors
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
