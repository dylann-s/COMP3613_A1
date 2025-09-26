from App.database import db
from .staff import Staff

class Admin(Staff):


    def __init__(self, staffID, fName, lName, role='admin'):
        
        super().__init__(staffID, fName, lName, role)
        self.role = role    