import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar
import sqlite3
from PIL import Image, ImageTk

# Function to validate integer input
def validate_integer_input(char):
    return char.isdigit() or char == ""  # Allow digits or empty string



# Function to validate and format the date of birth
def validate_date_of_birth():
    try:
        birthdate = f"{month_var.get()} {day_var.get()}, {year_var.get()}"
        datetime.strptime(birthdate, "%B %d, %Y")  # Check if the date is valid
        return birthdate
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid date of birth.")
        return None

# Function to validate and format the date of application
def validate_date_of_application():
    try:
        application_date = f"{month_var_app.get()} {day_var_app.get()}, {year_var_app.get()}"
        datetime.strptime(application_date, "%B %d, %Y")  # Check if the date is valid
        return application_date
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid date of application.")
        return None

# Validate input data
# Validate input data
def validate_input():
    error_messages = []  # List to collect error messages


    # Validate Mobile Number (must be an integer)
    try:
        mobile_number = int(entry33.get())
    except ValueError:
        print(entry33.get())
        error_messages.append("Mobile number must be a valid number.")

    # # Validate Landline (must be an integer)
    try:
        landline = int(entry34.get())
    except ValueError:
        print(entry34.get())
        error_messages.append(f"Landline must be a valid number.")

    # Validate Email (basic format check)
    # email = entry35.get()
    # emailAddress = entry37.get()
  
    # Validate Date of Birth
    birthdate = validate_date_of_birth()
    if not birthdate:
        error_messages.append("Please enter a valid date of birth.")

    # Validate Date of Application
    application_date = validate_date_of_application()
    if not application_date:
        error_messages.append("Please enter a valid date of application.")

    # If there are any errors, display them in one messagebox
    if error_messages:
        messagebox.showerror("Invalid Input", "\n".join(error_messages))
        return False

    return True  # All validations passed

# Function to display the review window with Close and Save buttons
def show_review_window(review_message, data):
    # Create a new window for reviewing data
    review_window = tk.Toplevel(root)
    review_window.title("Review Data")

    # Add the review message to the window
    review_label = tk.Label(review_window, text=review_message, justify=tk.LEFT)
    review_label.pack(padx=10, pady=10)

    # Define Close button
    def close_review_window():
        review_window.destroy()  # Close the review window

    # Define Save button to save data and close the window
    def save_data():
        save_to_database(data)  # Call your function to save data to the database
        messagebox.showinfo("Success", "Application submitted successfully!")
        clear_form()  # Clear the form after submission
        review_window.destroy()  # Close the review window

    # Add Close button
    close_button = tk.Button(review_window, text="Close", command=close_review_window)
    close_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Add Save button
    save_button = tk.Button(review_window, text="Save", command=save_data)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)



















