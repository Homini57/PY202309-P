from goal_py.class_date import Date, Today
from nltk.tokenize import word_tokenize
# 오늘 내일 등의 용어
# 1월, 2일 등 정해진 포맷

def extract_text_and_date(text):
    word_list = word_tokenize(text)
    date = Date()
    for word in word_list:
        date = date_phrase_to_date(word)
        if (date.day != 0):
            break
        month = date_text_to_month(word)
        day = date_text_to_day(word)
        date = Date(month, day)
        if (date.day != 0):
            break
    new_text = ' '.join(word_list)
    text = new_text
    return date
    

def date_phrase_to_date(word):
    today = Today()
    date_phrase_list = ['오늘', '내일', '모레', '글피']
    for i in range(0, 4):
        if is_in_token(word,date_phrase_list[i]):
            return today.get_next_date(i)
    return Date()

def date_text_to_month(word):
    month = Today().month
    try:
        month_index = word.index('월')
        month = int(word[:month_index])
    except:
        pass
    return month

def date_text_to_day(word):
    day = 0
    try:
        day_index = word.index('일')
        day = int(word[:day_index])
    except:
        pass
    return day


def extract_term_from_text(text):
    word_list = word_tokenize(text)
    term = 0
    for word in word_list:
        term = term_pharse_to_date(word)
        if (term != 0):
            break
        term = term_text_to_date(word)
        if (term != 0):
            break
    return term

def term_pharse_to_date(word):
    term_phrase_list = ['하루', '이틀', '사흘', '나흘']
    for i in range(0, 4):
        if is_in_token(word,term_phrase_list[i]):
            return i + 1
    if is_in_token(word, '매일'):
        return 1
    week_phrase_list = ['매주', '일주일', '월요일', '화요일',\
                        '수요일', '목요일', '금요일', '토요일', '일요일']
    for week_phrase in week_phrase_list:
        if is_in_token(word, week_phrase):
            return 7
    
def term_text_to_date(word):
    term = 0
    try:
        term_index = word.index('주') -1
        term = 7 * int(word[term_index])
        return term
    except:
        pass
    try:
        term_index = word.index('일') -1
        term = int(word[term_index])
    except:
        pass
    return term

def is_in_token(text, word):
    
    for i in range(0, len(text)-len(word) + 1):
        if text[i:len(word)] == word:
            return True
    return False


if __name__ == '__main__':
    pass
    