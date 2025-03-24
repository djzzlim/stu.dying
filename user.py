import customtkinter as ctk
from tkinter import *
from PIL import Image
import csv
import json
import subprocess
import datetime
import sys
from tkcalendar import DateEntry
import re


#create CTk instance
root = ctk.CTk()
root.title("Stu.dying")

# Set appearance mode to dark
ctk.set_appearance_mode("Dark")


# Get the screen resolution to set the window size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Set the minimum and current window size
root.minsize(width, height)
root.geometry(f"{width}x{height}+0+0")

# Maximize the window to cover the whole screen
try:
    root.after(0, lambda: root.state('zoomed'))
except:
    root.attributes('-zoomed', True)
else:
    root.state('zoomed')


# Create CTkFont instances
my_font_mini = ctk.CTkFont(family='SF Pro Display', size=12, weight='bold')
my_font_supersmall = ctk.CTkFont(family='SF Pro Display', size=15, weight='bold')
my_font_small = ctk.CTkFont(family='SF Pro Display', size=23, weight='bold')
my_font_medium = ctk.CTkFont(family='SF Pro Display', size=35, weight='bold')
my_font_notification = ctk.CTkFont(family='SF Pro Display', size=12, weight='bold')
my_font_large = ctk.CTkFont(family='SF Pro Display', size=40, weight='bold')

date = datetime.datetime.now()

# get user username and index
username = sys.argv[1]
username_list = sys.argv[2:]
user_index = username_list.index(username)


def change_mode():
    current_mode = ctk.get_appearance_mode()

    # change appearance mode and images
    if current_mode == "Light":
        ctk.set_appearance_mode("Dark")
        mode_label.configure(text="Dark Mode")
        logo_img = ctk.CTkImage(Image.open("./media/dark_mode/logo_dark.png"), size=(80,35))
        user_icon = ctk.CTkImage(Image.open("./media/dark_mode/user_dark.png"), size=(40,40))
        feedback_icon = ctk.CTkImage(Image.open("./media/dark_mode/feedback_dark.png"), size=(40,38))
        notification_icon = ctk.CTkImage(Image.open("./media/dark_mode/notification_dark.png"), size=(40,40))
    else:
        ctk.set_appearance_mode("Light")
        mode_label.configure(text="Light Mode")
        logo_img = ctk.CTkImage(Image.open("./media/light_mode/logo_light.png"), size=(80,35))
        user_icon = ctk.CTkImage(Image.open("./media/light_mode/user_light.png"), size=(40,40))
        feedback_icon = ctk.CTkImage(Image.open("./media/light_mode/feedback_light.png"), size=(40,38))
        notification_icon = ctk.CTkImage(Image.open("./media/light_mode/notification_light.png"), size=(40,40))

    logo.configure(image=logo_img)
    user_button.configure(image=user_icon)
    feedback_button.configure(image=feedback_icon)
    notification_button.configure(image=notification_icon)


notification_pane_open = False
def notification():
    global notification_pane_open, notification_pane

    # create notification pane
    if not notification_pane_open:
        notification_pane = ctk.CTkFrame(root, height=270, width=230, bg_color='transparent', border_width=2, fg_color='transparent')
        notification_info = ctk.CTkScrollableFrame(notification_pane, width=230, height=270, label_text="Notification", fg_color='transparent', label_font=my_font_supersmall)
        
        notification_info.grid(column=0, row=0, padx=10, pady=10)
        notification_pane.place(relx=0.75, y=61)

        # create text frame to display announcement
        text_frame = ctk.CTkFrame(notification_info, width=220, height=40, fg_color="transparent")
        text_frame.pack(fill='x', pady=2, ipadx=20)
        new_data = []
      
        with open('announcement.json') as db:
            data = json.load(db)
            for i in data:
                new_data.append(i)
        db.close()

        # display announcements
        for item in new_data[::-1]: 
            notice_frame = ctk.CTkFrame(text_frame, width=220)
            notice_frame.pack(side='top', fill='x', pady=5)

            name = ctk.CTkLabel(notice_frame, text=item["Admin"], font=my_font_supersmall, wraplength=100, text_color='#3B8ED0', justify='left')
            notice = ctk.CTkLabel(notice_frame, text=item["Announcement"], font=my_font_notification, wraplength=200, justify='left')
            date_time = ctk.CTkLabel(notice_frame, text=item["Date"], font=('SF Pro Display', 10, 'bold'))

            name.pack(side='top', anchor="w", padx=15)
            notice.pack(side='top', anchor="w", padx=15)
            date_time.pack(side="bottom", anchor="e", padx=15, pady=10)

        notification_pane_open = True
    else:
        notification_pane.destroy()
        notification_pane_open = False


