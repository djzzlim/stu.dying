from tkinter import *
import customtkinter as ctk
from PIL import Image
import csv
from tkcalendar import DateEntry
import re
import json
import datetime
import sys
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# set up the window
root = ctk.CTk()
root.title("Stu.dying")
ctk.set_appearance_mode("dark")
admin_username = sys.argv[1]

# Maximize the window to cover the whole screen
try:
    root.attributes('-zoomed', True)
except:
    root.state('zoomed')

root.after(0, lambda: root.state('zoomed'))

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.minsize(width, height)
root.geometry(f"{width}x{height}+0+0")

# Set up the fonts
my_font_mini = ctk.CTkFont(family='SF Pro Display', size=12, weight='bold')
my_font_supersmall = ctk.CTkFont(family='SF Pro Display', size=15, weight='bold')
my_font_small = ctk.CTkFont(family='SF Pro Display', size=23, weight='bold')
my_font_medium = ctk.CTkFont(family='SF Pro Display', size=35, weight='bold')
my_font_large = ctk.CTkFont(family='SF Pro Display', size=40, weight='bold')


top=None
def change_mode():
    global top
    current_mode = ctk.get_appearance_mode()

    # change appearance mode and images
    if current_mode == "Light":
        ctk.set_appearance_mode("Dark")
        mode_label.configure(text="Dark Mode")
        logo_img = ctk.CTkImage(Image.open("./media/dark_mode/logo_dark.png"), size=(80,35))
        menu_button_icon = ctk.CTkImage(Image.open("./media/dark_mode/menu_dark.png"), size=(30,30))
        user_icon = ctk.CTkImage(Image.open("./media/dark_mode/user_dark.png"), size=(40,40))
    else:
        ctk.set_appearance_mode("Light")
        mode_label.configure(text="Light Mode")
        logo_img = ctk.CTkImage(Image.open("./media/light_mode/logo_light.png"), size=(80,35))
        menu_button_icon = ctk.CTkImage(Image.open("./media/light_mode/menu_light.png"), size=(30,30))
        user_icon = ctk.CTkImage(Image.open("./media/light_mode/user_light.png"), size=(40,40))
      
    logo.configure(image=logo_img)
    menu_button.configure(image=menu_button_icon)
    user_button.configure(image=user_icon)


i = 0
def toggle_navigation_pane():
    global i, navigation_pane 
    i += 1
    if i % 2 == 1: 
        navigation_pane = ctk.CTkFrame(root, fg_color="transparent", width=300)
        manage_user_button = ctk.CTkButton(navigation_pane, text="Manage User", font=my_font_small, width=280, command=manage_user)
        performance_button = ctk.CTkButton(navigation_pane, text="Performance", font=my_font_small, width=280, command=performance)
        maintenance_button = ctk.CTkButton(navigation_pane, text="Maintenance", font=my_font_small, width=280, command=maintenance)
        
        navigation_pane.pack(side="left", fill="y", expand=FALSE)
        manage_user_button.pack(padx=10, pady=20)
        performance_button.pack(padx=10)
        maintenance_button.pack(padx=10, pady=20)
    else:
        navigation_pane.destroy()
        i = 0


def clear_frame():
    global i 
    for widgets in content_frame.winfo_children():
      widgets.destroy()
    navigation_pane.destroy()
    i=0

# set up a search bar to search user
def manage_user():
    global search_frame, search_name 
    clear_frame()

    def on_enter(event):
        if search_name.get() == "Username":
            search_name.delete(0, END)

    def on_leave(event):
        if search_name.get() == '': 
            search_name.insert(0, "Username")

    search_frame = ctk.CTkFrame(content_frame)
    search_name = ctk.CTkEntry(search_frame, width=500, height=40, font=my_font_supersmall)

    search_frame.pack(padx=20, pady=20)
    search_name.insert(0, "Username")
    search_name.pack(side=TOP) 
    search_name.bind("<FocusIn>", on_enter)
    search_name.bind("<FocusOut>", on_leave)
    search_name.bind("<KeyRelease>", search_user)