# Initialize the database
def initialize_database():
    conn = sqlite3.connect("ePassport.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ePassport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            middle_name TEXT,
            gender TEXT,
            date_of_birth TEXT,
            place_of_birth TEXT,
            civil_status TEXT,
            spouse_name TEXT,
            address TEXT,
            father_last_name TEXT,
            father_first_name TEXT,
            father_middle_name TEXT,
            father_citizenship TEXT,
            mother_last_name TEXT,
            mother_first_name TEXT,
            mother_middle_name TEXT,
            mother_citizenship TEXT,
            previous_passport_number TEXT,
            place_of_issue TEXT,
            current_address TEXT,
            occupation TEXT,
            work_address TEXT,
            visa_status TEXT,
            mobile_number TEXT,
            landline TEXT,
            email TEXT,
            contact_person_name TEXT,
            contact_person_number TEXT,
            contact_person_email TEXT,
            date_of_application TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_database(data):
    # Replace empty strings with None to ensure NULL values are stored in the database
    data = [None if item == '' else item for item in data]
    
    # Ensure the data tuple contains exactly 30 items (id included as None since it's auto-generated)
    if len(data) < 30:
        # Convert the tuple to a list to append missing values
        data = list(data)
        # Add None (or any default value) for missing fields
        data += [None] * (30 - len(data))  # Adding None for missing fields
    
    # Using a 'with' statement to ensure connection is properly closed after execution
    with sqlite3.connect("ePassport.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute(''' 
            INSERT INTO ePassport (
                first_name, last_name, middle_name, gender, date_of_birth, place_of_birth,
                civil_status, spouse_name, address, father_last_name, father_first_name,
                father_middle_name, father_citizenship, mother_last_name, mother_first_name,
                mother_middle_name, mother_citizenship, previous_passport_number, place_of_issue,
                current_address, occupation, work_address, visa_status, mobile_number, landline,
                email, contact_person_name, contact_person_number, contact_person_email, date_of_application
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(data))  # Convert list back to tuple before passing to execute
        
        # Committing the transaction
        conn.commit()



# Clear the form
def clear_form():
    for entry in [entry1, entry2, entry3, entry9, entry10, entry11, entry12, entry13,
                  entry18, entry19, entry20, entry21, entry22, entry23, entry24, entry25,
                  entry28, entry29, entry30, entry31, entry32, entry33, entry34, entry35,
                  entry36, entry37, entry38, entry43]:
        if isinstance(entry, tk.Text):
            entry.delete("1.0", tk.END)
        else:
            entry.delete(0, tk.END)
    gender_var.set("")
    month_var.set(months[0])
    day_var.set(days[0])
    year_var.set(current_year)



def submit():
    try:
        # Validate input data
        if not validate_input():
            return  # Stop submission if validation fails

        # Ensure that ComboBoxes have been initialized and properly fetched
        dob_month = month_var.get()  # Get month from ComboBox (StringVar)
        dob_day = day_var.get()      # Get day from ComboBox (IntVar)
        dob_year = year_var.get()    # Get year from ComboBox (IntVar)

        # Fetch Application Date in the same manner
        app_month = month_var_app.get()  # Get month from ComboBox (StringVar)
        app_day = day_var_app.get()      # Get day from ComboBox (IntVar)
        app_year = year_var_app.get()    # Get year from ComboBox (IntVar)

        # Format the dates properly
        dob = f"{dob_month} {dob_day}, {dob_year}"  # Date of Birth formatted  example  January 1, 2025
        application_date = f"{app_month} {app_day}, {app_year}"  # Date of Application formatted example  January 1, 2025

        print(dob)
        print(application_date)

        # Fields dictionary - Ensure correct values are passed for dates
        fields = {
            "first_name": entry3,
            "last_name": entry1,
            "middle_name": entry2,
            "gender": gender_var,
            "date_of_birth": dob,  # Directly assign formatted date of birth
            "place_of_birth": entry9,
            "civil_status": entry11,
            "spouse_name": entry12,
            "address": entry13,
            "father_last_name": entry18,
            "father_first_name": entry19,
            "father_middle_name": entry20,
            "father_citizenship": entry21,
            "mother_last_name": entry22,
            "mother_first_name": entry23,
            "mother_middle_name": entry24,
            "mother_citizenship": entry25,
            "previous_passport_number": entry28,
            "place_of_issue": entry29,
            "current_address": entry30,
            "occupation": entry31,
            "work_address": entry32,
            "visa_status": entry43,
            "mobile_number": entry33,
            "landline": entry34,
            "email": entry35,
            "contact_person_name": entry36,
            "contact_person_number": entry37,
            "contact_person_email": entry38,
            "date_of_application": application_date,  # Directly assign formatted application date
        }

        form_data = {}

        # Loop through the fields and fetch the values from widgets
        for field_name, widget in fields.items():
            try:
                # Check widget type and retrieve values
                if isinstance(widget, tk.Text):
                    form_data[field_name] = widget.get("1.0", tk.END).strip()  # Handle Text widgets properly
                elif isinstance(widget, tk.Entry):
                    form_data[field_name] = widget.get()  # For Entry widgets
                elif isinstance(widget, tk.StringVar):  # For StringVar (e.g., gender)
                    form_data[field_name] = widget.get()  # Use .get() for StringVar
                elif isinstance(widget, tk.IntVar):  # For IntVar (e.g., year in date)
                    form_data[field_name] = widget.get()  # Use .get() for IntVar
                elif isinstance(widget, ttk.Combobox):  # For ComboBox widgets
                    form_data[field_name] = widget.get()  # Get the selected value from ComboBox
                elif dob:  
                    form_data[field_name] = dob 
                elif application_date:  
                    form_data[field_name] = application_date 
                else:
                    print(f"Unsupported widget type for {field_name}: {type(widget)}")
                    continue
                print(f"{field_name}: {form_data[field_name]}")  # Print data for debugging
            except Exception as e:
                print(f"Error getting value for {field_name}: {e}")

        # Prepare data for database insertion
        data = tuple(form_data.values())

        # Create the review message to display
        review_message = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in form_data.items()])

        # Show the review window with the review message
        show_review_window(review_message, data)

    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging statement
        messagebox.showerror("Error", f"An error occurred: {e}")







