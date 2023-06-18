from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Appointment:
    db_name = "barber_shop"
    def __init__(self, data):
        self.id = data["id"]
        self.date = data["date"] 
        self.time = data["time"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None

    @classmethod 
    def add_image(cls, data):
            query = """
            INSERT INTO favorites (date, explanation, image)
            VALUES (%(date)s, %(explanation)s, %(image)s)
            """
            return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod 
    def search_db_by_date(cls, data):
            query = """
                    SELECT * from favorites
                    WHERE DATE = (%(date)s)
                    """
            results = connectToMySQL(cls.db_name).query_db(query, data)
            print("Results:", results)
            if len(results) == 0:
                return None
            else:
                return cls(results[0])

    @classmethod
    def get_all_appointments(cls):
        query = """
        SELECT * FROM appointments
        Join users
        ON users.id = appointments.creator_id
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        print("RESULTS:", results)
        list_of_appointment_objects = []
        for this_appointment_dictionary in results: 
    #Now we create the appointment object:
            new_appointment_object = cls(this_appointment_dictionary)

    #Grab the creator's information:
            user_dictionary = {
                "id":this_appointment_dictionary["users.id"],
                "is_owner": this_appointment_dictionary["is_owner"],
                "first_name":this_appointment_dictionary["first_name"],
                "last_name":this_appointment_dictionary["last_name"],
                "cell":this_appointment_dictionary["cell"],
                "email":this_appointment_dictionary["email"],
                "password":this_appointment_dictionary["password"],
                "created_at":this_appointment_dictionary["users.created_at"],
                "updated_at":this_appointment_dictionary["users.updated_at"]
            }
    #Create the user object:
            user_object = user.User(user_dictionary)

    #Link the user (creator) to this appointment:
            new_appointment_object.creator = user_object

            list_of_appointment_objects.append(new_appointment_object)
    
    #add the following code  in case there aren't any appointments in the database:

        if len(results) == 0:
            return []

        return list_of_appointment_objects

    @classmethod
    def get_one_appointment(cls, id):
        query = """
        SELECT * FROM appointments
        JOIN users
        ON users.id=appointments.creator_id
        WHERE appointments.id = %(id)s
        """
        data = {"id":id}
    #Below, need a data dictionary as we need the id of the appointment.
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
    #we use "results[0]", because SQL brings back a list of dictionaries. Here, we have one recipe dictionary that SQL brings back, so we use index of zero.
        if not results:
            return None
        else:
            new_appointment_object = cls(results[0])
            print("new appointment object:", new_appointment_object)
            #Grab the creator's information:
            
            user_dictionary = {
                "id":results[0]["users.id"],
                "first_name":results[0]["first_name"],
                "last_name":results[0]["last_name"],
                "email":results[0]["email"],
                "cell":results[0]["cell"],
                "is_owner":results[0]["is_owner"],
                "password":results[0]["password"],
                "created_at":results[0]["users.created_at"],
                "updated_at":results[0]["users.updated_at"]
            }
    #Create the user object:
            user_object = user.User(user_dictionary)

    #Link the user (creator) to this recipe:
            new_appointment_object.creator = user_object

#Results is a list, but we need to pass in a DICTIONARY, sp we need a specific dictionary, at this case at index 0. 
        return new_appointment_object

    @classmethod
    def create_appointment(cls, data_dictionary):
        
        query = """
        INSERT INTO appointments (time, date, creator_id) 
        VALUES (%(time)s, %(date)s, %(creator_id)s)
        """
        return connectToMySQL(cls.db_name).query_db(query, data_dictionary)

    @classmethod
    def update_appointment(cls, data_dictionary):
        query = """UPDATE appointments 
        SET date = %(date)s, time = %(time)s
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.db_name).query_db(query, data_dictionary)

    
    @staticmethod 
    def validate_appointments(form_data):
        is_valid = True
        print("HERE")
        print (form_data)
        if (form_data["time"]) == '':
            is_valid = False
            flash("You must select a time.")
        if (form_data["date"]) == '':
            is_valid = False
            flash("You must select a date.")
        # if "is_owner" not in form_data:
        #     is_valid = False
        #     flash("All fields are required")
        
        return is_valid 
    
    @classmethod
    def delete_appointment(cls,id):
        data = {"id":id}
        query = "DELETE FROM appointments where id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

        




