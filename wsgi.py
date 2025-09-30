import click, pytest, sys
from datetime import datetime
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Shift, Staff, Admin, staff
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    db.drop_all()
    db.create_all()

    staff1 = Staff(fName='John', lName='Doe', role='admin')
    staff2 = Staff(fName='Jane', lName='Smith', role='staff')
    staff3 = Staff(fName='Alice', lName='Johnson', role='staff')
    staff4 = Staff(fName='Bob', lName='Brown', role='staff')
    
    db.session.add_all([staff1, staff2, staff3, staff4])
    db.session.commit()

    shift1 = Shift(date=datetime(2025, 10, 1).date(), sTime=datetime(2025, 10, 1, 9, 0).time(), eTime=datetime(2025, 10, 1, 17, 0).time(), staffID=staff1.staffID)
    shift2 = Shift(date=datetime(2025, 10, 2).date(), sTime=datetime(2025, 10, 2, 10, 0).time(), eTime=datetime(2025, 10, 2, 18, 0).time(), staffID=staff3.staffID)
    shift3 = Shift(date=datetime(2025, 10, 3).date(), sTime=datetime(2025, 10, 3, 8, 0).time(), eTime=datetime(2025, 10, 3, 16, 0).time())
    shift4 = Shift(date=datetime(2025, 10, 4).date(), sTime=datetime(2025, 10, 4, 12, 0).time(), eTime=datetime(2025, 10, 4, 20, 0).time(), staffID=staff4.staffID)

    db.session.add_all([shift1, shift2, shift3, shift4])
    db.session.commit()

    print('database initialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)


'''
Staff Commands
'''
staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("list", help="List all staff members")
def list_staff_command():
    staff_list = Staff.query.all()
    for staff in staff_list:
        print(f"ID: {staff.staffID}, Name: {staff.fName} {staff.lName}, Role: {staff.role}")

@staff_cli.command("shifts", help="View shifts from ___ to ___ (format: YYYY-MM-DD)")
@click.argument("from_date") # Format: YYYY-MM-DD
@click.argument("to_date")   # Format: YYYY-MM-DD
def list_shifts_command(from_date, to_date):
    shift_list = Shift.query.filter(Shift.date >= from_date, Shift.date <= to_date).all()
    for shift in shift_list:
        assigned = f", Assigned to Staff ID: {shift.staffID}" if shift.staffID else ", Not assigned"
        print(f"Shift ID: {shift.shiftID}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}{assigned}")

@staff_cli.command("clock_in", help="Clock in to a shift")
@click.argument("shift_id")
@click.argument("staff_id")
def clock_in_command(shift_id, staff_id):
    shift = Shift.query.get(shift_id)
    staff = Staff.query.get(staff_id)
    if shift and staff:
        if shift.staffID == staff.staffID:
            if shift.clockIn is None:
                shift.clockIn = datetime.now().time()
                db.session.commit()
                print(f"{staff.fName} {staff.lName} clocked in to shift ID {shift_id} at {shift.clockIn}.")
            else:
                print(f"Shift ID {shift_id} already has a clock-in time: {shift.clockIn}.")
        else:
            print(f"Shift ID {shift_id} is not assigned to Staff ID {staff_id}.")
    else:
        print(f"Shift with ID {shift_id} or Staff with ID {staff_id} not found.")

@staff_cli.command("clock_out", help="Clock out from a shift")
@click.argument("shift_id")
@click.argument("staff_id")
def clock_out_command(shift_id, staff_id):
    shift = Shift.query.get(shift_id)
    staff = Staff.query.get(staff_id)
    if shift and staff:
        if shift.staffID == staff.staffID:
            if shift.clockOut is None:
                shift.clockOut = datetime.now().time()
                db.session.commit()
                print(f"{staff.fName} {staff.lName} clocked out from shift ID {shift_id} at {shift.clockOut}.")
            else:
                print(f"Shift ID {shift_id} already has a clock-out time: {shift.clockOut}.")
        else:
            print(f"Shift ID {shift_id} is not assigned to Staff ID {staff_id}.")
    else:
        print(f"Shift with ID {shift_id} or Staff with ID {staff_id} not found.")


app.cli.add_command(staff_cli)


'''
Admin Commands
'''
admin_cli = AppGroup('admin', help='Admin object commands')

@admin_cli.command("create_staff", help="Create a new staff member")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("role")
def create_staff_command(first_name, last_name, role):
    new_staff = Staff(fName=first_name, lName=last_name, role=role)
    db.session.add(new_staff)
    db.session.commit()
    print(f"Staff member {first_name} {last_name} created with role {role}. ID: {new_staff.staffID}")

@admin_cli.command("delete_staff", help="Delete a staff member by ID")
@click.argument("staff_id")
def delete_staff_command(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        print(f"Staff member, {staff.fName} {staff.lName} with ID {staff_id} deleted.")
    else:
        print(f"Staff member with ID {staff_id} not found.")

@admin_cli.command("create_shift", help="Create a new shift")
@click.argument("date")  # Format: YYYY-MM-DD
@click.argument("start_time")  # Format: HH:MM
@click.argument("end_time")  # Format: HH:MM
def create_shift(date, start_time, end_time):

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()  # For db.Date
        parsed_start_time = datetime.strptime(start_time, "%H:%M").time()  # For db.Time
        parsed_end_time = datetime.strptime(end_time, "%H:%M").time()      # For db.Time
    except ValueError as e:
        print(f"❌ Invalid date or time format: {e}")
        return

    new_shift = Shift(date=parsed_date, sTime=parsed_start_time, eTime=parsed_end_time)
    db.session.add(new_shift)
    db.session.commit()
    print(f"Shift created on {parsed_date} from {parsed_start_time} to {parsed_end_time}. ID: {new_shift.shiftID}")

@admin_cli.command("delete_shift", help="Delete a shift by ID")
@click.argument("shift_id")
def delete_shift(shift_id):
    shift = Shift.query.get(shift_id)
    if shift:
        db.session.delete(shift)
        db.session.commit()
        print(f"Shift with ID {shift_id} deleted.")
    else:
        print(f"Shift with ID {shift_id} not found.")

@admin_cli.command("add_to_shift", help="Add a staff member to a shift")
@click.argument("shift_id")
@click.argument("staff_id")
def add_to_shift_command(shift_id, staff_id):
    shift = Shift.query.get(shift_id)
    staff = Staff.query.get(staff_id)
    if shift and staff:
        shift.staffID = staff.staffID
        db.session.commit()
        print(f"Staff member {staff.fName} {staff.lName} added to shift ID {shift_id}.")
    else:
        print(f"Shift with ID {shift_id} or Staff with ID {staff_id} not found.")

@admin_cli.command("remove_from_shift", help="Remove a staff member from a shift")
@click.argument("shift_id")
def remove_from_shift_command(shift_id):
    shift = Shift.query.get(shift_id)
    if shift:
        shift.staffID = None
        db.session.commit()
        print(f"Staff member {staff.fName} {staff.lName} removed from shift ID {shift_id}.")
    else:
        print(f"Shift with ID {shift_id} not found.")


@admin_cli.command("roster_report", help="View full roster report")
def roster_report_command():
    shift_list = Shift.query.all()
    for shift in shift_list:
        if shift.staff:
            print(f"Shift ID: {shift.shiftID}, {shift.staff.fName} {shift.staff.lName}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}, Clock In: {shift.clockIn}, Clock Out: {shift.clockOut}")
        else:
            print(f"Shift ID: {shift.shiftID}, Unassigned staff, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}")

@admin_cli.command("individual_report", help="View individual report")
@click.argument("staff_id")
def individual_report_command(staff_id):
    roster = Shift.query.filter_by(staffID=staff_id).all()
    if roster:
        for shift in roster:
            staff = shift.staff  # Access the staff related to this shift
            if staff:  # Just in case it's None
                print(f"Shift ID: {shift.shiftID}, {staff.fName} {staff.lName}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}, Clock In: {shift.clockIn}, Clock Out: {shift.clockOut}")
            else:
                print(f"Shift ID: {shift.shiftID}, Unassigned staff, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}, Clock In: {shift.clockIn}, Clock Out: {shift.clockOut}")
    else:
        print(f"No shifts found for Staff ID: {staff_id}")

app.cli.add_command(admin_cli)

'''
Shifts Commands
'''

shifts_cli = AppGroup('shifts', help='Admin object commands')

@shifts_cli.command("from", help="View shifts from ___ to ___ (format: YYYY-MM-DD)")
@click.argument("from_date") # Format: YYYY-MM-DD
@click.argument("to_date")   # Format: YYYY-MM-DD
def list_shifts_from_command(from_date, to_date):
    shift_list = Shift.query.filter(Shift.date >= from_date, Shift.date <= to_date).all()
    for shift in shift_list:
        assigned = f", Assigned to Staff ID: {shift.staffID}" if shift.staffID else ", Not assigned"
        print(f"Shift ID: {shift.shiftID}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}{assigned}")

@shifts_cli.command("all", help="View all shifts")
def list_all_shifts_command():
    shift_list = Shift.query.all()
    for shift in shift_list:
        assigned = f", Assigned to Staff ID: {shift.staffID}" if shift.staffID else ", Not assigned"
        print(f"Shift ID: {shift.shiftID}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}{assigned}")


@shifts_cli.command("indi", help="View roster for a specific staff member by ID")
@click.argument("staff_id")
def individual_shifts_command(staff_id):
    roster = Shift.query.filter_by(staffID=staff_id).all()
    if roster:
        for shift in roster:
            staff = shift.staff  # Access the staff related to this shift
            if staff:  # Just in case it's None
                print(f"Shift ID: {shift.shiftID}, {staff.fName} {staff.lName}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}")
            else:
                print(f"Shift ID: {shift.shiftID}, Unassigned staff, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}")
    else:
        print(f"No shifts found for Staff ID: {staff_id}")


app.cli.add_command(shifts_cli)