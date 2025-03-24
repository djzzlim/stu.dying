import customtkinter as ctk
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = ""

def worktime(value):
    global WORK_MIN
    WORK_MIN = value
    work_timer_text.configure(text=f"{int(WORK_MIN)}:00")

def resttime1(value):
    global SHORT_BREAK_MIN
    SHORT_BREAK_MIN = value
    rest_timer_text1.configure(text=f"{int(SHORT_BREAK_MIN)}:00")

def resttime2(value):
    global LONG_BREAK_MIN
    LONG_BREAK_MIN = value
    rest_timer_text2.configure(text=f"{int(LONG_BREAK_MIN)}:00")

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    timer_text.configure(text="00:00")
    title_label.configure(text="Timer", text_color = 'white')
    check_marks.configure(text="")
    start_button.configure(state = 'normal')
    work_slider.configure(state = 'normal')
    rest_slider1.configure(state = 'normal')
    rest_slider2.configure(state = 'normal')
    reset_button.configure(state='disabled')
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    start_button.configure(state = 'disabled')
    work_slider.configure(state = 'disabled')
    rest_slider1.configure(state = 'disabled')
    rest_slider2.configure(state = 'disabled')
    reset_button.configure(state='normal')

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.configure(text="Break", text_color=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.configure(text="Break", text_color=PINK)
    else:
        count_down(work_sec)
        title_label.configure(text="Work", text_color=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    count_min = int(count_min)
    count_sec = int(count_sec)
    if count_sec < 10:
        count_sec = "0" + str(count_sec)

    timer_text.configure(text=f"{int(count_min)}:{str(count_sec).format('zfill(2)')}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.configure(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = ctk.CTk()
window.title("Pomodoro Timer")
window.attributes("-topmost", True)  # Set window to stay on top
window.config(padx=50, pady=25)

# Update the window to calculate its size
window.update_idletasks()

# Calculate the window position
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) // 2
y = (window.winfo_screenheight() - window.winfo_reqheight()) // 2

# Set the window position
window.geometry(f"+{x}+{y}")

window.resizable(False, False)

title_label = ctk.CTkLabel(window, text="Timer", font=(FONT_NAME, 35, "bold"))
title_label.grid(column=1, row=0)

timer_text = ctk.CTkLabel(window, text="00:00", font=(FONT_NAME, 15))
timer_text.grid(column=1, row=1)

work_text = ctk.CTkLabel(window, text="Work", font=(FONT_NAME, 15))
work_slider = ctk.CTkSlider(window, from_=10, to=100, command=worktime, number_of_steps=90)
work_slider.set(WORK_MIN)
work_timer_text = ctk.CTkLabel(window, text=f"{WORK_MIN}:00", font=(FONT_NAME, 15))
work_text.grid(column=0, row=2, pady=10)
work_slider.grid(column=1, row=2, pady=10)
work_timer_text.grid(column=2, row=2, pady=10)

rest_text1 = ctk.CTkLabel(window, text="Short Rest", font=(FONT_NAME, 15))
rest_slider1 = ctk.CTkSlider(window, from_=5, to=100, command=resttime1, number_of_steps=95)
rest_slider1.set(SHORT_BREAK_MIN)
rest_timer_text1 = ctk.CTkLabel(window, text=f"{SHORT_BREAK_MIN}:00", font=(FONT_NAME, 15))
rest_text1.grid(column=0, row=3, pady=10)
rest_slider1.grid(column=1, row=3, pady=10)
rest_timer_text1.grid(column=2, row=3, pady=10)

rest_text2 = ctk.CTkLabel(window, text="Long Rest", font=(FONT_NAME, 15))
rest_slider2 = ctk.CTkSlider(window, from_=5, to=100, command=resttime2, number_of_steps=95)
rest_slider2.set(LONG_BREAK_MIN)
rest_timer_text2 = ctk.CTkLabel(window, text=f"{LONG_BREAK_MIN}:00", font=(FONT_NAME, 15))
rest_text2.grid(column=0, row=4, pady=10)
rest_slider2.grid(column=1, row=4, pady=10)
rest_timer_text2.grid(column=2, row=4, pady=10)

start_button = ctk.CTkButton(window, text="Start", command=start_timer)
start_button.grid(column=0, row=5)

reset_button = ctk.CTkButton(window, text="Reset", command=reset_timer)
reset_button.configure(state='disabled')
reset_button.grid(column=2, row=5)

check_marks = ctk.CTkLabel(window, font=(FONT_NAME, 15), text='')
check_marks.grid(column=1, row=6)

window.mainloop()
