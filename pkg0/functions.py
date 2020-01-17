#  -------------------------CONTENTS of FUNCTIONS -----------------------------

# ------- SAVE / EXIT --------
# - save_data()                 > Pickles and unpickles the dictionary. This is run every time a dataframe is updated as a means of saving data
# - exit()                      > Returns programme to start (login/reg) page

# ------ CALENDAR FUNCTIONS --------
#  - day_view()                 > creates the GP availability and patient bookings of a single day
#  - fill_user_dict()           > adds a day_view to every day in a dict
#  - view_date()                > takes user to a specific date in calendar dictionary. Returns the day_view of that day.
#  - book_appts()               > for patients to book an appointment.


# --------- ACCOUNT PAGE FUNCTIONS ----------
#  - get_user_record()          > pulls up the user record (the data row from the df)
#  - indices_row_col()          > returns the row and column indices of a value in a dataframe
#  - overwrite_selection()      > overwrites a value in a dataframe with a new value
#  - edit_user_detail()         > allows the editing of values in user records (uses overwrite_selection())
#  - search_return_rows()       > Search a dataframe for a specific value and return records which contain that value. Set return_indices argument to 1 (or anything except 0) to also return the indices
#  - next()                     > Gives the user options on what to do next. Used at end of most account function processes.

#  - gp_account()               > pulls up account page
#  - patient_account()          > pulls up account page
#  - admin_account()            > pulls up account page

#  - add_availability_gp()      > allows gp to add availability
#  - next()                     > user is shown options for what they would like to do next

# -------------- USER CLASSES & REGISTRATION -----------------
#  - class user                 > base class from which the rest inherit
#  - class patient              > incl REGISTRATION
#  - class gp                   > incl REGISTRATION
#  - class admin                > Includes methods: confirm_application()


# Validation --- NEEDS FIXED (NOT CURRENTLY USED) -- USES *args
# def validation(user_df, entered_value, function_to_repeat, *accepted): # Trying out the *args functionality
#     print(accepted)
#     for i in accepted:
#         print("accepted i = ", i)
#     while entered_value not in accepted:
#         print(entered_value, "is not a valid entry. Please enter one of the following:" + str(accepted))
#         admin_class.confirm_application(user_df)
#     if entered_value in accepted:
#         print("Thank you.")


# ---------SAVE DATA + EXIT (LOGOUT / RESTART) -----------

# Save new data added (pickle and unpickle) - returns updated
def save_data(user_dataframe=0, days_dict_curr=0, days_dict_nx=0): # Replace the args of the dataframes which need updated with the dataframe variables. If stays at "0", it will be ignored.
    import pickle
    import datetime
    import pandas as pd
    today_date = datetime.date.today()
    curr_year = today_date.year
    nx_year = today_date.year + 1

    if isinstance(user_dataframe, pd.DataFrame): # If user_dataframe is a pandas dataframe (as opposed to the default 0):
        # User_df to pickle
        user_dataframe.to_pickle("user_df.pickle")

        # Unpickle user_df
        pickle_in = open("user_df.pickle", "rb")
        global user_df # Global so the updated user_df (post save_data()) can be returned to main
        user_df = pickle.load(pickle_in)
        return user_df

    if isinstance(days_dict_curr, dict):
        # CURRENT year calendar into pickle file
        pickle_out_cal_cur = open('days_dict_%s.pickle' % str(curr_year),
                                  "wb")  # Creating / opening new pickle file
        pickle.dump(days_dict_curr, pickle_out_cal_cur)  # Putting dictionary into new pickle file
        pickle_out_cal_cur.close()  # Closing pickle file

        # Unpickle days_dict_current
        pickle_in = open('days_dict_%s.pickle' % str(curr_year), "rb")
        global days_dict_current
        days_dict_current = pickle.load(pickle_in)
        return days_dict_current

    if isinstance(days_dict_nx, dict):
        # NEXT year calendar into pickle file
        pickle_out_cal_next = open('days_dict_%s.pickle' % str(nx_year),"wb")   # Creating / opening new pickle file
        pickle.dump(days_dict_nx, pickle_out_cal_next)  # Putting dictionary into new pickle file
        pickle_out_cal_next.close()  # Closing pickle file

        # Unpickle days_dict_next
        pickle_in = open('days_dict_%s.pickle' % str(nx_year), "rb")
        global days_dict_next
        days_dict_next = pickle.load(pickle_in)
        return days_dict_next


# Exit: go back to opening page
def exit():
    import sys
    import os
    os.execl(sys.executable, *([sys.executable] + sys.argv)) # Source: https://www.reddit.com/r/learnpython/comments/88i35j/besteasiest_way_to_restart_a_python_script_from/


# ------ CALENDAR FUNCTIONS ---------

