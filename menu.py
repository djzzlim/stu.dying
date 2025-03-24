# Import necessary libraries
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import ctypes
import time
from time import strftime

# Start timing the script
start_time = time.time()

# Create the main root window using customtkinter
root = ctk.CTk()
ctk.set_appearance_mode("dark")

# Maximize the window to cover the whole screen
root.after(0, lambda: root.state('zoomed'))

# Get the screen resolution to set the window size
width1 = root.winfo_screenwidth()
height1 = root.winfo_screenheight()

# Set the minimum and current window size
root.minsize(width1, height1)
root.geometry(f"{width1}x{height1}+0+0")

# Create a canvas to hold the video
canvas = ctk.CTkCanvas(root, width=width1, height=height1, bd=0, highlightthickness=0)
canvas.pack(side="right", expand=True, fill="both", anchor="center")

# Load the video and extract frames
try:
    # Get the screen resolution using ctypes.windll.user32 on Windows
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
except:
    # Get the screen resolution using X11 library on Linux
    x11 = ctypes.cdll.LoadLibrary('libX11.so')
    display = x11.XOpenDisplay(None)
    root = x11.XDefaultRootWindow(display)
    width = x11.XDisplayWidth(display, x11.XDefaultScreen(display))
    height = x11.XDisplayHeight(display, x11.XDefaultScreen(display))
    x11.XCloseDisplay(display)
    screensize = (width, height)

# Open the video file
cap = cv2.VideoCapture('./media/room2.mp4')
frames = []

# Extract each frame from the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, screensize, interpolation=cv2.INTER_LANCZOS4)
    frames.append(ImageTk.PhotoImage(Image.fromarray(frame)))

# Display the frames on the canvas in a loop
def play_video(index):
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=frames[index])
    root.after(40, play_video, (index + 1) % len(frames))

play_video(0)

def change_appearance_mode_event(event):
    ctk.set_appearance_mode(event)

def pomodoro_timer():
    pass

def nowtime():
    a=strftime("%#I : %M %p")
    l1.configure(text=a)
    l1.after(1000,nowtime)

# Create a CTkFont instance using your custom font
my_font_supersmall = ctk.CTkFont(family='SF Pro Display', size=15, weight='bold')
my_font_small = ctk.CTkFont(family='SF Pro Display', size=23, weight='bold')
my_font_medium = ctk.CTkFont(family='SF Pro Display', size=30, weight='bold')


#navigation panel
i = 0
def toggle_navigation_pane(event):
    global i, navigation_panel
    i += 1
    if i % 2 == 1:
        current_appearance = ctk.get_appearance_mode()
        navigation_panel = ctk.CTkFrame(root, width=150)
        navigation_pane_label = ctk.CTkLabel(navigation_panel, text='Stu.dying', font=my_font_medium)
        navigation_pane_label.pack(side="top", ipadx=20, ipady=20)
        leaderboard_button = ctk.CTkButton(navigation_panel, text='Leaderboard', font=my_font_small)
        leaderboard_button.pack(side="top", ipadx=20, pady=40, padx=10)
        appearance_mode_optionemenu = ctk.CTkOptionMenu(navigation_panel, values=["Light", "Dark", "System"],
                                                                            command=change_appearance_mode_event, font=my_font_supersmall)
        appearance_mode_optionemenu.set(current_appearance)
        appearance_mode_optionemenu.pack(side="bottom", ipadx=20, pady=40, padx=10)
        navigation_panel.pack(side='left', fill='y', ipadx=20, ipady=20)
        navigation_panel.lift()
        menu.place(anchor="nw", x=250)

    else:
        navigation_panel.destroy()
        menu.place(anchor="nw", x=10)


#time panel
l1=ctk.CTkLabel(root, font=("Agency FB", 80, 'bold'), padx=15, pady=8, anchor="center")
l1.lift()
l1.place(relx=1, rely=0, anchor='ne')
nowtime()

#Menu button
menu_button_image = ctk.CTkImage(Image.open("./media/menu-button.png"), size=(26, 26))
menu = ctk.CTkButton(root, image=menu_button_image, text='', width=10)
menu.bind("<Button-1>", toggle_navigation_pane)
menu.place(anchor="nw", x=10, y=5)

# End timing the script and print the elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)

# Start the main event loop
root.mainloop()
