'''Work Log DB
A program keep employee sharing what they are working on to everyone
create by: Harin Y.
create on October 1, 2015'''


from peewee import *
import re
import os
from datetime import date, datetime
import time



def main_menu():

    clear()
    print('--- MAIN MENU ---')
    valid_answer = False

    while valid_answer == False:
        answer = input('Please choose [A]dd entry, [S]earch entry, [E]dit entry, [D]elete entry or [Q]uit: ').lower()
        if answer == 'a':
            valid_answer = True
            add_entry()
        elif answer == 's':
            valid_answer = True
            search_menu()
        elif answer == 'd':
            valid_answer = True
            delete_id = input('Please enter entry ID you want to delete: ')
            delete_entry(delete_id)
        elif answer == 'e':
            valid_answer = True
            edit_id = input('Please enter entry ID you want to edit: ')
            edit_section = input('Do yo want to edit [E]mployee name, [T]askname or[D]etail?: ').lower()
            edit_entry(edit_id, edit_section)
        elif answer == 'q':
            valid_answer = True
            print('Bye Bye!')
            quit()
        else:
            print('Please Enter [A] for Add entry, [S] for Search entry or [Q] to Quit program')
            continue

        
def clear():
    print('\033c')


def id_generator():

    max_id = 0
    
    for row in Entry:
        if row.entry_id > max_id:
            max_id = row.entry_id
    
    return max_id + 1

            
def add_entry():
    clear()
    print('--- ADD ENTRY ---')
    employee_name = input('Please enter your name: ')
    taskname = input('Please enter Task Name: ')
    
    while True:
        try:
            timespent = int(input('How many minute(s) did you finish the task?: '))
            break
            
        except (ValueError, AttributeError):
            print('Please enter only number!')
            time.sleep(1.5)
            continue
            
    detail = input('Enter detail of the Task: ')
    
    Entry.create(entry_id = id_generator(),
                 employee = employee_name,
                 date = date.today().strftime('%Y%m%d'),
                 taskname = taskname,
                 timespent = timespent,
                 detail = detail)

    print('SUCCESSFULLY ADD NEW ENTRY')
    time.sleep(1.5)


def search_menu():    
    
    valid_answer = False
    
    while valid_answer == False:
        clear()
        print('--- SEARCH MENU ---')
        print('Search by [E]mployee, [T]ext, [P]attern, [M]inute spent, [D]ate of entry')
        answer = input('Or [Q]uit to main menu: ').lower()
        if answer == 't':
            navigate_list = search_text()
            if navigate_list:
                display_entry(navigate_list)
        elif answer == 'm':
            navigate_list = search_minute()
            if navigate_list:
                display_entry(navigate_list)
        elif answer == 'p':
            navigate_list = search_pattern()
            if navigate_list:
                display_entry(navigate_list)
        elif answer == 'd':
            navigate_list = search_date()
            if navigate_list:
                display_entry(navigate_list)
        elif answer == 'e':
            navigate_list = search_employee()
            if navigate_list:
                display_entry(navigate_list)
        elif answer == 'q':
            valid_answer = True
        else:
            print('You enter invalid command!')
            continue


def search_employee():

    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY EMPLOYEE NAME ---')
            answer = input('Please enter employee name: ')
            break
        except ValueError:
            continue

    entries = Entry.select().order_by(Entry.entry_id.desc())
    
    for row in entries:
        if answer.lower() in row.employee.lower():
            navigate_list.append({
                            'ID': row.entry_id,
                            'employee': row.employee,
                            'date': row.date,
                            'taskname': row.taskname,
                            'timespent': row.timespent,
                            'detail': row.detail
                            })
            
    if navigate_list == []:
        print('No entry found with that keyword!')
        time.sleep(1.5)
        clear()
    else:
        return navigate_list


        

def search_text():

    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY TEXT ---')
            answer = input('Please enter keyword or phrase: ')
            break
        except ValueError:
            continue

    entries = Entry.select().order_by(Entry.entry_id.desc())
    
    for row in entries:
        if answer.lower() in row.taskname.lower() or answer.lower() in row.detail.lower():
            navigate_list.append({
                            'ID': row.entry_id,
                            'employee': row.employee,
                            'date': row.date,
                            'taskname': row.taskname,
                            'timespent': row.timespent,
                            'detail': row.detail
                            })
            
    if navigate_list == []:
        print('No entry found with that keyword!')
        time.sleep(1.5)
        clear()
    else:
        return navigate_list


def search_pattern():

    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY REGEX PATTERN ---')
            print('Please enter REGEX pattern')
            print("No r', No \" or ' or any symbol, just regex escape or text you want, Example: \d\w") 
            answer = str(input(': '))
            break
        except ValueError:
            continue

    regex = "r'" + answer + "'"

    entries = Entry.select().order_by(Entry.entry_id.desc())

    for row in entries:
        if (re.search(answer, row.taskname) or re.search(answer, row.detail)):
            navigate_list.append({
                            'ID': row.entry_id,
                            'employee': row.employee,
                            'date': row.date,
                            'taskname': row.taskname,
                            'timespent': row.timespent,
                            'detail': row.detail
                            })

    if navigate_list == []:
        print('No entry found with that pattern!')
        time.sleep(1.5)
        clear()
    else:
        return navigate_list
        

