#Goal 클래스는 설정페이지에서 본격적으로 쓰일 것
from goal_py.class_date import today
from goal_py.class_goal import Goal

# 페이지 클래스 : 목표 레벨 삭제
class Page():
    opened_pages = []
    # 필드 : 페이지 제목, 목표 레벨, 출력 메뉴 항목
    # 출력 타입( 0 : 일반 페이지, 1 : 오늘 목표 페이지, 2 : 메인 목표 페이지)
    def __init__(self, title = '', menu_list = []):
        self.title = title
        self.menu_list = menu_list
        self.basic_menu = [' +. 추가           ','-. 삭제           ','enter. 세부 내용', \
                           '-1. 이전으로        ','0. 메인으로       ','    ?. 도움말  ', \
                            'esc.프로그램 종료']
    # 제목과 기본 메뉴를 출력 페이지 앞부분에 출력
    # C++의 가상함수처럼 이것도 상속으로 다르게 정의하고 같은 페이지 리스트에 저장할 수 있을까?
    def print_menu(self):
        
        print('')
        print('===================================================')
        print(self.title)
        print('===================================================')
        for menu in self.basic_menu:
            print(menu,end='')
            menu_index = self.basic_menu.index(menu)
            if menu_index % 3 == 2:
                print('')
        print('')
        print('---------------------------------------------------')
        for i in range(0,len(self.menu_list)):
            print(f"{i+1}. {self.menu_list[i]}")
        print('')
        

    def open_page(self, menu_list = []):
        self.print_menu()
        command = input()
        #return_message = RunMenu(goal_data_field, todays_goal_list, command)
        if(command == ''):
            print('세부 내용이 없습니다.')
        elif(command == '+'):
            next_page = AddPage(selected_goal)
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeletePage(selected_goal)
            self.in_opened_pages(next_page)
        elif(command == '0'):
            pass
        elif(command == '-1'):
            DeletePage()
        elif(command == 'esc'):
            return True
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        # 같은 코드 반복, 함수화 고려
        try:
            int_command = int(command)
        except:
            pass
        else:
            if 0 < int_command:
                selected_goal = menu_list[int_command - 1]
                next_page = GoalPage(selected_goal)
                self.in_opened_pages(next_page)
        return False
        

    def in_opened_pages(self,page):
        self.opened_pages.append(page)


    def delete_page(self):
        last_index = len(self.opened_pages) - 1
        del(self.opened_pages[last_index])


class GoalPage(Page):
    def __init__(self, selected_goal):
        # 선택한 목표 데이터 중 목표 내용, 하위 목표 항목 생성
        goal_content = selected_goal.get_goal_content()
        sub_goal_list = [goal for goal in selected_goal.goal_data_field \
                         if goal.get_higher_goal_number() == selected_goal.goal_numeber]
        sub_goal_contents = [goal.get_goal_content() for goal in sub_goal_list]
        super().__init__(goal_content, sub_goal_contents)
        
class DatePage(Page):
    def __init__(self, title = '', menu_list = []):
        super().__init__(title, menu_list)
        self.basic_menu[2] = 'enter. 다음 날짜'

class MainGoalPage(Page):
    def __init__(self, title = '메인 목표', menu_list = []):
        sample_goal = Goal()
        main_goal_list = [goal for goal in sample_goal.goal_data_field if goal.get_goal_level() == 0]
        main_goal_contents = [goal.get_goal_content() for goal in main_goal_list]
        super().__init__(title, main_goal_contents)
        self.basic_menu[4] = '0. 오늘 목표로 전환'
    
class TodaysGoalPage(DatePage):
    def __init__(self, title = '오늘 목표', menu_list = []):
        sample_goal = Goal()
        todays_goal_list = [goal for goal in sample_goal.goal_data_field if goal.check_date_in_term(today)]
        todays_goal_contents = [goal.get_goal_content() for goal in todays_goal_list]
        super().__init__(title, todays_goal_contents)
        self.basic_menu[4] = '0. 메인 목표로 전환'



    
    
class EditPage(Page):
    # 제목과 기본 메뉴를 출력 페이지 앞부분에 출력
    def __init__(self, title = '', menu_list = []):
        super().__init__(title, menu_list)
        for i in range(0,3):
            del(self.basic_menu[i])

class AddPage(EditPage):
    pass
class DeletePage(EditPage):
    pass
class HelpPage(Page):
    def __init__(self):
        super().__init__('도움말')

'''
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
'''


'''
페이지 종류
1. 메인 목표 페이지
2. 메인 날짜 페이지
3. 목표 페이지
4. 날짜 페이지
5. 목표 추가 페이지
6. 날짜 추가 페이지
7. 삭제 페이지(입력 : 현재 페이지 - 메뉴)
9. 도움말 페이지
'''

