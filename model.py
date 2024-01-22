import csv
import datetime
import json
from dataclasses import dataclass, field
from enum import IntEnum

DATEFORMAT = '%Y-%m-%d'


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
                self.priority.value,
                self.due,
                self.complete,
                self.completed_date
            ]
        )

    def as_dict(self):
        return {
            'description': self.description,
            'priority': self.priority.value,
            'due': str(self.due),
            'complete': self.complete,
            'completed_date': str(self.completed_date) if self.completed_date else None
        }

    @classmethod
    def from_json(cls, task_json):
        due_datetime = datetime.date.fromisoformat(task_json['due'])

        if task_json['completed_date']:
            completed_datetime = datetime.date.fromisoformat(task_json['completed_date'])
        else:
            completed_datetime = None

        return cls(
            description=task_json['description'],
            priority=Priority(task_json['priority']),
            due=due_datetime,
            complete=task_json['complete'],
            completed_date=completed_datetime
        )


@dataclass
class ToDoList:
    task_list: list[Task] = field(default_factory=list)

    def __iter__(self):
        return iter(self.task_list)

    def add_task(self, task: Task):
        self.task_list.append(task)

    def del_task(self, task: Task):
        self.task_list.remove(task)

    def get_tasks(self):
        return self.task_list

    def get_task_by_index(self, task_num):
        return self.task_list[task_num]

    def save(self, filename: str = 'test.json'):
        with open(filename, 'w', encoding='utf-8') as stream:
            json.dump([task.as_dict() for task in self.task_list], stream)

    def load(self, filename: str = 'test.json'):
        with open(filename, 'r', encoding='utf-8') as stream:
            data_json = json.load(stream)

            for item in data_json:
                print(item)

                self.add_task_from_json(item)

    def add_task_from_json(self, item_json):
        self.add_task(Task.from_json(item_json))