# Function to update the image position dynamically
def update_image_position(event):
    # Calculate the new position for the image
    new_x = root.winfo_width() - 320  # Adjust 320 based on your desired position
    new_y = 19  # Keep the Y position fixed
    image_label.place(x=new_x, y=new_y)


# Create the main application window
root = tk.Tk()
root.geometry("610x1000")
root.title("ePassport Application Form")

# Initialize the database
initialize_database()

# Create a Canvas and Scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = ttk.Frame(canvas)

# Pack the Canvas and Scrollbar
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Bind the Frame to the Canvas scroll region
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scroll_region)

# Submit Button
submit_button = tk.Button(scrollable_frame, text="Submit", font=("Times New Roman", 10, 'bold'), bg="green", fg="white", command=submit)
submit_button.grid(row=55, column=1, padx=450, sticky="w")
# Add labels and entry widgets to the scrollable_frame
# ... (Copy all your label and entry widget code here, but replace `frame` with `scrollable_frame`) ...

label1 = tk.Label(scrollable_frame, text="NOTE:", font=("Times New Roman", 5, 'bold'))
label1.grid(row=10, column=1, padx=5, sticky="W")

label1 = tk.Label(scrollable_frame, text="E M B A S S Y  O F  T H E  P H I L I P P I N E S", font=("Times New Roman", 11))
label1.grid(row=10, column=1, padx=178, sticky="W")

label2 = tk.Label(scrollable_frame, text="PERSONAL", font=("Times New Roman", 5, 'bold'))
label2.grid(row=11, column=1, padx=5, sticky="W")

label3 = tk.Label(scrollable_frame, text="APPEARANCE", font=("Times New Roman", 5, 'bold'))
label3.grid(row=12, column=1, padx=5, sticky="W")

label4 = tk.Label(scrollable_frame, text="OF THE APPLICANT", font=("Times New Roman", 5, 'bold'))
label4.grid(row=12, column=1, padx=5, sticky="W")

label5 = tk.Label(scrollable_frame, text="IS REQUIRED", font=("Times New Roman", 5, 'bold'))
label5.grid(row=13, column=1, padx=5, sticky="W")

label6 = tk.Label(scrollable_frame, text="ePASSPORT APPLICATION FORM", font=("Times New Roman", 15, 'bold'))
label6.grid(row=14, column=1, padx=175, sticky="W")

label7 = tk.Label(scrollable_frame, text="REQUIREMENTS: ORIGINAL & PHOTOCOPY OF CURRENT PASSPORT, 1 PASSPORT SIZE PHOTO (ANY BACKGROUND)", font=("Times New Roman",7))
label7.grid(row=15, column=1, padx=10, sticky="W")

label8 = tk.Label(scrollable_frame, text="PLEASE PRINT IN CAPITAL/BLOCK LETTERS:", font=("Times New Roman", 7))
label8.grid(row=16, column=1, padx=10, sticky="W")

label9 = tk.Label(scrollable_frame, text="Last Name     : ", font=("Times New Roman", 7))
label9.grid(row=17, column=1, padx=10, sticky="W")

label10 = tk.Label(scrollable_frame, text="Middle Name : ", font=("Times New Roman", 7))
label10.grid(row=18, column=1, padx=10, sticky="W")

label11 = tk.Label(scrollable_frame, text="First Name : ", font=("Times New Roman", 7))
label11.grid(row=17, column=1, padx=295, sticky="W")

label12 = tk.Label(scrollable_frame, text="Gender/sex : ", font=("Times New Roman",7))
label12.grid(row=18, column=1, padx=295, sticky="W")

label13 = tk.Label(scrollable_frame, text="Male ", font=("Times New Roman", 7))
label13.grid(row=18, column=1, padx=405, sticky="W")

label14 = tk.Label(scrollable_frame, text="Female", font=("Times New Roman", 7))
label14.grid(row=18, column=1, padx=505, sticky="W")

label15 = tk.Label(scrollable_frame, text="Month                                Day                    Year", font=("Times New Roman", 7))
label15.grid(row=19, column=1, padx=90, sticky="W")

label16 = tk.Label(scrollable_frame, text="Date of Birth :", font=("Times New Roman", 7))
label16.grid(row=20, column=1, padx=10, sticky="W")
label16 = tk.Label(scrollable_frame, text="           /         / ", font=("Times New Roman", 9))
label16.grid(row=20, column=1, padx=80, sticky="W")

