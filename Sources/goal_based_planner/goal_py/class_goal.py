from goal_py.class_date import Date
import csv

class Goal():
    DIGIT_SIZE = 2    #목표 번호의 단위 자릿수
    #goal_contents_field = {}

    def __init__(self, goal_number = '', date:Date = Date(), deadline:Date = Date(), term = 0, achivement =0.0):
        
        # 목표 번호와 날짜에 0 입력시 없음으로 인식하도록
        # 목표 번호는 문자열로 저장하여 마지막 자리의 0을 포함할 수 있도록 하기
        # 목표 번호 - 목표 내용 표를 따로 저장.
        self.goal_number = goal_number # 오른쪽부터 2자리 수씩 상위-> 하위 ex. 120302 : 02번 메인목표 - 03번 하위목표 - 12번 하위목표
        # self.higher_goal = 0 #goal 클래스 입력
        # self.sub_goal = []#목표 번호 입력, 필요한가?
        # self.is달성 = False #필요한가?
        
        self.date = date # date클래스
        # 디폴트값 = 오늘날짜
        self.deadline = deadline #date클래스
        self.term = term #주기 클래스 : 요일별, 격일, 격주, 격월
        self.achivement = achivement #정수? 부동소수형
        self.현재achivement = 0.0
       
        

        # 처음에 파일을 읽어서 리스트로 저장해 놓은 후
        #리스트에 접근하여 수정한 후
        #프로그램을 종료할 때 파일을 열어서 저장한 후 종료하기
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

    def get_goal(self, goal_number): #번호를 받아 목표 반환
        for goal in self.data:
            if goal.goal_number == goal_number:
                return goal
    #def getGoal(contents): 내용을 받아 해당하는 목표 리스트? 반환? (내용이 중복될 수 있으므로)
    #def getGoal(date) : 날짜를 받아 해당하는 목표 리스트 반환
    
if __name__ == '__main__':
    for data in GoalField().data:
        print(data.goal_number)