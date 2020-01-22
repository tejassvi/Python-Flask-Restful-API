from db import db

#this class interacts with SQLlite
class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    ref_id = db.Column(db.Integer)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))
    date = db.Column(db.String(80))

    def __init__(self,ref_id,fname,lname,email,password,role,date):
        self.ref_id = ref_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.role = role
        self.date = date

    def json(self):
        return {
            "id" : self.user_id,
            "ref_id" : self.ref_id,
            "fname" : self.fname,
            "lname" : self.lname,
            "email" : self.email,
            # password : self.password,
            "role" : self.role,
            "date" : self.date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, email):
        return cls.query.filter_by(email=email).first() #Select * from users

    @classmethod
    def find_by_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).first()