def feedback():
    fb = ctk.CTkToplevel(root)
    fb.title('stu.dying Feedback')
    fb_x = int(width / 2)
    fb_y = int(height / 10)
    fb.geometry(f'480x550+{fb_x}+{fb_y}')
    fb.resizable(False, False)
    fb.grab_set() # make toplevel stay on top parent window

    fb_frame = ctk.CTkFrame(fb, fg_color=("#ebebeb", "#242424"))
    fb_frame.pack(padx=40)

    feedback_heading = ctk.CTkLabel(fb_frame, text="Feedback Form", font=("SF Pro Display", 25, 'bold'))
    feedback_heading.grid(row=0, column=0, pady=15, sticky="w")

    # radio buttons
    feedback_option = ctk.CTkLabel(fb_frame, text="How was stu.dying?", font=("SF Pro Display", 16, 'bold'))
    feedback_option.grid(row=1, column=0, pady=6, sticky="w")

    radio_var = ctk.StringVar()
    radiobtn_1 = ctk.CTkRadioButton(fb_frame, text="It's helpful", variable=radio_var, value="It's helpful",
                                    radiobutton_width=15, radiobutton_height=15, border_width_checked=2)
    radiobtn_2 = ctk.CTkRadioButton(fb_frame, text="I found a bug or error message", variable=radio_var,
                                    value="I found a bug or error message", radiobutton_width=15, radiobutton_height=15,
                                    border_width_checked=2)
    radiobtn_3 = ctk.CTkRadioButton(fb_frame, text="The content was inappropriate", variable=radio_var,
                                    value="The content was inappropriate", radiobutton_width=15, radiobutton_height=15,
                                    border_width_checked=2)
    radiobtn_4 = ctk.CTkRadioButton(fb_frame, text="Others / Suggestions", variable=radio_var,
                                    value="Others / Suggestions",
                                    radiobutton_width=15, radiobutton_height=15, border_width_checked=2)

    radiobtn_1.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    radiobtn_2.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    radiobtn_3.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    radiobtn_4.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    # ratings
    ratings_frame = ctk.CTkFrame(fb_frame, fg_color=("#ebebeb", "#242424"))
    ratings_frame.grid(row=6, column=0, sticky="w")

    ratings_label = ctk.CTkLabel(ratings_frame, text="Rate us :  ", font=my_font_supersmall)
    ratings_label.grid(row=6, column=0, pady=10, sticky="w")

    star_1 = ctk.CTkButton(ratings_frame, width=1, height=10, text="", image=grey_star, fg_color=("#ebebeb", "#242424"),
                           command=lambda: rate(1, star_1, star_2, star_3, star_4, star_5))
    star_2 = ctk.CTkButton(ratings_frame, width=1, height=10, text="", image=grey_star, fg_color=("#ebebeb", "#242424"),
                           command=lambda: rate(2, star_1, star_2, star_3, star_4, star_5))
    star_3 = ctk.CTkButton(ratings_frame, width=1, height=10, text="", image=grey_star, fg_color=("#ebebeb", "#242424"),
                           command=lambda: rate(3, star_1, star_2, star_3, star_4, star_5))
    star_4 = ctk.CTkButton(ratings_frame, width=1, height=10, text="", image=grey_star, fg_color=("#ebebeb", "#242424"),
                           command=lambda: rate(4, star_1, star_2, star_3, star_4, star_5))
    star_5 = ctk.CTkButton(ratings_frame, width=1, height=10, text="", image=grey_star, fg_color=("#ebebeb", "#242424"),
                           command=lambda: rate(5, star_1, star_2, star_3, star_4, star_5))

    star_1.grid(row=6, column=1, sticky="w")
    star_2.grid(row=6, column=2, sticky="w")
    star_3.grid(row=6, column=3, sticky="w")
    star_4.grid(row=6, column=4, sticky="w")
    star_5.grid(row=6, column=5, sticky="w")

    # comments box
    comments_heading = ctk.CTkLabel(fb_frame, text="Leave Additional Comments", font=("SF Pro Display", 16, 'bold'))
    comments_heading.grid(row=7, column=0, pady=6, sticky="w")
    comments_box = ctk.CTkTextbox(fb_frame, width=400, height=100, border_color="#acb4b4", border_width=2, wrap="word")
    comments_box.grid(row=8, column=0, pady=10)

    # privacy policy checkbox
    check_var = ctk.StringVar(value="no")
    checkbox = ctk.CTkCheckBox(fb_frame, text="Send system information", variable=check_var, onvalue="yes",
                               offvalue="no",
                               checkbox_width=15, checkbox_height=15, border_width=2, corner_radius=0)
    policy = ctk.CTkLabel(fb_frame, text="By clicking send, your feedback will be used to improve stu.dying services.\n"
                                         "Our IT admin will be able to collect this data.", font=("Arial", 12), justify="left")
  
    checkbox.grid(row=9, column=0, sticky="w")
    policy.grid(row=10, column=0, sticky="w", pady=5)

    # send button
    send_btn = ctk.CTkButton(fb_frame, text="Send",
                             command=lambda: send(fb_frame, radio_var, comments_box, check_var, incomplete))
    send_btn.grid(row=11, column=0, pady=10, sticky="e")

    # feedback form incomplete label
    incomplete = ctk.CTkLabel(fb_frame, text="", font=my_font_notification)
    incomplete.grid(row=11, column=0, sticky="w")


