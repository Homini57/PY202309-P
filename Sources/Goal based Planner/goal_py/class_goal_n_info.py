class goal():
    def __init__(self):
        self.goal내용 = ''#어케하지?
        self.is달성 = False #필요한가?
        self.super_goal = '' #goal 클래스 입력
        self.sub_goal = []#goal 클래스 입력
        self.goal_level = 0
        self.입력achivement = 0 #정수? 부동소수형
        self.현재achivement = 0
        self.date = 1 # date클래스
        self.기간 = 0
        self.주기 = 0 #주기 클래스


class date():
    def __init__(self, month, day):
        self.month = month
        self.day = day
        # self.week = cal_week(month, day)
