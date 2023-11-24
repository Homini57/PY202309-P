from PageFunc import *

def OpenGoalPage(goal):
    # 페이지 생성
    goal_page = Page(goal.name)
    # opened_pages 리스트에 페이지 추가
    # 프론트 출력
    goal_page.PrintFront()
    # 메뉴 출력
    goal_page.PrintMenu()
    while(True):
        command = input()
        if(command == ''):
            print('설정')
        if(command == '+'):
            print('할일 추가')
        if(command == '-'):
            print('할일 삭제')
        if(command == 'number'): #숫자(목표 번호)가 입력될 시
            print('하위 목표 이름')
        if(command == '0'):
            print('오늘 할일')
        if(command == '-1'):
            print('이전')

def OpenAddGoal():
    add_goal = EditPage('+', )