label17 = tk.Label(scrollable_frame, text="Applicant Additional Information", font=("Times New Roman", 7))
label17.grid(row=21, column=1, padx=10, sticky="W")

label18 = tk.Label(scrollable_frame, text="City / Town - Province / Region", font=("Times New Roman", 7))
label18.grid(row=22, column=1, padx=87, sticky="W")

label19 = tk.Label(scrollable_frame, text="Place of Birth :", font=("Times New Roman", 7))
label19.grid(row=23, column=1, padx=10, sticky="W")

label20 = tk.Label(scrollable_frame, text="Country", font=("Times New Roman", 7))
label20.grid(row=22, column=1, padx=380, sticky="W")

label21 = tk.Label(scrollable_frame, text="Civil Status     :", font=("Times New Roman", 7))
label21.grid(row=24, column=1, padx=10, sticky="W")

label22 = tk.Label(scrollable_frame, text="Spouse Name :", font=("Times New Roman", 7))
label22.grid(row=24, column=1, padx=255, sticky="W")

label23 = tk.Label(scrollable_frame, text="Location", font=("Times New Roman", 7))
label23.grid(row=25, column=1, padx=87, sticky="W")
label24 = tk.Label(scrollable_frame, text="Zip Code", font=("Times New Roman", 7))
label24.grid(row=25, column=1, padx=300, sticky="W")
label25 = tk.Label(scrollable_frame, text="City / Town", font=("Times New Roman", 7))
label25.grid(row=25, column=1, padx=365, sticky="W")

label26 = tk.Label(scrollable_frame, text="Address           :", font=("Times New Roman", 7))
label26.grid(row=26, column=1, padx=10, sticky="W")

label27 = tk.Label(scrollable_frame, text="Province/ Region ", font=("Times New Roman", 7))
label27.grid(row=27, column=1, padx=300, sticky="W")

label28 = tk.Label(scrollable_frame, text="Country ", font=("Times New Roman", 7))
label28.grid(row=27, column=1, padx=476, sticky="W")

label29 = tk.Label(scrollable_frame, text="Father's Identity", font=("Times New Roman", 7))
label29.grid(row=31, column=1, padx=10, sticky="W")

label26 = tk.Label(scrollable_frame, text="Last name:", font=("Times New Roman", 7))
label26.grid(row=32, column=1, padx=10, sticky="W")

label27 = tk.Label(scrollable_frame, text="First Name  :", font=("Times New Roman", 7))
label27.grid(row=32, column=1, padx=315, sticky="W")

label28 = tk.Label(scrollable_frame, text="Middle name:", font=("Times New Roman", 7))
label28.grid(row=33, column=1, padx=10, sticky="W")

label29 = tk.Label(scrollable_frame, text="Citizenship:", font=("Times New Roman", 7))
label29.grid(row=33, column=1, padx=315, sticky="W")

label30 = tk.Label(scrollable_frame, text="Mother's Identity", font=("Times New Roman", 7))
label30.grid(row=34, column=1, padx=10, sticky="W")

label31 = tk.Label(scrollable_frame, text="Last name:", font=("Times New Roman", 7))
label31.grid(row=35, column=1, padx=10, sticky="W")

label32 = tk.Label(scrollable_frame, text="First Name  :", font=("Times New Roman", 7))
label32.grid(row=35, column=1, padx=315, sticky="W")

label33 = tk.Label(scrollable_frame, text="Middle name:", font=("Times New Roman",7))
label33.grid(row=36, column=1, padx=10, sticky="W")

label34 = tk.Label(scrollable_frame, text="Citizenship:", font=("Times New Roman", 7))
label34.grid(row=36, column=1, padx=315, sticky="W")

label35 = tk.Label(scrollable_frame, text="Renewal", font=("Times New Roman", 7, 'bold'))
label35.grid(row=37, column=1, padx=202, sticky="W")

label36 = tk.Label(scrollable_frame, text="Replacement of the Lost Passport", font=("Times New Roman", 7, 'bold'))
label36.grid(row=37, column=1, padx=342, sticky="W")

label37 = tk.Label(scrollable_frame, text="Previous Passport Number:", font=("Times New Roman", 7))
label37.grid(row=38, column=1, padx=10, sticky="W")

label38 = tk.Label(scrollable_frame, text="Place of issue                         :", font=("Times New Roman", 7))
label38.grid(row=39, column=1, padx=10, sticky="W")

label39 = tk.Label(scrollable_frame, text="CURRENT ADDRESS IN UAE (HOUSE NO./STREET/VILLAGE/BRGY./TOWN/PROVINCE/COUNTRY)", font=("Times New Roman", 7))
label39.grid(row=40, column=1, padx=10, sticky="W")

