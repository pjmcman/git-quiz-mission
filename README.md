# E1-2 나만의 퀴즈 게임 (Python 콘솔)

## 1. 프로젝트 개요

터미널에서 동작하는 **객관식 퀴즈 게임**을 Python으로 처음부터 끝까지 구현하는 미션입니다.

- 메뉴에서 퀴즈 풀기 / 추가 / 목록 / 점수 확인 / 종료를 선택한다.
- 클래스(`Quiz`, `QuizGame`)로 역할을 나눠 코드를 구조화한다.
- 퀴즈와 최고 점수를 `state.json`에 저장해, 프로그램을 다시 실행해도 데이터가 유지된다.
- Git으로 기능 단위 커밋, 브랜치 생성·병합, clone·pull을 경험한다.

## 2. 퀴즈 주제와 선정 이유

**주제: 이번 미션에서 배운 Python·Git 기초 개념**

이 미션이 끝나면 배운 내용으로 시험을 본다. 그래서 퀴즈 게임 자체를 **시험 대비 복습 도구**로 만들었다.
변수와 자료형, 조건문·반복문, 함수, 클래스와 `self`, 파일 입출력과 JSON, 예외 처리, Git 명령어를 문제로 출제한다.
게임을 만들면서 직접 쓴 개념을, 게임을 풀면서 다시 확인할 수 있다.

> 이하 항목(실행 방법, 기능 목록, 파일 구조, 데이터 파일 설명)은 기능을 구현하면서 채워 나갑니다.

## 진행 체크리스트

> 한 단계가 끝날 때마다 `[ ]`를 `[x]`로 바꾼다. 🙋 표시는 **내가 직접** 해야 하는 일이다.

### 0. 준비 🙋
- [x] GitHub에 새 저장소 만들기 (Public, README/.gitignore 체크 안 함)
- [x] 로컬 저장소와 연결: `git remote add origin <저장소 URL>`
- [x] 첫 push: `git push -u origin main`
- [x] 개발 환경 스크린샷 찍기 (VSCode, `python --version`, `git config --list`) → `docs/screenshots/env.png`

### 1. 기능 개발 (단계마다 커밋)
- [x] 1. Chore: 초기 설정 (.gitignore, README 개요)
- [x] 2. Feat: 메뉴 출력과 입력 예외 처리 (잘못된 입력, 빈 입력, Ctrl+C/EOF)
- [x] 3. Feat: Quiz 클래스 (문제·선택지 4개·정답, 출력, 정답 확인)
- [x] 4. Feat: 기본 퀴즈 데이터 10개
- [x] 5. Feat: 퀴즈 풀기 🙋 **브랜치 작업**
  - `git checkout -b feature/play` → 개발·커밋
  - `git checkout main` → `git merge feature/play` → `git push`
- [x] 6. Feat: state.json 저장/불러오기 (파일 없음·손상 처리)
- [x] 7. Feat: 퀴즈 추가
- [x] 8. Feat: 퀴즈 목록
- [x] 9. Feat: 최고 점수 확인
- [x] 10. Feat: 랜덤 출제 + 점수 기록 히스토리 (보너스)
- [ ] 11. Refactor: QuizGame 구조 정리
- [ ] 12. Docs: README 완성 (실행 방법, 기능 목록, 파일 구조, state.json 설명) → 최종 push

### 2. clone / pull 실습 🙋
- [ ] 다른 폴더에서 `git clone <저장소 URL>`
- [ ] 복제한 폴더에서 README에 한 줄 추가 → commit → push
- [ ] 원래 폴더로 돌아와 `git pull` → 변경 반영 확인

### 3. 제출물 🙋
- [ ] 실행 화면 스크린샷 → `docs/screenshots/` (menu.png, play.png, add_quiz.png, score.png)
- [ ] `git log --oneline --graph` 스크린샷 → `docs/screenshots/git_log.png`
- [ ] GitHub 저장소 URL 제출