def search_date():

    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY DATE RANGE ---')
            print('Please enter a range of entry date you want to search')
            print('INPUT FORMAT: YYYYMMDD. Only number, no space or symbol')
            min_date = int(input('Search Entry from date: '))
            max_date = int(input('Search Entry to date: '))
            break
        except ValueError:
            continue

    entries = Entry.select().order_by(Entry.entry_id.desc())

    for row in entries:
        if min_date <= int(row.date) <= max_date:
            navigate_list.append({
                            'ID': row.entry_id,
                            'employee': row.employee,
                            'date': row.date,
                            'taskname': row.taskname,
                            'timespent': row.timespent,
                            'detail': row.detail
                            })

    if navigate_list == []:
        print('Cound not find any entry in given date range')
        time.sleep(1.5)
        clear()
    else:
        return navigate_list


def search_minute():

    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY MINUTE RANGE ---')
            print('Please enter range of task duration you want to look for')
            print('INPUT FORMAT: Only number, no space or symbol')
            min_minute = int(input('Minimum task duration: '))
            max_minute = int(input('Maximum task duration: '))
            break
        except ValueError:
            continue

    entries = Entry.select().order_by(Entry.entry_id.desc())

    for row in entries:
        if min_minute <= row.timespent <= max_minute:
            navigate_list.append({
                            'ID': row.entry_id,
                            'employee': row.employee,
                            'date': row.date,
                            'taskname': row.taskname,
                            'timespent': row.timespent,
                            'detail': row.detail
                            })

    if navigate_list == []:
        print('Cound not find any entry in given duration range')
        time.sleep(1.5)
        clear()
    else:
        return navigate_list

    
def display_entry(navigate_list):

    navigate = True
    navigate_index = 0

    while navigate == True:
        clear()
        print('Displaying entry {}/{}'.format(navigate_index + 1, len(navigate_list)))
        print('ID : {}'.format(navigate_list[navigate_index]['ID']))
        print('==========================================')
        print('Employee: {}'.format(navigate_list[navigate_index]['employee']))
        print('Task Name: {}'.format(navigate_list[navigate_index]['taskname']))
        date_object = datetime.strptime(navigate_list[navigate_index]['date'], '%Y%m%d')
        print('Date of Entry: {}'.format(datetime.strftime(date_object, '<%A> %B %d, %Y')))
        print('Duration: {} Minute(s)'.format(navigate_list[navigate_index]['timespent']))
        print('==========================================')
        print('Detail of Entry:')
        print(navigate_list[navigate_index]['detail'])
        answer = input('\n\nView [N]ext entry, [P]revious entry, [D]elete this entry or [B]ack to search menu: ').lower()

        if navigate_index == 0 and answer == 'p':
            continue
        elif navigate_index == len(navigate_list)-1 and answer == 'n':
            continue
        elif answer == 'p':
            navigate_index -= 1
            continue
        elif answer == 'n':
            navigate_index += 1
            continue
        elif answer == 'd':
            delete_entry(navigate_list[navigate_index]['ID'])
        elif answer == 'b':
            navigate = False
            clear()

def delete_entry(delete_id):

    if id_check(delete_id) == True:

        entries = Entry.select().order_by(Entry.entry_id.desc())
        answer = input('Are you sure to delete this entry?[y/N]')
        if answer.lower() == 'y':
            delete_row = Entry.get(Entry.entry_id == delete_id)
            delete_row.delete_instance()
            print('Delete sucessfully!')
            time.sleep(1.5)

    else:
        print('You have given bad entry ID!!')
        time.sleep(1.5)
            

def edit_entry(edit_id, edit_section):

    if id_check(edit_id) == True:
        
        if edit_section == 'd':
            new_detail = input('Please enter new detail you want to update: ')
            Entry.update(detail=new_detail).where(Entry.entry_id == edit_id).execute()
            print('Edit successfully!')

        if edit_section == 't':
            new_taskname = input('Please enter new Taskname you want to update: ')
            Entry.update(taskname=new_taskname).where(Entry.entry_id == edit_id).execute()
            print('Edit successfully!')

        if edit_section == 'e':
            new_employee = input('Please enter new employee you want to update: ')
            Entry.update(employee=new_employee).where(Entry.entry_id == edit_id).execute()
            print('Edit successfully!')
    
        time.sleep(1.5)

    else:
        if id_check(edit_id) == False:
            print('Error: Your given entry ID not found in Database!')
        elif id_check(edit_id) == 2:
            print('Error: Your have given invalid entry ID!')
        time.sleep(1.5)

def id_check(check_id):

    try:
        checker = Entry.select().where(Entry.entry_id == int(check_id))
        if checker:
            return True
        else:
            return False
        
    except ValueError:
        return 2


db = SqliteDatabase('worklog.db')

class Entry(Model):
    entry_id = IntegerField(primary_key=True, unique=True)
    employee = CharField(max_length=255)
    date = CharField(max_length=8)
    taskname = CharField(max_length=255)
    timespent = IntegerField()
    detail = TextField()

    class Meta:
        database = db
        
if __name__ == '__main__':
    db.connect()
    db.create_table(Entry, safe=True)
    while True:
        main_menu()

                    
            
    
  
            
        
            

        
        
    
        

        
        
    
    




        
    
        





    

