import datetime
from typing import Callable

import model
import tkinter as tk


class TaskView(tk.Radiobutton):
    def __init__(self, master: tk.Frame | tk.Tk, task: model.Task, value: int, variable: tk.IntVar, *args, **kwargs):
        super().__init__(master, variable=variable, value=value, *args, **kwargs)

        self.master = master
        self.task = task

        self.update()

    def update(self):
        status = f'{self.task.due} {self.task.description} ({self.task.priority.name})'

        if self.task.complete:
            status += f'Completed ({self.task.completed_date})'

        self.config(text=status)


class TaskViewer(tk.Frame):
    def __init__(self, master: tk.Frame | tk.Tk, todo_list: model.ToDoList, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.todo_list = todo_list
        self.selected_task = tk.IntVar()
        self.selected_task.set(0)

        self.task_views: list[model.Task: TaskView] = []

        self.populate()

    def add_task(self, task):
        i = len(self.task_views)

        task_view = TaskView(self, task, value=i, variable=self.selected_task)

        self.task_views.append(task_view)

        task_view.grid(row=i)

    def remove_task_view(self, i):
        task_view = self.task_views.pop(i)
        task_view.destroy()
        return task_view

    def populate(self):
        for task in self.todo_list:
            self.add_task(task)

    def get_selection(self):
        i = self.selected_task.get()
        return i, self.task_views[i]

    def update_all_tasks(self):
        for task_view in self.task_views:
            task_view.update()


class ToDoViewTkInter(tk.Frame):
    def __init__(self, master: tk.Frame | tk.Tk, todo_list: model.ToDoList(), *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.todo_list = todo_list

        # Start by describing GUI

        self.title_label = tk.Label(self, text='ToDo')
        self.tasks_viewer = TaskViewer(self, self.todo_list)
        self.actions_frame = ActionsFrame(self)

        # And grid them

        self.title_label.grid()
        self.tasks_viewer.grid()
        self.actions_frame.grid()

    def update_tasks(self):
        self.tasks_viewer.update_all_tasks()

    def get_new_task(self):
        my_modal = NewTaskModal(self)
        return my_modal.get()


class NewTaskModal(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title('New task')

        self.description_stringvar = tk.StringVar()
        self.due_date_stringvar = tk.StringVar()
        self.priority_stringvar = tk.StringVar()

        self.description_label = tk.Label(self, text='Description')
        self.description_entry = tk.Entry(self, textvariable=self.description_stringvar)

        self.due_date_label = tk.Label(self, text='Due date')
        self.due_date_entry = tk.Entry(self, textvariable=self.due_date_stringvar)

        self.priority_label = tk.Label(self, text='Priority')
        self.priority_entry = tk.Entry(self, textvariable=self.priority_stringvar)

        self.ok_button = tk.Button(self, text='Submit', command=self.submit)

        # Layout

        self.description_label.grid(row=0, column=0)
        self.description_entry.grid(row=0, column=1)

        self.due_date_label.grid(row=1, column=0)
        self.due_date_entry.grid(row=1, column=1)

        self.priority_label.grid(row=2, column=0)
        self.priority_entry.grid(row=2, column=1)

        self.ok_button.grid(row=3)

    def get(self):
        self.wm_deiconify()
        self.description_entry.focus_force()
        self.wait_window()

        task = model.Task(
            description=self.description_stringvar.get(),
            due=datetime.datetime.strptime(self.due_date_stringvar.get(), model.DATEFORMAT).date(),
            priority=model.Priority(int(self.priority_stringvar.get()))
        )

        return task

    def submit(self):
        self.destroy()


class ActionsFrame(tk.Frame):
    def __init__(self, master: tk.Frame | tk.Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Describe our buttons

        self.add_button = tk.Button(self, text='Add')
        self.mark_complete_button = tk.Button(self, text='Complete')
        self.delete_button = tk.Button(self, text='Delete')
        self.load_button = tk.Button(self, text='Load')
        self.save_button = tk.Button(self, text='Save')

        # Place them

        self.add_button.grid(row=0, column=0)
        self.mark_complete_button.grid(row=0, column=1)
        self.delete_button.grid(row=0, column=2)
        self.load_button.grid(row=0, column=3)
        self.save_button.grid(row=0, column=4)
