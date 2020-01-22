from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.markers import MarkerModel
import sqlite3


class Marker(Resource):
    parser = reqparse.RequestParser()
    #Can be used to parse html page fields as well
    parser.add_argument('locationdata',
        type=str,
        required=True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('date',
        type=str,
        required=True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('submittedby_id',
        type=int,
        required=True,
        help = "This field cannot be left blank!"
    )
    
    @jwt_required()
    def get(self,submittedby_id):
        marker = MarkerModel.find_by_id(submittedby_id)
        if marker:
            return marker
        else:
            return {"message" : "Marker not found"}, 404

    @jwt_required()
    def post(self, submittedby_id):
        data = Marker.parser.parse_args()
        marker = {'locationdata' : data['locationdata'], 'date' : data['date'],'submittedby_id' : data['submittedby_id']}

        try:
            marker.insert()
        except:
            return {"message" : "An error occurred inserting the marker"}, 500 #Internal Server Error
        
        return marker.json(), 201

    def delete(self,submittedby_id):
        marker = MarkerModel.find_by_id(submittedby_id)
        if marker:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query ="DELETE FROM markers where id=?"
            cursor.execute(query,(submittedby_id,))
            connection.commit()
            connection.close()
            return {"message" : "Marker Id : {} deleted from database!".format(submittedby_id)}, 201
        else:
            return {"message" : "Marker not found"}, 404

    #idempotent, put can be used to both create or update an existing item
    def put(self,submittedby_id):
        data = Marker.parser.parse_args()

        marker = MarkerModel.find_by_id(submittedby_id)
        updated_marker = {'locationdata' : data['locationdata'],'date' : data['date'],'submittedby_id': data['submittedby_id']}
        

        if marker is None:
            try:
                updated_marker.insert()
            except:
                return {"message" : "An error ocurred inserting the item"}, 500
        else:
            try:
                updated_marker.insert()
            except:
                return {"message" : "An error ocurred updating the item"}, 500
        return updated_marker.json()


class MarkerList(Resource):
    TABLE_NAME = 'markers'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM markers"
        result = cursor.execute(query)
        markers = []
        for row in result:
            markers.append({'id': row[0], 'locationdata': row[1], 'date' : row[2], 'submittedby_id' : row[3]})

        connection.close()
        return {'Markers': markers}

