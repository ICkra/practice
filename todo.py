import json
import tkinter as tk

# Load saved tasks and history from a JSON file
try:
    with open("task_manager.json", "r") as f:
        data = json.load(f)
        tasks = data["tasks"]
        completed_tasks = data["completed_tasks"]
        deleted_tasks = data["deleted_tasks"]
except FileNotFoundError:
    tasks = []
    completed_tasks = []
    deleted_tasks = []

# Function for saving tasks and history to a JSON file
def Save_Data():
    data = {"tasks": tasks, "completed_tasks": completed_tasks, "deleted_tasks": deleted_tasks}
    with open("task_manager.json", "w") as f:
        json.dump(data, f)

# Function for adding a new task
def Add_Task():
    task_name = task_entry.get()
    if task_name == "":
        return
    task_id = len(tasks) + 1
    task = {"task_id": task_id, "name": task_name, "status": "pending"}
    tasks.append(task)
    Save_Data()
    task_listbox.insert(tk.END, f"{task_name}")
    task_entry.delete(0, tk.END)

# Function for marking a task as done
def Done_Task():
    task_index = task_listbox.curselection()[0]
    task = tasks[task_index]
    task["status"] = "completed"
    completed_tasks.append(task)
    tasks.remove(task)
    Save_Data()
    status_label.config(text="Task was marked as done")
    task_listbox.delete(task_index)

# Function for deleting a task
def Delete_Task():
    task_index = task_listbox.curselection()[0]
    task = tasks[task_index]
    task["status"] = "deleted"
    deleted_tasks.append(task)
    tasks.remove(task)
    Save_Data()
    status_label.config(text="Task was deleted")
    task_listbox.delete(task_index)

# Function for showing last 10 completed and deleted tasks
def History_Data():
    # Hide/show listboxes
    if completed_listbox.winfo_ismapped() or deleted_listbox.winfo_ismapped():
        completed_listbox.grid_remove()
        deleted_listbox.grid_remove()
    else:
        completed_listbox.grid(row=10, column=0, padx=5, pady=7, sticky="w")
        deleted_listbox.grid(row=10, column=1, padx=5, pady=7, sticky="w")
    
    # Print last 10 completed tasks
    completed_listbox.delete(0, tk.END)
    completed_listbox.insert(0, "Completed tasks:")
    for task in completed_tasks[-10:]:
        completed_listbox.insert(tk.END, f"{task['name']}")
   
    # Print last 10 deleted tasks
    deleted_listbox.delete(0, tk.END)
    deleted_listbox.insert(0, "Deleted tasks:")
    for task in deleted_tasks[-10:]:
        deleted_listbox.insert(tk.END, f"{task['name']}")

# Function for showing current tasks
def Show_Tasks():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, f"{task['name']}")

# Create the main window
root = tk.Tk()
root.title("Task Manager")
root.minsize(400,300)
root.configure(bg="#edebeb")
root.columnconfigure(0, weight=1, minsize=75)
root.rowconfigure(list(range(1, 4)), weight=1, minsize=50)

# Create the widgets
task_label = tk.Label(root, background="#edebeb", text="Task name:")
task_entry = tk.Entry(root, width=30)
add_button = tk.Button(root, text="Add", background="white", command=Add_Task)
task_listbox = tk.Listbox(root, height=10, width=50, foreground="white", background="#666666")
done_button = tk.Button(root, text="Mark as done", height=1, width=12,background="white", command=Done_Task)
delete_button = tk.Button(root, text="Delete", height=1, width=12,background="white", command=Delete_Task)
status_label = tk.Label(root, text="", background="#edebeb", wraplength=100)
history_button = tk.Button(root, text="Show history", height=1, width=12, background="white", command=History_Data)
completed_listbox = tk.Listbox(root, height=11, width=30)
deleted_listbox = tk.Listbox(root, height=11, width=30)

# Add the widgets to the main window
task_label.grid(row=0, column=0, pady=5)
task_entry.grid(row=0, column=1, pady=5, ipady=2)
add_button.grid(row=0, column=2, padx = 15, pady=5, ipadx=5, ipady=2)
task_listbox.grid(row=1, column=0, padx=5, pady=5, columnspan=3, rowspan=6, sticky="nsew")
done_button.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
delete_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
status_label.grid(row=0, column=3, padx=5, pady=7)
history_button.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

Show_Tasks()

root.mainloop()
