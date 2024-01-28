import datetime
import sqlite3
import xml.etree.ElementTree as ET
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
    id: int = None
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


class ToDoList:
    def __init__(self):
        self.cur = None
        self.con = None
        self.initialise_db()
        # self.task_list: list[Task] = []

    def __iter__(self):
        task_list = self.get_tasks()
        return iter(task_list)

    def add_task(self, task: Task):
        if task.complete:
            completed_date = task.completed_date.isoformat()
        else:
            completed_date = None

        self.cur.execute('INSERT INTO '
                         'Task(description, PriorityID, DueDate, Complete, CompleteDate) '
                         'VALUES '
                         '(?, ?, ?, ?, ?)',
                         (
                             task.description,
                             task.priority.value,
                             task.due.isoformat(),
                             task.complete,
                             completed_date
                         )
                         )
        self.con.commit()

    def del_task(self, task: Task):
        self.cur.execute('DELETE FROM Task WHERE id = ?',
                         (task.id,))
        self.con.commit()

    def get_tasks(self):
        task_list_query = self.cur.execute('SELECT * FROM Task')

        all_tasks = task_list_query.fetchall()

        task_list = []

        for task_tuple in all_tasks:
            (
                task_id,
                description,
                priority_int,
                due_iso,
                complete_int,
                complete_date_iso
            ) = task_tuple

            if complete_int:
                completed_date = datetime.date.fromisoformat(complete_date_iso)
            else:
                completed_date = None

            task_list.append(
                Task(
                    id=task_id,
                    description=description,
                    priority=Priority(priority_int),
                    due=datetime.date.fromisoformat(due_iso),
                    complete=bool(complete_int),
                    completed_date=completed_date
                )
            )

        return task_list

    def mark_task_complete(self, task):
        task.mark_complete()
        self.cur.execute('UPDATE Task '
                         'SET Complete = 1, '
                         'CompleteDate = ? '
                         'WHERE id = ?;',
                         (task.completed_date.isoformat(), task.id,)
                         )
        self.con.commit()

    def get_task_by_index(self, task_num):
        return self.task_list[task_num]

    def initialise_db(self, filename: str = 'task_list.sqlite3'):
        self.con = sqlite3.connect(filename)

        self.cur = self.con.cursor()

        table_name_query = self.cur.execute('SELECT distinct name FROM sqlite_master')
        table_names = table_name_query.fetchall()

        if ('Priority',) not in table_names:
            print('Creating Priority table')
            self.cur.execute('CREATE TABLE Priority(PriorityID INTEGER, PriorityName TEXT)')

        if ('Task',) not in table_names:
            print('Creating Task table')
            self.cur.execute('CREATE TABLE Task(id INTEGER PRIMARY KEY, description TEXT, PriorityID INTEGER, '
                             'DueDate TEXT, Complete INTEGER, CompleteDate TEXT)')

        self.con.commit()

        table_name_query = self.cur.execute('SELECT distinct name FROM sqlite_master')
        table_names = table_name_query.fetchall()

        print(table_names)
