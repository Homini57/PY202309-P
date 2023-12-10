from goal_py.class_goal import *
from page_py.class_page import *


if __name__ == '__main__':
    # 프로그램 시작 : 첫번째 페이지를 열린 페이지에 추가
    page = Page()
    start_page = MainGoalPage()
    page.opened_pages.append(start_page)
    # 열려있는 페이지의 내용을 업데이트 후, 마지막 페이지를 실행, 반복
    while True:
        last_index = len(page.opened_pages) - 1
        next_page = page.opened_pages[last_index]
        next_page.update_page()
        terminate = next_page.open_page()
        # 종료 메시지 입력시 현재까지 수정된 데이터 저장 후 프로그램 종료
        if terminate == True:
            write_data_file(GoalField().data)
            write_contents_file(GoalField().contents)
            print('프로그램을 종료합니다.')
            break