# Allows GPs to view calendar year, month or single date
# Book appt is also built into this
def view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month):
    import calendar
    import datetime
    year_q = int(input("For which year? Enter 1 for this year or 2 for next year: " '\n')) # Appointments can only be made for the current month and next month. Domain research showed that GP appointments in the UK can rarely be booked further in advance than this)
    today_date = datetime.date.today()
    current_month = today_date.strftime('%-m')
    month = 0
    while year_q != 1 and year_q != 2:
        print("Please enter 1 for this year or 2 for next year")
        view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year,
                  current_month, next_month)
    if year_q == 1:
        year = current_year
        days_dict = days_dict_current
        for i in days_dict:
            i = days_dict[i]
            print(i)
    elif year_q == 2 and current_month == 12: # If we are in the month of December, allow next year calendar to be viewed (otherwise, don't allow)
        year = next_year
        days_dict = days_dict_next
        for i in days_dict:
            i = days_dict[i]
            print(i)
    elif year_q == 2 and current_month != 12:
        print("The calendar for next year is not available yet. This will only be shown in December of the current year." '\n')
        view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
    # validation(year_q, function_to_repeat, 1, 2)  # Function which rejects if valid value not entered
    month_q = int(input("Enter 1 to view this month, 2 to view next month or 0 to see main menu: " '\n'))  # (Note, appointments can only be made for the current month and next month)") # Domain research showed that GP appointments in the UK can rarely be booked further in advance than this
    if month_q == 1:
        for i in days_dict:
            i = days_dict[i]
            if i.iloc[14,0].month == int(current_month):
                print(i)
    elif month_q == 2:
        for i in days_dict:
            i = days_dict[i]
            if i.iloc[14,0].month == int(next_month):
                print(i)
    elif month_q == 0:
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    else:
        view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
    date_q = int(input("Enter the date you would like to view or enter 0 to exit" '\n'))
    while date_q not in range(0,32):
        print("That's an invalid entry, please try again.")
        date_q = int(input("Enter the date you would like to view or enter 0 to exit:" '\n'))
    if date_q == 0:
        exit()
    date_to_view = datetime.date(year, month_q, date_q)
    date_to_view_str = (str(year) + "-" + str(month_q) + "-" + str(date_q)) # Creating date as string in so it can be used to search days_dict (without padded zeros)
    date_to_book_day_view = days_dict[date_to_view_str]
    print(date_to_book_day_view)
    if date_q != 0 and user_type == "PATIENT":
        book_appt(user_df, date_to_book_day_view, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
    elif date_q != 0 and user_type == "GP":
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    elif date_q == 0:
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)

def book_appt(user_df, date_to_book_day_view, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month):
    # Change date_selected in date_to_book_day_view to "BOOKED"
    user_type = user_current_rec_def["User Type"]
    doc_name = input("To book an appointment, please enter the NAME of the GP you would like to see, as it appears on the screen. Ex: Dr Smith:" '\n')
    while doc_name not in date_to_book_day_view.head():
        print("The GP name you entered isn't valid for this day")
        doc_name = input(
            "To book an appointment, please enter the NAME of the GP you would like to see, as it appears on the screen. Ex: Dr Smith:" '\n')
    time = input("Please enter the appointment TIME as it appears on the screen. Ex: 9.30 or enter 0 to exit:" '\n')
    while time not in date_to_book_day_view.values:
        print("The time you entered is not valid. Please enter the time as you see it on the screen, for example 14.00: ")
        time = input("Please enter the appointment TIME as it appears on the screen. Ex: 9.30 or enter 0 to exit:" '\n')
    if time == 0:
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    elif time in date_to_book_day_view.values and doc_name in date_to_book_day_view.head():
        row, column = indices_row_col(date_to_book_day_view, doc_name, time)
        if date_to_book_day_view.iloc[row, column] != "BOOKED" and date_to_book_day_view.iloc[row, column] != "PENDING":
            overwrite_cell(date_to_book_day_view, time, doc_name, "PENDING", print_df=1, append=0)
            save_data(days_dict_nx=days_dict_next, days_dict_curr=days_dict_current)
        elif type(date_to_book_day_view.iloc[row, column]) != int:
            print("That appointment is not currently available, Please enter a different one: ")
    else:
        print('\n',"Sorry that is not an available appointment number. Please try again.")
        view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year,
                  next_year, current_month, next_month)
    print(date_to_book_day_view) # Printing the day view with "PENDING" added.

    # Adding date and time of the booking to the "Booked Appts" section on the user account profile page.
    date = date_to_book_day_view.iloc[14, 0] # Loading date into "date" variable
    date_time_string = (str(date) + " at " + str(time))
    # date_time string needs appended as a list here
    edit_user_detail(user_current_rec_def, user_current_rec_def, user_current_rec_def["Email"], "Booked Appts", date_time_string, append=1)
    save_data(user_dataframe=user_df)
    print('\n' "Thanks, the following appointment has been provisionally booked:", date_time_string, "\n" "Please check your profile in 24 hours to see if it's confirmed.")
    next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)

# Creates a "day_view" - i.e., a pandas dataframe showing appt times, to which GP availability is later added
def day_view(year, month, date):
    import datetime
    import pandas as pd
    global date_str
    date_str = (str(year) + "-" + str(month) + "-" + str(date))
    global date_fmt
    date_fmt = datetime.date(int(year), int(month), int(date))
    global df
    df = pd.DataFrame(
        {"Time": ["9.00", "9.30", "10.00", "10.30", "11.00", "11.30", "12.00", "12.30", "14.00", "14.30", "15.00", "15.30", "16.00", "16.30", date_fmt, date_fmt.strftime('%A')]})
    return df


# Create dictionary calendar for the year (with a day view for each date)
def fill_year_dict(year, dict_name):
    import datetime
    import calendar
    jan_1st = datetime.date(year,1,1)
    for date in (jan_1st + datetime.timedelta(n) for n in range(365)): # *** < Needs edited for leap year. # Adapted from the following: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
        day_view_date = day_view(date.year, date.month, date.day)
        dict_name[date_str] = day_view_date


# ----------- ACCOUNT PAGE FUNCTIONS ------------

