#날짜 클래스와 목표 클래스, 페이지 클래스를 하나의 패키지로 통합?
from goal_py.class_date import *
#Goal 클래스는 설정페이지에서 본격적으로 쓰일 것
from goal_py.class_date import Today
from goal_py.class_goal import Goal, GoalField, to_digit_number
from .processing_text import extract_text_and_date, extract_term_from_text
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




# 목표 기반 페이지
class GoalPage(Page):
    def __init__(self, selected_goal):
        # 선택한 목표 데이터 중 목표 내용, 하위 목표 항목 생성
        self.goal = selected_goal
        goal_content = selected_goal.get_content()
        self.sub_goal_list = GoalField().get_sub_goal_list(self.goal)
        '''
        업데이트 전 하위 목표 생성 코드
        self.sub_goal_list = [goal for goal in GoalField().data
                         if goal.get_higher_goal_number() == selected_goal.goal_number]
        '''
        
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
            next_page = GoalInformationPage(self.goal)
            self.in_opened_pages(next_page)
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
                date = extract_text_and_date(command)
                if(date != Date()):
                    next_page = DatePage(date)
                    self.in_opened_pages(next_page)
                    return False
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
            next_page = TodaysGoalPage()
            self.in_opened_pages(next_page)
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
                date = extract_text_and_date(command)
                if(date != Date()):
                    next_page = DatePage(date)
                    self.in_opened_pages(next_page)
                    return False
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
            GoalField().set_sub_goal(self.goal,Goal(), command)

            
        terminate = False
        return terminate

# 목표 삭제 페이지
class DeleteGoalPage(EditGoalPage):
    # 페이지 열기
    def open_page(self):
        self.print_page('목표 삭제')
        if(len(self.sub_goal_list) == 0):
            print('목표가 존재하지 않습니다.')
            self.delete_page()
            terminate = False
            return terminate
        
        command = input()
        # 하위 목표가 존재하는지 확인
        
        # 0 입력시 메인 목표 페이지로 이동
        if(command == '0'):
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
    def __init__(self, date = Date()):
        # 입력 날짜 저장
        self.date = date
        # 제목 = 월, 일, 요일
        date_title = str(date.month) + '월'+ str(date.day) +'일' + date.get_weekday()
        # 해당 날짜의 목표들 저장
        self.goal_list = [goal for goal in GoalField().data \
                         if goal.date.month == date.month and goal.date.day == date.day]
        goal_content = [goal.get_content() for goal in self.goal_list]
        # 초기화
        super().__init__(date_title, goal_content)
        self.basic_menu[2] = 'enter. 다음 날짜'

    def update_page(self):
        self.__init__(self.date)
    
    def open_page(self):
        self.print_page()
        command = input()

        # 기본 메뉴 선택시
        if(command == ''):
            next_date = self.date.get_next_date()
            next_page = DatePage(next_date) 
            self.in_opened_pages(next_page)
        elif(command == '+'):
            next_page = AddDatePage(self.goal) 
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteDatePage(self.goal) 
            self.in_opened_pages(next_page)
        # 0 입력시 오늘 목표 페이지 생성
        elif(command == '0'):
            next_page = TodaysGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        # esc 입력시 프로그램 종료 값 반환
        elif(command == 'esc'):
            terminate = True
            return terminate
        else:
            try:
                int_command = int(command)
            except:
                date = extract_text_and_date(command)
                if(date != Date()):
                    next_page = DatePage(date)
                    self.in_opened_pages(next_page)
                    return False
            else:
                if (0 < int_command and int_command <= len(self.menu_list)):
                    selected_goal = self.goal_list[int_command - 1]
                    next_page = GoalPage(selected_goal)
                    self.in_opened_pages(next_page)
                    return False
            print('잘못 입력하였습니다.')
        terminate = False
        return terminate
class WeekPage(Page):
    def __init__(self, week = 1, month = datetime.now().month):
        # 입력 정보 저장
        self.month = month
        self.week = week
        # 제목 = 월, 주
        date_title = str(month) + '월' + str(week) + '주차'
        self.goal_list = [[None] * 7 for i in range(0, 7)]
        for goal in GoalField().data:
            if goal.date.month== month and goal.date.week == week:
                weekday = goal.date.weekday()
                self.goal_list[weekday].append(goal)
        super().__init__(date_title)
        self.basic_menu[2] = 'enter. 다음 주'
    def update_page(self):
        self.__init__(self.week, self.month)
    def open_page(self):
        self.print_page()
        command = input()

        # 기본 메뉴 선택시
        if(command == ''):
            pass
        elif(command == '+'):
            next_page = AddDatePage(self.goal) # 날짜 입력
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteDatePage(self.goal) # 날짜 입력
            self.in_opened_pages(next_page)
        # 0 입력시 오늘 목표 페이지 생성
        elif(command == '0'):
            next_page = TodaysGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        # esc 입력시 프로그램 종료 값 반환
        elif(command == 'esc'):
            terminate = True
            return terminate

