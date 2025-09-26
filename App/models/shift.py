from App.database import db

class Shift(db.Model):
    shiftID = db.Column(db.Integer, primary_key=True, unique=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sTime = db.Column(db.DateTime, nullable=False)
    eTime = db.Column(db.DateTime, nullable=False)
    clockIn = db.Column(db.DateTime, nullable=True)
    clockOut = db.Column(db.DateTime, nullable=True)

    def __init__(self, shiftID, staffID, date, sTime, eTime, clockIn=None, clockOut=None):
        self.shiftID = shiftID
        self.staffID = staffID
        self.date = date
        self.sTime = sTime
        self.eTime = eTime
        self.clockIn = clockIn
        self.clockOut = clockOut

    def get_json(self):
        return{
            
        }