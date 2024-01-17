import csv
import datetime
from dataclasses import dataclass, field
from enum import IntEnum

DATEFORMAT = '%d/%m/%Y'

class Priority(IntEnum):
    Low = 0
    Medium = 1
    High = 2

PRIORITIES = [
    Priority.Low,
    Priority.Medium,
    Priority.High
]


@dataclass
class Task:
    description: str = ''
    priority: 'Priority' = Priority.Low
    due: datetime.date | None = None
    complete: bool = False
    completed_date: datetime.date | None = None

    def mark_complete(self):
        self.complete = True
        self.completed_date = datetime.date.today()

    def __repr__(self):
        status = f'{self.due} - {self.description} ({self.priority.name}) '

        if self.complete:
            status += f'completed {self.completed_date}'

        return status

    def __iter__(self):
        return iter(
            [
                self.description,
                self.priority,
                self.due,
                self.complete,
                self.completed_date
            ]
        )
@dataclass
class ToDoList:
    task_list: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.task_list.append(task)

    def del_task(self, task: Task):
        self.task_list.remove(task)

    def get_tasks(self):
        return self.task_list

    def get_task_by_index(self, task_num):
        return self.task_list[task_num]

    def save(self, filename: str = 'test.csv'):
        with open(filename, 'w') as stream:
            writer = csv.writer(stream)

            writer.writerows(self.task_list)

    def load(self, filename: str = 'test.csv'):
        with open(filename, 'r') as stream:
            reader = csv.reader(stream)

            for row in reader:
                print(row)

                if not row:
                    break

                (description, priority_str, due_str, completed_str, completed_date_str) = row

                if completed_str == 'False':
                    completed = False
                else:
                    completed = True

                if completed_date_str:
                    completed_date = datetime.datetime.strptime(completed_date_str, '%Y-%m-%d').date()
                else:
                    completed_date = None

                self.task_list.append(
                            Task(
                                description,
                                Priority(int(priority_str)),
                                datetime.datetime.strptime(due_str, '%Y-%m-%d').date(),
                                completed,
                                completed_date
                            )
                )
