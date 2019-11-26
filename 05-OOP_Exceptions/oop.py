import datetime
from dataclasses import dataclass
from collections import defaultdict


class CourseError(Exception):
    """Base exceptions of errors in course"""


class DeadlineError(CourseError):
    """Deadline's up"""


class Homework:
    __slots__ = {'text', 'deadline', 'created', }

    def __init__(self, text: str, deadline: int):
        self.text = text
        self.deadline = datetime.timedelta(days=deadline)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        return datetime.datetime.now() < self.created + self.deadline


@dataclass(frozen=True)
class Person:
    __slots__ = {'last_name', 'first_name', }
    first_name: str
    last_name: str


class HomeworkResult:
    __slots__ = {'author', 'homework', 'solution', 'created', }

    def __init__(self, author: Person, homework: Homework, solution: str):
        self.author = author
        if not isinstance(homework, Homework):
            raise TypeError('You gave a not Homework object')
        self.homework = homework
        self.solution = solution
        self.created = datetime.datetime.now()


class Student(Person):
    def do_homework(self, homework: Homework, solution: str) -> HomeworkResult:
        if not homework.is_active():
            raise DeadlineError("You are late")
        return HomeworkResult(self, homework, solution)


class Teacher(Person):
    homework_done = defaultdict(set)

    @staticmethod
    def create_homework(text: str, deadline: int) -> Homework:
        return Homework(text, deadline)

    @classmethod
    def check_homework(cls, answer: HomeworkResult) -> bool:
        if len(answer.solution) > 5:
            cls.homework_done[answer.homework].add(answer)
            return True
        return False

    @classmethod
    def reset_results(cls, homework: Homework = None) -> dict:
        if homework:
            cls.homework_done.pop(homework)
        else:
            cls.homework_done.clear()
        return cls.homework_done


if __name__ == '__main__':
    opp_teacher = Teacher('Daniil', 'Shadrin')
    advanced_python_teacher = Teacher('Aleksandr', 'Smetanin')

    lazy_student = Student('Ivan', 'Romaneko')
    good_student = Student('Lev', 'Sokolov')

    oop_hw = opp_teacher.create_homework('Learn OOP', 1)
    docs_hw = opp_teacher.create_homework('Read docs', 5)

    result_1 = good_student.do_homework(oop_hw, 'I have done this hw')
    result_2 = good_student.do_homework(docs_hw, 'I have done this hw too')
    result_3 = lazy_student.do_homework(docs_hw, 'done')
    try:
        result_4 = HomeworkResult(good_student, "fff", "Solution")
    except TypeError:
        print('There was an exception here')
    opp_teacher.check_homework(result_1)

    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done
    assert temp_1 == temp_2

    print(Teacher.homework_done[oop_hw])
    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)
    for homework in Teacher.homework_done:
        print(homework, Teacher.homework_done[homework])
    print(Teacher.reset_results())
