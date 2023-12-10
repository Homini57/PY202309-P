#날짜 클래스와 목표 클래스, 페이지 클래스를 하나의 패키지로 통합?

#Goal 클래스는 설정페이지에서 본격적으로 쓰일 것
from goal_py.class_date import Today
from goal_py.class_goal import Goal, GoalField, to_digit_number
# 페이지 클래스
class Page():
    opened_pages = []
    # 필드 : 페이지 제목, 목표 레벨, 출력 메뉴 항목
    def __init__(self, title = '', menu_list = []):
        self.title = title
        self.menu_list = menu_list
        self.basic_menu = [' +. 추가           ','-. 삭제           ','enter. 세부 내용', \
                           '-1. 이전으로       ','0. 메인으로       ','    ?. 도움말  ', \
                            'esc.프로그램 종료']
    # 페이지 내용 업데이트
    def update_page(self):
        self.__init__(self.title, self.menu_list)
    # 페이지 출력
    def print_page(self):
        
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
        print('\n')
    # 페이지 열기(상속)
    def open_page(self):
        pass
    # 열린 페이지에 추가
    def in_opened_pages(self,page):
        self.opened_pages.append(page)
    # 마지막 페이지 삭제
    def delete_page(self):
        last_index = len(self.opened_pages) - 1
        if last_index > 0:
            del self.opened_pages[last_index]
        else:
            print('이전 페이지가 없습니다.')
# 매우 중요! : 0 입력시 실행될 페이지의 타입을 입력받고, 오픈페이지 메서드를 통합하는 방법 고려

# 목표 기반 페이지
class GoalPage(Page):
    def __init__(self, selected_goal):
        # 선택한 목표 데이터 중 목표 내용, 하위 목표 항목 생성
        self.goal = selected_goal
        goal_content = selected_goal.get_content()
        self.sub_goal_list = [goal for goal in GoalField().data \
                         if goal.get_higher_goal_number() == selected_goal.goal_number]
        sub_goal_contents = [goal.get_content() for goal in self.sub_goal_list]
        super().__init__(goal_content, sub_goal_contents)
    # 페이지 업데이트
    def update_page(self):
        self.__init__(self.goal)
    # 페이지 열기
    def open_page(self):
        self.print_page()
        command = input()
        if(command == ''):
            pass
        elif(command == '+'):
            next_page = AddGoalPage(self.goal)
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteGoalPage(self.goal)
            self.in_opened_pages(next_page)
        # 0 입력시 오늘 목표 페이지 생성
        elif(command == '0'):
            next_page = MainGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        # esc 입력시 프로그램 종료 값 반환
        elif(command == 'esc'):
            terminate = True
            return terminate
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        else:
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
            print('잘못 입력하였습니다.')
        terminate = False
        return terminate

class MainGoalPage(GoalPage):
    def __init__(self):
        self.goal = Goal()
        super().__init__(self.goal)
        del self.sub_goal_list[0]
        del self.menu_list[0]
        #main_goal_list = [goal for goal in GoalField().data if goal.get_level() == 0]
        #main_goal_contents = [goal.get_content() for goal in main_goal_list]
        self.basic_menu[4] = '0. 오늘 목표로 전환'
    def update_page(self):
        self.__init__()

    def open_page(self):
        self.print_page()
        command = input()
        if(command == ''):
            print('세부 내용이 없습니다.')
        elif(command == '+'):
            next_page = AddGoalPage(self.goal)
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteGoalPage(self.goal)
            self.in_opened_pages(next_page)
        # 0 입력시 오늘 목표 페이지 생성
        elif(command == '0'):
            pass #next_page = TodaysGoalPage()
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            terminate = True
            return terminate
        # 1 이상의 정수를 입력받을 경우 해당 목표 페이지 열기
        else:
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
            print('잘못 입력하였습니다.')
        terminate = False
        return terminate

# 목표 추가, 삭제 페이지
class EditGoalPage(GoalPage):

    def __init__(self, goal):
        super().__init__(goal)
        # 이 조건은 왜 self.goal == Goal()이 안되는 건지?
        # 메인 목표 페이지에서 실행시 첫 하위 목표(메인 목표를 나타내는 목표) 삭제
        if self.goal.goal_number == Goal().goal_number:
            del self.sub_goal_list[0]
            del self.menu_list[0]
        # 기본 메뉴 : -1, 0, ?, esc
        for i in range(0,3):
            del self.basic_menu[0]
    # 페이지 업데이트
    def update_page(self):
        self.__init__(self.goal)
    # 편집 제목 출력 + 페이지 출력
    def print_page(self, edit_title):
        self.title = edit_title + '\n\n' + self.title
        super().print_page()



