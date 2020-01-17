# Coursework - due Jan 13th

# * * * * * * * * * * READ ME * * * * * * * * * * *

# -------------------- SUMMARY POINTS -------------------
# This programme was based on research with practicing GPs in the field, and is built on some key principles
# # taken from this research:
# 1) Appointments cannot be booked further than the month after the current month
# 2) We are assuming there are 4 available consulting rooms in the GP surgery. Once there are doctors on all 4, they cannot
#   add their avaiblity (no of rooms can be increased or decreased for different practices)
# 3) Domain research told me that GPs don't approve patient appointments - it would be an uneccessary use of GP time. I
#    included the functionality anyway to keep to brief!
# Also:
# 4) I have written this code to show that I "can put in practice what we have covered in lectures and practicals" as per the
    # marking scheme on the courework brief. Therefore, I have sometimes arbitrarily done things in different ways purely to show this.
# 5) At any time, pressing the run button will take user back to opening page (login or reg)
# 6) Almost all the functions are in the doc functions.py within in pkg0 and loaded into this page at the start.


# ------------- OVERVIEW OF THE 2 MAIN DATABASES ---------
# 1) user_df = the user directory containing the details (First Name, Last Name, Email, DOB etc) of all users (GPs, Patients, Admin). A pandas dataframe.
# 2) days_dict = the calendar containing all bookings and GP availability. A dictionary where keys are date in str(YYYY-MM-DD) form and values are a pandas dataframe "day_view" (see next line) for each day of the year
#    (NOTE: day_view = the booking / availability page for a specific day in the calendar showing doctor availability, available slots and bookings. Pandas dataframe).
# These are pickled and unpickled between sessions as a means of keeping data persistent:

import pkg0
from pkg0.functions import *
import pandas as pd
pd.set_option('display.max_columns', 30) # Configuring pandas to show 30 (in this case all) columns when printed in console - for convenience of developer
import csv  # Delete?
import os
import sys
import pickle
import calendar
import datetime

global user_current_rec # Global so an updated version of user_current_rec can be returned to Main when it is edited in functions

# ESTABLISHING DATE VARIABLES FOR USE IN FUNCTIONS LATER

today_date = datetime.date.today()
current_year = today_date.year
next_year = today_date.year+1

current_month = today_date.month
if current_month < 12:
    next_month = today_date.month+1
elif current_month == 12:
    jan_1st_next = datetime.date(next_year, 1, 1)
    next_month = jan_1st_next.month
    next_month_str = jan_1st_next.strftime("%B")


#  -------------- LOADING/CREATING USER DIRECTORY & CALENDAR DICTIONARY  --------------

# USER DIRECTORY
# If user_df hasn't been created yet (i.e., it's a GP surgery using this software for the first time), create it:
if os.path.exists('user_df.pickle') == False:
    user_df = pd.DataFrame(
                    {"User Type":[],
                    "First Name":[],
                    "Last Name":[],
                    "Email":[],
                    "User Id":[],
                    "Date Of Birth":[],
                     "Password": [],
                     "Prescriptions":[],
                     "Test Results":[],
                     "Booked Appts":[],
                     "Validation":[]})
elif os.path.exists('user_df.pickle') == True: # Uncpickle user_df from previous session
    pickle_in = open("user_df.pickle", "rb")
    user_df = pickle.load(pickle_in)


# CALENDAR
# If days_dict for CURRENT YEAR hasn't been created and filled yet, fill it with a day view for each day of the current year.
# If it has been created already, unpickle it
if os.path.exists('days_dict_%s.pickle' %str(current_year)) == False:
    days_dict_current = {}
    fill_year_dict(current_year, days_dict_current) # WORKING
elif os.path.exists('days_dict_%s.pickle' %str(current_year)) == True: # Uncpickle calendar/dict from previous session
    pickle_in = open('days_dict_%s.pickle' %str(current_year), "rb")
    days_dict_current = pickle.load(pickle_in)

# If we're in December and days_dict for the NEXT YEAR hasn't been created and filled yet, fill it with a day view for
# # each day of the current year. If it has been created already, unpickle it

if os.path.exists('days_dict_%s.pickle' % str(next_year)) == False:
    days_dict_next = {}
    fill_year_dict(next_year, days_dict_next)
elif os.path.exists('days_dict_%s.pickle' % str(next_year)) == True:  # Uncpickle calendar/dict from previous session
    pickle_in = open('days_dict_%s.pickle' % str(next_year), "rb")
    days_dict_next = pickle.load(pickle_in)

# --------------------------- ********************** READ ME ************************** --------------------------------

# --------------------------------------** HOW TO REGISTER AN ADMIN **--------------------------------------------------
# Admins have access to a lot of sensitive patient data and therefore do not register the normal way. They can only be
# registered by the Practice Manager. To add an administrator account, the Practice Manager needs to un-comment the
# following block of code and re-execute the programme, i,e., click run. (This would be on a back-end user screen in real life).
# # # ------------------------------------------- code block start ---------------------------------------------------------