label40 = tk.Label(scrollable_frame, text="OCCUPATION               :", font=("Times New Roman", 7))
label40.grid(row=42, column=1, padx=10, sticky="W")

label40 = tk.Label(scrollable_frame, text="WORK ADDRESS        :", font=("Times New Roman", 7))
label40.grid(row=43, column=1, padx=10, sticky="W")

label41 = tk.Label(scrollable_frame, text="VISA STATUS  :", font=("Times New Roman", 7))
label41.grid(row=42, column=1, padx=315, sticky="W")

label42 = tk.Label(scrollable_frame, text="CONTACT INFORMATION IN UAE", font=("Times New Roman", 7))
label42.grid(row=44, column=1, padx=10, sticky="W")

label42 = tk.Label(scrollable_frame, text="LANDLINE", font=("Times New Roman", 7))
label42.grid(row=44, column=1, padx=295, sticky="W")

label42 = tk.Label(scrollable_frame, text="EMAIL", font=("Times New Roman", 7))
label42.grid(row=45, column=1, padx=295, sticky="W")

label43 = tk.Label(scrollable_frame, text="MOBILE NUMBER", font=("Times New Roman", 7))
label43.grid(row=45, column=1, padx=10, sticky="W")

label44 = tk.Label(scrollable_frame, text="CONTACT PERSON IN THE PHILIPPINES IN CASE OF EMERGENCY:", font=("Times New Roman", 7))
label44.grid(row=46, column=1, padx=10, sticky="W")

label45 = tk.Label(scrollable_frame, text="NAME                 :", font=("Times New Roman", 7))
label45.grid(row=47, column=1, padx=10, sticky="W")

label46 = tk.Label(scrollable_frame, text="TEL./MOBILE NO. :", font=("Times New Roman", 7))
label46.grid(row=48, column=1, padx=10, sticky="W")

label46 = tk.Label(scrollable_frame, text="EMAIL ADDRESS", font=("Times New Roman", 7))
label46.grid(row=48, column=1, padx=315, sticky="W")

label47 = tk.Label(scrollable_frame, text="DATE OF APPLICATION:                 DAY:                     MONTH:                                     YEAR:", font=("Times New Roman", 7))
label47.grid(row=49, column=1, padx=10, pady=4, sticky="W")

label48 = tk.Label(scrollable_frame, text="          I SOLEMNLY SWEAR", font=("Times New Roman", 7, 'bold'))
label48.grid(row=50, column=1, padx=10, sticky="W")

label49 = tk.Label(scrollable_frame, text="that I) 1 am a filipino citizen 2) The information I provided in this application is true and correct. 3) The supporting documents attached are", font=("Times New Roman", 6, 'italic'))
label49.grid(row=50, column=1, padx=130, sticky="W")

label50 = tk.Label(scrollable_frame, text="authentic issued a passport under any. 4) I have not been issued a passport under any other name. 5) I am aware that under the law. I am allowed to hold only one Philippine", font=("Times New Roman", 6, 'italic'))
label50.grid(row=51, column=1, padx=10, sticky="W")

label51 = tk.Label(scrollable_frame, text="passport at a given time. 6) I am aware that making future statements in passport application for furnishing falsified or forged documents in support thereof are punishable by law", font=("Times New Roman", 6, 'italic'))
label51.grid(row=52, column=1, padx=10, sticky="W")

label52 = tk.Label(scrollable_frame, text="APPROVED", font=("Times New Roman", 7))
label52.grid(row=53, column=1, padx=70, sticky="W")

label52 = tk.Label(scrollable_frame, text="SIGNATURE OF APPLICANT", font=("Times New Roman", 7))
label52.grid(row=54, column=1, padx=363, sticky="W")

label53 = tk.Label(scrollable_frame, text="DISAPPROVED", font=("Times New Roman", 7))
label53.grid(row=54, column=1, padx=70, sticky="W")

label53 = tk.Label(scrollable_frame, text="Name and Signature of  Processor", font=("Times New Roman", 7))
label53.grid(row=55, column=1, padx=169, sticky="W")

label54 = tk.Label(scrollable_frame, text="     ", font=("Times New Roman", 7))
label54.grid(row=56, column=1, padx=169, sticky="W")


# Continue adding the remaining widgets like above...

# Entry widgets
entry1 = tk.Entry(scrollable_frame, width=35, bg="#f2ddc5")
entry1.grid(row=17, column=1, padx=82, sticky="W")

