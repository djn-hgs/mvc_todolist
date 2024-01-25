import datetime
import xml.etree.ElementTree as et
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
    def from_dict(cls, task_dict):
        due_datetime = datetime.date.fromisoformat(task_dict['due'])

        if task_dict['completed_date']:
            completed_datetime = datetime.date.fromisoformat(task_dict['completed_date'])
        else:
            completed_datetime = None

        return cls(
            description=task_dict['description'],
            priority=Priority(task_dict['priority']),
            due=due_datetime,
            complete=task_dict['complete'],
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

    def save(self, filename: str = 'task_list.xml'):
        task_list_xml = et.Element('TaskList')

        for task in self.task_list:
            task_xml = et.SubElement(task_list_xml, 'Task')
            description_xml = et.SubElement(task_xml, 'Description')
            description_xml.text = task.description
            priority_xml = et.SubElement(task_xml, 'Priority')
            priority_xml.text = str(task.priority.value)
            due_date_xml = et.SubElement(task_xml, 'DueDate')
            due_date_xml.text = datetime.date.isoformat(task.due)
            complete_xml = et.SubElement(task_xml, 'Complete')
            complete_xml.text = str(task.complete)
            if task.complete:
                complete_date_xml = et.SubElement(task_xml, 'CompletionDate')
                complete_date_xml.text = datetime.date.isoformat(task.completed_date)

            tree = et.ElementTree(task_list_xml)

            tree.write(filename)

    def load(self, filename: str = 'task_list.xml'):
        tree = et.parse(filename)

        task_list_root_xml = tree.getroot()

        for task_xml in task_list_root_xml:

            description_text = task_xml.find('Description').text

            priority_text = task_xml.find('Priority').text
            priority = int(priority_text)

            due_date_text = task_xml.find('DueDate').text
            due_date = datetime.date.fromisoformat(due_date_text)

            complete_text = task_xml.find('Complete').text

            if complete_text == 'True':
                complete = True
            else:
                complete = False

            if complete:
                complete_date_text = task_xml.find('CompleteDate').text
                complete_date = datetime.date.fromisoformat(complete_date_text)
            else:
                complete_date = None

            self.task_list.append(
                Task(
                    description=description_text,
                    priority=Priority(priority),
                    due=due_date,
                    complete=complete,
                    completed_date=complete_date
                )
            )