#  View user record
def get_user_record(user_df, user_email): # Function to select user record from the user directory and return it in an easy-to-read format
    import numpy as np # Using numpy to get row number
    if user_email not in user_df.values:
        print("Can't pull user record as the email entered isn't in the database.")
        # Return to something here
    elif user_email in user_df.values:
        row, column = indices_row_col(user_df, "Email", user_email)
        row = int(row)
        # indices = np.where(user_df == user_email)  # Gets the row and column of the user email
        # row = int(indices[0]) # *** BREAKS here if is nothing is in indices
        user_current_rec = user_df.iloc[row] # Grabs the row number number "row" represents
        return user_current_rec

# Gets the indices of a call based on column_name and row identifier
def indices_row_col(dataframe, column_name, row_identifier):
    # row_identifier: a unique value in the row to be selected. In user_df this will be user_email. In days_dict it will be _________
    import numpy as np
    import pandas as pd
    if column_name not in dataframe:
        print("The column name is not in the dataframe")
    elif row_identifier not in dataframe.values:
        print("The row identifier is not in the dataframe")
    else:
        indices_user = np.where(dataframe == row_identifier)
        row_num = int(indices_user[0]) # BREAKS here if nothing in indices
        if isinstance(dataframe, pd.Series): # We now need to get the column index of the column name - the function to do thisi s different on pd.DataFrame (ie for user_df) and for pd.Series (ie user_current_rec)
            value = dataframe[column_name]
            column_num = list(dataframe).index(value)
        else: # This block works if dataframe is a df (not a series)
            column_num = dataframe.columns.get_loc(column_name)
            column_num = int(column_num)
        return row_num, column_num


# Overwrite a cell in a dataframe
def overwrite_cell(dataframe, row_value, column_name, new_val, print_df=0, append=0): # Used for changing elements in the user_df + the days_dict calendar
    # If append=1 (rather than default 0), this function appends the new value to the existing value in the cell rather than overwrites.
    # row_value arg: should be a unique value in the row you would like to select. Ex user_df this unique value could be email. In days_dict it could be the time.
    import numpy as np
    row, column = indices_row_col(dataframe, column_name, row_value)  # NOT WORKING
    if column_name == "Booked Appts" or column_name == "Prescriptions" or column_name == "Test Results":
        dataframe[column_name].append(new_val)
    elif column_name != "Booked Appts" or column_name == "Prescriptions" or column_name == "Test Results":
        if append == 0:
            dataframe.iloc[row, column] = new_val
        elif append == 1:
            new_val_append = (str(dataframe.iloc[row, column]) + ", " + str(new_val))
            dataframe.iloc[row, column] = new_val_append
        if print_df == "1":
            return dataframe

# Edit a user record for users (i.e., can change Email, Password etc) and for GPs (can add Prescriptions etc).
# Returns updated user record
def edit_user_detail(user_df, user_current_rec_def, user_email, column_name, new_val, append=0): # append=1 if want to apend rather than replace data in cell > goes through to overwrite_cell() function
    # Put in validations for date of birth so it is replaced as a datetime object (rather than string) which can later be read as such
    if column_name == "Date Of Birth":
        import datetime
        today_date = datetime.date.today()
        curr_year = today_date.year
        year = int(input("Year of birth. Year (ex: 1986): "))
        month = int(input("Month of birth. Ex: 7 for July (no leading 0s): "))
        date = int(input("Date of birth. Ex: 8 for 8th (no leading 0s): "))
        while year not in range(1900, curr_year) and month not in range (1,12) and date not in range(0,31):
            print("This date of birth is not valid, please check and re-enter. Enter the 4-digit year, month (ex: 9 for Sept, not 09) date (ex: 4 for 4th, not 04)")
            year = int(input("Year of birth. Year (ex: 1986) "))
            month = int(input("Month of birth. Ex: 7 for July; no 0s"))
            date = int(input("Date of birth. Ex: 8 for 8th Jan; no 0s"))
        new_val = datetime.date(year, month, date)
    if new_val == "#": # User is told to enter "#" if they simply want to delete the contents of the cell
        overwrite_cell(user_df, user_email, column_name, new_val = "", print_df=0, append=0)
    elif new_val !="#" and append == 1:
        overwrite_cell(user_df, user_email, column_name, new_val, print_df=0, append=1)
    elif new_val !="#" and append == 0:
        overwrite_cell(user_df, user_email, column_name, new_val, print_df=0, append=0)
    save_data(user_dataframe=user_df)

    if column_name != "Email":
        user_current_rec = get_user_record(user_df, user_current_rec_def["Email"])
        return user_current_rec
    elif column_name == "Email": # A different rule needs added if Email is being changed as get_user_rec() uses Email to find the record
        user_current_rec = get_user_record(user_df, new_val)
        return user_current_rec

# Search a dataframe for a specific value and return records which contain that value.
def search_return_rows(user_df, item_to_search): # Only works if there are no lists in df
    return user_df[user_df.isin({item_to_search}).any(1)] # Source: https://stackoverflow.com/questions/38185688/select-rows-containing-certain-values-from-pandas-dataframe

def next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month):
    next = input("What would you like to do next? Enter 1 to go to your account page or 0 to exit: " '\n')
    if next == "1" and user_current_rec_def["User Type"] == "PATIENT":
        patient_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month)
    elif next == "1" and user_current_rec_def["User Type"] == "GP":
        gp_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month)
    elif next == "0":
        exit()

