from goal_py.class_goal import *
from page_py.class_page import *


if __name__ == '__main__':
    #start_page = open_todays_goal(goal_data_field)
    print(Goal('01').get_higher_goal_number())
    '''
    page = Page()
    start_page = MainGoalPage()
    page.opened_pages.append(start_page)
    while True:
        last_index = len(page.opened_pages) - 1
        next_page = page.opened_pages[last_index]
        terminate = next_page.open_page() # 다음 페이지 생성 or 현재 페이지 삭제 or 종료 메시지?
        if terminate == True:
            break

    '''
    
#오픈 함수 : 실행 후 페이지 생성
# 이전 : 현재,이전 페이지 삭제, 이전 페이지 실행
# 실행 : 실행
# 종료 : 종료
#1. 실행함수 2.종료 3. 이전