grey_star = ctk.CTkImage(Image.open("./media/star_grey.png"))
yellow_star = ctk.CTkImage(Image.open("./media/yellow star.png"))

selected_rating = "0 star(s)"


def rate(index, star_1, star_2, star_3, star_4, star_5):
    r = [star_1, star_2, star_3, star_4, star_5]
  
    # change star colour when user click
    for i in range(0, 5):
        if i < index:  
            r[i].configure(image=yellow_star)
        else:
            r[i].configure(image=grey_star)
          
    global selected_rating
    selected_rating = f'{index} star(s)'

  
def send(fb_frame, radio_var, comments_box, check_var, incomplete):
    global selected_rating
    radio_value = radio_var.get()
    comments = comments_box.get("1.0", "end-1c")
    check_value = check_var.get()

    # check if feedback form is completely filled in
    if radio_value == "" or comments == "": # not filled in
        incomplete.configure(text="Please fill in every field.", text_color="red")
    elif check_value == "no": # user did not agree with privacy policy
        incomplete.configure(text="Please agree with privacy policy.", text_color="red")
    else:
        if incomplete is not None: # hide incomplete label
            incomplete.configure(text_color=("#ebebeb", "#242424"))

        date_text = str(date.strftime("%x" + " " + "%X"))
        
        feedback = [{
            "Username": username,
            "Radio value": radio_value,
            "Comments": comments,
            "Ratings": selected_rating,
            "DateTime": date_text
        }]

        # add new feedback to json file
        with open("feedback.json", "r") as feedback_file:  # read old feedback
            data = json.load(feedback_file)  
            data.append(feedback[0])  
        with open("feedback.json", "w") as feedback_file: # update feedback file
            json.dump(data, feedback_file, indent=4)  

        # close feedback form
        for widgets in fb_frame.winfo_children():
            widgets.destroy()
        thank_you = ctk.CTkLabel(fb_frame, text="Thank you\nfor your feedback.", font=my_font_medium)
        thank_you.pack(pady=200)
        selected_rating = "0 star(s)"


# Variable to track if the user has already logged out
already_logout = False

def on_close():
    global already_logout 
    already_logout = True
    total_run_time()
    exit()


def logout(): 
    top = ctk.CTkToplevel(root)
    top.title("Stu.dying")
    top.grab_set()
    top.resizable(0,0)
    coordinate_x = int((width/2)-65)
    coordinate_y = int((height/2)-35)
    top.geometry("{}x{}+{}+{}".format(400,200,coordinate_x,coordinate_y))

    def confirm():
        global already_logout
        top.destroy()
        already_logout = True
        total_run_time()
        subprocess.Popen(['python', './main.py'])
        exit()

    confirm_frame = ctk.CTkFrame(top, fg_color="transparent")
    confirm_label = ctk.CTkLabel(confirm_frame, text="Confirm to logout?", font=my_font_supersmall)
    confirm_button = ctk.CTkButton(confirm_frame, text="Confirm", font=my_font_supersmall, command=confirm)
    cancel_button = ctk.CTkButton(confirm_frame, text="Cancel", font=my_font_supersmall, command=top.destroy)

    confirm_frame.pack(expand=TRUE, padx=(0,8), pady=(0,10))
    confirm_label.pack()
    confirm_button.pack(pady=2)
    cancel_button.pack()

    top.protocol("WM_DELETE_WINDOW", top.destroy)

start_timer = datetime.datetime.now()