# search and display users that match with input
filtered_frame = None 
info_frame = None
def search_user(event):
    global info_frame, filtered_frame 
    username_list = []
    filtered_list = []
    entered_name = search_name.get()

    # clear the info frame if exists
    if info_frame is not None:
        info_frame.destroy() 

    # destroy username that already packed
    if filtered_frame is not None:
        filtered_frame.destroy()

    filtered_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
    filtered_frame.pack()

    with open("users.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
            username_list.append(line["Username"])
    db.close

    # find users that match with input
    for item in username_list:
        if item.startswith(entered_name):
            filtered_list.append(item)

    # when there is no input
    if len(entered_name) == 0:
        filtered_list = []
        filtered_frame.destroy()
    # when there is username match with input
    elif len(filtered_list) == 0:
        notfound_label = ctk.CTkLabel(filtered_frame, text="User not found", font=my_font_supersmall)
        notfound_label.pack()
    else:
        # change the color of label when mouse hovered over it
        def button_enter(event):  
            try:
                event.widget.configure(foreground="#008FC9")
            except TclError:
                pass
        def button_leave(event):
            try:
                if ctk.get_appearance_mode() == "Light": 
                    event.widget.configure(foreground="Black")
                else:
                    event.widget.configure(foreground="White")
            except TclError:
                pass  
            
        # sort the list in A-Z form
        filtered_list.sort() 
        for filtered_username in filtered_list: 
            filtered_username = ctk.CTkLabel(filtered_frame, text=filtered_username, font=my_font_supersmall, width=500)
            filtered_username.pack(pady=3)
            filtered_username.bind("<Enter>", button_enter)
            filtered_username.bind("<Leave>", button_leave)
            filtered_username.bind("<Button-1>", get_name)


# get the username of the label cliked
def get_name(event):
    try: 
        selected_username = event.widget.cget("text") 
        search_name.delete(0, END) 
        content_frame.focus_set()
        filtered_frame.destroy()
        show_profile(selected_username)
    except TclError:
        pass


key = ["Username","First Name","Last Name","Birth Date","Study Hours","Email Address"]
def show_profile(selected_username):
    global info_frame, delete_button, edit_button, user_info, button_frame, hours, minutes
    username_list = []
    info = []

    if info_frame is not None:
        info_frame.destroy()

    #get all username and info from users.csv 
    with open("users.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
            username_list.append(line["Username"])
            info.append(line)
    db.close
    
    index = username_list.index(selected_username)
    selected = info[index] 
    info_frame = ctk.CTkFrame(content_frame, width=600, border_width=2, border_color=("#acb4b4", "#535b5b"))
    user_info = ctk.CTkFrame(info_frame, fg_color="transparent")

    info_frame.pack(side=TOP, fill=Y, expand=TRUE, pady=(10, 30))
    info_frame.pack_propagate(False)
    user_info.pack(anchor=W, padx=20, pady=20)

    #label and display selected user's info
    for key_index, item in enumerate(key):
        if item == "Study Hours":
            studyhours = int(selected["Study Hours"]) // 60
            hours, minutes = divmod(studyhours, 60)
            info_label = ctk.CTkLabel(user_info, text=f"{item}:  {hours} hours {minutes} minutes", font=my_font_supersmall)
        else: 
            info_label = ctk.CTkLabel(user_info, text=f"{item}:  {selected[item]}", font=my_font_supersmall)
        info_label.grid(row=key_index, sticky=W, padx=20, pady=10)

    button_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    edit_button = ctk.CTkButton(button_frame, text="Edit", font=my_font_supersmall, state=NORMAL,
                                 command=lambda: confirmation(selected_username, index, info, "Confirm to edit this profile?"))
    delete_button = ctk.CTkButton(button_frame, text="Delete", font=my_font_supersmall, state=NORMAL, 
                                  command=lambda: confirmation(selected_username, index, info, "Confirm to delete this profile?"))
    
    button_frame.pack(padx=5, pady=5, side=BOTTOM, anchor=E)
    edit_button.grid(sticky=E, row=0, column=0, padx=10, pady=10)
    delete_button.grid(sticky=E, row=0, column=1, padx=(0,10), pady=10)


# confirmation of administrator action
def confirmation(selected_username, index, info, prompt):
    global top 
    top = ctk.CTkToplevel(root)
    top.title("Stu.dying")
    top.grab_set()
    top.resizable(0,0)
    coordinate_x = int((width/2)-65)
    coordinate_y = int((height/2)-35)
    top.geometry("{}x{}+{}+{}".format(400,200,coordinate_x,coordinate_y))

    confirm_frame = ctk.CTkFrame(top, fg_color="transparent")
    confirm_label = ctk.CTkLabel(confirm_frame, text=prompt, font=my_font_supersmall)

    if prompt == "Confirm to delete this profile?":
        confirm_button = ctk.CTkButton(confirm_frame, text="Confirm", font=my_font_supersmall, command=lambda: delete_profile(index, info))
    else:
        confirm_button = ctk.CTkButton(confirm_frame, text="Confirm", font=my_font_supersmall, command=lambda: edit_profile(selected_username, index, info))
    
    cancel_button = ctk.CTkButton(confirm_frame, text="Cancel", font=my_font_supersmall, command=top.destroy)

    confirm_frame.pack(expand=TRUE)
    confirm_label.pack()
    confirm_button.pack(pady=2)
    cancel_button.pack()

    top.protocol("WM_DELETE_WINDOW", top.destroy) 


def edit_profile(selected_username, index, info): 
    global edit_frame, save_button, all_entry
    all_entry = []
    user_info.destroy()
    
    for widgets in button_frame.winfo_children():
      widgets.destroy()
    top.destroy()
    selected = info[index]

    edit_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
    edit_frame.pack(anchor=W, padx=20, pady=20)
  
    # set up entry index to edit info
    for i, item in enumerate(key): 
        grid_index = i * 2 
        key_label = ctk.CTkLabel(edit_frame, text=f"{item}:  ", font=my_font_supersmall)
        key_label.grid(row=grid_index, column = 0, sticky=W, padx=20, pady=10) 

        if item == "Birth Date":
            edit_entry = DateEntry(edit_frame, font=my_font_small, width=27, border_color=("#acb4b4", "#535b5b"), date_pattern="dd-mm-yyyy", state="readonly")
            edit_entry.grid(row=grid_index, column=1, columnspan=4)
            all_entry.append(edit_entry) 
        elif item == "Study Hours": 
            edit_entry1 = ctk.CTkEntry(edit_frame, font=my_font_supersmall, width=115, border_color=("#acb4b4", "#535b5b")) 
            edit_label1 = ctk.CTkLabel(edit_frame, text="hours", font=my_font_supersmall)
            edit_entry2 = ctk.CTkEntry(edit_frame, font=my_font_supersmall, width=115, border_color=("#acb4b4", "#535b5b")) 
            edit_label2 = ctk.CTkLabel(edit_frame, text="minutes", font=my_font_supersmall)

            edit_entry1.grid(row=grid_index, column=1, sticky=W)
            edit_label1.grid(row=grid_index, column=2, sticky=W)
            edit_entry2.grid(row=grid_index, column=3, sticky=W)
            edit_label2.grid(row=grid_index, column=4, sticky=W)
            all_entry.append(edit_entry1)
            all_entry.append(edit_entry2)  
            
            edit_entry1.insert(0, hours)
            edit_entry2.insert(0, minutes)
        else: 
            edit_entry = ctk.CTkEntry(edit_frame, font=my_font_supersmall, width=350, border_color=("#acb4b4", "#535b5b"))
            edit_entry.grid(row=grid_index, column=1, columnspan=4)
            all_entry.append(edit_entry) 
            ori_info = selected[item]
            edit_entry.insert(0, ori_info)

    for entry_index, entry in enumerate(all_entry): 
        entry.bind("<KeyRelease>", lambda event, entry_index = entry_index: input_valid(event, entry_index)) 

    save_button = ctk.CTkButton(button_frame, text="Save", font=my_font_supersmall, command=lambda: save_info(selected_username, index, info))
    cancel_button = ctk.CTkButton(button_frame, text="Cancel", font=my_font_supersmall, command=lambda: show_profile(selected_username))

    save_button.grid(sticky=E, row=0, column=0, padx=10, pady=10)
    cancel_button.grid(sticky=E, row=0, column=1, padx=(0,10), pady=10)


labels = {} 
def input_valid(event, entry_index):
    global labels
    input = str(all_entry[entry_index].get())
  
    # label reminder when input is unacceptable
    def error(entry_index, error_text):
        all_entry[entry_index].configure(border_color="red")

        if entry_index not in labels: 
            if entry_index in (4,5):
                if entry_index == 4:
                    label_column = 1
                else:
                    label_column = 3
                labels[entry_index] = ctk.CTkLabel(edit_frame, text=error_text, font=my_font_mini, height=2, text_color="red")
                labels[entry_index].grid(row=9, column=label_column, columnspan=2, sticky=W)
            else:
                labels[entry_index] = ctk.CTkLabel(edit_frame, text=error_text, font=my_font_mini, height=2, text_color="red")
                labels[entry_index].grid(row=(entry_index * 2) + 1, column=1, columnspan=4)
        else:
            labels[entry_index].configure(text=error_text)

    def normal(entry_index): 
        if entry_index in labels: 
            labels[entry_index].destroy()
            del labels[entry_index] 
            all_entry[entry_index].configure(border_color=("#acb4b4", "#535b5b"))

    if input == "":
        error_text = "Pleaese don't leave it blank"
        error(entry_index, error_text)
    else:
        normal(entry_index)

      # set up the unacceptable value and error text for different info
        if entry_index in (0,1,2,4,5):
            if entry_index in (0,1): 
                regex = r'[\d!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}\~\\ ]' # punctuation and digits
                error_text = "Please enter text without punctuation or number"
            elif entry_index == 2: 
                regex = r'[\d!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}\~\\]' # punctuation and digits except space
                error_text = "Please enter text without punctuation or number except a space"
            elif entry_index in (4,5): 
                regex = r'[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}\~\\ a-zA-Z]' # punctuation and alphabet
                error_text = "Please enter a valid number"

            # search for unacceptable value in input
            if re.search(regex, input):
                error(entry_index, error_text)
            else: 
                normal(entry_index)
                            
        elif entry_index == 6:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' # email format
            error_text = "Please enter a valid email"
          
            # match the input with email format
            if not re.match(regex, input): 
                error(entry_index, error_text)
            else: 
                normal(entry_index)

    if len(labels) == 0:
        save_button.configure(state=NORMAL)
    else:
        save_button.configure(state=DISABLED)


csv_header = ["Username","First Name","Last Name","Password","Birth Date","Study Hours","Total Run Time","Email Address","Admin"] 
def save_info(selected_username, index, info):
    new_info = []
    old_info = info[index]

    for entry in all_entry:
        text = entry.get()
        new_info.append(text)

    # change hours and minutes to secods
    study_hours = (int(new_info[4])*3600) + (int(new_info[5])*60)

    info_dic = {
        "Username": new_info[0],
        "First Name": new_info[1],
        "Last Name": new_info[2],
        "Password": old_info["Password"],
        "Birth Date": new_info[3],
        "Study Hours": study_hours,
        "Total Run Time": old_info["Total Run Time"],
        "Email Address": new_info[6],
        "Admin": old_info["Admin"]
        }
    
    info.pop(index)
    info.insert(index, info_dic)

    # rewrite users.csv with new info list
    with open("users.csv", "w", newline="") as db:
        writer = csv.DictWriter(db, fieldnames=csv_header)
        writer.writeheader()
        for item in info:
            writer.writerow(item)
        db.close

    selected_username = new_info[0]
    show_profile(selected_username)



def delete_profile(index,info):
    top.destroy()
    info.pop(index)

    # rewrite user.csv with info list that already deleted selected info
    with open("users.csv", "w", newline="") as db:
        writer = csv.DictWriter(db, fieldnames=csv_header)
        writer.writeheader()
        for item in info:
            writer.writerow(item)
        db.close

    info_frame.destroy()


def performance():
    clear_frame()

    # Lists to store usernames and total run times
    all_username = []
    all_total_run_time = []

    # Read data from the "users.csv" file
    with open("users.csv") as db:
        reader = csv.DictReader(db)
        for line in reader:
          if line["Admin"] == "False":
            # Append usernames and total run times to the respective lists
            all_username.append(line["Username"])
            all_total_run_time.append(int(line["Total Run Time"]))

    # Sort the indices based on total run times in descending order
    sorted_indices = sorted(range(len(all_total_run_time)), key=lambda k: all_total_run_time[k], reverse=True)
    # Create sorted lists based on the sorted indices
    sorted_username = [all_username[i] for i in sorted_indices]
    sorted_total_run_time = [all_total_run_time[i] for i in sorted_indices]

    # Create a new frame to hold the performance graph
    graph_frame = ctk.CTkFrame(content_frame)
    graph_frame.pack(expand=True, padx=20, pady=20)

    performance_label = ctk.CTkLabel(graph_frame, text="User Performance", font=my_font_medium)
    performance_label.pack(pady=(10, 0))

    # Create the user performance graph using a bar chart
    plt.style.use("fivethirtyeight")
    figure = plt.figure(figsize=(10, 6))
    plt.bar(sorted_username, sorted_total_run_time, color="#444444")
    plt.title("Total Run Time")
    plt.xlabel("Username")
    plt.ylabel("Time (seconds)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Create a tkinter canvas and draw the graph on it
    canvas = FigureCanvasTkAgg(figure, master=graph_frame)
    canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
    canvas.draw()


def on_close():
    exit()


def maintenance():
    clear_frame()

    # adding scrollbar
    canvas = ctk.CTkCanvas(content_frame, highlightthickness=0)  
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = ctk.CTkScrollbar(content_frame, command=canvas.yview) 
    scrollbar.pack(side=RIGHT, fill=Y)

    # notify scrollbar when it scrolls
    canvas.configure(yscrollcommand=scrollbar.set)  

    maintenance_frame = ctk.CTkFrame(canvas, corner_radius=0)
    canvas.create_window((0, 0), window=maintenance_frame, anchor="nw", tags="maintenance_frame")  
    maintenance_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  
    canvas.bind('<Configure>', canvas.itemconfig('maintenance_frame', width=canvas.winfo_width()))  
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    # admin announcement
    announcement_label = ctk.CTkLabel(maintenance_frame, text="Announcement", font=my_font_large)
    announcement_box = ctk.CTkTextbox(maintenance_frame, bg_color="transparent", border_color=("#acb4b4", "#535b5b"),
                                      border_width=2, width=800, height=180, font=("Arial", 16), wrap="word")
    publish_btn = ctk.CTkButton(maintenance_frame, text="Publish", width=80, text_color="white", fg_color="grey",
                                command=lambda: publish(announcement_box, maintenance_frame))

    announcement_label.grid(row=0, column=0, padx=200, pady=20, sticky="ew")
    announcement_box.grid(row=1, column=0, padx=50, pady=20, sticky="ew")
    publish_btn.grid(row=3, column=0, padx=65, sticky="e")

    maintenance_frame.columnconfigure(0, weight=1)

    # admin feedback
    admin_fb_heading = ctk.CTkLabel(maintenance_frame, text="Feedback", font=my_font_large)
    admin_fb_frame = ctk.CTkFrame(maintenance_frame, border_width=2, border_color=("#acb4b4", "#535b5b"), height=50)
    username_frame = ctk.CTkFrame(admin_fb_frame, border_color=("#acb4b4", "#535b5b"), fg_color=("#cfcfcf", "#333333"))
    fb_details_frame = ctk.CTkFrame(admin_fb_frame, fg_color=("#cfcfcf", "#333333"))

    admin_fb_heading.grid(row=4, column=0, padx=200, pady=20, sticky="ew")
    admin_fb_frame.grid(row=5, column=0, padx=50, pady=30, sticky="ew")
    username_frame.grid(row=0, column=0, sticky="ns", padx=2, pady=2)
    fb_details_frame.grid(row=0, column=1, padx=150, pady=30, sticky="nsew")

    admin_fb_frame.columnconfigure(1, weight=1)

    admin_feedback(username_frame, fb_details_frame)


def publish(announcement_box, maintenance_frame):
    announcement_text = announcement_box.get("1.0", "end-1c")
    no_announcement = ctk.CTkLabel(maintenance_frame, text="This field is required.", font=my_font_mini,
                                   text_color="red")
    no_announcement.grid(row=3, column=0, sticky="w", padx=50)  

    # check if there is input in announcement box
    if announcement_text == "": # no input
        announcement_box.configure(border_color=("red", "dark red"))
    else:
        if no_announcement is not None:  # got input
            announcement_box.configure(border_color=("#acb4b4", "#535b5b"))
            no_announcement.configure(text_color=("#dbdbdb", "#2b2b2b")) 

        date_text = str(date.strftime("%d/%m/%Y"))
        announcement = [{
            "Admin": admin_username,
            "Announcement": announcement_text,
            "Date": date_text
        }]

        # add new announcement to json file
        with open("announcement.json", "r") as announcement_file:  # read old announcement
          data = json.load(announcement_file)  
          data.append(announcement[0])  
        with open("announcement.json", "w") as announcement_file: # update announcement file
            json.dump(data, announcement_file, indent=4)  

        announcement_box.delete("1.0", "end") # clear announcement box

 
def admin_feedback(username_frame, fb_details_frame):
    # adding scrollbar
    fb_canvas = ctk.CTkCanvas(username_frame, highlightthickness=0, height=630)  
    fb_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = ctk.CTkScrollbar(username_frame, command=fb_canvas.yview) 
    scrollbar.pack(side=RIGHT, fill=Y)

    fb_canvas.configure(yscrollcommand=scrollbar.set)  
  
    fb_canvas_frame = ctk.CTkFrame(fb_canvas, corner_radius=0)
    fb_canvas.create_window((0, 0), window=fb_canvas_frame, anchor="nw", tags="fb_canvas_frame")  
    fb_canvas_frame.bind('<Configure>', lambda e: fb_canvas.configure(scrollregion=fb_canvas.bbox("all")))  
    fb_canvas.bind('<Configure>', fb_canvas.itemconfig('fb_canvas_frame', width=fb_canvas.winfo_width()))

    # create new feedback buttons
    with open("feedback.json", "r") as data_file:
        data = json.load(data_file)  
        data.reverse()
        for i in data:
            new_feedback = ctk.CTkButton(fb_canvas_frame, text=i['Username'], font=my_font_supersmall, fg_color="grey", border_width=1, border_color=("#acb4b4", "#535b5b"), corner_radius=0, command=lambda x=i: display_details(fb_details_frame, new_feedback, x))
            new_feedback.pack(side="top", fill="x", ipadx=100, ipady=10)
            
    details_label = ctk.CTkLabel(fb_details_frame, text="Click the username buttons to view their feedbacks", justify='center', text_color="grey")
    details_label.grid(row=0, column=0, pady=50, sticky='ew')
    fb_details_frame.columnconfigure(0, weight=1) 


def display_details(fb_details_frame, new_feedback, x):
   # clear frame
    for widget in fb_details_frame.winfo_children():
        widget.destroy()

    # display feedback details
    username = ctk.CTkLabel(fb_details_frame, text=x['Username'], font=my_font_small)
    ratings = ctk.CTkLabel(fb_details_frame, text=x['Ratings'], font=('SF Pro Display', 14), text_color='grey')
    radio_value = ctk.CTkLabel(fb_details_frame, text=x['Radio value'], font=('SF Pro Display', 16))
    comments = ctk.CTkLabel(fb_details_frame, text=x['Comments'], font=('SF Pro Display', 16), wraplength=600, justify='left')
    date_time = ctk.CTkLabel(fb_details_frame, text=x['DateTime'], font=('SF Pro Display', 12), text_color='grey')
    back_btn = ctk.CTkButton(fb_details_frame, text='Back', command=lambda: back(fb_details_frame))

    username.grid(row=0, column=0, columnspan=3, pady=5, sticky='w')
    ratings.grid(row=1, column=0, columnspan=3, pady=5, sticky='w')
    radio_value.grid(row=2, column=0, columnspan=3, ipady=20, sticky='w')
    comments.grid(row=3, column=0, columnspan=3, ipady=20, sticky='w')
    date_time.grid(row=4, column=0, columnspan=3, pady=5, sticky='w')
    back_btn.grid(row=5, column=1, padx=5, sticky='se')
    fb_details_frame.columnconfigure(0, weight=1)
    fb_details_frame.rowconfigure(5, weight=1)


def back(fb_details_frame):
    for widget in fb_details_frame.winfo_children():
        widget.destroy()
 
    details_label = ctk.CTkLabel(fb_details_frame, text="Click the username buttons to view their feedbacks", justify='center', text_color="grey")
    details_label.grid(row=0, column=0, pady=50)


# confirmation of administrator action
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
      
        # back to login page
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


date = datetime.datetime.now()


# create menu area
menu_frame = ctk.CTkFrame(root, fg_color="transparent")
menu_button_icon = ctk.CTkImage(Image.open("./media/dark_mode/menu_dark.png"), size=(30, 30))     #here
menu_button = ctk.CTkButton(menu_frame, text=" ", image=menu_button_icon, command=toggle_navigation_pane, fg_color="transparent", width=10, hover=FALSE)
tittle_label = ctk.CTkLabel(menu_frame, text="Stu.dying", font=my_font_medium)

menu_frame.pack(side="top", fill="x")
logo_img = ctk.CTkImage(Image.open("./media/dark_mode/logo_dark.png"), size=(80,35))     #here
logo = ctk.CTkLabel(menu_frame, image=logo_img, text=" ")
menu_button.pack(side=LEFT, pady=12, padx=(10,0))
tittle_label.pack(side=LEFT)
logo.pack(side=LEFT, padx=5)


# create mode switch and logout button
user_icon = ctk.CTkImage(Image.open("./media/dark_mode/user_dark.png"), size=(40,40))
user_button = ctk.CTkButton(menu_frame, image=user_icon, text="", fg_color="transparent", width=10, hover=False, command=logout)
mode_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
mode_switch = ctk.CTkSwitch(mode_frame, text=" ", command=change_mode, width=10)
mode_label = ctk.CTkLabel(mode_frame, text=ctk.get_appearance_mode() + " Mode", font=my_font_supersmall)

user_button.pack(side=RIGHT, padx=(0,10))
mode_frame.pack(side=RIGHT)
mode_switch.pack(side=RIGHT, padx=(10,0))
mode_label.pack(side=RIGHT)


# create main content area
content_frame = ctk.CTkFrame(root)
content_frame.pack(side=RIGHT, fill="both", expand=TRUE)


root.protocol("WM_DELETE_WINDOW", on_close)



root.mainloop()