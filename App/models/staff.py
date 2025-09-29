from App.database import db

class Staff(db.Model):
    staffID = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(10), nullable=False)
    lName = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='staff')

    def __init__(self, fName, lName, role='staff'):
        self.fName = fName
        self.lName = lName
        self.role = role

    def get_json(self):
        return{
            'staffID': self.staffID,
            'fName': self.fName,
            'lName': self.lName,
            'role': self.role
        }

    def view_staff(self):
        return f'Staff ID: {self.staffID}, Name: {self.fName} {self.lName}, Role: {self.role}'
    
    def clock_in(self, shift_id):
        from .shift import Shift
        shift = Shift.query.get(shift_id)
        if shift and shift.staffID == self.staffID:
            # Add clock in logic here
            return f'{self.fName} {self.lName} clocked in for shift {shift_id}'
        return f'Shift {shift_id} not found or not assigned to you'
    
    def clock_out(self, shift_id):
        from .shift import Shift
        shift = Shift.query.get(shift_id)
        if shift and shift.staffID == self.staffID:
            # Add clock out logic here
            return f'{self.fName} {self.lName} clocked out from shift {shift_id}'
        return f'Shift {shift_id} not found or not assigned to you'

    def view_roster(self):
        from .shift import Shift
        shifts = Shift.query.filter_by(staffID=self.staffID).all
        return f'Roster for {self.fName} {self.lName}: {len(shifts)} shifts'

    def view_indi_roster(self, staffID):
        return f'Individual Roster for Staff ID: {staffID}'