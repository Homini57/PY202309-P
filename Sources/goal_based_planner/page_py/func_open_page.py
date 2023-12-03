from goal_py.class_date import today
#Goal 클래스는 Edit, Setting Page에서 주로 쓰일 것
from goal_py.class_goal import Goal
from page_py.class_page import *

def CreatePage(PAGE_TITLE, GOAL_LEVEL, goal_contents):
        goal_page = Page(PAGE_TITLE, GOAL_LEVEL , goal_contents)
        opened_page_list.append(goal_page)
        return goal_page
def DeletePage():
    last_index = len(opened_page_list) - 1
    del(opened_page_list[last_index])

def RunMenu(goal_data_field, goal_list, command):
    if(command == ''):
        print('세부 내용')
        #OpenDetails()
        return 'continue'
    elif(command == '+'):
        print('할일 추가')
        #OpenAddGoal()
        return 'continue'
    elif(command == '-'):
        print('할일 삭제')
        #OpenDeleteGoal()
        return 'continue'
    elif(command == '0'):
        open_main_goal(goal_data_field)
    elif(command == '-1'):
        DeletePage()
        return 'back'
    elif(command == 'esc'):
        return 'terminate'
    try:
        int_command = int(command)
    except:
        return 'continue'
    else:
        if 0 < int_command:
            selected_goal = goal_list[int_command - 1]
            terminate = open_goal(selected_goal)
            if terminate == 'terminate':
                return 'terminate'
            return 'continue'
#오픈 함수 : 실행 후 페이지 생성
# 이전 : 현재,이전 페이지 삭제, 이전 페이지 실행
# 실행 : 실행
# 종료 : 종료
#1. 실행함수 2.종료 3. 이전


# 오늘 목표 페이지 열기
def open_todays_goal(goal_data_field):
    # 현재 목표의 레벨 : 현재 목표 위의 상위 목표의 개수
    TODAYS_PAGE_TITLE = '오늘 목표'
    TODAYS_GOAL_LEVEL = 0
    while(True):
        # 오늘 목표 읽어오기
        todays_goal_list = [goal for goal in goal_data_field if goal.check_date_in_term(today)]
        todays_goal_contents = [goal.get_goal_content() for goal in todays_goal_list]
        # 페이지 생성 후, 해당 단계의 열려있는 페이지 저장 리스트에 추가 or 갱신
        # 이 아랫부분은 함수 or 메소드화 가능할 것
        DeletePage()
        goal_page = CreatePage(TODAYS_PAGE_TITLE, TODAYS_GOAL_LEVEL , todays_goal_contents)
        # 오늘 목표 페이지 출력
        goal_page.print_front()
        goal_page.print_menu()
        
        
        # 메뉴 입력, 입력에 따른 페이지 열기
        # continue : '이전으로' 메뉴를 통해 돌아온 경우 페이지 재출력
        # return : 해당 페이지를 종료하고, 다음 실행에 대한 값 반환 
        command = input()
        #return_message = RunMenu(goal_data_field, todays_goal_list, command)
        if(command == ''):
            print('세부 내용이 없습니다.')
            continue
        elif(command == '+'):
            #open_add_goal()
            continue
        elif(command == '-'):
            #open_delete_goal()
            continue
        elif(command == '0'):
            open_main_goal(goal_data_field)
        elif(command == '-1'):
            DeletePage()
            return False
        elif(command == 'esc'):
            return True
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        # 같은 코드 반복, 함수화 고려
        try:
            int_command = int(command)
        except:
            continue
        else:
            if 0 < int_command:
                selected_goal = todays_goal_list[int_command - 1]
                terminate = open_goal(selected_goal)
                if terminate == True:
                    return True
                continue

# 메인 목표 페이지 열기
def open_main_goal(goal_data_field):
    MAIN_GOAL_LEVEL = 0
    MAIN_PAGE_TITLE = '메인 목표'
    # 메인 목표 읽어오기
    while(True):
        main_goal_list = [goal for goal in goal_data_field if goal.get_goal_level() == MAIN_GOAL_LEVEL]
        main_goal_contents = [goal.get_goal_content() for goal in main_goal_list]
        # 페이지 생성, 페이지 저장 리스트에 추가 or 갱신
        DeletePage()
        goal_page = CreatePage(MAIN_PAGE_TITLE, MAIN_GOAL_LEVEL , main_goal_contents)
        # 메인 목표 페이지 출력
        goal_page.print_front()
        goal_page.print_menu()

    
        # 메뉴 입력, 입력에 따른 페이지 열기
        command = input()
        if(command == ''):
            print('세부 내용이 없습니다.')
            continue
        elif(command == '+'):
            #open_add_goal()
            continue
        elif(command == '-'):
            #open_delete_goal()
            continue
        
        elif(command == '0'):
            open_main_goal(goal_data_field)
        elif(command == '-1'):
            DeletePage()
            return False
        elif(command == 'esc'):
            return True
        # 입력 받은 정수 번호의 목표 페이지를 열고, 다시 돌아오면 코드 반복
        try:
            int_command = int(command)
        except:
            continue
        else:
            if 0 < int_command:
                selected_goal = main_goal_list[int_command - 1]
                terminate = open_goal(selected_goal)
                if terminate == True:
                    return True
                continue

# 선택한 목표 페이지 열기
def open_goal(selected_goal, goal_data_field):
    while(True):
        # 선택한 목표 데이터 중 목표 내용, 레벨, 하위 목표 항목 생성
        goal_content = selected_goal.get_goal_content()
        goal_level = selected_goal.get_goal_level()
        sub_goal_list = [goal for goal in goal_data_field \
                         if goal.get_higher_goal_number() == selected_goal.goal_numeber]
        sub_goal_contents = [goal.get_goal_content() for goal in sub_goal_list]
        # 페이지 생성, 페이지 저장 리스트에 추가 or 갱신
        DeletePage()
        goal_page = Page(goal_content, goal_level, sub_goal_contents)
        if len(opened_page_list) == goal_level:
            opened_page_list.append(goal_page)
        else:
            opened_page_list[goal_level] = goal_page
        # 선택 목표 페이지 출력
        goal_page.print_front()

        goal_page.print_menu()

        # 메뉴 입력, 입력에 따른 페이지 열기
        command = input()
        if(command == ''):
            print('세부 내용')
            #OpenDetails()
            continue
        elif(command == '+'):
            print('할일 추가')
            #OpenAddGoal()
            continue
        elif(command == '-'):
            print('할일 삭제')
            #OpenDeleteGoal()
            continue
        elif(command == '0'):
            open_main_goal(goal_data_field)
        elif(command == '-1'):
            DeletePage()
            return False
        elif(command == 'esc'):
            return True
        try:
            int_command = int(command)
        except:
            continue
        else:
            if 0 < int_command:
                selected_goal = sub_goal_list[int_command - 1]
                terminate = open_goal(selected_goal)
                if terminate == True:
                    return True
                continue
                
#이전 페이지의 타이틀에 넣어야 함.
# 목표 -> 상위 목표, 날짜 -> 날짜
#아무것도 없는 곳은 새로 만들어야 함?
def open_add_goal(page_title,opened_goal):
    ADD_PAGE_TITLE = '목표 추가'
    goal_content = opened_goal.get_goal_content()
    add_page = EditPage(ADD_PAGE_TITLE,'+')
    add_page.print_front()
    print('\n')
    input_date = input()




def open_delete_goal(current_page):
    delete_page = EditPage(current_page, '-')