def total_run_time():
    global start_timer, already_logout
    # List to store all user information
    all_info = []

    # Check if the user has already logged out
    if already_logout: 
        end_timer = datetime.datetime.now()
        # Calculate the total run time and convert to seconds
        run_time = end_timer - start_timer
        run_seconds = int(run_time.total_seconds())

        # Read the user information from the "users.csv" file
        with open ("users.csv") as db:
            reader = csv.DictReader(db)
            for line in reader:
                all_info.append(line)
        db.close

        selected_info = all_info[user_index]
        ori_runtime = int(selected_info["Total Run Time"])
        selected_info["Total Run Time"] = ori_runtime + run_seconds
        all_info.pop(user_index)
        all_info.insert(user_index, selected_info)

        # Read the user information from the "users.csv" file
        with open("users.csv", "w", newline="") as db:
            writer = csv.DictWriter(db, fieldnames=csv_header)
            writer.writeheader()
            for item in all_info:
                writer.writerow(item)
            db.close
          
        # set the logout flag for future logouts
        already_logout = False


todo = None
todo_frame = None
game_start = False
def todolist():
    global todo
    all_task = []
    all_no = {}
    all_label = {}

    if todo is not None:
        todo.destroy()

    def on_enter(event):
        if entry.get() == "Task to be completed today (press enter to add)":
            entry.delete(0, END)
        if len(all_task) < 13:
            entry.configure(state=NORMAL)

    def on_leave(event):
        if entry.get() == '': 
            entry.insert(0, "Task to be completed today (press enter to add)")


    def label_input(event):
        global todo_frame
        entry.configure(state=NORMAL, border_color="#777")
        task = entry.get() 

        if task != "":
            all_task.append(task)
        entry.delete(0, END)

        # limit the number of task
        if len(all_task) < 13:
            entry.configure(state=NORMAL)
        else:
            entry.configure(state=DISABLED)

        if todo_frame is not None:
            todo_frame.destroy()

        todo_frame = ctk.CTkFrame(todo, fg_color="transparent")
        todo_frame.pack(side=TOP, fill=X, padx=2)
        
      # display all task entered by user
        for no, task in enumerate(all_task):
            all_no[no] = ctk.CTkLabel(todo_frame, text=f"{no+1}. ", font=my_font_supersmall)
            all_no[no].grid(row=no, column=0, sticky=W, padx=(13,0), pady=(5,0))
            all_label[no] = ctk.CTkLabel(todo_frame, text=task, font=my_font_supersmall)
            all_label[no].grid(row=no, column=1, sticky=W, padx=(5,0), pady=(5,0))
            all_label[no].bind("<Double-Button-1>", lambda event, no = no: edit(event, no))


    # set up entry widget to edit task
    def edit(event, no):
        try:
            selected = str(event.widget.cget("text"))
            edit_entry = ctk.CTkEntry(todo_frame, font=my_font_supersmall, width=410)
            edit_entry.grid(row=no, column=1, sticky=EW, pady=(5,0))
            edit_entry.insert(0, selected)
            edit_entry.focus_set()
            edit_entry.bind("<FocusOut>", lambda event: save(event, no))
            edit_entry.bind("<KeyPress>", lambda event: check(event, edit_entry))
            todo.bind("<Button-1>", lambda event: entry.focus_set()) 
        except (TclError, UnboundLocalError):
            pass


        def save(event, no):
            edit_task = edit_entry.get() 

            # edit the arrangement of all task when a edit entry is empty
            if edit_task == "":
                last_no = len(all_task)-1 
                all_no[last_no].destroy()
                all_no.pop(last_no)
                edit_entry.destroy()

                for i in range (no, len(all_label)):
                    if i+1 == len(all_label):
                        all_label[i].destroy()
                        del all_label[i]
                    else: 
                        next_task = all_task[i+1]
                        all_label[i].configure(text=next_task)
                        
                all_task.pop(no)
            else:
                # destroy edit entry and display the input
                edit_entry.destroy()
                all_task.pop(no)
                all_task.insert(no, edit_task)
                all_label[no].configure(text=edit_task)
              

    def check(event, widget):
        text = widget.get()
        if event.keysym == "BackSpace": 
            text = text[:-1]
        elif event.keysym.isalpha() or event.keysym.isnumeric(): 
            text= text + event.char
        else: 
            text = text

        text_width = my_font_supersmall.measure(text)

        # limit the width of input
        if text_width >= 350:
            while text_width >= 350:
                text = text[:-1] 
                text_width = my_font_supersmall.measure(text)
            widget.delete(0, END)
            widget.insert(0, text)
            widget.configure(border_color="red")
        else:
            widget.configure(border_color="#777")


    def pygame():
        global game_start
        all_info = []

        if not game_start:
            game_start = True

            # open pygame and collect the start time and end time to count the total study hours
            start_time = datetime.datetime.now()
            root.withdraw()
            process = subprocess.Popen(['python', './game.py', *all_task])
            process.wait()
            end_time = datetime.datetime.now()
            total_time = end_time - start_time
            total_seconds = int(total_time.total_seconds())
            root.deiconify()

            try:
                root.after(0, lambda: root.state('zoomed'))
            except:
                root.attributes('-zoomed', True)
            else:
                root.state('zoomed')
                
            game_start = False

        # add the total study hours and the total previous study hours and record it
        with open ("users.csv") as db:
            reader = csv.DictReader(db)
            for line in reader:
                all_info.append(line)
        db.close

        selected_info = all_info[user_index]
        ori_studyhours = int(selected_info["Study Hours"])
        selected_info["Study Hours"] = ori_studyhours + total_seconds
        all_info.pop(user_index)
        all_info.insert(user_index, selected_info)

        with open("users.csv", "w", newline="") as db:
            writer = csv.DictWriter(db, fieldnames=csv_header)
            writer.writeheader()
            for item in all_info:
                writer.writerow(item)
            db.close()
        
        todolist()
        dashboard()
        leaderboard()


    # set up and display frame, todolist label, a entry widget and start button
    todo = ctk.CTkFrame(todo_list, fg_color="transparent")
    title_frame = ctk.CTkFrame(todo, fg_color="transparent")
    todolist_label = ctk.CTkLabel(title_frame, text="To-Do List", font=my_font_large, width=50)
    date_str = str(date.strftime("%x"))
    date_label = ctk.CTkLabel(title_frame, text=date_str, font=my_font_supersmall, width=20)
    start_button = ctk.CTkButton(todo, text="Start Session", font=my_font_small, height=35, command=pygame)
    entry = ctk.CTkEntry(todo, font=my_font_supersmall, height=45)

    todo.pack(fill=BOTH, expand=True, padx=5, pady=5)
    title_frame.pack(side=TOP,anchor=W)
    todolist_label.pack(side=LEFT, padx=20, pady=10)
    date_label.pack(side=LEFT, anchor=S, pady=10)
    start_button.pack(side=BOTTOM, fill=X, padx=20, pady=(0,15))
    entry.pack(side=BOTTOM, fill=X, padx=15, pady=15)
    entry.insert(0,"Task to be completed today (press enter to add)")
    entry.bind("<FocusIn>", on_enter)
    entry.bind("<FocusOut>", on_leave)
    entry.bind("<Return>", label_input)
    entry.bind("<KeyPress>", lambda event: check(event, entry))


