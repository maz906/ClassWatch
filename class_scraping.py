from datetime import datetime
from utilities import createsoup
import time
import sys
from twilio.rest import TwilioRestClient

class_idx_idx = 0

subject_idx, numer_idx, section_idx = 1, 2, 3
max_enroll_idx, curr_enroll_idx, avail_idx = 5, 6, 7

min_to_wait, secs_per_min = 1, 60

def class_info(subj, clno, curr_term=1166):
    course_info = 'http://student.apps.utah.edu/uofu/stu/ClassSchedules/main/{0}/sections.html?subj={1}&catno={2}'.format(curr_term, subj.upper(), clno)
    info = createsoup(course_info).find_all('tr')
    return list(dict(zip([x.string for x in info[0].findChildren(['th'])],
			[x.string for x in info[i].findChildren(['td'])])) for i in range(1, len(info)))

def monitor_desired_section(subject, class_no, section_nos):
    try:
        desired_sections = { int(x) for x in section_nos }
    except ValueError as e:
        print('Section numbers must be integers.')
        raise e


    while True:
        info = class_info(subject, class_no)
        print(datetime.now())
        for section_info in info:
            try:
                if int(section_info['Section']) in desired_sections:
                    if int(section_info[avail_idx]) != 0:
                        print('SECTION {0} AVAILABLE. ADD CLASS INDEX TO CART: {1}'.format(section_info[section_idx], section_info[class_idx_idx]))
                        return
                    print('{0} {1}-{2}: {3}/{4}'.format(section_info[subject_idx], section_info[numer_idx], section_info[section_idx], section_info[curr_enroll_idx], section_info[max_enroll_idx]))
            except IndexError:
                continue
        time.sleep(min_to_wait*secs_per_min)

def monitor_desired_class(subject, class_no):
    while True:
        info = class_info(subject, class_no)
        print(datetime.now())
        for section in info:
            if int(section['Seats Available']) > 0:
                ACCOUNT_SID = "YOUR_SID" 
                AUTH_TOKEN = "YOUR_TOKEN" 

                client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
                client.messages.create(
                    to="PHONE_TO", 
                    from_="PHONE_FROM", 
                    body='{0} {1}-{2} is open. Class number is {3}'.format(section['Subject'], section['Catalog #'], section['Section'], section['Class #']),  
                )	
                return
                try:
                    print('{0} {1}-{2}: {3}'.format(section['Subject'], section['Catalog #'], section['Section'], section['Seats Available']))
                except IndexError:
                    continue

                time.sleep(1)

def main():
    if len(sys.argv) >= 4:
        monitor_desired_section(sys.argv[1], sys.argv[2], sys.argv[3:])
    elif len(sys.argv) == 3:
        monitor_desired_class(sys.argv[1], sys.argv[2])
    else:
        print('Usage is: CREATE BETTER USAGE INFO')


if __name__ == '__main__':
    main()




