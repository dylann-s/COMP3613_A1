from App.database import db
from .staff import Staff

class Admin(Staff):


    def __init__(self, staffID, fName, lName, role='admin'):
        
        super().__init__(staffID, fName, lName, role)

    def add_staff(self,fname, lname):
        new_staff = Staff(fName=fname, lName=lname)
        db.session.add(new_staff)
        db.session.commit()
        return f'Admin {self.fName} {self.lName} added staff: {fname} {lname} (ID: {new_staff.staffID})'

    def remove_staff(self, staff_id):
        staff = Staff.query.get(staff_id)
        if staff:
            db.session.delete(staff)
            db.session.commit()
            return f'Admin {self.fName} {self.lName} removed staff: {staff.fName} {staff.lName} (ID: {staff.staffID})'
        return f'Staff ID: {staff_id} not found.'

    def create_shift():
        pass

    def delete_shift():
        pass

    def add_to_shift(self):
        pass

    def remove_from_shift():
        pass

    def remove_all_shifts():
        pass

    def view_shift_report():
        pass