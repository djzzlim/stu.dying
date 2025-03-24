import customtkinter as ctk
import smtplib
import random
import csv
import re
import time
import hashlib
from PIL import ImageTk, Image
import tkinter as tk

unique_code = '*)(!)'
start_time = 0
reset_true = False

def email(receiver):
    global unique_code

    def send_email(sender_email, sender_password, recipient_email, subject, message):
        try:
            # Set up the SMTP server
            smtp_server = 'smtp.gmail.com'  # Change this if using a different email provider
            smtp_port = 587

            # Create a secure connection with the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Compose the email
            email_content = f"Subject: {subject}\n\n{message}"

            # Retry sending the email a maximum of 3 times
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    # Send the email
                    server.sendmail(sender_email, recipient_email, email_content)
                    print('Email sent successfully!')
                    break  # Email sent successfully, exit the loop
                except Exception as e:
                    print(f'Error occurred while sending the email: {str(e)}')
                    if attempt < max_attempts - 1:
                        print('Retrying...')
                        time.sleep(1)  # Wait for 1 second before retrying
                    else:
                        raise  # Maximum attempts reached, raise the exception

        except Exception as e:
            print(f'Error occurred while setting up the email server: {str(e)}')

        finally:
            # Close the SMTP server connection
            server.quit()

    # Email Format
    sender_email = 'stu.dying2004z@gmail.com'
    sender_password = 'nucrnmsxqwqbhcht'
    recipient_email = receiver
    subject = 'Reset Password'
    unique_code = generate_code()
    message = f"We heard that you lost your Stu.dying password. Sorry about that!\n\nDon't worry! You can use the following code to reset your password:\n\n {unique_code} \n\nIf you don't use the code within 5 minutes, it will expire.\n\nThanks,\nThe Stu.dying Team"
    # Generate a code
    print(unique_code)
    send_email(sender_email, sender_password, recipient_email, subject, message)

def generate_code():
    # Generate a random 5-digit code
    code = random.randint(10000, 99999)
    return code

email_list = []
user_list = []

with open('users.csv') as db:
    data = csv.DictReader(db)
    for user in data:
        email_list.append(user["Email Address"])
        user_list.append(user)
    db.close()

def check_time_and_generate_code():
    global unique_code, start_time, reset_true

    if reset_true and time.time() - start_time > 300:
        unique_code = generate_code()
        reset_true = False
        start_time = 0

    root.after(1000, check_time_and_generate_code)

def send():
    global start_time, reset_true, index

    email_input = email_entry.get()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.match(regex, email_input):
        if email_input in email_list:
            email_entry.configure(border_color="#777")
            notify_label.configure(text=" ")
            index = email_list.index(email_input)
            code_entry.configure(state="normal")
            reset_button.configure(state="normal")
            email_entry.configure(state="disabled")
            email(email_input)
            start_time = time.time()
            reset_true = True
            code_entry.focus()
        else:
            email_entry.configure(border_color="red")
            notify_label.configure(text="Email is not registered.")
    else:
        email_entry.configure(border_color="red")
        notify_label.configure(text="Enter the correct format.")

def reset():
    global email_frame, reset_button, password_input, confirm_password_input, confirm_button

    try:
        code = int(code_entry.get())

        if code == unique_code:
            notify_label.configure(text=" ")
            reset_button = False
            time.sleep(1)

            for widgets in email_frame.winfo_children():
                widgets.destroy()

            password_label = ctk.CTkLabel(email_frame, text="New Password:", font=my_font_supersmall, text_color='#7a7a7a')
            password_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            cpassword_label = ctk.CTkLabel(email_frame, text="Confirm Password:", font=my_font_supersmall, text_color='#7a7a7a')
            cpassword_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

            password_input =  ctk.CTkEntry(email_frame, width=200)
            password_input.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            confirm_password_input =  ctk.CTkEntry(email_frame, width=200)
            confirm_password_input.grid(row=3, column=0, padx=10, pady=10, sticky="w")

            confirm_button = ctk.CTkButton(email_frame, text="Confirm", font=my_font_supersmall, command=change_password, width=100)
            confirm_button.grid(row=4, column=0, padx=20, pady=5, sticky="e")
        else:
            code_entry.configure(border_color="red")
            notify_label.configure(text="Wrong Code!!!")
    except:
        code_entry.configure(border_color="red")
        notify_label.configure(text="Wrong Code!!!")

def change_password():
    password1 = password_input.get()
    password2 = confirm_password_input.get()
    if password1 == password2:
        password = hashlib.md5(password1.encode())
        user_list[index]["Password"] = password.hexdigest()
        with open("users.csv", "w") as db:
            field_name = ["Username", "First Name", "Last Name", "Password", "Birth Date", "Study Hours","Total Run Time", "Email Address", "Admin"]
            writer = csv.DictWriter(db, field_name)
            writer.writeheader()
            writer.writerows(user_list)
        db.close()
        for widgets in email_frame.winfo_children():
            widgets.destroy()
        root.destroy()


# Create CTk instance
root = ctk.CTk()
root.title("Stu.dying Forgot Password")

# Set appearance mode to current
current = ctk.get_appearance_mode()
ctk.set_appearance_mode('light')


# Get the screen resolution to set the window size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root_x = int(width / 2)
root_y = int(height / 4)
# Set the minimum and current window size
# root.minsize(width, height)
root.geometry(f"480x350+{root_x}+{root_y}")
root.resizable(False, False)
root.grab_set()

# Maximize the window to cover the whole screen
# try:
#     root.after(0, lambda: root.state('zoomed'))
# except:
#     root.attributes('-zoomed', True)
# else:
#     root.state('zoomed')

# Create CTkFont instances
my_font_supersmall = ctk.CTkFont(family='SF Pro Display', size=15, weight='bold')
my_font_small = ctk.CTkFont(family='SF Pro Display', size=23, weight='bold')
my_font_medium = ctk.CTkFont(family='SF Pro Display', size=35, weight='bold')
my_font_notification = ctk.CTkFont(family='SF Pro Display', size=12, weight='bold')

email_frame = ctk.CTkFrame(root, bg_color="transparent", fg_color="#ebebeb")

text = ctk.CTkLabel(email_frame, text="Reset your Password", font=my_font_small, text_color='#737373')
text.grid(row=0, column=0, columnspan=3, pady=15)

email_label = ctk.CTkLabel(email_frame, text="Enter your Email:", font=my_font_supersmall, text_color='#7a7a7a')
email_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

email_entry = ctk.CTkEntry(email_frame, width=200)
email_entry.grid(row=2, column=0, padx=10, pady=5)

send_button = ctk.CTkButton(email_frame, text="Send", font=my_font_supersmall, command=send)
send_button.grid(row=2, column=1, padx=20, pady=5)

code_label = ctk.CTkLabel(email_frame, text="Enter code:", font=my_font_supersmall, text_color='#7a7a7a')
code_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

code_entry = ctk.CTkEntry(email_frame, width=200, state='disabled')
code_entry.grid(row=4, column=0, padx=10, pady=5)

reset_button = ctk.CTkButton(email_frame, text="Reset", font=my_font_supersmall, command=reset, state='disabled')
reset_button.grid(row=4, column=1, padx=20, pady=5)

notify_label = ctk.CTkLabel(email_frame, text=" ", font=my_font_supersmall, text_color="red")
notify_label.grid(row=5, column=0, padx=10, pady=5, columnspan=3)

email_frame.pack(side="top", padx=50, pady=50)

check_time_and_generate_code()
root.mainloop()
