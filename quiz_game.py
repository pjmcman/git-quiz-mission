"""게임 전체 흐름을 관리하는 QuizGame 클래스.

메서드는 역할별로 나뉘어 있다.
  1) 저장 / 불러오기 : state.json 읽기·쓰기, 손상 시 복구
  2) 입력 처리       : 빈 입력·문자·범위 밖 입력 검증
  3) 메뉴 기능       : 퀴즈 풀기 / 추가 / 목록 / 점수 확인
  4) 메인 루프       : 메뉴 반복, 종료·Ctrl+C·EOF 처리
"""

import json
import os
import random
from datetime import datetime

from quiz import Quiz
from quiz_data import create_default_quizzes

LINE = '-' * 40
DOUBLE_LINE = '=' * 40
TITLE = '        🎯 나만의 퀴즈 게임 🎯'
HISTORY_SHOW_COUNT = 5   # 점수 확인 화면에 보여줄 최근 기록 수


class QuizGame:
    """퀴즈 목록·최고 점수·게임 기록을 들고, 메뉴에 따라 기능을 실행한다."""

    # 메뉴 번호 → (화면에 보일 이름, 실행할 메서드 이름). 메뉴를 바꿀 때는 여기만 고친다.
    MENU = {
        1: ('퀴즈 풀기', 'play'),
        2: ('퀴즈 추가', 'add_quiz'),
        3: ('퀴즈 목록', 'list_quizzes'),
        4: ('점수 확인', 'show_score'),
        5: ('종료', None),
    }
    EXIT_CHOICE = 5

    def __init__(self, state_file='state.json'):
        self.state_file = state_file
        self.quizzes = []        # Quiz 인스턴스 리스트
        self.best_score = None   # 최고 점수(100점 만점). 아직 풀지 않았으면 None
        self.best_detail = None  # 최고 점수를 낸 판의 {'correct': 맞힌 수, 'total': 문제 수}
        self.history = []        # 모든 게임 기록 [{'played_at', 'total', 'correct', 'score'}, ...]
        self.load_state()

    # ------------------------------------------------------------------
    # 1) 저장 / 불러오기 (state.json)
    # ------------------------------------------------------------------
    def reset_to_default(self):
        """기본 퀴즈 데이터로 초기화한다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_detail = None
        self.history = []

    def load_state(self):
        """state.json을 읽는다. 없거나 손상되었으면 기본 데이터로 시작한다."""
        if not os.path.exists(self.state_file):
            print('📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.')
            self.reset_to_default()
            self.save_state()
            return

        try:
            with open(self.state_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.apply_state(data)
            print(f'📂 저장된 데이터를 불러왔습니다. '
                  f'(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_text()})')
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            # 읽기 실패, JSON 문법 오류, 키 누락, 잘못된 값(선택지 3개 등) 모두 여기로
            print(f'⚠️  데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({error})')
            self.reset_to_default()
            self.save_state()

    def apply_state(self, data):
        """읽어 온 dict를 검사하고 속성에 넣는다. 형식이 틀리면 예외를 낸다."""
        quizzes = [Quiz.from_dict(item) for item in data['quizzes']]

        best_score = data.get('best_score')
        if best_score is not None and not isinstance(best_score, int):
            raise ValueError('best_score는 정수여야 합니다.')

        history = data.get('history', [])
        if not isinstance(history, list):
            raise ValueError('history는 리스트여야 합니다.')

        # 모두 검사를 통과한 뒤에 한꺼번에 반영한다.
        self.quizzes = quizzes
        self.best_score = best_score
        self.best_detail = data.get('best_detail')
        self.history = history

    def save_state(self):
        """현재 퀴즈 목록, 최고 점수, 게임 기록을 state.json에 UTF-8로 저장한다."""
        data = {
            'quizzes': [quiz.to_dict() for quiz in self.quizzes],
            'best_score': self.best_score,
            'best_detail': self.best_detail,
            'history': self.history,
        }
        try:
            with open(self.state_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f'⚠️  데이터를 저장하지 못했습니다. ({error})')

    # ------------------------------------------------------------------
    # 2) 입력 처리
    # ------------------------------------------------------------------
    @staticmethod
    def read_text(prompt):
        """빈 문자열이 아닌 글자를 받을 때까지 다시 묻는다. 앞뒤 공백은 제거한다."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print('⚠️  빈 값은 입력할 수 없습니다. 다시 입력하세요.')

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
                number = None          # 숫자로 바꿀 수 없음 → 아래에서 안내
            if number is not None and minimum <= number <= maximum:
                return number
            print(f'⚠️  잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.')

    def read_answer(self, prompt):
        """1~4 정답 번호를 입력받는다."""
        return self.read_number(prompt, 1, Quiz.CHOICE_COUNT)

    # ------------------------------------------------------------------
    # 3) 메뉴 기능
    # ------------------------------------------------------------------
    def has_quizzes(self):
        """퀴즈가 하나라도 있으면 True. 없으면 안내 후 False."""
        if self.quizzes:
            return True
        print('⚠️  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.')
        return False

    # --- 1. 퀴즈 풀기 ---------------------------------------------------
    def play(self):
        """퀴즈를 무작위 순서로 출제하고, 다 풀면 결과를 보여주고 기록한다."""
        print()
        if not self.has_quizzes():
            return

        quizzes = self.quizzes[:]   # 원본 순서(목록 화면)는 그대로 두고 복사본만 섞는다
        random.shuffle(quizzes)
        total = len(quizzes)

        print(f'📝 퀴즈를 시작합니다! (총 {total}문제)')
        print()

        correct = 0
        for number, quiz in enumerate(quizzes, start=1):
            if self.ask_question(number, quiz):
                correct += 1

        score = round(correct / total * 100)
        self.show_result(score, correct, total)
        self.record_history(score, correct, total)

    def ask_question(self, number, quiz):
        """문제 하나를 출제하고 정답이면 True를 돌려준다."""
        print(LINE)
        quiz.display(number)
        answer = self.read_answer('정답 입력: ')
        if quiz.is_correct(answer):
            print('✅ 정답입니다!')
            print()
            return True
        print(f'❌ 오답입니다. 정답은 {quiz.answer}번 '
              f'({quiz.choices[quiz.answer - 1]}) 입니다.')
        print()
        return False

    def show_result(self, score, correct, total):
        """결과를 보여주고 최고 점수를 갱신한다."""
        print(DOUBLE_LINE)
        print(f'🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)')
        if self.update_best_score(score, correct, total):
            print('🎉 새로운 최고 점수입니다!')
        else:
            print(f'현재 최고 점수: {self.best_score}점')
        print(DOUBLE_LINE)

    def update_best_score(self, score, correct, total):
        """이번 점수가 최고 점수보다 높으면 갱신하고 True를 돌려준다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_detail = {'correct': correct, 'total': total}
            return True
        return False

    def record_history(self, score, correct, total):
        """이번 게임 기록(날짜/시간, 문제 수, 맞힌 수, 점수)을 추가하고 저장한다."""
        self.history.append({
            'played_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total': total,
            'correct': correct,
            'score': score,
        })
        self.save_state()

    # --- 2. 퀴즈 추가 ---------------------------------------------------
    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록하고 저장한다."""
        print()
        print('📌 새로운 퀴즈를 추가합니다.')
        print()
        question = self.read_text('문제를 입력하세요: ')
        choices = [self.read_text(f'선택지 {index}: ')
                   for index in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = self.read_answer(f'정답 번호 (1-{Quiz.CHOICE_COUNT}): ')

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print()
        print(f'✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)')

    # --- 3. 퀴즈 목록 ---------------------------------------------------
    def list_quizzes(self):
        """등록된 퀴즈의 문제를 번호와 함께 보여준다."""
        print()
        if not self.has_quizzes():
            return

        print(f'📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)')
        print()
        print(LINE)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f'[{index}] {quiz.question}')
        print(LINE)

    # --- 4. 점수 확인 ---------------------------------------------------
    def best_text(self):
        """최고 점수를 '80점' 또는 '없음' 같은 글자로 돌려준다."""
        return '없음' if self.best_score is None else f'{self.best_score}점'

    def show_score(self):
        """최고 점수와 최근 게임 기록을 보여준다. 아직 풀지 않았으면 안내한다."""
        print()
        if self.best_score is None:
            print('⚠️  아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 퀴즈를 풀어 보세요.')
            return

        message = f'🏆 최고 점수: {self.best_text()}'
        if self.best_detail:
            message += (f" ({self.best_detail['total']}문제 중 "
                        f"{self.best_detail['correct']}문제 정답)")
        print(message)
        self.show_history()

    def show_history(self):
        """최근 게임 기록을 최대 HISTORY_SHOW_COUNT개 보여준다."""
        if not self.history:
            return
        recent = self.history[-HISTORY_SHOW_COUNT:]
        print()
        print(f'🎮 플레이 기록 (총 {len(self.history)}회, 최근 {len(recent)}회)')
        print(LINE)
        for record in recent:
            print(f"{record.get('played_at', '-')}  "
                  f"{record['total']}문제 중 {record['correct']}문제 정답 "
                  f"({record['score']}점)")
        print(LINE)

    # ------------------------------------------------------------------
    # 4) 메인 루프
    # ------------------------------------------------------------------
    def show_menu(self):
        """MENU 표를 그대로 화면에 출력한다."""
        print()
        print(DOUBLE_LINE)
        print(TITLE)
        print(DOUBLE_LINE)
        for number, (label, _) in self.MENU.items():
            print(f'{number}. {label}')
        print(DOUBLE_LINE)

    def run(self):
        """종료를 고를 때까지 메뉴를 반복한다. Ctrl+C·EOF에도 저장 후 안전하게 끝낸다."""
        try:
            while True:
                self.show_menu()
                choice = self.read_number('선택: ', min(self.MENU), max(self.MENU))
                if choice == self.EXIT_CHOICE:
                    self.save_state()
                    print('👋 게임을 종료합니다. 데이터가 저장되었습니다.')
                    break
                _, method_name = self.MENU[choice]
                getattr(self, method_name)()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료(Ctrl+Z/Ctrl+D) 시 비정상 종료하지 않는다.
            print()
            print('⚠️  입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.')
            self.save_state()
