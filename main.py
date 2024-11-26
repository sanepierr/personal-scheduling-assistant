import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from matplotlib import pyplot as plt


# Task class to hold task details
class Task:
    def __init__(self, name, category, priority, deadline, duration):
        self.name = name
        self.category = category
        self.priority = priority
        self.deadline = deadline  # datetime object
        self.duration = duration  # in hours

    def __repr__(self):
        return (f"Task({self.name}, {self.category}, Priority={self.priority}, "
                f"Deadline={self.deadline}, Duration={self.duration})")


# Scheduler class with core functionalities
class Scheduler:
    def __init__(self):
        self.tasks = []  # List of Task objects

    def add_task(self, task):
        """Add a new task to the scheduler."""
        self.tasks.append(task)

    def remove_task(self, task_name):
        """Remove a task by its name."""
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def get_task_list(self):
        """Return a list of all tasks."""
        return self.tasks

    def display_gantt_chart(self):
        """Generate a Gantt chart for the scheduled tasks."""
        self.tasks.sort(key=lambda task: task.deadline)
        fig, ax = plt.subplots(figsize=(10, 5))
        current_time = datetime.datetime.now()
        for i, task in enumerate(self.tasks):
            start_time = max(current_time, task.deadline - datetime.timedelta(hours=task.duration))
            end_time = start_time + datetime.timedelta(hours=task.duration)
            ax.barh(i, (end_time - start_time).total_seconds() / 3600, left=start_time.timestamp(), color='skyblue')
            ax.text(start_time.timestamp(), i, task.name, va='center')
        ax.set_xlabel("Time")
        ax.set_yticks(range(len(self.tasks)))
        ax.set_yticklabels([task.name for task in self.tasks])
        plt.show()


# GUI Class for Tkinter application
class SchedulerApp:
    def __init__(self, root, scheduler):
        self.root = root
        self.scheduler = scheduler
        self.root.title("Task Scheduler")
        
        # Input fields
        tk.Label(root, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_combo = ttk.Combobox(root, values=["Personal", "Academic"], state="readonly")
        self.category_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Priority:").grid(row=2, column=0, padx=5, pady=5)
        self.priority_combo = ttk.Combobox(root, values=[1, 2, 3], state="readonly")
        self.priority_combo.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=3, column=0, padx=5, pady=5)
        self.deadline_entry = tk.Entry(root)
        self.deadline_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(root, text="Duration (hours):").grid(row=4, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(root, text="Remove Task", command=self.remove_task).grid(row=5, column=1, padx=5, pady=5)
        tk.Button(root, text="Show Gantt Chart", command=self.show_gantt_chart).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Task List
        tk.Label(root, text="Task List:").grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def add_task(self):
        """Add a new task based on user input."""
        name = self.name_entry.get()
        category = self.category_combo.get()
        priority = self.priority_combo.get()
        deadline = self.deadline_entry.get()
        duration = self.duration_entry.get()

        try:
            deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            duration = float(duration)
            priority = int(priority)
        except ValueError:
            messagebox.showerror("Input Error", "Please provide valid inputs for deadline and duration.")
            return

        if not (name and category and priority and deadline and duration):
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        task = Task(name, category, priority, deadline, duration)
        self.scheduler.add_task(task)
        self.refresh_task_list()
        messagebox.showinfo("Success", f"Task '{name}' added successfully!")

    def remove_task(self):
        """Remove the selected task from the list."""
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_name = selected_task.split(",")[0].split(":")[1].strip()
            self.scheduler.remove_task(task_name)
            self.refresh_task_list()
            messagebox.showinfo("Success", f"Task '{task_name}' removed successfully!")
        else:
            messagebox.showerror("Selection Error", "Please select a task to remove.")

    def refresh_task_list(self):
        """Refresh the task list display."""
        self.task_listbox.delete(0, tk.END)
        for task in self.scheduler.get_task_list():
            self.task_listbox.insert(tk.END, f"Name: {task.name}, Category: {task.category}, Priority: {task.priority}")

    def show_gantt_chart(self):
        """Display the Gantt chart for the tasks."""
        if not self.scheduler.get_task_list():
            messagebox.showerror("No Tasks", "No tasks available to display.")
            return
        self.scheduler.display_gantt_chart()


# Run the Tkinter application
if __name__ == "__main__":
    scheduler = Scheduler()
    root = tk.Tk()
    app = SchedulerApp(root, scheduler)
    root.mainloop()