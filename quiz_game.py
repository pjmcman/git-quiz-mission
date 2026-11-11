"""게임 전체 흐름(메뉴, 입력 처리)을 관리하는 QuizGame 클래스."""

from quiz import Quiz
from quiz_data import create_default_quizzes

LINE = '-' * 40
DOUBLE_LINE = '=' * 40

MENU_MIN = 1
MENU_MAX = 5


class QuizGame:
    """메뉴를 보여주고, 사용자가 고른 기능을 실행한다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()   # Quiz 인스턴스 리스트

    # ------------------------------------------------------------------
    # 입력 처리
    # ------------------------------------------------------------------
    @staticmethod
    def read_number(prompt, minimum, maximum):
        """minimum~maximum 범위의 정수를 받을 때까지 다시 묻는다.

        - 앞뒤 공백은 제거한다.         ' 1 '  -> 1
        - 빈 입력(Enter)은 다시 묻는다.  ''
        - 숫자가 아니면 다시 묻는다.     'abc'
        - 범위 밖이면 다시 묻는다.       '9'
        """
        while True:
            value = input(prompt).strip()
            if not value:
                print('⚠️  빈 값은 입력할 수 없습니다. 다시 입력하세요.')
                continue
            try:
                number = int(value)
            except ValueError:
                print(f'⚠️  잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.')
                continue
            if not minimum <= number <= maximum:
                print(f'⚠️  잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.')
                continue
            return number

    # ------------------------------------------------------------------
    # 메뉴 기능 (각 기능은 다음 단계에서 구현)
    # ------------------------------------------------------------------
    def show_menu(self):
        print()
        print(DOUBLE_LINE)
        print('        🎯 나만의 퀴즈 게임 🎯')
        print(DOUBLE_LINE)
        print('1. 퀴즈 풀기')
        print('2. 퀴즈 추가')
        print('3. 퀴즈 목록')
        print('4. 점수 확인')
        print('5. 종료')
        print(DOUBLE_LINE)

    def play(self):
        """저장된 퀴즈를 차례대로 출제하고, 다 풀면 결과를 보여준다."""
        if not self.quizzes:
            print('⚠️  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.')
            return

        total = len(self.quizzes)
        correct = 0

        print()
        print(f'📝 퀴즈를 시작합니다! (총 {total}문제)')
        print()

        for number, quiz in enumerate(self.quizzes, start=1):
            print(LINE)
            quiz.display(number)
            answer = self.read_number('정답 입력: ', 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(answer):
                correct += 1
                print('✅ 정답입니다!')
            else:
                print(f'❌ 오답입니다. 정답은 {quiz.answer}번 '
                      f'({quiz.choices[quiz.answer - 1]}) 입니다.')
            print()

        score = round(correct / total * 100)
        print(DOUBLE_LINE)
        print(f'🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)')
        print(DOUBLE_LINE)

    def add_quiz(self):
        print('🚧 퀴즈 추가 기능은 준비 중입니다.')

    def list_quizzes(self):
        print('🚧 퀴즈 목록 기능은 준비 중입니다.')

    def show_score(self):
        print('🚧 점수 확인 기능은 준비 중입니다.')

    # ------------------------------------------------------------------
    # 메인 루프
    # ------------------------------------------------------------------
    def run(self):
        """종료(5)를 고를 때까지 메뉴를 반복한다."""
        actions = {
            1: self.play,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
        }
        try:
            while True:
                self.show_menu()
                choice = self.read_number('선택: ', MENU_MIN, MENU_MAX)
                if choice == MENU_MAX:
                    print('👋 게임을 종료합니다.')
                    break
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료(Ctrl+Z/Ctrl+D) 시 비정상 종료하지 않는다.
            print()
            print('⚠️  입력이 중단되었습니다. 프로그램을 안전하게 종료합니다.')