# Get GP account page
def gp_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month):
    import datetime
    today_date = datetime.date.today()
    current_year = today_date.year
    next_year = today_date.year + 1
    user_type = "GP"
    print('\n' "*******************************************************************")
    print('\n' "Welcome to your GP account page" '\n')
    today_date = datetime.date.today()
    print("Date today:", today_date)
    operations_list = (
          "On this page you can:" '\n''\n'
          "1. Add your work availability"  '\n' 
          "2. View and approve requested appointments" '\n' 
          "3. View calendar (including booked appointments)" '\n' 
          "4. Add prescriptions or test results to a patient account" '\n'
          "5. View/change your personal details" '\n'
          "0. Logout" '\n') # DONE
    print(operations_list)
    operation = input("Please choose what you would like to do by entering the number of the operation. "
                      "(Example: To view and change work availability, enter 1): " '\n')
    if operation == "1": # ADD WORK AVAILABILITY
        add_availability_gp(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
        save_data(user_df, days_dict_current, days_dict_next)
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    if operation == "2": # CONFIRM APPTS
        doc_name = "Dr %s" % user_current_rec_def["Last Name"]
        for i in days_dict_current:
            i = days_dict_current[i]
            if doc_name in i.head():
                if "PENDING" in i[doc_name].values:
                    print(i)
                    time = input("Enter the time of the appt you would like to confirm")
                    while time not in i.values:
                        print("That is not a valid time, please try again.")
                        time = input("Enter the time of the appointment you would like to confirm")
                    if time in i.values and doc_name in i.head():
                        row, column = indices_row_col(i, doc_name, time)
                        while i.iloc[row, column] != "PENDING":
                            print("That appointment is not pending, Please enter a different one: ")
                            time = input("Enter the time of the appt you would like to confirm")
                        if i.iloc[row, column] == "PENDING":
                            overwrite_cell(i, time, doc_name, "BOOKED", print_df=0, append=0)
                            save_data(days_dict_nx=days_dict_next, days_dict_curr=days_dict_current)
                            print("Thanks - that appointment has now been changed to \"BOOKED\" and will show on a such on the patient profile. To confirm more appointments, just start this process again on the next screen.") # Using the escape operation taught in class
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year,next_year)
    if operation == "3":  # VIEW CALENDAR
        view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    if operation == "4":  # ADD PRESCRIPTIONS or TEST RESULTS
        which = int(input("Would you like to add a prescription or a test result?" '\n' "Prescription: Enter 1" '\n' "Test result: Enter 2:"))
        while which != 1 and which != 2:
            which = int(input(
                "Would you like to add a prescription or a test result?" '\n' "Prescription: Enter 1" '\n' "Test result: Enter 2:"))
        if which == 1:
            column = "Prescriptions"
        elif which == 2:
            column = "Test Results"
        patient_email = input("Please enter the email of the patient who's %s you would like to add:" '\n' %column)
        while patient_email not in user_df["Email"].values:
            print("That user is not recognised")
            patient_email = input("Please enter the email of the patient who's %s you would like to add:" '\n' %column)
        if patient_email in user_df["Email"].values:
            user_patient_rec = get_user_record(user_df, patient_email)
            print(user_patient_rec)
            entry = input("Please enter the %s to be added to the account of %s: " %(column, patient_email))
            edit_user_detail(user_patient_rec, user_current_rec_def, patient_email, column, entry, append=1)
            save_data(user_dataframe=user_df)
            user_patient_rec = get_user_record(user_df, patient_email)
            print(user_patient_rec)
            next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    if operation == "5": # VIEW / CHANGE PERSONAL DETAILS
        # *** PUT IN FUNCTION? This whole block is repeated in patient_account()
        print(user_current_rec_def)
        field = input("To change something on your profile, enter the name of the item, i.e., Email. Or enter 0 to go back to main menu: ").title()  # Converting input into title case to avoid case errors
        if field not in user_current_rec_def:
            print("%s is not the name of an item on your profile. Please try again and enter the exact name of the item you would like to change i.e., First Name or Password.")
            gp_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month)
        elif field in user_current_rec_def:
            new_val = input("Please enter the new value to add. (To simply delete the current value, enter #): ")
            edit_user_detail(user_df, user_current_rec_def, user_current_rec_def["Email"], field, new_val)
            save_data(user_dataframe=user_df)
            if field == "Email":
                user_current_rec = get_user_record(user_df, new_val) # Creating UPDATED user record variable based on updated dataframe.
            else:
                user_current_rec = get_user_record(user_df, user_current_rec_def["Email"])
            gp_account(user_df, user_current_rec, days_dict_current, days_dict_next, current_month, next_month)
        elif field == "0":
            gp_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month)
    if operation == "0":
        exit()

