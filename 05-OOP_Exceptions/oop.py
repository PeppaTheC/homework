import datetime
from dataclasses import dataclass
from collections import defaultdict


class CourseError(Exception):
    """Base exceptions of errors in course"""


class HomeworkTypeError(CourseError):
    """Type of object doesn't match type of Homework"""


class DeadlineError(CourseError):
    """Deadline's up"""


@dataclass()
class Homework:
    __slots__ = {'text', 'deadline', 'created', }
    text: str
    deadline: int

    def __post_init__(self):
        self.deadline = datetime.timedelta(days=self.deadline)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        return datetime.datetime.now() < self.created + self.deadline

    def __hash__(self):
        return id(self)


class HomeworkResult:
    __slots__ = {'author', 'homework', 'solution', 'created', }

    def __init__(self, author, homework: Homework, solution: str):
        self.author = author
        if not isinstance(homework, Homework):
            raise HomeworkTypeError('You gave a not Homework object')
        self.homework = homework
        self.solution = solution
        self.created = datetime.datetime.now()

    def __gt__(self, other):
        return len(self.solution) > other


@dataclass(frozen=True)
class Person:
    __slots__ = {'last_name', 'first_name', }
    first_name: str
    last_name: str


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
        if answer > 5:
            cls.homework_done[answer.homework].add(answer)
            return True
        return False

    @classmethod
    def reset_results(cls, homework: Homework = None):
        if homework:
            cls.homework_done.pop(homework)
        else:
            cls.homework_done.clear()


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
    except HomeworkTypeError:
        print('There was an exception here')
    opp_teacher.check_homework(result_1)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result_1)
    temp_2 = Teacher.homework_done
    assert temp_1 == temp_2

    opp_teacher.check_homework(result_2)
    opp_teacher.check_homework(result_3)

    print(Teacher.homework_done[oop_hw])
    for homework in Teacher.homework_done:
        print(homework)
    Teacher.reset_results()
