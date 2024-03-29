from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument. SO, MAKE SURE YOU import the app first (row 2)



@app.route('/register_&_login_view')         
def login_register_page(): 
    return render_template("Register_&_Login.html")

@app.route('/register_process', methods = ["POST"]) 
def register():
    print (request.form)
    #validate to make sure everything looks good
    #If the validations are no good, we send the client back and display the error messages.
    if not user.User.validate_registration(request.form):
        return redirect ('/register_&_login_view')
    
    #If the validations are okay, then we can add the new user to the database and send them to the next route (in this case, the dashboard route).

    else:
    # Hash the password, because we do not want to add a non-hashed password to the database.
        hash_password = bcrypt.generate_password_hash(request.form['password'])
        #Now, we need to send all of the information to the database, including the hashed password. So, we need a new data dictionary:

        data = {
            "is_owner": request.form["is_owner"],
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "cell":request.form["cell"],
            "email":request.form["email"],
            "password":hash_password,
            "is_owner":request.form["is_owner"]
        }

        session["user_id"] = user.User.register_user(data) #Talks to the model to saves the new user in the database.
        #Above will return the user id, which is useful so we can save the ID in session and then not let a user in if they are not properly registered. Now, we need to add a class method, in the model file, to grab who is logged in based on ID.

        #Next, in the model, we will need to create a query to find out which user is logged in by ID. So, we add the @classmethod "grab_one_user_by_id"
        
        #get user info so can determine if they are an owner:
        if data["is_owner"] == "1":
            return redirect ('/appointments_table')
        else:
            return redirect ('/create_appointment')
        
        
    # if(user.User.register_user(request.form)):
    #     return redirect('/test')   
    
    # return redirect ('/register_&_login_view')

@app.route('/login_process', methods = ["POST"]) 
def login():
    if not user.User.validate_login(request.form): #return of validate_loging() is "is_valid", so we are saying, "if is_valid is false..."
        return redirect('/register_&_login_view')
    else:
        data = {
            "email":request.form["email"]#we got email and password from login form
        }
        
        found_user = user.User.grab_one_user_by_email(data)
        #above, we get an object back (see grab_one_user_by_email method in user.py model)
        session["user_id"] = found_user.id #Now we can use the id  whereever the user goes throughout the different URLs/Routes of our web ap.

        #Get user info from MYSQL to determine if they are an owner:
        id = {
            "id":session["user_id"]
        }
        user_data = user.User.grab_one_user_by_id(id)
        #if they aret an owner:
        if user_data.is_owner==True:
            return redirect ('/appointments_table')
        else:
            return redirect('/create_appointment')


@app.route('/logout') 
def logout():
    session.clear() #Delete everything from session
    return redirect ('/register_&_login_view')

@app.route('/clients/view/<int:id>')
def view_client(id):
    if "user_id" not in session:
        print ("not logged in, going back to root route")
        return redirect('/register_&_login_view')

    this_user = user.User.get_one_user(id)
    print("this user instance from SQL:", this_user)
    logged_user = user.User.grab_one_user_by_id({"id":session["user_id"]})
    return render_template("view_client.html", this_user = this_user, logged_user=logged_user)


