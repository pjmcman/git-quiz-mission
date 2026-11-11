"""기본 퀴즈 데이터: 이번 미션에서 배운 Python·Git 기초 개념 10문제."""

from quiz import Quiz


def create_default_quizzes():
    """기본 퀴즈 10개를 Quiz 인스턴스 리스트로 새로 만들어 반환한다."""
    return [
        # 자료형
        Quiz("type([1, 2, 3])의 결과로 알맞은 것은?",
             ['int', 'str', 'list', 'dict'], 3),
        # 반복문
        Quiz('반복 횟수를 미리 알 수 없고, 조건이 참인 동안 계속 반복할 때 알맞은 문법은?',
             ['for', 'while', 'if', 'def'], 2),
        # 클래스 / 객체
        Quiz('클래스의 __init__ 메서드는 언제 호출되는가?',
             ['클래스를 정의할 때',
              '객체(인스턴스)가 생성될 때',
              '객체가 삭제될 때',
              '메서드를 처음 호출할 때'], 2),
        Quiz('메서드의 첫 번째 매개변수 self가 가리키는 것은?',
             ['클래스 자체',
              '부모 클래스',
              '그 메서드를 호출한 객체(인스턴스)',
              '현재 실행 중인 모듈'], 3),
        # 파일 입출력 / JSON
        Quiz('파이썬 객체(dict 등)를 JSON 파일에 저장할 때 쓰는 함수는?',
             ['json.load()', 'json.loads()', 'json.read()', 'json.dump()'], 4),
        Quiz('파일을 열 때 with open(...) 구문을 쓰는 가장 큰 이유는?',
             ['파일 읽기 속도가 빨라진다',
              '블록이 끝나면 예외가 나도 파일이 자동으로 닫힌다',
              '파일이 없으면 오류 없이 무시된다',
              '여러 파일을 동시에 열 수 있다'], 2),
        # 예외 처리
        Quiz("int('abc')를 실행하면 발생하는 예외는?",
             ['TypeError', 'KeyError', 'ValueError', 'IndexError'], 3),
        Quiz('input() 입력 중 Ctrl+C를 누르면 발생하는 예외는?',
             ['KeyboardInterrupt', 'EOFError', 'SystemExit', 'StopIteration'], 1),
        # Git
        Quiz('새 브랜치를 만들면서 바로 그 브랜치로 이동하는 명령어는?',
             ['git branch -d 이름',
              'git checkout -b 이름',
              'git merge 이름',
              'git switch main'], 2),
        Quiz('git clone과 git pull의 차이로 옳은 것은?',
             ['clone은 원격 저장소를 처음 복제하고, pull은 이미 받은 저장소에 새 변경을 가져온다',
              'clone은 내 커밋을 원격에 올리고, pull은 원격 커밋을 지운다',
              '둘 다 똑같이 동작한다',
              'pull은 새 저장소를 만들고, clone은 브랜치를 병합한다'], 1),
    ]
