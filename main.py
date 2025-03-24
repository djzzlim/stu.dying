# Import necessary modules
from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import csv
import hashlib
from tkcalendar import DateEntry
import re
import subprocess


# Function to create a popup window with a given prompt message
def open_popup(prompt):
  # Set up the popup window
  top = Toplevel(root)
  top.resizable(0,0)
  top.title("Stu.dying")
  top.configure(bg="#f4ebde")
  
  # Get screen dimensions and calculate popup window coordinates
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  coordinate_x = int((screen_width/2) - 200)
  coordinate_y = int((screen_height/2) - 150)
  
  # Set popup window geometry in center and create a frame
  top.geometry("{}x{}+{}+{}".format(400, 300, coordinate_x, coordinate_y))
  popup_frame = Frame(top,bg="#f4ebde")
  popup_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
  
  # Add a label with the prompt message and an "Ok" button to close the window
  empty_label = Label(popup_frame, text='', bg="#f4ebde").grid(row=1, column=0)
  Label(popup_frame, text=prompt, font=lexend_font,bg="#f4ebde").grid(row=0, column=0)
  Button(popup_frame,text="Ok", font=lexend_font, command=top.destroy,bg="#f4ebde", width=5).grid(row=2, column=0)
  
# Function to handle user login attempts
def login():
  # Check status and initialize email and password lists and get user input
  admin_list = []
  email_list = []
  password = []
  username = []
  temp_email = email.get()
  temp_passwd = passwd.get()

  # Hash the password with MD5 encoding
  hashed_temp_passwd = hashlib.md5(temp_passwd.encode())

  # Read user data from CSV file
  with open("users.csv") as db:
    reader = csv.DictReader(db)
    for line in reader:
      admin_list.append(line["Admin"])
      email_list.append(line["Email Address"])
      password.append(line["Password"])
      username.append(line["Username"])
  db.close()
  
  # Check for missing email or password, and compare input with user data
  if temp_email != '':
      if temp_passwd != '':
          if temp_email in email_list:
              index = email_list.index(temp_email)
              if password[index] == hashed_temp_passwd.hexdigest():
                if admin_list[index] == 'True':
                  print('Admin Login Successful')
                  subprocess.Popen(['python', 'admin.py', username[index]])
                  exit()
                else:
                  print('Login Successful')
                  user = [username[index], *username]
                  subprocess.Popen(['python', 'user.py', *user])
                  exit()
              else:
                # Show a "Login Failed" popup if the password is incorrect
                open_popup('Login Failed')
                print('Login Failed')
          elif temp_email == 'Email' and temp_passwd == 'Password':
            open_popup('Please Enter Credential')
          else:
            # Show a "User Not Found" popup if the email address is not in the user list
            open_popup('User Not Found')
            print("User Not Found")
      else:
        # Show a "Please Enter Password" popup if the password field is blank
        open_popup('Please Enter Password')
        print('Please Enter Password')
  else:
    # Show a "Please Enter Email" popup if the email field is blank
    open_popup('Please Enter Email')
    print('Please Enter Email')


# Set up the main window
root = Tk()
root.title("Stu.dying")
root.geometry("925x435")
root.minsize(925,435)  #set minimum size
# Load the PNG image
icon_image = ImageTk.PhotoImage(Image.open('./media/logo/fishfish.png'))

# Set the application icon
root.iconphoto(True, icon_image)
# Maximize the window if possible
try:
  root.attributes('-zoomed', True)
except:
  root.state('zoomed')

# Set up the background image label
bgimg = ImageTk.PhotoImage(Image.open("./media/bg_img.png"))
bg_label = Label(root, image=bgimg)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Function to handle window resize events
def on_resize(event):
    # Resize the background image to fit the window
    bgimg = Image.open("./media/bg_img.png").resize((event.width, event.height))
    bg_label.image = ImageTk.PhotoImage(bgimg)
    bg_label.configure(image=bg_label.image)

# Bind the on_resize function to the window resize event
root.bind('<Configure>', on_resize)

# Set up the fonts
lexend_font_large = tkFont.Font(family="Lexend Deca", size=64)
lexend_font = tkFont.Font(family="Lexend Deca", size=14)
lexend_font_small = tkFont.Font(family="Lexend Deca", size=11)

