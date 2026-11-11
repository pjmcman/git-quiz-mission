"""퀴즈 게임 실행 진입점: python main.py"""

import sys

from quiz_game import QuizGame


def main():
    # Windows 콘솔에서 이모지/한글이 깨지지 않도록 UTF-8로 출력
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    QuizGame().run()


if __name__ == '__main__':
    main()