class TodaysGoalPage(DatePage):
    def __init__(self):
        super().__init__(Today())
        title = '오늘 목표'
        self.basic_menu[2] = 'enter. 내일'
        self.basic_menu[4] = '0. 메인 목표로 전환'
    def update_page(self):
        self.__init__()
    def open_page(self):
        self.print_page()
        command = input()

        # 기본 메뉴 선택시
        if(command == ''):
            next_date = self.date.get_next_date()
            next_page = DatePage(next_date) 
            self.in_opened_pages(next_page)
        elif(command == '+'):
            next_page = AddDatePage(self.date) # 날짜 입력
            self.in_opened_pages(next_page)
        elif(command == '-'):
            next_page = DeleteDatePage(self.date) # 날짜 입력
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
        else:
            try:
                int_command = int(command)
            except:
                date = extract_text_and_date(command)
                if(date != Date()):
                    next_page = DatePage(date)
                    self.in_opened_pages(next_page)
                    return False
            else:
                if (0 < int_command and int_command <= len(self.menu_list)):
                    selected_goal = self.goal_list[int_command - 1]
                    next_page = GoalPage(selected_goal)
                    self.in_opened_pages(next_page)
                    return False
            print('잘못 입력하였습니다.')
        terminate = False
        return terminate

# 날짜 페이지에서 목표 추가, 삭제
class EditDatePage(DatePage):
    def __init__(self, date = Date()):
        super().__init__(date)
        # 기본 메뉴 : -1, 0, ?, esc
        for i in range(0, 3):
            del self.basic_menu[0]
    # 페이지 업데이트
    def update_page(self):
        self.__init__(self.date)
    # 편집 제목 출력 + 페이지 출력
    def print_page(self, edit_title):
        self.title = edit_title + '\n\n' + self.title
        super().print_page()

# 날짜 페이지에서 목표 추가
class AddDatePage(EditDatePage):
    def open_page(self):
        # 페이지 출력
        self.print_page('목표 추가')
        command = input()
        # 0 입력시 오늘 목표 페이지로 이동
        if(command == '0'):
            next_page = TodaysGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            terminate = True
            return terminate
        else:
            # 페이지 날짜를 날짜로 하는 목표 생성
            last_number = 0
            for goal in GoalField().data:
                if goal.get_goal_level() == 0:
                    last_number += 1
            goal_number = to_digit_number(last_number + 1, Goal().DIGIT_SIZE)
            GoalField().data.append(Goal(goal_number, self.date))
            GoalField().contents[goal_number] = command
        terminate = False
        return terminate

# 날짜 페이지에서 목표 삭제
class DeleteDatePage(EditDatePage):
    def open_page(self):
        # 페이지 출력
        self.print_page('목표 삭제')
        if(len(self.goal_list) == 0):
            print('목표가 존재하지 않습니다.')
            self.delete_page()
            terminate = False
            return terminate
        command = input()
        # 0 입력시 오늘 목표 페이지로 이동
        if(command == '0'):
            next_page = TodaysGoalPage()
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
                        selected_goal = self.goal_list[int_command - 1]
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

class GoalInformationPage(Page):
    def __init__(self, goal = Goal()):
        self.goal = goal
        goal_content = goal.get_content()
        higher_goal = GoalField.contents[goal.get_higher_goal_number()]
        date = goal.date.get_date_string()
        deadline = goal.deadline.get_date_string()
        term = str(goal.term)
        achievment = str(goal.achivement)
        self.information_menu = {'상위 목표':higher_goal, '날짜':date,'기한':deadline, '반복':term, '달성량':achievment}
        super().__init__(goal_content)
        # 기본 메뉴 : -1, 0, ?, esc
        for i in range(0,3):
            del self.basic_menu[0]

    def update_page(self):
        self.__init__(self.goal)
    # 편집 제목 출력 + 페이지 출력
    def print_page(self, edit_title):
        self.title = edit_title + '\n\n' + self.title
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
        i = 1
        for menu in self.information_menu.items():
            print(f"{i}. {menu[0]} : {menu[1]}")
            i += 1
        print('\n')
    
    def open_page(self):
        self.print_page('목표 정보')
        command = input()
        if(command == '0'):
            next_page = MainGoalPage()
            self.in_opened_pages(next_page)
        elif(command == '-1'):
            self.delete_page()
        elif(command == 'esc'):
            terminate = True
            return terminate
        elif (command == '1'):
            self.set_higher_goal()
        elif (command == '2'):
            self.set_date()
        elif (command == '3'):
            self.set_deadline()
        elif (command == '4'):
            self.set_term()
        else:
            print('잘못 입력하였습니다.')
        

    # 상위 목표 설정
    def set_higher_goal(self):
        print('---------------------------------------------------')
        higher_goal_content = input("\n상위 목표 변경 : ")
        try:
            higher_goal_number = GoalField().get_goal_number(higher_goal_content)
            higher_goal = GoalField().get_goal(higher_goal_number)
            GoalField().set_sub_goal(higher_goal, self.goal, self.goal.get_content())
        except:
            print('입력한 목표가 존재하지 않습니다.')
    # 날짜 성정
    def set_date(self):
        print('---------------------------------------------------')
        input_text = input("\n날짜 변경 : ")
        date = extract_text_and_date(input_text)
        if(date != Date()):
            self.goal.date = date
        else:
            print('날짜를 인식하지 못하였습니다.')
    # 기한 설정
    def set_deadline(self):
        print('---------------------------------------------------')
        input_text = input("\n기한 변경 : ")
        date = extract_text_and_date(input_text)
        if(date != Date()):
            self.goal.deadline = date
        else:
            print('기한을 인식하지 못하였습니다.')
    # 기간 설정
    def set_term(self):
        print('---------------------------------------------------')
        input_text = input("\n주기 변경 : ")
        try:
            int_text = int(input_text)
        except:
            pass
        else:
            self.goal.term = term
        term = extract_term_from_text(input_text)
        if(term != 0):
            self.goal.term = term
        else:
            print('주기를 인식하지 못하였습니다.')
    
        
class HelpPage(Page):
    def __init__(self):
        super().__init__('도움말')
