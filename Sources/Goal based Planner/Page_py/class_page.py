from goal_py.class_goal_n_info import *
class Page():
    def __init__(self, name :str = '', menu_list :list = [], type = 0):
        self.name = name
        self.menu_list = menu_list
        self.type = type
    
    def PrintFront(self):
        if(type == 0):
            minus_one = '이전으로    '
            zero = '메인으로       '
        elif(type == 1):
            minus_one = '프로그램 종료'
            zero = '메인 목표로 전환'
        elif(type == 2):
            minus_one = '프로그램 종료'
            zero = '오늘 목표로 전환'
        else: # 실수로 다른 값을 입력하여도 정상적으로 작성하도록 예외처리 
            minus_one = ''
            zero = ''
        print('=================================================')
        print( ' +. 추가         -. 삭제           enter. 세부 내용') #To EditPage
        print(f'-1. {minus_one} 0. {zero}     ?. 도움말')
        print('-------------------------------------------------')
        print(self.name)

    def PrintMenu(self):
        for i in range(0,len(self.menu_list)):
            print(f"{i+1}. {self.menu_list[i]}")

    
    
class EditPage(Page):
    def __init__(self, menu_list :list = [], type = '+'):
        if (type == '+'):
            super.__init__('목표 추가', menu_list, -1)
    def PrintFront(self):
        print('=================================================')
        print('-1. 이전으로     0. 메인으로            ?. 도움말')
        print('-------------------------------------------------')
        print(self.name)

    

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