db_frame = None
def dashboard():
    global db_frame, selected_hours, selected_minutes, checkin_date
    all_info = []
    users = []
    dates = []
    checkin_date = []

    # read user's total study hours and change it into hours and minutes
    with open ("users.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
            all_info.append(line)
    db.close

    selected_info = all_info[user_index]

    total_seconds = int(selected_info["Study Hours"])
    total_minutes = total_seconds // 60
    selected_hours, selected_minutes = divmod(total_minutes, 60)

    # read user‘s all checkedin date and check if today alr checked in
    with open ("checkin.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
            users.append(line["CheckedIn User"])
            dates.append(line["Date"])
    db.close

    for user, date in zip(users, dates):
        if user == username:
            checkin_date.append(date)

    if str(datetime.date.today()) not in checkin_date:
        with open ("checkin.csv", "a", newline="") as db:
            writer = csv.writer(db)
            checkin = [username,datetime.date.today()]
            writer.writerow(checkin)
        db.close 

    if db_frame is not None:
        db_frame.destroy()

    # set up and display user's total study hours and total chekedin day
    db_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
    db_frame.pack(side=LEFT, anchor=N, padx=5, pady=5)
    dashboard_label = ctk.CTkLabel(db_frame, text="Dashboard", font=my_font_medium)
    total_study = ctk.CTkLabel(db_frame, text=f"Total Study Hours:   {selected_hours} hours {selected_minutes} minutes", font=("SF Pro Display", 18))
    total_checkin = ctk.CTkLabel(db_frame, text=f"Total Checked-In Days:   {len(checkin_date)} days", font=("SF Pro Display", 18))

    dashboard_label.pack(side=TOP, anchor=W, padx=25, pady=20)
    total_study.pack(side=TOP, anchor=W, padx=25)
    total_checkin.pack(side=TOP, anchor=W, padx=25, pady=20)


lb_frame = None
def leaderboard():
    global lb_frame
    all_username = []
    all_studyhours = []
    sorted_username = []

    # read all username and their total study hours
    with open ("users.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
            if line["Admin"] == "False":
                all_username.append(line["Username"])
                all_studyhours.append(int(line["Study Hours"]))
    db.close

    # sorted all user total study hours from large to small
    sorted_studyhours, sorted_username = zip(*sorted(zip(all_studyhours, all_username), reverse=True))

    if lb_frame is not None:
        lb_frame.destroy()

    # set up and display user's ranking
    lb_frame = ctk.CTkFrame(leaderboard_frame, fg_color="transparent")
    lb_frame.pack(side=LEFT, anchor=N, padx=5, pady=5)
    leaderboard_label = ctk.CTkLabel(lb_frame, text="Leaderboard", font=my_font_medium)

    leaderboard_label.pack(side=TOP, anchor=W, padx=25, pady=25)

    selected_index = sorted_username.index(username)

    selected_label = ctk.CTkLabel(lb_frame, text=f"{selected_index+1}.   {username} ----- {selected_hours} hours {selected_minutes} minutes", font=("SF Pro Display", 18))
    selected_label.pack(side=TOP, anchor=W, padx=25, pady=(0,15))

    # set up and display the top 10 users and their total study hours
    for i, item in enumerate(sorted_studyhours[:10]):
        item = item // 60
        hours, minutes = divmod(item, 60)

        ranking_label = ctk.CTkLabel(lb_frame, text=f"{i+1}.   {sorted_username[i]} ----- {hours} hours {minutes} minutes", font=my_font_supersmall)
        ranking_label.pack(side=TOP, anchor=W, padx=25)


def badges():
    # badges images
    login_badge1 = ctk.CTkImage(Image.open("media/badges/fish1.png"), size=(50, 50))
    login_badge2 = ctk.CTkImage(Image.open("media/badges/fish2.png"), size=(70, 70))
    login_badge3 = ctk.CTkImage(Image.open("media/badges/fish3.png"), size=(100, 100))
    login_badge4 = ctk.CTkImage(Image.open("media/badges/fish4.png"), size=(110, 110))

    studyhr_badge1 = ctk.CTkImage(Image.open("media/badges/book1.png"), size=(50, 50))
    studyhr_badge2 = ctk.CTkImage(Image.open("media/badges/book2.png"), size=(50, 50))
    studyhr_badge3 = ctk.CTkImage(Image.open("media/badges/book3.png"), size=(50, 50))
    studyhr_badge4 = ctk.CTkImage(Image.open("media/badges/book4.png"), size=(50, 50))

    # create badges and labels
    login_badge = ctk.CTkButton(badges_frame, image=login_badge1, width=80, height=80, text="", fg_color=('#cfcfcf', '#333333'), hover=False)
    login_label = ctk.CTkLabel(badges_frame, text=f"logged in for {len(checkin_date)} day(s)")
    studyhr_badge = ctk.CTkButton(badges_frame, image=studyhr_badge1, width=80, height=80, text="", fg_color=('#cfcfcf', '#333333'), hover=False)
    studyhr_label = ctk.CTkLabel(badges_frame, text=f"studied for {selected_hours} hour(s)")

    login_badge.grid(row=0, column=0)
    login_label.grid(row=1, column=0, pady=5)
    studyhr_badge.grid(row=0, column=1)
    studyhr_label.grid(row=1, column=1, pady=5)

    badges_frame.columnconfigure((0, 1), weight=1)

    # unlock login_badge
    if 1 <= len(checkin_date) < 3: 
        login_badge.configure(image=login_badge1)
    elif 3 <= len(checkin_date) < 5:
        login_badge.configure(image=login_badge2)
    elif 5 <= len(checkin_date) < 7:
        login_badge.configure(image=login_badge3)
    elif 7 <= len(checkin_date):
        login_badge.configure(image=login_badge4)

    # unlock studyhr_badge
    if 1 <= selected_hours < 3:
        studyhr_badge.configure(image=studyhr_badge1)
    elif 3 <= selected_hours < 5:
        studyhr_badge.configure(image=studyhr_badge2)
    elif 5 <= selected_hours < 7:
        studyhr_badge.configure(image=studyhr_badge3)
    elif 7 <= selected_hours:
        studyhr_badge.configure(image=studyhr_badge4)
    else:
        studyhr_badge.destroy()
        studyhr_label.destroy()


info_frame = None
button_frame = None
all_error = []
csv_header = ["Username","First Name","Last Name","Password","Birth Date","Study Hours","Total Run Time","Email Address","Admin"] 
def user_profile():
    global info_frame
    all_info = []
    key = ["Username","First Name","Last Name","Birth Date"]

    with open ("users.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
            all_info.append(line)
    db.close

    selected_info = all_info[user_index]
    user.configure(text=username + "'s Profile")

    if info_frame is not None:
        info_frame.destroy()
    if button_frame is not None:
        button_frame.destroy()


    def edit_profile():
        global button_frame, all_entry, all_label, save_button
        all_entry = []
        all_label = []
        user_info.destroy()
        edit_button.destroy()

        edit_frame = ctk.CTkFrame(info_frame)
        edit_frame.pack(side=TOP, anchor=W, expand=False)

        # set up entry widget to edit info
        for i, item in enumerate(key):
            key_label = ctk.CTkLabel(edit_frame, text=f"{item}:", font=("SF Pro Display", 18))

            if item == "Birth Date":
                edit_entry = DateEntry(edit_frame, font=("SF Pro Display", 18), width=23, border_color=("#acb4b4", "#535b5b"), date_pattern="dd-mm-yyyy", state="readonly")
            else:
                edit_entry = ctk.CTkEntry(edit_frame, font=("SF Pro Display", 18), width=300, border_color=("#acb4b4", "#535b5b"))
            
            all_entry.append(edit_entry)
            ori_info = selected_info[item]
            edit_entry.insert(0,ori_info)
            
            for entry_index, entry in enumerate(all_entry):
                entry.bind("<KeyRelease>", lambda event, entry_index = entry_index: input_valid(event, entry_index))

            # label error text
            if item == "Last Name":
                error_text = "Please enter text without punctuation or number \n except a space"
            elif item == "Birth Date":
                error_text = ""
            else: 
                error_text = "Please enter text without punctuation or number"
            
            error_label = ctk.CTkLabel(edit_frame, text=error_text, font=my_font_mini, text_color=("#dbdbdb", "#2b2b2b"))
            all_label.append(error_label)
        
            key_label.grid(row=i*2, column=0, sticky=W, padx=(0,20))
            edit_entry.grid(row=i*2, column=1, sticky=W)            
            error_label.grid(row=(i*2)+1, column=1, pady=(0,8))
        # save and cancel button
        button_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", font=my_font_supersmall, command=user_profile)
        save_button = ctk.CTkButton(button_frame, text="Save", font=my_font_supersmall, command=save_info)
        
        button_frame.pack(side=BOTTOM, anchor=E, padx=5, pady=5)
        cancel_button.pack(side=RIGHT, padx=10, pady=15)
        save_button.pack(side=RIGHT, padx=10, pady=15)


    def input_valid(event, entry_index):
        global all_error
        input = str(all_entry[entry_index].get())
        
        if input != "":
            if entry_index in (0,1):
                regex = r'[\d!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}\~\\ ]' #punctuation and digits
            elif entry_index == 2:
                regex = r'[\d!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}\~\\]' #punctuation and digits except space

            if re.search(regex, input):
                all_entry[entry_index].configure(border_color="red")
                all_label[entry_index].configure(text_color="red")
                save_button.configure(state=DISABLED)
                if entry_index not in all_error:
                    all_error.append(entry_index)
            else:
                all_entry[entry_index].configure(border_color=("#acb4b4", "#535b5b"))
                all_label[entry_index].configure(text_color=("#dbdbdb", "#2b2b2b"))
                save_button.configure(state=NORMAL)
                if entry_index in all_error:
                    all_error.remove(entry_index)
        else:
            all_entry[entry_index].configure(border_color="red")
            if entry_index not in all_error:
                all_error.append(entry_index)

        if len(all_error) == 0:
            save_button.configure(state=NORMAL)
        else:
            save_button.configure(state=DISABLED)


    def save_info():
        global username
        new_info = []
        old_info = selected_info
        
        for entry in all_entry:
            info = entry.get()
            new_info.append(info)

        info_dic={
            "Username": new_info[0],
            "First Name": new_info[1],
            "Last Name": new_info[2],
            "Password": old_info["Password"],
            "Birth Date": new_info[3],
            "Study Hours": old_info["Study Hours"],
            "Total Run Time": old_info["Total Run Time"],
            "Email Address": old_info["Email Address"],
            "Admin": old_info["Admin"]
            }
        
        all_info.pop(user_index)
        all_info.insert(user_index, info_dic)

        # rewrite users.csv with new info list
        with open("users.csv", "w", newline="") as db:
            writer = csv.DictWriter(db, fieldnames=csv_header)
            writer.writeheader()
            for item in all_info:
                writer.writerow(item)
            db.close
            
        username = new_info[0]
        user_profile()

    # set up and display user's info
    info_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
    user_info = ctk.CTkFrame(info_frame, fg_color="transparent")

    info_frame.pack(side=TOP, anchor=W, expand=False, padx=25, pady=15)
    user_info.pack()

    for i, item in enumerate(key):
        info_label = ctk.CTkLabel(user_info, text=f"{item}:   {selected_info[item]}", font=("SF Pro Display", 18))
        info_label.grid(row=i*2, sticky=W, pady=(0,36))
    
    edit_button = ctk.CTkButton(profile_frame, text="Edit", font=my_font_supersmall, command=edit_profile)
    edit_button.pack(side=BOTTOM, anchor=E, padx=20, pady=20)



# create menu area
menu = ctk.CTkFrame(root, fg_color="transparent")
tittle_label = ctk.CTkLabel(menu, text="Stu.dying", font=my_font_medium)
logo_img = ctk.CTkImage(Image.open("./media/dark_mode/logo_dark.png"), size=(80,35))
logo = ctk.CTkLabel(menu, image=logo_img, text=" ")
user_icon = ctk.CTkImage(Image.open("./media/dark_mode/user_dark.png"), size=(40,40))
user_button = ctk.CTkButton(menu, image=user_icon, text="", fg_color="transparent", width=10, hover=False, command=logout)
feedback_icon = ctk.CTkImage(Image.open("./media/dark_mode/feedback_dark.png"), size=(40,38))
feedback_button = ctk.CTkButton(menu, image=feedback_icon, text="", fg_color="transparent", width=10, hover=FALSE, command=feedback)
notification_icon = ctk.CTkImage(Image.open("./media/dark_mode/notification_dark.png"), size=(40,40))
notification_button = ctk.CTkButton(menu, image=notification_icon, text="", fg_color="transparent", width=10, hover=FALSE, command=notification)

menu.pack(side=TOP, fill=X)
tittle_label.pack(side=LEFT, padx=(25,0), pady=12)
logo.pack(side=LEFT, padx=10)
user_button.pack(side=RIGHT, padx=(0,20))
feedback_button.pack(side=RIGHT, padx=(0,7), pady=(0,2))
notification_button.pack(side=RIGHT, pady=(1,0))

# create mode switcher
mode_frame = ctk.CTkFrame(menu, fg_color="transparent")
mode_switch = ctk.CTkSwitch(mode_frame, text=" ", width=10, command=change_mode)
mode_label = ctk.CTkLabel(mode_frame, text=ctk.get_appearance_mode() + " Mode", font=my_font_supersmall)

mode_frame.pack(side=RIGHT)
mode_switch.pack(side=RIGHT, padx=(10,0))
mode_label.pack(side=RIGHT)


# create to-do list area
todo_list = ctk.CTkFrame(root, width=450, border_width=2, border_color=("#acb4b4", "#535b5b"))
todo_list.pack(side=LEFT, padx=30, pady=(5,30), fill=BOTH)
todo_list.pack_propagate(False)
todolist()

middle_frame = ctk.CTkFrame(root, fg_color="transparent")
middle_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

# create dashboard area
dashboard_frame = ctk.CTkFrame(middle_frame, border_width=2, border_color=("#acb4b4", "#535b5b"))
dashboard_frame.pack(side=TOP, pady=(5,30), fill=BOTH, expand=TRUE)
dashboard()

# create leaderboard area
leaderboard_frame = ctk.CTkFrame(middle_frame, border_width=2, border_color=("#acb4b4", "#535b5b"))
leaderboard_frame.pack(side=TOP, pady=(0,30), fill=BOTH, expand=TRUE)
leaderboard()

#create user profile area
profile_frame = ctk.CTkFrame(root, width=460, border_width=2, border_color=("#acb4b4", "#535b5b"))
profile_frame.pack(side=LEFT, fill=BOTH, padx=30, pady=(5,30))
profile_frame.pack_propagate(False)

user = ctk.CTkLabel(profile_frame, text=username + "'s Profile", font=my_font_medium)
badges_frame = ctk.CTkFrame(profile_frame)

user.pack(side=TOP, anchor=W, padx=25, pady=20)
badges_frame.pack(side=TOP, anchor=W, fill='x', padx=20, pady=2)
badges()
user_profile()

root.protocol("WM_DELETE_WINDOW", on_close)



root.mainloop()