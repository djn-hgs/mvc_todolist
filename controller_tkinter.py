import datetime
import tkinter as tk
import model
import view_tkinter


class ToDoControllerTkInter:
    def __init__(self, todo_list: model.ToDoList, view: view_tkinter.ToDoViewTkInter):
        self.todo_list = todo_list
        self.view = view

        self.view.actions_frame.add_button.config(command=self.add_task)
        self.view.actions_frame.mark_complete_button.config(command=self.mark_complete)
        self.view.actions_frame.delete_button.config(command=self.del_task)

        self.view.actions_frame.load_button.config(command=self.load)
        self.view.actions_frame.save_button.config(command=self.save)

    def del_task(self):
        i, task_view = self.view.tasks_viewer.get_selection()

        if task_view:
            self.view.tasks_viewer.remove_task_view(i)
            self.todo_list.del_task(task_view.task)

    def mark_complete(self):
        i, task_view = self.view.tasks_viewer.get_selection()

        if task_view:
            self.todo_list.mark_task_complete(task_view.task)
            task_view.update()

    def add_task(self):
        task = self.view.get_new_task()

        print(task)

        self.todo_list.add_task(task)
        self.view.tasks_viewer.add_task(task)

    def save(self):
        self.todo_list.save()

    def load(self):
        self.todo_list.load()
        self.view.tasks_viewer.clear()
        self.view.tasks_viewer.populate()


if __name__ == '__main__':
    root = tk.Tk()

    todo_list = model.ToDoList()
    # todo_list.load()

    view = view_tkinter.ToDoViewTkInter(root, todo_list)

    controller = ToDoControllerTkInter(todo_list, view)

    view.grid()

    root.mainloop()