entry2 = tk.Entry(scrollable_frame, width=35, bg="#f2ddc5")
entry2.grid(row=18, column=1, padx=82, sticky="W")

entry3 = tk.Entry(scrollable_frame, width=38, bg="#f2ddc5")
entry3.grid(row=17, column=1, padx=350, sticky="W")

entry4 = tk.Checkbutton(scrollable_frame)
entry4.grid(row=18, column=1, padx=380, sticky="W")

entry5 = tk.Checkbutton(scrollable_frame)
entry5.grid(row=18, column=1, padx=480, sticky="W")

entry6 = tk.Entry(scrollable_frame, width=3, bg="#f2ddc5")
entry6.grid(row=20, column=1, padx=90, sticky="W")

entry7 = tk.Entry(scrollable_frame, width=2, bg="#f2ddc5")
entry7.grid(row=20, column=1, padx=124, sticky="W")

entry8 = tk.Entry(scrollable_frame, width=3, bg="#f2ddc5")
entry8.grid(row=20, column=1, padx=152, sticky="W")

entry9 = tk.Entry(scrollable_frame, width=40, bg="#f2ddc5")
entry9.grid(row=23, column=1, padx=78, sticky="W")
entry10 = tk.Entry(scrollable_frame, width=30, bg="#f2ddc5")
entry10.grid(row=23, column=1, padx=328, sticky="W")

entry11 = tk.Entry(scrollable_frame, width=27, bg="#f2ddc5")
entry11.grid(row=24, column=1, padx=78, sticky="W")
entry12 = tk.Entry(scrollable_frame, width=42, bg="#f2ddc5")
entry12.grid(row=24, column=1, padx=328, sticky="W")

entry13 = tk.Text(scrollable_frame, width=27, height=3, bg="#f2ddc5")
entry13.grid(row=26, column=1, rowspan=5, padx=78, sticky="w")

entry14 = tk.Entry(scrollable_frame, width=9, bg="#f2ddc5")
entry14.grid(row=26, column=1, padx=300, sticky="W")
entry15 = tk.Entry(scrollable_frame, width=35, bg="#f2ddc5")
entry15.grid(row=26, column=1, padx=365, sticky="W")

entry16 = tk.Entry(scrollable_frame, width=26, bg="#f2ddc5")
entry16.grid(row=28, column=1, padx=300, sticky="W")

entry17 = tk.Entry(scrollable_frame, width=17, bg="#f2ddc5")
entry17.grid(row=28, column=1, padx=477, sticky="W")

entry18 = tk.Entry(scrollable_frame, width=39, bg="#f2ddc5")
entry18.grid(row=32, column=1, padx=78, sticky="W")

entry19 = tk.Entry(scrollable_frame, width=35, bg="#f2ddc5")
entry19.grid(row=32, column=1, padx=370, sticky="W")

entry20 = tk.Entry(scrollable_frame, width=39, bg="#f2ddc5")
entry20.grid(row=33, column=1, padx=78, sticky="W")

entry21 = tk.Entry(scrollable_frame, width=28, bg="#f2ddc5")
entry21.grid(row=33, column=1, padx=370, sticky="W")

entry22 = tk.Entry(scrollable_frame, width=39, bg="#f2ddc5")
entry22.grid(row=35, column=1, padx=78, sticky="W")

entry23 = tk.Entry(scrollable_frame, width=35, bg="#f2ddc5")
entry23.grid(row=35, column=1, padx=370, sticky="W")

entry24 = tk.Entry(scrollable_frame, width=39, bg="#f2ddc5")
entry24.grid(row=36, column=1, padx=78, sticky="W")

entry25 = tk.Entry(scrollable_frame, width=28, bg="#f2ddc5")
entry25.grid(row=36, column=1, padx=370, sticky="W")

entry26 = tk.Checkbutton(scrollable_frame)
entry26.grid(row=37, column=1, padx=178, sticky="W")

entry27 = tk.Checkbutton(scrollable_frame)
entry27.grid(row=37, column=1, padx=318, sticky="W")

entry28 = tk.Entry(scrollable_frame, width=31, bg="#f2ddc5")
entry28.grid(row=38, column=1, padx=125, sticky="W")

entry29 = tk.Entry(scrollable_frame, width=31, bg="#f2ddc5")
entry29.grid(row=39, column=1, padx=125, sticky="W")

entry30 = tk.Entry(scrollable_frame, width=80, bg="#f2ddc5")
entry30.grid(row=41, column=1, padx=10, sticky="W")

