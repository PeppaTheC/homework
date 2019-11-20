import datetime
from dataclasses import dataclass


@dataclass(frozen=False)
class Homework:
    __slots__ = {'text', 'deadline', 'created'}
    text: str
    deadline: datetime.timedelta

    def __post_init__(self):
        self.deadline = datetime.timedelta(days=float(self.deadline))
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        return datetime.datetime.now() < self.created + self.deadline


@dataclass(frozen=True)
class Student:
    __slots__ = {'last_name', 'first_name'}
    first_name: str
    last_name: str

    @staticmethod
    def do_homework(homework: Homework):
        if homework.is_active():
            return homework
        print("You are late")


@dataclass(frozen=True)
class Teacher:
    __slots__ = {'first_name', 'last_name'}
    first_name: str
    last_name: str

    @staticmethod
    def create_homework(text, deadline) -> Homework:
        return Homework(text, deadline)


def test():
    teacher = Teacher('Daniil', 'Shadrin')
    student = Student('Ivan', 'Romanenko')
    assert teacher.last_name == 'Shadrin'
    assert student.first_name == 'Ivan'

    expired_homework = teacher.create_homework('Learn functions', 0)
    assert expired_homework.deadline == datetime.timedelta(days=0)
    assert expired_homework.text == 'Learn functions'

    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    assert student.do_homework(oop_homework) is oop_homework
    assert not student.do_homework(expired_homework)


if __name__ == '__main__':
    test()