# print("Registering an admin", '\n')
# user_current_object = admin_class(user_df) # "0", user_df, days_dict_current, days_dict_next, current_year, next_year
# new_user = pd.DataFrame({"User Type": ["Admin"], "First Name": [user_current_object.first_name], "Last Name": [user_current_object.last_name], "Email": [user_current_object.email], "User Id": [user_current_object.user_id], "Date Of Birth":[user_current_object.DOB], "Password": [user_current_object.password], "Prescriptions":["N/A"], "Test Results":["N/A"], "Booked Appts":["N/A"], "Validation":["N/A"]})
# user_df = user_df.append(new_user, ignore_index=True) # Adding the new row to the user_df.
# save_data(user_dataframe=user_df)
# sys.exit()

#--------------------------------------------- code block end ---------------------------------------------------------


# ------------------ SCREEN 1 - LOGIN / REGISTER---------------------

# LOGIN FUNCTION

def login(user_df, days_dict_current, days_dict_next, current_year, next_year): # User logs in. If successful, they are taken to their account page
    global login_email
    login_email = input("Please enter your email address: ").lower()
    while login_email not in user_df["Email"].values:
        print("This email address is not recognised")
        login_email = input("Please enter your email address: ").lower()
    if login_email in user_df["Email"].values:
        global user_current_rec
        user_current_rec = get_user_record(user_df, login_email) # Pulling user record, based on email, so password can be checked
        if user_current_rec["Validation"] != "PENDING":
            password = input("Please enter your password: ") # NOTE: This works fine but I can't get rid of this warning!: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
            if password == user_current_rec["Password"]:
                print("Login successful!" '\n')
            else:
                print("Incorrect email and password combination, please try again")
                login(user_df, days_dict_current, days_dict_next, current_year, next_year)
        elif user_current_rec["Validation"] == "PENDING": # GPs trying to login before their application has been approved get this message
            print("Your application had not yet been approved. Please try again later. If it has been more than 24 hours since you registered, please call the Practice Manager on 020 1234 567")
            exit()
    print(user_current_rec)


# SCREEN 1 - OPENING PAGE
global login_or_reg
login_or_reg = input("\n" "Welcome to Doctored e-Health!" "\n" "\n" "Enter 1 to login and 2 to register: ")
while login_or_reg != "1" and login_or_reg != "2" and login_or_reg != "0":
    login_or_reg = input("Enter 1 to login and 2 to register: ")

# This variable will shortly be loaded with  either GP, PATIENT or ADMIN
global user_type

# LOGIN
if login_or_reg == "1": # LOGIN
    login(user_df, days_dict_current, days_dict_next, current_year, next_year)
    user_type = user_current_rec["User Type"]

# REGISTER
elif login_or_reg == "2":
    user_type_input = input("Enter 1 if you are a Patient and 2 if you are a GP: ")
    while user_type_input != "1" and user_type_input != "2":
        print("That is not a valid entry")
        user_type_input = input("Enter 1 if you are a GP and 2 if you are a patient: ")
    if user_type_input == "2": # GP REGISTRATION
        user_current_object = gp_class(user_df)  # Executes registration for GPs
        # Putting registration info into a dataframe row
        new_user = pd.DataFrame({"User Type": [user_current_object.user_type], "First Name": [user_current_object.first_name], "Last Name": [user_current_object.last_name], "Email": [user_current_object.email], "User Id": [user_current_object.user_id], "Date Of Birth":[user_current_object.DOB], "Password": [user_current_object.password], "Prescriptions":["N/A"], "Test Results":["N/A"], "Booked Appts":["N/A"], "Validation":["PENDING"]})
        user_df = user_df.append(new_user, ignore_index=True) # Adding the new row to the main user_df
        save_data(user_dataframe=user_df) # Pickling and unpickling the updated user_df to save it
        exit()
    elif user_type_input == "1": # PATIENT REGISTRATION
        # Create new object of patient class called user_current_object
        user_type = "PATIENT"
        user_current_object = patient_class(user_df) # Executes registration for PATIENTS
        print("user_current_object.email =", user_current_object.email, type(user_current_object.email))
        if user_current_object.email in user_df["Email"]:
            print("This email is already registered, you are being redirected to login.")
            exit()
        # Putting registration info into a dataframe row
        new_user = pd.DataFrame({"User Type": [user_current_object.user_type], "First Name": [user_current_object.first_name], "Last Name": [user_current_object.last_name], "Email": [user_current_object.email], "User Id": [user_current_object.user_id], "Date Of Birth":[user_current_object.DOB], "Password": [user_current_object.password], "Prescriptions":[[]], "Test Results":[[]], "Booked Appts":[[]], "Validation":["N/A"]})
        # Adding the new row to the user_df
        user_df = user_df.append(new_user, ignore_index=True)
        save_data(user_dataframe=user_df)
        user_current_rec = get_user_record(user_df, user_current_object.email)

# If login or patient reg successful we move onto this:
print('\n'"Thank you. You are entering as a " + user_type)

# (3) WHAT WOULD THE USER LIKE TO DO NEXT
if user_type == "GP":
    gp_account(user_df, user_current_rec, days_dict_current, days_dict_next, current_month, next_month)
elif user_type == "PATIENT":
    patient_account(user_df, user_current_rec, days_dict_current, days_dict_next, current_month, next_month)
elif user_type == "Admin":
    admin_account(user_df)