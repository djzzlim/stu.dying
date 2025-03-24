import customtkinter as ctk
from tkinter import *
import subprocess

root = ctk.CTk()
root.title("Stu.dying")
ctk.set_appearance_mode("Dark")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

my_font_mini = ctk.CTkFont(family='SF Pro Display', size=12, weight='bold')
my_font_supersmall = ctk.CTkFont(family='SF Pro Display', size=15, weight='bold')
my_font_small = ctk.CTkFont(family='SF Pro Display', size=23, weight='bold')
my_font_medium = ctk.CTkFont(family='SF Pro Display', size=35, weight='bold')

todo_frame = None
def todolist():
    all_task = []
    all_label = {}
    all_no = {}
    todo = ctk.CTkToplevel(root)
    todo.title("Stu.dying")
    todo.grab_set()
    todo.resizable(0,0)
    x = int((width - 150) / 2)
    y = int((height - 650)/ 2)
    todo.geometry("450x600+{}+{}".format(x, y))

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
        if len(all_task) < 13:
            entry.configure(state=NORMAL)
        else:
            entry.configure(state=DISABLED)
        if todo_frame is not None:
            todo_frame.destroy()
        todo_frame = ctk.CTkFrame(todo, fg_color="transparent")
        todo_frame.pack(side=TOP, fill=X)
        for no, task in enumerate(all_task):
            all_no[no] = ctk.CTkLabel(todo_frame, text=f"{no+1}. ", font=my_font_supersmall)
            all_no[no].grid(row=no, column=0, sticky=W, padx=(15,5), pady=(5,0))
            all_label[no] = ctk.CTkLabel(todo_frame, text=task, font=my_font_supersmall)
            all_label[no].grid(row=no, column=1, sticky=W, pady=(5,0))
            all_label[no].bind("<Double-Button-1>", lambda event, no = no: edit(event, no))

    def edit(event, no):
        try:
            selected = str(event.widget.cget("text"))
            edit_entry = ctk.CTkEntry(todo_frame, font=my_font_supersmall, width=400)
            edit_entry.grid(row=no, column=1, sticky=W, pady=(5,0))
            edit_entry.insert(0, selected)
            edit_entry.focus_set()
            edit_entry.bind("<FocusOut>", lambda event: save(event, no))
            edit_entry.bind("<KeyPress>", lambda event: check(event, edit_entry))
            todo.bind("<Button-1>", lambda event: entry.focus_set()) 
        except (TclError, UnboundLocalError):
            pass

        def save(event, no):
            edit_task = edit_entry.get() 
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
        if text_width >= 370:
            while text_width >= 370:
                text = text[:-1] 
                text_width = my_font_supersmall.measure(text)
            widget.delete(0, END)
            widget.insert(0, text)
            widget.configure(border_color="red")
        else:
            widget.configure(border_color="#777")

    def pygame():
        todo.destroy()
        root.destroy()
        subprocess.run(["python", "game.py", *all_task])


    todolist = ctk.CTkLabel(todo, text="To-Do List", font=my_font_medium)
    todolist.pack(anchor=NW, padx=10, pady=5)
    done_button = ctk.CTkButton(todo, text="Done", font=my_font_supersmall, command=pygame)
    done_button.pack(side=BOTTOM, anchor=E, padx=10, pady=(0,10))
    entry = ctk.CTkEntry(todo, font=my_font_supersmall, height=40)
    entry.insert(0,"Task to be completed today (press enter to add)")
    entry.pack(side=BOTTOM, fill=X, padx=10, pady=10)
    entry.bind("<FocusIn>", on_enter)
    entry.bind("<FocusOut>", on_leave)
    entry.bind("<Return>", label_input)
    entry.bind("<KeyPress>", lambda event: check(event, entry))


todolist_button = ctk.CTkButton(root, text="to-do list", font=my_font_supersmall, command=todolist)
todolist_button.pack(expand=TRUE)


root.mainloop()