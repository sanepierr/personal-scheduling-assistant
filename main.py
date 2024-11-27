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
        self.tasks = self.quick_sort(self.tasks, key=lambda t: t.deadline)  # Keep tasks sorted by deadline

    def quick_sort(self, arr, key=lambda x: x):
        """Quick sort implementation for tasks."""
        if len(arr) <= 1:
            return arr
        pivot = key(arr[len(arr) // 2])
        left = [x for x in arr if key(x) < pivot]
        middle = [x for x in arr if key(x) == pivot]
        right = [x for x in arr if key(x) > pivot]
        return self.quick_sort(left, key) + middle + self.quick_sort(right, key)

    def binary_search(self, name):
        """Search for a task by name using binary search."""
        low, high = 0, len(self.tasks) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.tasks[mid].name == name:
                return mid
            elif self.tasks[mid].name < name:
                low = mid + 1
            else:
                high = mid - 1
        return -1  # Task not found

    def remove_task(self, task_name):
        """Remove a task by its name using binary search."""
        idx = self.binary_search(task_name)
        if idx != -1:
            self.tasks.pop(idx)

    def max_non_overlapping_tasks(self):
        """Use dynamic programming to find the maximum number of non-overlapping tasks."""
        n = len(self.tasks)
        if n == 0:
            return []
        self.tasks.sort(key=lambda task: task.deadline)
        
        dp = [0] * n
        dp[0] = 1
        prev = [-1] * n  # Store the previous index for traceback
        
        for i in range(1, n):
            include = 1
            for j in range(i - 1, -1, -1):
                if self.tasks[j].deadline + datetime.timedelta(hours=self.tasks[j].duration) <= self.tasks[i].deadline:
                    include += dp[j]
                    prev[i] = j
                    break
            dp[i] = max(dp[i - 1], include)
        
        selected_tasks = []
        i = n - 1
        while i >= 0:
            if prev[i] != -1 and dp[i] != dp[i - 1]:
                selected_tasks.append(self.tasks[i])
                i = prev[i]
            else:
                i -= 1

        return selected_tasks

    def get_task_list(self):
        """Return a list of all tasks."""
        return self.tasks

    def display_gantt_chart(self):
        """Generate a Gantt chart for the scheduled tasks."""
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
        tk.Button(root, text="Optimal Schedule", command=self.show_optimal_schedule).grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Task List
        tk.Label(root, text="Task List:").grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

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

    def show_optimal_schedule(self):
        """Display the optimal schedule using dynamic programming."""
        optimal_tasks = self.scheduler.max_non_overlapping_tasks()
        if not optimal_tasks:
            messagebox.showinfo("Optimal Schedule", "No non-overlapping tasks found.")
        else:
            messagebox.showinfo("Optimal Schedule", f"Optimal tasks: {[task.name for task in optimal_tasks]}")


# Run the application
if __name__ == "__main__":
    scheduler = Scheduler()
    root = tk.Tk()
    app = SchedulerApp(root, scheduler)
    root.mainloop()
