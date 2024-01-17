import datetime
import model


class ToDoController:
    def __init__(self, todo_list: model.ToDoList):
        self.todo_list = todo_list

    def play(self):
        while True:
            self.show()

            print('''
                (0) Add Task
                (1) Mark Task Complete
                (2) Delete Task
                (3) Load
                (4) Save
                ''')

            choice = int(input('Make a choice: '))

            if choice == 0:
                self.add_task()

            elif choice == 1:
                self.mark_task_complete()

            elif choice == 2:
                self.delete_task()

            elif choice == 3:
                self.load_list()

            elif choice == 4:
                self.save_list()

    def show(self):
        for i, task in enumerate(self.todo_list.get_tasks()):
            print(f'({i}) - {task}')

    def show_priorities(self):
        for i in model.PRIORITIES:
            print(f'({i}) {model.Priority(i).name}')

    def choose_task(self):
        self.show()

        task_num = int(input('Choose task: '))

        return self.todo_list.get_task_by_index(task_num)

    def add_task(self):
        description = input('Description: ')

        self.show_priorities()

        priority_int = int(input('Priority: '))
        priority = model.Priority(priority_int)

        due_date_str = input(f'Due date ({model.DATEFORMAT}): ')

        due_date = (datetime.datetime.strptime(due_date_str, model.DATEFORMAT)).date()

        self.todo_list.add_task(model.Task(
            description,
            priority,
            due_date

        ))

    def mark_task_complete(self):
        task = self.choose_task()

        task.mark_complete()

    def delete_task(self):
        task = self.choose_task()

        self.todo_list.del_task(task)

    def save_list(self):
        self.todo_list.save()

    def load_list(self):
        self.todo_list.load()


if __name__ == '__main__':
    todo_list = model.ToDoList()
    controller = ToDoController(todo_list)

    controller.play()
