from App.database import db

class Roster(db.Model):
    rosterID = db.Column(db.Integer, primary_key=True, unique=True)
    shifts = db.relationship('Shift', backref='roster', lazy=True)

    def __init__ (self, rosterID):
        self.rosterID = rosterID
        self.shifts = []    

    def __repr__(self):