entry31 = tk.Entry(scrollable_frame, width=31, bg="#f2ddc5")
entry31.grid(row=42, column=1, padx=125, sticky="W")

entry32 = tk.Entry(scrollable_frame, width=31, bg="#f2ddc5")
entry32.grid(row=43, column=1, padx=125, sticky="W")

entry33 = tk.Entry(scrollable_frame, width=30, bg="#f2ddc5")
entry33.grid(row=45, column=1, padx=100, sticky="W")

entry34 = tk.Entry(scrollable_frame, width=25, bg="#f2ddc5")
entry34.grid(row=44, column=1, padx=382, sticky="W")

entry35 = tk.Entry(scrollable_frame, width=25, bg="#f2ddc5")
entry35.grid(row=45, column=1, padx=382, sticky="W")

entry36 = tk.Entry(scrollable_frame, width=70, bg="#f2ddc5")
entry36.grid(row=47, column=1, padx=97, sticky="W")

entry37 = tk.Entry(scrollable_frame, width=35, bg="#f2ddc5")
entry37.grid(row=48, column=1, padx=97, sticky="W")

entry38 = tk.Entry(scrollable_frame, width=17, bg="#f2ddc5")
entry38.grid(row=48, column=1, padx=400, sticky="W")

entry39 = tk.Checkbutton(scrollable_frame)
entry39.grid(row=53, column=1, padx=46, sticky="W")

entry40 = tk.Entry(scrollable_frame, width=25, bg="#f2ddc5")
entry40.grid(row=53, column=1, padx=350, sticky="W")

entry41 = tk.Checkbutton(scrollable_frame)
entry41.grid(row=54, column=1, padx=46, sticky="W")

entry42 = tk.Entry(scrollable_frame, width=25, bg="#f2ddc5")
entry42.grid(row=54, column=1, padx=160, sticky="W")

entry43 = tk.Entry(scrollable_frame, width=31, bg="#f2ddc5")
entry43.grid(row=42, column=1, padx=378, sticky="W")




gender_var = tk.StringVar(value="Male")  # Default to "Male"

# Radiobuttons for gender selection
tk.Radiobutton(scrollable_frame, text="Male", variable=gender_var, value="Male").grid(row=18, column=1, padx=380, sticky="W")
tk.Radiobutton(scrollable_frame, text="Female", variable=gender_var, value="Female").grid(row=18, column=1, padx=480, sticky="W")


# Date dropdown variables for Date of Birth
current_year = datetime.now().year
months = list(calendar.month_name)[1:]  # Months (Jan-Dec)
days = list(range(1, 32))               # Days 1-31
years = list(range(current_year - 100, current_year + 1))  # Last 100 years

month_var, day_var, year_var = tk.StringVar(), tk.IntVar(), tk.IntVar()

# Month Dropdown for Date of Birth
ttk.Combobox(scrollable_frame, textvariable=month_var, values=months, width=10, state="readonly").grid(row=20, column=1, padx=90, sticky="W")
month_var.set(months[0])

# Day Dropdown for Date of Birth
ttk.Combobox(scrollable_frame, textvariable=day_var, values=days, width=5, state="readonly").grid(row=20, column=1, padx=179, sticky="W")
day_var.set(days[0])

# Year Dropdown for Date of Birth
ttk.Combobox(scrollable_frame, textvariable=year_var, values=years, width=8, state="readonly").grid(row=20, column=1, padx=238, sticky="W")
year_var.set(current_year)

# Date dropdown variables for Date of Application
month_var_app, day_var_app, year_var_app = tk.StringVar(), tk.IntVar(), tk.IntVar()

# Month Dropdown for Date of Application
ttk.Combobox(scrollable_frame, textvariable=month_var_app, values=months, width=7, state="readonly").grid(row=49, column=1, padx=260, sticky="W")
month_var_app.set(months[0])

# Day Dropdown for Date of Application
ttk.Combobox(scrollable_frame, textvariable=day_var_app, values=days, width=2, state="readonly").grid(row=49, column=1, padx=180, sticky="W")
day_var_app.set(days[0])

# Year Dropdown for Date of Application
ttk.Combobox(scrollable_frame, textvariable=year_var_app, values=years, width=6, state="readonly").grid(row=49, column=1, padx=362, sticky="W")
year_var_app.set(current_year)



# Initialize the Submit button as NORMAL
submit_button = tk.Button(scrollable_frame, text="Submit", font=("Times New Roman", 10, 'bold'),
                          bg="green", fg="white", command=submit, state=tk.NORMAL)
