from utilities import createsoup

#idx of table of the html page that has all the courses
courses_idx = 4


class_idx_idx = 1
dept_idx = 2
course_no_idx = 3
section_idx = 4

type_idx = 5
credit_idx = 6

days_idx = 7
times_idx = 8
room_idx = 9

teacher_idx = 11
cost_idx = 14




def courses_info(dept, curr_term = 1158):
    dept_page = 'http://www.acs.utah.edu/uofu/stu/scheduling?term={0}&dept={1}&classtype=g&cmd='.format(curr_term, dept, '')
    course_table = createsoup(dept_page).find_all('table')[courses_idx].find_all('tr')[2:]
    return [[x.get_text().replace('\xa0', '').strip(' \n') for x in course.find_all('td')] for course in course_table]

