"""퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4)를 가진 퀴즈 한 개."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        if len(choices) != self.CHOICE_COUNT:
            raise ValueError(f'선택지는 {self.CHOICE_COUNT}개여야 합니다.')
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f'정답은 1~{self.CHOICE_COUNT} 사이여야 합니다.')
        self.question = question
        self.choices = list(choices)
        self.answer = answer

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        title = f'[문제 {number}]' if number is not None else '[문제]'
        print(title)
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f'{index}. {choice}')
        print()

    def is_correct(self, user_answer):
        """사용자 답(정수)이 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self):
        return {
            'question': self.question,
            'choices': self.choices,
            'answer': self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['question'], data['choices'], int(data['answer']))
