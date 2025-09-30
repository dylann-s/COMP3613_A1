from App.database import db
from datetime import datetime, time, date

class Shift(db.Model):
    shiftID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    sTime = db.Column(db.Time, nullable=False)
    eTime = db.Column(db.Time, nullable=False)
    clockIn = db.Column(db.Time, nullable=True)
    clockOut = db.Column(db.Time, nullable=True)

    staff = db.relationship("Staff", backref="shifts")

    def __init__(self, date, sTime, eTime, staffID=None, clockIn=None, clockOut=None):
        self.staffID = staffID
        self.date = date
        self.sTime = sTime
        self.eTime = eTime
        self.clockIn = clockIn
        self.clockOut = clockOut



    def get_json(self):
        return{
            
        }