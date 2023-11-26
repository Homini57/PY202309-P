from page_py.func_open_page import open_todays_goal, open_main_goal
from goal_py import *

if __name__ == '__main__':

    while True:
        print(goal_data_field)
        return_value = open_todays_goal(goal_data_field)
        if return_value == False:
            write_data_file(goal_data_field)
            write_contents_file(goal_contents_field)
            break
        return_value = open_main_goal(goal_data_field)
        if return_value == False:
            write_data_file(goal_data_field)
            write_contents_file(goal_contents_field)
            break