# Set up the login frame
login_frame = Frame(root,bg="#f4ebde")
empty_label1 = Label(login_frame, text='', bg="#f4ebde")
empty_label2 = Label(login_frame, text='', bg="#f4ebde")
empty_label3 = Label(login_frame, text='', bg="#f4ebde", height=3)
label1 = Label(login_frame, text="Welcome", font=lexend_font_large, fg='#224957', bg="#f4ebde")
#####################Email#########################################
def on_enter(e):
  email.delete(0, 'end')

def on_leave(e):
  code=email.get()
  if code=='':
    email.insert(0,'Email')

email = Entry(login_frame, width=30, font=lexend_font_small, bg="#ffffff", fg='#000000')

email.insert(0, 'Email')
email.bind('<FocusIn>', on_enter)
email.bind('<FocusOut>', on_leave)
#####################Password#########################################
def on_enter(e):
  passwd.delete(0, 'end')

def on_leave(e):
  psd=passwd.get()
  if psd=='':
    passwd.insert(0,'Password')
passwd = Entry(login_frame, width=30, show="*", font=lexend_font_small,  bg="#ffffff", fg='#000000')
passwd.insert(0, 'Password')
passwd.bind('<FocusIn>', on_enter)
passwd.bind('<FocusOut>', on_leave)
#####################################################################




# Set up the register frame
def register_window():
  global register_window
  register_window = Toplevel()
  root.withdraw()
  register_window.title("Stu.dying")
  register_window.geometry("1080x560")
  register_window.minsize(1080,560)  #set minimum size

  # Maximize the window if possible
  try:
    register_window.attributes('-zoomed', True)
  except:
    register_window.state('zoomed')

  # Set up the background image label
  bgimg2 = ImageTk.PhotoImage(Image.open("./media/bg_img2.png"))
  bg_label = Label(register_window, image=bgimg2)
  bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

  def on_resize(event):
    # Resize the background image to fit the window
    bgimg2 = Image.open("./media/bg_img2.png").resize((event.width, event.height))
    bg_label.image = ImageTk.PhotoImage(bgimg2)
    bg_label.configure(image=bg_label.image)

  def root_page(event):
    register_window.withdraw()
    root.deiconify()
    # Maximize the window if possible
    try:
      root.attributes('-zoomed', True)
    except:
      root.state('zoomed')

  def register():
    email_list = []
    username_list=[]
    temp_username = username_input.get()
    temp_firstname = first_name_input.get()
    temp_lastname = last_name_input.get()
    temp_birth_date = birth_date.get()
    temp_email = email_input.get()
    temp_password = password_input.get()
    temp_password2 = confirm_password_input.get()

    if not all([temp_username, temp_firstname, temp_lastname, temp_birth_date, temp_email, temp_password, temp_password2]):
        open_popup('Please enter all credentials')
        return
    
    with open('users.csv') as db:
      reader = csv.DictReader(db)
      for user in reader:
        email_list.append(user['Email Address'])
        username_list.append(user['Username'])
    db.close()
    if temp_password == temp_password2:
      if temp_email not in email_list and temp_username not in username_list:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.match(regex, temp_email):
          password = hashlib.md5(temp_password.encode())
          info = {
            "Username": temp_username,
            "First Name": temp_firstname,
            "Last Name": temp_lastname,
            "Password": password.hexdigest(),
            "Birth Date": temp_birth_date,
            "Study Hours": 0,
            "Total Run Time": 0,
            "Email Address": temp_email,
            "Admin": False
          }
          with open('users.csv', 'a') as db:
            writer = csv.DictWriter(db, ["Username", "First Name", "Last Name", "Password", "Birth Date", "Study Hours","Total Run Time", "Email Address", "Admin"])
            writer.writerow(info)
          db.close()
        else:
          open_popup('Please Enter The Correct Format of Email')
      else:
        open_popup('User Exists')
    else:
      open_popup('Please Enter The Password Correctly')


