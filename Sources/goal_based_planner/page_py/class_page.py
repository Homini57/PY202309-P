#Goal 클래스는 설정페이지에서 본격적으로 쓰일 것
from goal_py.class_date import Today
from goal_py.class_goal import Goal, GoalField, to_digit_number
# 페이지 클래스
class Page():
    opened_pages = []
    # 필드 : 페이지 제목, 목표 레벨, 출력 메뉴 항목
    # 출력 타입( 0 : 일반 페이지, 1 : 오늘 목표 페이지, 2 : 메인 목표 페이지)
    def __init__(self, title = '', menu_list = []):
        self.title = title
        self.menu_list = menu_list
        self.basic_menu = [' +. 추가           ','-. 삭제           ','enter. 세부 내용', \
                           '-1. 이전으로       ','0. 메인으로       ','    ?. 도움말  ', \
                            'esc.프로그램 종료']
    def update_page(self):
        self.__init__(self.title, self.menu_list)
    # 제목과 기본 메뉴를 출력 페이지 앞부분에 출력
    # C++의 가상함수처럼 이것도 상속으로 다르게 정의하고 같은 페이지 리스트에 저장할 수 있을까?
    def print_menu(self):
        
        print('')
        print('===================================================')
        for menu in self.basic_menu:
            print(menu,end='')
            menu_index = self.basic_menu.index(menu)
            if menu_index % 3 == 2:
                print('')
        print('')
        print('---------------------------------------------------')
        print(self.title)
        print('---------------------------------------------------')
        for i in range(0,len(self.menu_list)):
            print(f"{i+1}. {self.menu_list[i]}")
        print('')
        
    def open_page(self):
        pass
    
        

    def in_opened_pages(self,page):
        self.opened_pages.append(page)


    def delete_page(self):
        last_index = len(self.opened_pages) - 1
        if last_index > 0:
            del(self.opened_pages[last_index])
        else:
            print('이전 페이지가 없습니다.')


class GoalPage(Page):
    def __init__(self, selected_goal):
        # 선택한 목표 데이터 중 목표 내용, 하위 목표 항목 생성
        self.goal = selected_goal
        goal_content = selected_goal.get_content()
        self.sub_goal_list = [goal for goal in GoalField().data \
                         if goal.get_higher_goal_number() == selected_goal.goal_number]
        sub_goal_contents = [goal.get_content() for goal in self.sub_goal_list]
        super().__init__(goal_content, sub_goal_contents)

    def update_page(self):
        self.__init__(self.goal)

    def open_page(self):
        self.print_menu()
        command = input()
        #return_message = RunMenu(goal_data_field, todays_goal_list, command)
        if(command == ''):
            pass
        elif(command == '+'):
            next_page = AddGoalPage(self.goal)
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteGoalPage(self.goal)
            self.in_opened_pages(next_page)
        elif(command == '0'):
            next_page = MainGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            return True
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        # 같은 코드 반복, 함수화 고려
        try:
            int_command = int(command)
        except:
            pass
        else:
            if (0 < int_command and int_command <= len(self.menu_list)+ 1):
                selected_goal = self.sub_goal_list[int_command - 1]
                next_page = GoalPage(selected_goal)
                self.in_opened_pages(next_page)
        return False

class MainGoalPage(GoalPage):
    def __init__(self):
        self.goal = Goal()
        super().__init__(self.goal)
        del(self.sub_goal_list[0])
        del(self.menu_list[0])
        #main_goal_list = [goal for goal in GoalField().data if goal.get_level() == 0]
        #main_goal_contents = [goal.get_content() for goal in main_goal_list]
        self.basic_menu[4] = '0. 오늘 목표로 전환'
    def update_page(self):
        self.__init__()

    def open_page(self):
        self.print_menu()
        command = input()
        #return_message = RunMenu(goal_data_field, todays_goal_list, command)
        if(command == ''):
            print('세부 내용이 없습니다.')
        elif(command == '+'):
            next_page = AddGoalPage(self.goal)
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteGoalPage(self.goal)
            self.in_opened_pages(next_page)
        elif(command == '0'):
            pass #next_page = MainDatePage()
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            return True
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        # 같은 코드 반복, 함수화 고려
        try:
            int_command = int(command)
        except:
            pass
        else:
            if (0 < int_command and int_command <= len(self.menu_list)):
                selected_goal = self.sub_goal_list[int_command - 1]
                next_page = GoalPage(selected_goal)
                self.in_opened_pages(next_page)
        return False

class EditGoalPage(GoalPage):
    # 제목과 기본 메뉴를 출력 페이지 앞부분에 출력
    def __init__(self, goal):
        super().__init__(goal)
        for i in range(0,3):
            del(self.basic_menu[0])
    def update_page(self):
        self.__init__(self.goal)
    def print_menu(self, edit_title):
        for menu in self.basic_menu:
            print(menu,end='')
            menu_index = self.basic_menu.index(menu)
            if menu_index % 3 == 2:
                print('')
        print('')
        print('---------------------------------------------------')
        print(f'{edit_title} : ', end = '')
    

        # self.title이 내용인 목표의 번호를 필드에서 찾기 (GetGoal(contents).goal_number 활용)
        # 목표 번호의 하위 항목 중 가장 마지막 번호 찾기 + (위의 goal_number == Goal().get_higher_goal_number()인 Goal()클래스 찾기)
        # 해당 번호의 각 필드에 새로운 목표 생성, 입력을 내용에 저장(GoalField().data.append(Goal(goal_number))), GoalField().contents[goal_number] = contents)
        return False
class AddGoalPage(EditGoalPage):
    def open_page(self):
        self.print_menu('목표 추가')
        command = input()
        #return_message = RunMenu(goal_data_field, todays_goal_list, command)
        if(command == '0'):
            next_page = MainGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            return True
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        # 같은 코드 반복, 함수화 고려
        else:
            current_goal_number = self.goal.goal_number
            last_goal = None
            for goal in GoalField().data:
                if goal.get_higher_goal_number() == current_goal_number:
                    last_goal = goal
            if last_goal != None:
                goal_level = last_goal.get_goal_level()
                last_part_number = last_goal.get_part_number(goal_level)
                if last_part_number != '':
                    new_part_number = to_digit_number(int(last_part_number)+1, 2)
                else:
                    new_part_number = '01'
                new_goal_number = current_goal_number + new_part_number
                last_index = GoalField().data.index(last_goal)
            else:
                new_goal_number = current_goal_number + '01'
                last_index = GoalField().data.index(self.goal)
            GoalField().data.insert(last_index+1,Goal(new_goal_number))
            GoalField().contents[new_goal_number] = command
class DeleteGoalPage(EditGoalPage):
    pass
        
class DatePage(Page):
    def __init__(self, title = '', menu_list = []):
        super().__init__(title, menu_list)
        self.basic_menu[2] = 'enter. 다음 날짜'

    def update_page(self):
        self.__init__(self.self.title, self.menu_list)


    
class TodaysGoalPage(DatePage):
    def __init__(self, title = '오늘 목표', menu_list = []):
        sample_goal = Goal()
        todays_goal_list = [goal for goal in GoalField().data if goal.check_date_in_term(Today())]
        todays_goal_contents = [goal.get_content() for goal in todays_goal_list]
        super().__init__(title, todays_goal_contents)
        self.basic_menu[4] = '0. 메인 목표로 전환'

    def update_page(self):
        self.__init__(self.self.title, self.menu_list)



    
    


class EditDatePage(DatePage):
    pass
class AddDatePage(EditDatePage):
    pass
class DeleteDatePage(EditDatePage):
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
    goal_content = opened_goal.get_content()
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