# 목표 추가 페이지
class AddGoalPage(EditGoalPage):
    # 페이지 열기
    def open_page(self):
        # 페이지 출력
        self.print_page('목표 추가')
        command = input()
        # 0 입력시 메인 목표 페이지로 이동
        if(command == '0'):
            next_page = MainGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            terminate = True
            return terminate
        # 입력받은 내용을 목표에 추가
        else:
            # 마지막 하위 목표 탐색
            current_goal_number = self.goal.goal_number
            last_sub_goal_index = len(self.sub_goal_list) - 1
            # 목표 데이터 필드 상 마지막 하위 목표의 인덱스 계산, 새 목표의 마지막 번호 계산
            # 하위 목표가 존재할 경우 생성 방법
            if last_sub_goal_index >= 0:
                last_sub_goal = self.sub_goal_list[last_sub_goal_index]
                goal_level = last_sub_goal.get_goal_level()
                last_part_number = last_sub_goal.get_part_number(goal_level)
                new_part_number = to_digit_number(int(last_part_number)+1, last_sub_goal.DIGIT_SIZE)
                last_index = GoalField().data.index(last_sub_goal)
            # 하위 목표가 없는 경우 현재 페이지의 목표의 인덱스로 계산
            else:
                new_part_number = '01'
                last_index = GoalField().data.index(self.goal)
            # 새 목표의 목표 번호 계산
            new_goal_number = current_goal_number + new_part_number
            # 위치에 맞게 데이터 필드에 새 목표 입력, 내용 필드에 내용 추가
            GoalField().data.insert(last_index+1,Goal(new_goal_number))
            GoalField().contents[new_goal_number] = command
        terminate = False
        return terminate

        '''
        else:
            current_goal_number = self.goal.goal_number
            last_goal = None
            # 마지막 하위 목표 탐색
            for goal in GoalField().data:
                if goal.get_higher_goal_number() == current_goal_number:
                    last_goal = goal
            # 하위 목표가 존재하면 
            if last_goal != None:
                goal_level = last_goal.get_goal_level()
                last_part_number = last_goal.get_part_number(goal_level)
                if last_part_number != '':
                    new_part_number = to_digit_number(int(last_part_number)+1, last_goal.DIGIT_SIZE)
                else:
                    new_part_number = '01'
                new_goal_number = current_goal_number + new_part_number
                last_index = GoalField().data.index(last_goal)
            # 하위 목표가 없는 경우, 1번 하위 목표 추가, 입력받은 내용 저장
            else:
                new_goal_number = current_goal_number + '01'
                last_index = GoalField().data.index(self.goal)
            GoalField().data.insert(last_index+1,Goal(new_goal_number))
            GoalField().contents[new_goal_number] = command
        
        '''
# 목표 삭제 페이지
class DeleteGoalPage(EditGoalPage):
    # 페이지 열기
    def open_page(self):
        self.print_page('목표 삭제')
        command = input()
        
        # 하위 목표가 존재하는지 확인
        if(len(self.sub_goal_list) == 0):
            print('목표가 존재하지 않습니다.')
            self.delete_page()
        # 0 입력시 메인 목표 페이지로 이동
        elif(command == '0'):
            next_page = MainGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            terminate = True
            return terminate
        
        else:
            try:
                int_command = int(command)
            except:
                pass
            else:
                # 하위 목표 리스트의 번호 내의 정수 입력시
                if (0 < int_command and int_command <= len(self.menu_list)):
                    # 정말 삭제할지 확인받기
                    do_delete = input('정말 목표를 삭제하시겠습니까? (Y/N): ').lower()
                    if do_delete == 'y':
                        selected_goal = self.sub_goal_list[int_command - 1]
                        goal_level = selected_goal.get_goal_level()
                        # 해당 목표와 모~ 든 하위 항목(해당 목표의 레벨까지 목표번호가 동일한 목표)들을 삭제
                        for goal in GoalField().data:
                            check_number = goal.goal_number[0:(goal_level + 1) * goal.DIGIT_SIZE]
                            if check_number == selected_goal.goal_number:
                                GoalField().data.remove(goal)
                                GoalField().contents.pop(goal.goal_number)
                        terminate = False
                        return terminate
                    elif do_delete == 'n':
                        terminate = False
                        return terminate
            # 잘못 입력시
            print('잘못 입력하였습니다.')
        terminate = False
        return terminate
        








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

