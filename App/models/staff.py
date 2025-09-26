from App.database import db

class Staff(db.Model):
    staffID = db.Column(db.Integer, primary_key=True, unique=True)
    fName = db.Column(db.String(10), nullable=False)
    lName = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='staff')

    def __init__(self, staffID, fName, lName, role='staff'):
        self.staffID = staffID
        self.fName = fName
        self.lName = lName
        self.role = role

    def get_json(self):
        return{
            'staffID': self.staffID,
            'fName': self.fName,
            'lName': self.lName
        }