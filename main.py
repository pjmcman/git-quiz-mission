"""퀴즈 게임 실행 진입점: python main.py"""

import os
import sys

from quiz_game import QuizGame

# 어느 폴더에서 실행하든 프로젝트 루트(main.py가 있는 폴더)의 state.json을 쓴다.
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state.json')


def main():
    # Windows 콘솔에서 이모지/한글이 깨지지 않도록 UTF-8로 출력
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    QuizGame(STATE_PATH).run()


if __name__ == '__main__':
    main()
