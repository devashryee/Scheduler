'''
Create a JSON holding sample data
'''

import json

# More detailed info for rooms
rooms = ['655', '666', '745a', '745b', '433','201','115a','115b']        
room_capacities = {
                '655' : 30,
                '666' : 30,
                '745a' : 22,
                '745b' : 40,
                '433' : 31,
                '201' : 28,
                '115a' : 35,
                '115b' : 40
        }

# Course details
courses = ['physics','chemistry','biochemistry','biology 1','biology 2','molecular biology','calculus 1', 'calculus 4','astrophysics']
course_no_students = {
        'physics' : 35,
        'chemistry' : 26,
        'biochemistry' : 22,
        'molecular biology': 20,
        'biology 1' : 38,
        'biology 2' : 25,
        'calculus 1' : 34,
        'calculus 4' : 21,
        'astrophysics' : 15,
        }
course_mins = {
        'physics' : 60,
        'chemistry' : 90,
        'biochemistry' : 90,
        'biology 1' : 90,
        'biology 2' : 60,
        'molecular biology' : 60,
        'calculus 1' : 60,
        'calculus 4' : 60,
        'astrophysics' : 60
        }

course_no_sections = {
        'physics' : 2,
        'chemistry' : 2,
        'biochemistry' : 1,
        'biology 1' : 2,
        'biology 2' : 1,
        'molecular biology' : 1,
        'calculus 1' : 2,
        'calculus 4' : 1,
        'astrophysics' : 1
        }

course_days_weekly = {
        'physics' : 3,
        'chemistry' : 2,
        'biochemistry' : 2,
        'biology 1' : 2,
        'biology 2' : 3,
        'molecular biology' : 1,
        'calculus 1' : 3,
        'calculus 4' : 2,
        'astrophysics' : 1
        }

# Info about professors
professors = ['John Smith', 'Lisa Jones', 'Mike Williams',
              'Tim Simpson', 'Rachel Smith','Gregg Woods',
              'Simon Valinski','Chu Yen','Peter Parker',
              'Lisa Mullen','Elizabeth Walker','Brian K. Dickson',
              'Jamir Abdullah']
prof_info = {
                'John Smith' : {
                        'courses' : ['physics', 'chemistry'],
                        'start_time' : 8,
                        'end_time' : 17
                        },
                'Lisa Jones' : {
                        'courses' : ['physics'],
                        'start_time' : 9,
                        'end_time' : 18
                },
                'Mike Williams': {
                        'courses' : ['biology 1'],
                        'start_time' : 9,
                        'end_time' : 15
                },
                'Tim Simpson': {
                        'courses' : ['calculus 1', 'calculus 4'],
                        'start_time' : 9,
                        'end_time' : 18
                },
                'Rachel Smith': {
                        'courses' : ['calculus 4','biology 2'], 
                        'start_time' : 9,
                        'end_time' : 18
                },
                'Gregg Woods': {
                        'courses' : ['chemistry', 'biochemistry'],
                        'start_time' : 8,
                        'end_time' : 17
                },
                'Simon Valinski': {
                        'courses' : ['calculus 1', 'physics','astrophysics'],
                        'start_time' : 8,
                        'end_time' : 17
                },
                'Chu Yen': {
                        'courses' : ['calculus 1', 'calculus 4','physics','astrophysics'],
                        'start_time' : 10,
                        'end_time' : 18
                },
                'Peter Parker': {
                        'courses' : ['biology 1', 'biology 2','biochemistry','chemistry','molecular biology'],
                        'start_time' : 8,
                        'end_time' : 14
                },
                'Lisa Mullen': {
                        'courses' : ['calculus 1', 'calculus 4'],
                        'start_time' : 9,
                        'end_time' : 13
                },
                'Elizabeth Walker': {
                        'courses' : ['calculus 1', 'calculus 4'],
                        'start_time' : 9,
                        'end_time' : 18
                },
                'Brian K. Dickson': {
                        'courses' : ['calculus 4', 'physics'],
                        'start_time' : 9,
                        'end_time' : 18
                },
                'Jamir Abdullah': {
                        'courses' : ['chemistry', 'calculus 4'],
                        'start_time' : 10,
                        'end_time' : 18
                }
        }


def make_data():
    data = {'courses':courses,'professors':professors,'rooms':rooms,
        'room_capacities' : room_capacities, 'prof_info' : prof_info,
        'course_no_students' : course_no_students, 'course_mins' : course_mins,'course_no_sections':course_no_sections,
        'course_days_weekly':course_days_weekly}
    with open('sample_data.txt','w') as outfile:
        json.dump(data,outfile)