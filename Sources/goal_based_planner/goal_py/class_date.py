from datetime import datetime
import calendar

class Date():
    def __init__(self,month = 0, day = 0):
        self.month = month
        self.day = day
        self.week = self.get_week(self.month, self.day)
        if self.week == "유효하지 않은 날짜":
            print("유효하지 않은 날짜입니다.")
        

    
    def get_week(self, month, day):
        try:
            if day == 0:
                return 0
            current_date = datetime.now()
            current_year = current_date.year
            first_date = datetime(current_year, month, 1)
            input_date = datetime(current_year, month, day)
            first_date_week = int(first_date.strftime('%U'))
            # strftime('%U')은 해당 날짜의 주차를 0부터 시작하여 반환합니다.
            week = int(input_date.strftime('%U')) - first_date_week + 1
            return week
        except ValueError:
            return "유효하지 않은 날짜"
    def get_weekday(self):
        date = datetime(datetime.now().year, self.month, self.day)
        weekday_number = date.weekday()
        weekday_list = ('월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일')
        return weekday_list[weekday_number]

    def set_today(self):
        current_date = datetime.now()
        self.month = current_date.month
        self.day = current_date.day
        self.week = self.get_week(self.month, self.day)
    def get_next_date(self, next = 1):
        month = self.month + (self.day + next - 1) // last_day_of_month(self.month)
        day = (self.day + next - 1) %  last_day_of_month(self.month) + 1
        next_date = Date(month, day)
        return next_date
    def get_date_string(self, return_type = 0):
        if(return_type == 1):
            return_string = str(self.month) + '월'
        elif(return_type == 2):
            return_string = str(self.day) + '일'
        elif(return_type == 3):
            return_string = str(self.week) + '번째 주'
        else:
            return_string = str(self.month) + '월' + str(self.day) + '일'
        return return_string

class Today(Date):
    def __init__(self):
        self.set_today()



def last_day_of_month(year = datetime.now().year, month = Today().month):
    last_day = calendar.monthrange(year , month)[1]
    return last_day
if __name__ == '__main__':
    today = Today()
    print(today.day, today. month, today.week)

# Date 인스턴스 생성
#date_instance1 = Date()
#print(f"Date(): week={date_instance1.week}, month={date_instance1.month}, day={date_instance1.day}")

# Date(1) 인스턴스 생성
#date_instance2 = Date(33)
#print(f"Date(1): week={date_instance2.week}, month={date_instance2.month}, day={date_instance2.day}")




# 현재 날짜를 가져와서 사용
#current_date = datetime.now()
#current_month = current_date.month()
#current_day = current_date.day()