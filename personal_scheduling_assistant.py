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


