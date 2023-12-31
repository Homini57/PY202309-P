# 모듈 이름은 goal_module로 수정?
#패키지를 풀고 날짜 클래스와 목표 클래스를 분리?

from goal_py.class_date import Date
import csv

class Goal():
    DIGIT_SIZE = 2    #목표 번호의 단위 자릿수
    #goal_contents_field = {}

    def __init__(self, goal_number = '', date:Date = Date(), deadline:Date = Date(), term = 0, achivement =0.0):
        
        self.goal_number = goal_number # 오른쪽부터 2자리 수씩 상위-> 하위 ex. 120302 : 02번 메인목표 - 03번 하위목표 - 12번 하위목표
        self.date = date 

        self.deadline = deadline 
        self.term = term
        self.achivement = achivement
        self.achivement_now = 0.0
       
        
        # 목표 레벨 = 목표 번호 개수 -1
    def get_goal_level(self):
        digits_number = len(self.goal_number)
        goal_level = digits_number // self.DIGIT_SIZE - 1
        return goal_level
        #자릿수 / 2 - 1

        # 입력 레벨의 번호 반환 메서드
    def get_part_number(self, level):
        start_index = level * self.DIGIT_SIZE
        '001020(level)0...(goal_level*2)0'
        part_number = self.goal_number[start_index : start_index + self.DIGIT_SIZE]
        return part_number
    
        #상위 목표의 번호 반환 메서드
    def get_higher_goal_number(self):
        end_index = len(self.goal_number) - self.DIGIT_SIZE
        higer_goal_number = self.goal_number[0 : end_index]
        return higer_goal_number

            # 맨 앞 두자리수 제외한 숫자

        # def 현재achivement입력(self):
    def set_content(self, content):
        GoalField().contents[self.goal_number] = content
    # goal_contents를 매개변수로 받아야 할까?
    def get_content(self):
        goal_content = GoalField().contents[self.goal_number]
        return goal_content
    
        # 이 날짜에 반복해야 하는지 확인
    def check_date_in_term(self, date):
        deadline_month = self.deadline.month
        deadline_day = self.deadline.day
        if self.deadline.day == 0:
            deadline_month = 13
            deadline_day = 32

        if self.date.month <= date.month and date.month <= self.deadline.month:
            if self.date.day <= date.day and date.day <= self.deadline.day:
                return True

def read_data_file():
    data_field = []
    file_path = 'goal_csv/goal_data.csv'
    # goal_number, date, deadline, term, achivement
    with open(file_path, 'r', encoding ='utf-8') as file:
        try:
            reader = csv.reader(file)

            for row in reader:
                # goal class arguement : goal_number, date, deadline, term, achivement
                goal_instance = Goal(row[0], Date(int(row[1]), int(row[2])),\
                                      Date(int(row[3]), int(row[4])), int(row[5]), float(row[6]))
                data_field.append(goal_instance)
        except IndexError:
            print('1 : 데이터 로드(인덱스 에러) 이상')
        except:
            print('1 : 데이터 로드에 이상이 생겼습니다.')
        return data_field
#목표들 저장
def write_data_file(data_field):
    try:
        file_path = 'goal_csv/goal_data.csv'
        with open(file_path, 'w', encoding ='utf-8', newline='') as file:
            writer = csv.writer(file)
            data_list = []
            for goal in data_field:
                data = [goal.goal_number, goal.date.month, goal.date.day,\
                        goal.deadline.month, goal.deadline.day, goal.term,\
                        goal.achivement]
                data_list.append(data)
            writer.writerows(data_list)
    except:
       print('1 : 데이터 저장에 이상이 있습니다.')
        
#목표 번호와 내용 딕셔너리 생성
def read_contents_file():
    try:
        contents_field = {}
        file_name = 'goal_csv/goal_contents.csv'
        with open(file_name, 'r', encoding ='utf-8') as file: 
            reader = csv.reader(file)
            for row in reader:
                contents_field[row[0]] = row[1]
    except:
        '2 : 데이터 로드에 이상이 생겼습니다.'
    return contents_field

def write_contents_file(contents_field):
    try:
        file_name = 'goal_csv/goal_contents.csv'
        with open(file_name, 'w', encoding ='utf-8', newline='') as file:
            writer = csv.writer(file)
            contents_lists = [[key] + [value] for key, value in contents_field.items()]
            writer.writerows(contents_lists)
    except:
        '2 : 데이터 저장에 이상이 있습니다.'

def to_digit_number(number, digit_size):
    digit_number = ''
    for i in range(0, digit_size - len(str(number))):
        digit_number += '0'
    digit_number += str(number)
    return digit_number

class GoalField():
    data = read_data_file()
    contents = read_contents_file()

    def get_goal_number(self, content):
        for goal_number in self.contents:
            if self.contents[goal_number] == content:
                return goal_number

    def get_goal(self, goal_number): #번호를 받아 목표 반환
        for goal in self.data:
            if goal.goal_number == goal_number:
                return goal
            
    def get_sub_goal_list(self, selected_goal):
        sub_goal_list = []
        for goal in self.data:
                if goal.goal_number == '':
                    continue
                elif goal.get_higher_goal_number() == selected_goal.goal_number:
                    sub_goal_list.append(goal)
        return sub_goal_list
    def set_sub_goal (self, higher_goal, sub_goal = Goal(), sub_goal_content = ''):
        current_goal_number = higher_goal.goal_number
        sub_goal_list = self.get_sub_goal_list(higher_goal)
        last_sub_goal_index = len(sub_goal_list) - 1
        # 목표 데이터 필드 상 마지막 하위 목표의 인덱스 계산, 새 목표의 마지막 번호 계산
        # 하위 목표가 존재할 경우 생성 방법
        if last_sub_goal_index >= 0:
            last_sub_goal = sub_goal_list[last_sub_goal_index]
            goal_level = last_sub_goal.get_goal_level()
            last_part_number = last_sub_goal.get_part_number(goal_level)
            new_part_number = to_digit_number(int(last_part_number)+1, last_sub_goal.DIGIT_SIZE)
            last_index = self.data.index(last_sub_goal)
        # 하위 목표가 없는 경우 현재 페이지의 목표의 인덱스로 계산
        else:
            new_part_number = '01'
            last_index = self.data.index(higher_goal)
        # 새 목표의 목표 번호 계산
        new_goal_number = current_goal_number + new_part_number
        if( sub_goal.goal_number != ''):
            sub_sub_goal_list = self.get_sub_goal_list(sub_goal)
            del self.contents[sub_goal.goal_number]
            sub_goal.goal_number = new_goal_number
            self.contents[new_goal_number] = sub_goal_content
            for sub_sub_goal in sub_sub_goal_list:
                GoalField().set_sub_goal(sub_goal, sub_sub_goal, sub_sub_goal.get_content())
        # 위치에 맞게 데이터 필드에 새 목표 입력, 내용 필드에 내용 추가
        else:
            self.data.insert(last_index+1,Goal(new_goal_number))
            self.contents[new_goal_number] = sub_goal_content
    #def getGoal(contents): 내용을 받아 해당하는 목표 리스트? 반환? (내용이 중복될 수 있으므로)
    #def getGoal(date) : 날짜를 받아 해당하는 목표 리스트 반환
    
if __name__ == '__main__':
    for data in GoalField().data:
        print(data.goal_number)