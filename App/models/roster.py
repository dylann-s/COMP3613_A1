from App.database import db

class Roster(db.Model):
    rosterID = db.Column(db.Integer, primary_key=True, unique=True)
    shifts = db.relationship('Shift', backref='roster', lazy=True)

    def __init__ (self, rosterID):
        self.rosterID = rosterID
        self.shifts = []    
        pass

    def get_shifts(self):
        return self.shifts
    
    def get_staff_shifts(self, staffID):
        staff_shifts = [shift for shift in self.shifts if shift.staffID == staffID]
        return staff_shifts
    
    def get_shifts_report(self):
        report = f'Roster ID: {self.rosterID} has {len(self.shifts)} shifts.'
        return report
