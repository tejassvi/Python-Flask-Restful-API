import sqlite3
from db import db

class MarkerModel(db.Model):
    __tablename__ = 'markers'

    id = db.Column(db.Integer, primary_key =True)
    locationdata = db.Column(db.String(200))
    date = db.Column(db.String(20))
    submittedby_id = db.Column(db.Integer)


    def __init__(self,locationdata,date,submittedby_id):
        # self._id = _id
        self.locationdata = locationdata
        self.date = date
        self.submittedby_id = submittedby_id

    def json(self):
        return {"Location Data" : self.locationdata, "Date" : self.date, "Submitted By Id" : self.submittedby_id}

    @classmethod
    def find_by_id(cls,submittedby_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT users.fname, users.lname,markers.locationdata,markers.submittedby_id from markers INNER JOIN users where users.id = markers.submittedby_id and markers.submittedby_id=?"
        result = cursor.execute(query,(submittedby_id,))
        rows = result.fetchall()
        if rows:
            data = []
            for row in rows:
                data.append({"Fname" : row[0], "Lname" : row[1], "Location Data" : row[2], "Submittted By Id" : row[3]})
            connection.close()
            return {"Markers submitted by ID {}".format(submittedby_id) : data},201

        else:
            {"message" : "Marker not found"}, 404
                            
    @classmethod
    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query ="INSERT INTO markers VALUES (NULL,?,?,?)"
        cursor.execute(query,(self.locationdata,self.date,self.submittedby_id))

        connection.commit()
        connection.close()

    
    @classmethod
    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query ="UPDATE markers SET locationdata=?, date=? where submittedbyid=?"
        cursor.execute(query,(self.locationdata,self.date,self.submittedby_id))

        connection.commit()
        connection.close()