# Get patient account page
def patient_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month):
    user_type = "PATIENT"
    # Establishing some time variables for use specifically in this function
    import datetime
    today_date = datetime.date.today()
    current_year = today_date.year
    next_year = today_date.year + 1
    age = datetime.date.today() - user_current_rec_def["Date Of Birth"] # Getting patient age for flu jab notification
    age = int(age.days) / 365
    print('\n' "*******************************************************************")
    print('\n'"Welcome to your patient account page" '\n'
          "Date today:", today_date, '\n')
    if age > 65:
        print("NOTICE! Did you know that as you are over 65 years of age, you can get a FREE flu vaccination? Why not book an appointment now! Just enter 2 below." '\n')
    print("On this page you can:" '\n''\n'
          "1. View or cancel upcoming appointments"  '\n'  # Shows only the list of appts
          "2. Book a new appointment" '\n'
          "3. View your profile (including test results and prescriptions) and edit your details" '\n'
          "0. Logout" '\n')
    operation = input("Please choose what you would like to do by entering the number of the option. "
                      "(For example: To book an appointment, enter 2): " '\n')
    if operation == "1": # VIEW / CANCEL UPCOMING APPTS
        user_curr_rec = get_user_record(user_df, user_current_rec_def["Email"])
        booked_appts = user_curr_rec["Booked Appts"]
        if len(booked_appts) == 0:
            print("You have no booked appointments - you can book one from your account page.")
            next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
        else:
            print(booked_appts)
            next_move = int(input("Would you like to cancel an appointment? Enter 1 for yes and 2 for no: "))
        if next_move == 2:
            next(user_df, user_curr_rec, days_dict_current, days_dict_next, current_year, next_year)
        elif next_move == 1:
            for i in user_current_rec_def["Booked Appts"]:
                year = int(i[0:4])
                month = int(i[5:7])
                date = int(i[8:10])
                for i in days_dict_current:
                    i = days_dict_current[i]
                    if datetime.date(year, month, date) in i.values:
                        print(i)
                        doc_name = input("Please enter the Doctor name of the appointment you would like to cancel:")
                        while doc_name not in i.head():
                            print("That is not a valid doctor Name, please try again.")
                            doc_name = input(
                                "Please enter the Doctor name of the appointment you would like to cancel:")
                        time = input("Please enter the time of the appointment you would like to cancel:")
                        while time not in i.values:
                            print("That is not a valid time, please try again.")
                            time = input("Enter the time of the appointment you would like to confirm: ")
                        # Creating date-time string in same format as the appt appears in the user profile under "Booked Appts"
                        if len(str(month)) == 1: # If the month is 1-9, add leading 0 so it matches the string in the user record
                            date = (str(year) + "-" + "0" + str(month) + "-" + str(date))
                        else:
                            date = (str(year) + "-" + str(month) + "-" + str(date))
                        if (date + " at " + time) not in user_current_rec_def["Booked Appts"]:
                            print("The details entered don't correspond to one of your appointments. Please re-start and try again.")
                            patient_account(user_df, user_current_rec_def, days_dict_current, days_dict_next,
                                            current_month,
                                            next_month)
                        elif (date + " at " + time) in user_current_rec_def["Booked Appts"]:
                            overwrite_cell(i, time, doc_name, "AVAILABLE", print_df=0, append=0)
                            user_current_rec_def["Booked Appts"].remove(date + " at " + time) # ** NOTE! *** In the video this operation (next 3 lines) wasn't working - I fixed it after making the video. It removes the cancelled appt from the user record
                        print("Thanks - that appointment has now been cancelled and made \"AVAILABLE\" to other patients.")  # Using the escape operation taught in class
                        save_data(user_dataframe=user_df, days_dict_curr=days_dict_current)
                        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    if operation == "2": # BOOK APPT
        view_date(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
    if operation == "3": # VIEW / CHANGE PERSONAL DETAILS
        print(user_current_rec_def)
        field = input("\n" "To change something on your profile, enter the NAME OF THE FIELD, i.e., Email or Password. Or enter 0 to go back to main menu." "\n" "(Note: You can only change your Names, Email or Password. To change DOB please bring an updated birth certificate into the practice.): ").title() # Converting input into title case to avoid case errors
        if field == "0":
            patient_account(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month,
                            next_month)
        while field not in user_current_rec_def or field == "Prescriptions" or field == "Test Results" or field == "Booked Appts" or field == "Validation":
            print("\n" "%s is not the name of an editable field on your profile. Please try again and enter the exact name of the FIELD you would like to change i.e., First Name or Password." %field)
            field = input("\n" "To change something on your profile, enter the NAME OF THE FIELD, i.e., Email or Password. Or enter 0 to go back to main menu: ").title() # Converting input into title case to avoid case-related input errors
        if field in user_current_rec_def:
            new_val = input("Please enter the new value to add. (To delete the current value, enter #): ")
            edit_user_detail(user_df, user_current_rec_def, user_current_rec_def["Email"], field, new_val)
            save_data(user_dataframe=user_df)
            if field == "Email": # Creating UPDATED user record variable based on updated dataframe.
                user_current_rec = get_user_record(user_df, new_val)
                print(user_current_rec)
            else:
                user_current_rec = get_user_record(user_df, user_current_rec_def["Email"])
                print(user_current_rec)
            patient_account(user_df, user_current_rec, days_dict_current, days_dict_next, current_month, next_month)
    if operation == "0": # Logout / exit
        exit()

def admin_account(user_df):
    import datetime
    today_date = datetime.date.today()
    print('\n' "*******************************************************************")
    print('\n'"Welcome to the admin account page" '\n'
          "Date today:", today_date, '\n''\n'
          "On this page you can:" '\n''\n'
          "1. Confirm GP applications"  '\n''\n' 
          "2. View GPs directory (plus deactivate, delete or add GP / patient accounts)" '\n''\n'
          "3. Edit GP or patient accounts" '\n''\n' 
          "0. Logout" '\n')

    operation = input("Please choose what you would like to do by entering the number of the option. "
                      "(For example: To view GPs directory, enter 2. Enter 0 to go back to your main account page): " '\n')
    if operation == "1": # CONFIRM GP APPLICATIONS
        admin_class.confirm_application(user_df)
        admin_account(user_df) # (Saved within function)
    if operation == "2": # VIEW GP DIRECTORY / DELETE GP ACCOUNTS
        for i in user_df.values:
            if "GP" in i:
                print(i)
        # print(search_return_rows(user_df, "GP"))
        to_do = input('\n' "What would you like to do next? Enter:" '\n''\n'  "1. To delete a GP account" '\n' "2. To temporarily deactivate a GP account" '\n' "3. To add a GP account" '\n' "0 to go back to main menu" '\n')
        if to_do == "0":
            admin_account(user_df)
        if to_do == "1": # DELETE GP ACCOUNT
            email = input("Please enter the GP/patient email of the account you would like to delete: ")
            while email not in user_df.values:
                print("That email does not exist, please try again.")
                email = input("Please enter the GP/patient email of the account you would like to delete: ")
            gp_rec_delete = get_user_record(user_df, email)
            sure = input("Are you sure you want to delete this account? This cannot be undone. Press 1 for yes or any other number to exit.")
            if sure == "1":
                row,column = indices_row_col(user_df, "Email", gp_rec_delete["Email"])
                user_df = user_df.drop(row)
                num = 1
                for i in user_df.values:
                    if "GP" in i:
                        print("GP:", num)
                        print(i)
                        num = num + 1
                print("Thanks, the record for %s has now been deleted. The updated GP directory is printed above." %email)
                save_data(user_dataframe=user_df)
                admin_account(user_df)
        elif to_do == "2": # DEACTIVATE GP ACCOUNT
            email = input("Please enter the GP/patient email of the account you would like to deactivate: ")
            while email not in user_df.values:
                print("Invalid entry, try again.")
                email = input("Please enter the GP/patient email of the account you would like to deactivate: ")
            if email in user_df.values:
                gp_rec_deact = get_user_record(user_df, email)
                print(gp_rec_deact)
                sure = input("Are you sure you want to temporarily deactivate this account? Press 1 for yes or any other number to exit:")
                if sure == "1":
                    edit_user_detail(user_df, gp_rec_deact, gp_rec_deact["Email"], "Validation", "PENDING")
                    print("Thanks, the record for %s has now been deactivated. To recativate a GP, please confirm as normal in the 'Confirm GP Applications' section" % email)
                    save_data(user_dataframe=user_df)
                    print(get_user_record(user_df, email))
                    admin_account(user_df)
                elif sure != "1":
                    admin_account()
            # elif email not in user_df.values:
            #     print("%s is not the name of an field on your profile. You are being redirected to the main page - please try again and enter the exact name of the FIELD you would like to change i.e., First Name or Password.")
            #     admin_account(user_df)
        elif to_do == "3": # ADD GP ACCOUNT *** BUG HERE
            import pandas as pd
            print("To create a new GP account, please enter their details below. You will then need to approve them as normal before their account is activated: ")
            user_current_object = gp_class(user_df) # EXITS HERE
            print(user_current_object)
            new_user = pd.DataFrame(
                {"User Type": ["GP"], "First Name": [user_current_object.first_name],
                 "Last Name": [user_current_object.last_name], "Email": [user_current_object.email],
                 "User Id": [user_current_object.user_id], "Date Of Birth": [user_current_object.DOB],
                 "Password": [user_current_object.password], "Prescriptions": ["N/A"], "Test Results": ["N/A"],
                 "Booked Appts": ["N/A"], "Validation": ["CONFIRMED"]})
            # Adding the new row to the user_df
            user_df = user_df.append(new_user, ignore_index=True)
            save_data(user_dataframe=user_df)
            admin_account(user_df)
    if operation == "3": # EDIT PATIENT/ GP RECORDS
        email = input("Please enter the GP or patient email of the account you would like to edit: ")
        while email  not in user_df.values():
            print("That's not a valid email, please try again.")
            email = input("Please enter the GP or patient email of the account you would like to edit: ")
        rec_edit = get_user_record(user_df, email)
        print(rec_edit)
        field = input('\n' "Which field would you to edit? Enter the name of the field: ").title()
        if field not in rec_edit:
            print("%s is not the name of an item on user profile. You are being redirected to the main page - please try again and enter the exact name of the item you would like to change i.e., First Name or Password." %field)
            admin_account(user_df)
        elif field in rec_edit:
            new_val = input("Enter the new value for this field (it will replace the previous value): ")
            edit_user_detail(user_df, rec_edit, rec_edit["Email"], field, new_val)
            save_data(user_dataframe=user_df)
            if field == "Email":
                rec_edit = get_user_record(user_df, new_val) # The get_user_record() function uses email address to retrieve user record if "Email" is the field that has been changed, we need to use the new email address to pull record.
            elif field != "Email":
                rec_edit = get_user_record(user_df, email)
            print(rec_edit)
            admin_account(user_df)
    if operation == "0":
        exit()

# Adding GP availability to days_dict calendar for year/ month or a single day
# (There's quit a bit of code duplication within this function - I just ran out of time to make it slicker)
def add_availability_gp(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month):
    import datetime
    doc_name = "Dr %s" % user_current_rec_def["Last Name"]
    today_date = datetime.date.today()
    today_date_str = (str(today_date.year) + "-" + str(today_date.month) + "-" + str(today_date.day))
    column = ["AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", "AVAILABLE", " ", " "]
    print('\n' "Reminder: to REMOVE availability, please contact the Practice Manager directly as we will need to ensure we have cover for that day. Thanks." '\n')
    year_q = int(input("Welcome to the work scheduler. For which YEAR would you like to enter availability? Enter: " '\n' "1 for this year" '\n' "2 for next year: " '\n')) # (Note, appointments can only be made for the current month and next month)") # Domain research showed that GP appointments in the UK can rarely be booked further in advance than this
    global year
    while year_q != 1 and year_q != 2:
        print("Apologies but that's an incorrect entry - please enter 1 or 2")
        year_q = int(input(
            "For which YEAR? Enter 1 for this year or 2 for next year: " '\n'))  # (Note, appointments can only be made for the current month and next month)") # Domain research showed that GP appointments in the UK can rarely be booked further in advance than this
    if year_q == 1:
        year = current_year
        days_dict = days_dict_current
        for i in days_dict:
            i = days_dict[i] # i is now the day_view of each date in the calendar
            print(i)
    elif year_q == 2 and current_month == 12: # Allowing GP to access availability for following year if we're in December of current year
        year = next_year
        days_dict = days_dict_next
        for i in days_dict:
            i = days_dict[i]
            print(i)
    else:
        print("Sorry, whole-year availability can only be edited for the current year unless we are in the last month of the current year. You can start again on account page.")
        add_availability_gp(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
    year_or_month = input("\n" "Would you like to enter availablity for:" "\n" "\n" "The whole year - enter 1" "\n" "A single month or date - enter 2: " '\n')
    while year_or_month != "1" and year_or_month != "2":
        print("Apologies, but that's an incorrect entry")
        year_or_month = input("Would you like to enter availablity for" "\n" "The whole year - Enter 1" "\n" "A single month/date - Enter 2: " '\n')
# WHOLE YEAR CHANGE
    if year_or_month == "1":
        period_str = datetime.date(year, 1, 1).strftime("%Y") # creating date variable so it can be used in next print statement
        period = datetime.date(year, 1, 1).year
        days = input("Which WEEKDAYS can you work in %s?" '\n' "Please enter a number for all the days you can work divided by a space. Enter:" '\n' "0 for Mondays" '\n' "1 for Tuesdays" '\n' "2 for Wednesdays" '\n' "3 for Thursdays" '\n' "4 for Fridays." '\n' % period_str).split()
        for i in days_dict:
            i = days_dict[i] # i becomes the df for each day view
            date_formatted = i.iloc[14, 0]  # Pulling date object from each day
            if doc_name in i.head():
                print("You are already working on", str(i.iloc[14, 0]), "Please start again and select different day/s.")
                add_availability_gp(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year, current_month, next_month)
            if doc_name not in i.head() and str(date_formatted.weekday()) in days and i.shape[1] < 5: # i.shape: Limiting the number of doctors per day to the number of consulting rooms which is assumed to be 4 here
                i[doc_name] = column
            elif i.shape[1] == 5: # Once all consulting rooms are booked, the GP is given the following message:
                print("All our consulting rooms are fully booked with doctors on that day, please choose another.")
            print(i)
        print("Thanks. Your availability has been changed (see above).")
        if year_q == 1:
            save_data(days_dict_curr=days_dict_current)
        elif year_q == 2:
            save_data(days_dict_nx=days_dict_next)
        next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_year, next_year)
# WHOLE MONTH CHANGE
    elif year_or_month == "2":
        month = int(input("For which MONTH in %d would you like to enter your availablity (enter 1-12)?: " '\n' % year))
        while month not in range(1,13):
            print("Apologies, that's an incorrect entry. Please enter a number from 1 to 12")
            month = int(input("For which MONTH in %d would you like to enter your availablity (enter 1-12)?: " '\n' % year))
        date_or_month = int(input("Would like to enter availablity for the whole month (enter 1) or a single date (enter 2)?: " '\n'))
        while date_or_month not in range(1,3):
            print("Apologies, that's an incorrect entry. Please enter the number 1 or 2")
            date_or_month = int(input("Would like to enter availablity for the whole month (enter 1) or a single date (enter 2)?: " '\n'))
        if date_or_month == 1:
            month_str = datetime.date(year, month, 1).strftime("%B")
            days = input("Which WEEKDAYS can you work in %s?" '\n' "Please enter a number for all the days you can work divided by a space. Enter:" '\n' "0 for Mondays" '\n' "1 for Tuesdays" '\n' "2 for Wednesdays" '\n' "3 for Thursdays" '\n' "4 for Fridays." '\n' % month_str).split()
            for i in days_dict:
                i = days_dict[i]  # i becomes the df for each day view
                date_formatted = i.iloc[14, 0]  # Pulling date object from each day
                if doc_name in i.head():
                    print("You are already working on", str(i.iloc[14, 0]),
                          "Please start again and select different day/s.")
                    add_availability_gp(user_type, user_df, user_current_rec_def, days_dict_current, days_dict_next,
                                        current_year, next_year, current_month, next_month)
                if doc_name not in i.head() and str(date_formatted.weekday()) in days and i.iloc[14,0].month == month and i.shape[1] < 5:  # i.shape: Limiting the number of doctors per day to the number of consulting rooms which is assumed to be 4 here
                    i[doc_name] = column
                elif i.shape[1] == 5:  # Once all consulting rooms are booked, the GP is given the following message:
                    print("All our consulting rooms are fully booked with doctors on that day, please choose another.")
                print(i)
            print("Thanks. Your availability has been changed (see above).")
            if year_q == 1:
                save_data(days_dict_curr=days_dict_current)
            elif year_q == 2:
                save_data(days_dict_nx=days_dict_next)
            next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month)
