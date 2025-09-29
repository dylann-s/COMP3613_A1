import click, pytest, sys
from datetime import datetime
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Roster, Shift, Staff, Admin
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
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

app.cli.add_command(staff_cli)

@staff_cli.command("shifts", help="View shifts from ___ to ___ (format: YYYY-MM-DD)")
@click.argument("from_date") # Format: YYYY-MM-DD
@click.argument("to_date")   # Format: YYYY-MM-DD
def list_shifts_command(from_date, to_date):
    shift_list = Shift.query.filter(Shift.date >= from_date, Shift.date <= to_date).all()
    for shift in shift_list:
        assigned = f", Assigned to Staff ID: {shift.staffID}" if shift.staffID else ", Not assigned"
        print(f"Shift ID: {shift.shiftID}, Date: {shift.date}, Start: {shift.sTime}, End: {shift.eTime}{assigned}")

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
        # Convert inputs to proper Python types
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

app.cli.add_command(admin_cli)

'''
Shifts Commands
'''

'''
Roster Commands
'''