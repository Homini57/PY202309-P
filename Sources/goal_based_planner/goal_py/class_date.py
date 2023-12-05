from datetime import datetime


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
        
    def set_today(self):
        current_date = datetime.now()
        self.month = current_date.month
        self.day = current_date.day
        self.week = self.get_week(self.month, self.day)

class Today(Date):
    def __init__(self):
        current_date = datetime.now()
        month = current_date.month
        day = current_date.day
        super.__init__(month, day)

today = Date()
today.set_today()
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