# SINGLE DATE CHANGE
        elif date_or_month == 2:
            month_str = datetime.date(year, month, 1).strftime("%B")
            date = int(input("For which DATE in %s %s would you like to add availability?: " '\n' %(month_str, year)))
            date_formatted = datetime.date(year, month, date)
            date_str = (str(year) + "-" + str(month) + "-" + str(date))
            i = days_dict[date_str]
            if doc_name in i.head():
                print("You are already working on", str(i.iloc[14,0]), "You will now be redirected to start again.")
                add_availability_gp(user_type, user_df, user_current_rec_def, days_dict_current,
                                    days_dict_next,
                                    current_year, next_year, current_month, next_month)
            elif i.shape[1] < 5 and doc_name not in i:
                    i[doc_name] = column
                    print("Thanks, your availability has been updated.")
            elif i.shape[1] == 5:
                print("All our consulting rooms are fully booked with doctors on that day, please choose another.")
            if year_q == 1:
                save_data(days_dict_curr=days_dict_current)
            elif year_q == 2:
                save_data(days_dict_nx=days_dict_next)
            print(i)
            next(user_df, user_current_rec_def, days_dict_current, days_dict_next, current_month, next_month)




# ---------------- USER CLASSES + REGISTRATION ----------------

class user_class:
    def __init__(self):
        import datetime
        today_date = datetime.date.today()
        curr_year = today_date.year
        self.first_name = input("First Name: ")
        self.last_name = input("Last Name: ")
        email = input("Email Address: ").lower() # < Standardizing case so login can be case in-sensitive
        while "@" not in email:
                print("This is not a valid email address. Please re-enter")
                email = input("Email Address: ").lower()
        self.email = email
        self.user_id = round(id(self), 0)
        self.year = int(input("Year of birth. Year (ex: 1986): "))
        self.month = int(input("Month of birth. Ex: 7 for July (no leading 0s): "))
        self.date = int(input("Date of birth. Ex: 8 for 8th (no leading 0s): "))
        while self.year not in range(1900, curr_year) and self.month not in range (1,12) and self.date not in range(0,31):
            print("This date of birth is not valid, please check and re-enter. Enter the 4-digit year, month (ex: 9 for Sept, not 09) date (ex: 4 for 4th, not 04)")
            self.year = int(input("Year of birth. Year (ex: 1986) "))
            self.month = int(input("Month of birth. Ex: 7 for July; no 0s"))
            self.date = int(input("Date of birth. Ex: 8 for 8th Jan; no 0s"))
        self.DOB = datetime.date(self.year, self.month, self.date)
        password1 = input("Password: ")
        password2 = input("Re-enter password: ")
        while password1 != password2:
            print("Passwords do not match, please re-enter")
            password1 = input("Password: ")
            password2 = input("Re-enter password: ")
        if password1 == password2:
            print("Passwords match" '\n')
        self.password = password1 # *** Password protect __var?


