from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import appointment, user

@app.route('/') 
def home():
    return redirect('/register_&_login_view')

@app.route('/create_appointment')         
def create_appointment(): 
    if "user_id" not in session:
        return redirect ('/register_&_login_view')

    else:
        logged_user = user.User.grab_one_user_by_id({"id":session["user_id"]})
        return render_template ("create_appointment.html", logged_user = logged_user)

@app.route('/create_appointment_process', methods = ["POST"])         
def create_appointment_process(): 
    if "user_id" not in session:
        return redirect ('/register_&_login_view')

    if not appointment.Appointment.validate_appointments(request.form):
        return redirect ("/create_appointment")
    else:
        form_results = {
            "time": request.form["time"],
            "date": request.form["date"],
            "creator_id": session["user_id"]
        }
        appointment_id = appointment.Appointment.create_appointment(form_results)

        return redirect (f"/view_appointment/{appointment_id}")

@app.route('/view_appointment/<int:id>')         
def view_appointment(id): 
    this_appointment = appointment.Appointment.get_one_appointment(id)

    return render_template("view_appointment.html", this_appointment = this_appointment)

@app.route('/appointment/edit/<int:id>') #viewing one recipe          
def edit_appointment(id):
    this_appointment = appointment.Appointment.get_one_appointment(id)
    return render_template("edit_appointment.html", this_appointment = this_appointment)


@app.route('/appointment/edit_process/<int:id>', methods = ["POST"]) #viewing one recipe          
def edit_appointment_process(id):
    if "user_id" not in session:
        print ("not logged in, going back to root route")
        return redirect('/register_&_login_view')
    if not appointment.Appointment.validate_appointments(request.form):
        return redirect (f"/appointment/edit/{id}")
    form_results = {
            "date":request.form["date"],
            "time":request.form["time"],
            "id":id #so we know which query to edit in the database
        }
    appointment.Appointment.update_appointment(form_results)

    return redirect(f'/view_appointment/{id}')

@app.route('/appointment/delete/<int:id>')           
def delete_appointment(id):
    if "user_id" not in session:
        print ("not logged in, going back to root route")
        return redirect('/register_&_login_view')
    appointment.Appointment.delete_appointment(id)
    return redirect ("/create_appointment")

@app.route('/owner/appointment/delete/<int:id>')           
def owner_delete_appointment(id):
    if "user_id" not in session:
        print ("not logged in, going back to root route")
        return redirect('/register_&_login_view')
    appointment.Appointment.delete_appointment(id)
    return redirect ("/appointments_table")

@app.route('/appointments_table')         
def appointments_table(): 
    if "user_id" not in session:
        return redirect ('/register_&_login_view')
    else:
        All_appointment_objects = appointment.Appointment.get_all_appointments()
        logged_user = user.User.grab_one_user_by_id({"id":session["user_id"]})
        return render_template ("appointments_table.html", logged_user=logged_user, List_Appointment_Objects=All_appointment_objects) 


@app.route('/test')
def test():
    return render_template ("test.html" )