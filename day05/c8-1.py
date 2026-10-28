# 절차지향 프로그래밍: 데이터를 순서대로 처리하고 하향식 순차 실행 흐름, C
# 객체지향 프로그래밍: 객체들의 상호작용으로 프로그래밍 설계, JAVA,PYTHON,JS
# 관점지향 프로그래밍: 공통되는 기능(로근/검증/보안 등)들을 분리하여 프로그래밍 설계, SPRING
# 추상화: 핵심적인 개념 또는 기능 간추려 내는 것
# 객체: 속섬명과 속성값으로 표현 [리스트],{딕셔너리} 객체이다.
# 클래스: 추상화한 데이터들을 구조화 한것(설계도)
# 객체: 세강에 존재하는 모든 데이터들을 추상화(실체x) -> 개념적 객체
# 인스턴스: 추상화한것을 객체 만든것(실체o) -> 물리적 객체
# 인스턴스화: 컴퓨터내 객체 정보 저장, JAVA : new 생성자(), PY: 생성자()
# 생성자: 클래스 기반으로 인스턴스 만드는 함수 -> 인스턴스 초기화함수

# 1. 클래스 만들기
class Student:
    pass
student = Student()
students = [
    Student(),
    Student(),
    Student(),
    Student(),
    Student(),
    Student() 
]

# 2. 생성자 
class Student:
    def __init__(self, name, korean, math, english, science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
    # def 메소드명(self, 매개변수1):
    def get_sum(self):
        return self.korean + self.math + self.english + self.science
    def get_average(self):
        return self.get_sum()/4
    def to_string(self):
        return"{} \t {} \t {}".format(self.name, self.get_sum(), self.get_average())
# 일반함수와 메소드 차이? 일반함수는 클래스밖에서 독립선언/ 메소드는 클래스 안에서 내부선언
# 일반함수에서는 self 없고 메소드는 self 있다.
 
# 생성자 이용하 인스턴스 생성
students = [
    Student2("윤민성",87,98,88,85),
    Student2("윤민성",87,98,88,85),
    Student2("윤민성",87,98,88,85),
    Student2("윤민성",87,98,88,85),
    Student2("윤민성",87,98,88,85),
    Student2("윤민성",87,98,88,85),
]

# 인스턴스내 멤버변수 호출
print(students[0].korean) # 87호출