class patient_class(user_class): # Inheriting from user class
    def __init__(self, user_df):
        user_class.__init__(self)
        self.user_type = "PATIENT"
        if self.email in user_df["Email"].values:
            print("You are already registered with Doctored e-Health! Next time, please enter 'login' at the start.")
            exit()
        else:
            print("Thanks, you have now registered as a patient with Doctored e-Health."'\n')


class gp_class(user_class): # Inheriting from user class
    def __init__(self, user_df):
        user_class.__init__(self)
        self.user_type = "GP"
        self.validation = "PENDING"
        if self.email not in user_df["Email"].values:
            import datetime
            from datetime import timedelta, datetime
            twenty_4_hours = datetime.now() + timedelta(hours=24)
            twenty_4_time = twenty_4_hours.strftime("%H:%M")
            twenty_4_date = twenty_4_hours.strftime("%D")
            print("Thanks, we have received your application to be a GP with Doctored e-Health. Please take note of your password for future logins. Our admin team will confirm your application shortly. Please try logging in 24 hours from now at %s on %s: " %(twenty_4_time, twenty_4_date), '\n')
        else:
            print("You are already registered with Doctored e-Health! Please start again and enter 'login'.")
            exit()

class admin_class(user_class): # Inheriting from user class
    def __init__(self, user_df):
        user_class.__init__(self)
        if self.email in user_df["Email"]:
            print("This email is already registered, you are being redirected to login.")
            exit()
        self.user_type = "ADMIN"
        print("This administrator has now been registered. Please comment out the code block, and click run to again to login via login screen" '\n')

    @staticmethod  # Static in case developers want to use this function outside admin_class, i.e., if the software develops.
    def confirm_application(user_df):
        import numpy as np
        value_to_search = "PENDING"
        if value_to_search in user_df.values:
            for record in user_df.values:
                if value_to_search in record:
                    user_email = record[2]
                    user_rec = get_user_record(user_df, user_email)
                    print(user_rec)
                    edit = input("Would you like to confirm this GP's application? Please enter Y or N. This will allow the GP to start using Doctored eHealth as a working consultant: ")
                    if edit == "Y":
                        edit_user_detail(user_df, user_rec, user_rec["Email"], "Validation", "CONFIRMED")
                        save_data(user_dataframe=user_df)
                        print(get_user_record(user_df, user_email))
                        return get_user_record(user_df, user_rec["Email"])
                    elif edit == "N":
                        pass
                    elif edit != "Y" and edit != "N":
                        print(edit, "isn't a valid entry. Please enter Y or N")
        elif value_to_search not in user_df.values:
            print("You're all up to date! There are no new GP applications to review")
        print("All applications have now been reviewed.")

    @staticmethod # This function is kept hidden from admin as no one should really be exporting patient health records! Just added as an extra.
    def export_dataframe(user_dataframe):
        user_dataframe.to_csv('User_df.csv')
