from goal_py.class_date import Date
from goal_py.class_goal import Goal
import csv
# 리스트를 딕셔너리화하기
    
def read_data_file():
    data_field = []
    file_path = 'goal_csv/goal_data.csv'
    # goal_number, date, deadline, period, achivement
    with open(file_path, 'r', encoding ='utf-8') as file:
        try:
            reader = csv.reader(file)
            for row in reader:
                goal_number = row[0]
                date_month = int(row[1])
                date_day = int(row[2])
                date = Date(date_month, date_day)
                deadline_month = int(row[3])
                deadline_day = int(row[4])
                deadline = Date(deadline_month, deadline_day)
                term = int(row[5])
                achivement = float(row[6])

                goal_instance = Goal(goal_number, date, deadline, term, achivement)
                data_field.append(goal_instance)
        except:
            print('데이터 로드에 이상이 생겼습니다.')
        return data_field

def write_data_file(data_field):
    try:
        file_path = 'goal_csv/goal_data.csv'
        with open(file_path, 'w', encoding ='utf-8') as file:
            writer = csv.writer(file)
            data_lists = [[data for data in [goal.goal_number, goal.date.month, goal.date.day,\
                                            goal.deadline.date.month, goal.deadline.date.day,\
                                            goal.term, goal.achivement]] for goal in data_field]
            writer.writerows(data_lists)
    except:
        print('데이터 저장에 이상이 있습니다.')
        

def read_contents_file():
    try:
        contents_field = {}
        file_name = 'goal_csv/goal_contents.csv'
        with open(file_name, 'r', encoding ='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                contents_field[row[0]] = row[1]
    except:
        '데이터 로드에 이상이 생겼습니다.'
    return contents_field

def write_contents_file(contents_field):
    try:
        file_name = 'goal_csv/goal_contents.csv'
        with open(file_name, 'w', encoding ='utf-8') as file:
            writer = csv.writer(file)
            contents_lists = [[key] + [value] for key, value in contents_field.items()]
            writer.writerows(contents_lists)
    except:
        '데이터 저장에 이상이 있습니다.'

