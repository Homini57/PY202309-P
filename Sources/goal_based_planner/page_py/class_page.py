#Goal 클래스는 설정페이지에서 본격적으로 쓰일 것
from goal_py.class_goal import Goal
# 페이지 클래스
class Page():
    # 필드 : 페이지 제목, 목표 레벨, 출력 메뉴 항목
    # 출력 타입( 0 : 일반 페이지, 1 : 오늘 목표 페이지, 2 : 메인 목표 페이지)
    def __init__(self, title = '',goal_level = 0, menu_list = [], type = 0):
        self.title = title
        self.goal_level = goal_level
        self.menu_list = menu_list
        self.type = type
    # 제목과 기본 메뉴를 출력 페이지 앞부분에 출력
    def print_front(self):
        if(self.type == 0):
            minus_one = '이전으로    '
            zero = '메인으로       '
        elif(self.type == 1):
            minus_one = '프로그램 종료'
            zero = '메인 목표로 전환'
        elif(self.type == 2):
            minus_one = '프로그램 종료'
            zero = '오늘 목표로 전환'
        else: # 실수로 다른 값을 입력하여도 정상적으로 작성하도록 예외처리 
            minus_one = ''
            zero = ''
        print('')
        print('===================================================')
        print(self.title)
        print('===================================================')
        print( ' +. 추가           -. 삭제           enter. 세부 내용') #To EditPage
        print(f'-1. {minus_one}   0. {zero}     ?. 도움말')
        print('---------------------------------------------------')

    # 메뉴 출력
    def print_menu(self):
        for i in range(0,len(self.menu_list)):
            print(f"{i+1}. {self.menu_list[i]}")
        print('')

            


    
    
class EditPage(Page):
    def __init__(self, title = '', sub_goal_list = [], type = '+'):
        if (type == '+'):
            super.__init__(title, sub_goal_list, -1)
    # 제목과 기본 메뉴를 출력 페이지 앞부분에 출력
    def print_front(self):
        print('---------------------------------------------------')
        print(self.title)
        print('---------------------------------------------------')
        print('-1. 이전으로       0. 메인으로            ?. 도움말')
        print('---------------------------------------------------')

    

class HelpPage(Page):
    def __init__(self):
        super.__init__('도움말')



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