# Bind the on_resize function to the window resize event
  register_window.bind('<Configure>', on_resize)

  register_frame = Frame(register_window, bg="#f4ebde")
  empty_label4 = Label(register_frame, text=" ", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  label1 = Label(register_frame, text="Register", font=lexend_font_large, fg='#224957', bg="#f4ebde")
  first_name_label = Label(register_frame, text="First Name", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  last_name_label = Label(register_frame, text="Last name", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  username_label = Label(register_frame, text="Username:", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  username_input = Entry(register_frame, width=30, font=lexend_font_small, fg='#224957', bg='#f4ebde')
  birth_date = DateEntry(register_frame, width= 28, font=lexend_font_small, foreground='#224957', background="#f4ebde", bd=2, date_pattern="dd-mm-yyyy")
  birth_date.delete(0, "end")
  birth_date_label = Label(register_frame, text="Birth Date:", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  email_label = Label(register_frame, text="Email:", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  password_label = Label(register_frame, text="Password:", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  confirm_password_label = Label(register_frame, text="Confirm Password:", font=lexend_font_small, fg='#224957', bg="#f4ebde")
  register_button = Button(register_frame, text="Register", command=lambda: register(), font=lexend_font, width=13)
  login_page_button = Button(register_frame, text="Login", command=lambda: root_page(), font=lexend_font, width=13)
  login_page_button = Label(register_frame, text="<-- Back to Login", font=lexend_font_small, bg="#f4ebde", width=20, height=3)
  login_page_button.bind("<Button-1>", root_page)
  first_name_input = Entry(register_frame, width=18, font=lexend_font_small, fg='#224957', bg='#f4ebde')
  last_name_input = Entry(register_frame, width=18, font=lexend_font_small, fg='#224957', bg='#f4ebde')
  email_input = Entry(register_frame, width = 30, font=lexend_font_small, fg='#224957', bg='#f4ebde')
  password_input = Entry(register_frame, width = 30, font=lexend_font_small, fg='#224957', bg='#f4ebde')
  confirm_password_input = Entry(register_frame, width = 30, font=lexend_font_small, fg='#224957', bg='#f4ebde')

  # Place the register frame widget
  register_frame.place(relx=0.7, rely=0.5, anchor=CENTER)
  label1.grid(row=0, column=0, columnspan=2)
  first_name_label.grid(row=1, column=0, sticky="W")
  first_name_input.grid(row=2, column=0, sticky="W")
  last_name_label.grid(row=1, column=1, sticky="W", padx=80)
  last_name_input.grid(row=2, column=1, sticky="W", padx=80)
  empty_label4.grid(row=3, column=0)
  username_label.grid(row=4, column=0, sticky="W")
  username_input.grid(row=4, column=1)
  birth_date_label.grid(row=5, column=0, sticky="W")
  birth_date.grid(row=5, column=1)
  email_label.grid(row=6, column=0, sticky="W")
  email_input.grid(row=6, column=1)
  password_label.grid(row=7, column=0, sticky="W")
  password_input.grid(row=7, column=1)
  confirm_password_label.grid(row=8, column=0, sticky="W")
  confirm_password_input.grid(row=8, column=1)
  register_button.grid(row=9, column=1)
  login_page_button.grid(row=9, column=0)


login_button = Button(login_frame, text="Login", command=lambda: login(), font=lexend_font, width=13)
register_page_button = Button(login_frame, text="Register", command=register_window, font=lexend_font, width=13)

# Set the image
email_icon = Image.open('./media/email_icon.png')
password_icon = Image.open('./media/password_icon.png')
icon1 = email_icon.resize((40, 40), Image.Resampling.LANCZOS)
icon2 = password_icon.resize((40, 40), Image.Resampling.LANCZOS)
icon1 = ImageTk.PhotoImage(icon1)
icon2 = ImageTk.PhotoImage(icon2)
email_label_icon = Label(login_frame, image=icon1, bg="#f4ebde")
password_label_icon = Label(login_frame, image=icon2, bg="#f4ebde")


# Place the login frame widgets
login_frame.place(relx=0.3, rely=0.5, anchor=CENTER)
label1.grid(row=0, column=0, columnspan=2)
empty_label3.grid(row=1, column=0)
email_label_icon.grid(row=2, column=0)
email.grid(row=2, column=1)
empty_label1.grid(row=3, column=0)
password_label_icon.grid(row=4, column=0)
passwd.grid(row=4, column=1)
empty_label2.grid(row=5, column=0)

subprocess_running = False  # Flag variable to track the state of the subprocess

def reset(event):
    global subprocess_running  # Declare the flag variable as global

    if not subprocess_running:  # Check if the subprocess is not already running
        process = subprocess.Popen(['python', 'forgot_password.py'])
        subprocess_running = True

        # Optionally, you can wait for the subprocess to finish running before allowing it to be triggered again
        process.wait()
        subprocess_running = False

label_button = Label(login_frame, text="Forgot password?", font=lexend_font_small, bg="#f4ebde", width=20, height=3)
label_button.grid(row=6, column=1)
label_button.bind("<Button-1>", reset)

# Configure button to behave like a button
login_button.grid(row=7, column=0)
register_page_button.grid(row=7, column=1)


current_frame = login_frame  # Set the current frame

# Start the main loop
root.mainloop()