submit_button.grid(row=55, column=1, padx=450, sticky="w")

def validate_form():
    """
    Check if all required fields are filled.
    """
   
    # Helper function to handle both tk.Entry and tk.Text widgets
    def get_widget_value(widget):
        if isinstance(widget, tk.Text):  # For Text widgets
            return widget.get("1.0", tk.END).strip()
        elif isinstance(widget, tk.Entry):  # For Entry widgets
            return widget.get().strip()
        else:
            return ""

    # List of required fields with proper handling
    required_fields = [
        get_widget_value(entry1),  # Last Name
        get_widget_value(entry2),  # Middle Name
        get_widget_value(entry3),  # First Name
        gender_var.get(),  # Gender
        month_var.get(),  # Date of Birth (Month)
        day_var.get(),  # Date of Birth (Day)
        year_var.get(),  # Date of Birth (Year)
        get_widget_value(entry9),  # Place of Birth
        get_widget_value(entry11),  # Civil Status
        get_widget_value(entry13),  # Address
        get_widget_value(entry18),  # Father's Last Name
        get_widget_value(entry19),  # Father's First Name
        get_widget_value(entry20),  # Father's Middle Name
        get_widget_value(entry21),  # Father's Citizenship
        get_widget_value(entry22),  # Mother's Last Name
        get_widget_value(entry23),  # Mother's First Name
        get_widget_value(entry24),  # Mother's Middle Name
        get_widget_value(entry25),  # Mother's Citizenship
        get_widget_value(entry28),  # Previous Passport Number
        get_widget_value(entry29),  # Place of Issue
        get_widget_value(entry30),  # Current Address
        get_widget_value(entry31),  # Occupation
        get_widget_value(entry32),  # Work Address
        get_widget_value(entry43),  # Visa Status
        get_widget_value(entry33),  # Mobile Number
        get_widget_value(entry34),  # Landline
        get_widget_value(entry35),  # Email
        get_widget_value(entry36),  # Contact Person Name
        get_widget_value(entry37),  # Contact Person Number
        get_widget_value(entry38),  # Contact Person Email
        month_var_app.get(),  # Date of Application (Month)
        day_var_app.get(),  # Date of Application (Day)
        year_var_app.get(),  # Date of Application (Year)
    ]

    # Check if all fields are filled
    if all(field for field in required_fields):
        submit_button.config(state=tk.NORMAL)  # Enable the button
    else:
        submit_button.config(state=tk.NORMAL)  # Disable the button

    

# Bind the validation function to all entry fields
def bind_validation_to_entries():
    for entry in [entry1, entry2, entry3, entry9, entry10, entry11, entry12, entry13,
                  entry18, entry19, entry20, entry21, entry22, entry23, entry24, entry25,
                  entry28, entry29, entry30, entry31, entry32, entry33, entry34, entry35,
                  entry36, entry37, entry38, entry43]:
        if isinstance(entry, tk.Text):
            entry.bind("<KeyRelease>", lambda event: validate_form())
        else:
            entry.bind("<KeyRelease>", lambda event: validate_form())

    # Bind validation to dropdowns
    for var in [month_var, day_var, year_var, month_var_app, day_var_app, year_var_app]:
        var.trace_add("write", lambda *args: validate_form())

    # Bind validation to gender radio buttons
    gender_var.trace_add("write", lambda *args: validate_form())




# Bind validation to all entry fields
bind_validation_to_entries()


# Load the image using Pillow
image_path = r"assets/logo.jpg"
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print("Error: Image file not found. Check the path.")
    exit()

# Resize the image to the desired dimensions (e.g., 45x45)
new_size = (45, 45)  # Adjust this to your desired size
resized_image = image.resize(new_size, Image.Resampling.LANCZOS)  # Use LANCZOS for better quality

# Convert the resized image to a format that tkinter can use
photo_resized = ImageTk.PhotoImage(resized_image)

# Create a label to display the resized image (outside the scrollable area)
image_label = tk.Label(scrollable_frame, image=photo_resized)
image_label.grid(row=0, column=1, sticky="ne", pady=10)
#image_label.place(x=290, y=19)  # Place the image at a fixed position
#image_label.pack(pady=10, sticky="W")
# Keep a reference to the image to prevent garbage collection
image_label.photo = photo_resized
# Bind the <Configure> event to update the image position
root.bind("<Configure>", update_image_position)

# Run the application
root.mainloop()