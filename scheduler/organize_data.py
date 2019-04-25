from .models import Course
from .models import Room


def organize(form_data):
    courses_from_form = create_list_of_all_courses(form_data.items())
    all_courses = Course.objects.filter(cname__in=list(courses_from_form)).order_by('capacity')
    all_rooms = Room.objects.all().order_by('capacity')
    data = {
        'consumers': organize_courses(courses_from_form, all_courses),
        'resources': {
            'rooms': organize_rooms(all_rooms)
        }
    }
    return data


def create_list_of_all_courses(form_data):
    all_courses = []
    for key, value in form_data:
        if key != 'csrfmiddlewaretoken' and int(value) != 0:
            all_courses.extend([key] * int(value))
    return all_courses


def organize_courses(courses_from_form, all_courses):
    course_info = {}

    for course in all_courses:
        course_info[course.cname] = {
            'capacity': course.capacity,
            'cnt': 0,
            'times': course.times.all(),
            'days': course.days.all(),
            'duration': course.duration
        }

    ret_courses = {}
    for course in courses_from_form:
        if course in course_info:
            curr_course = {
                'type': ['rooms'],
                'capacity': {
                    'value': course_info[course]['capacity']
                },
                'time': {
                    'value': organize_course_time(course_info[course]['times'],
                                                  course_info[course]['days'],
                                                  course_info[course]['duration'])
                }
            }
            course_info[course]['cnt'] += 1
            course_name = course + "_" + str(course_info[course]['cnt'])
            ret_courses[course_name] = curr_course

    return dict(sorted(ret_courses.items(), key=lambda k: k[1]['capacity']['value'], reverse=True))


def organize_rooms(all_rooms):
    ret_rooms = {}
    for room in all_rooms:
        curr_room = {
            'capacity': {
                'value': room.capacity,
                'op_type': "GE"
            },
            'time': {
                'value': organize_room_time(room.times.all(),
                                            room.days.all()),
                'op_type': 'IN'
            }
        }
        ret_rooms[room.rname] = curr_room
    return dict(sorted(ret_rooms.items(), key=lambda k: k[1]['capacity']['value']))


def organize_course_time(times_list, days_list, duration):
    expand_times_list = []
    expand_day_times_list = []
    for time_object in times_list:
        time_int = int(time_object.times)
        expand_times = []
        for time_slots in range(time_int, time_int + duration):
            expand_times.append(str(time_slots))
        expand_times_list.append(expand_times)

    for expand_times in expand_times_list:
        for day_object in days_list:
            expand_day_time = []
            for time_slots in expand_times:
                day_str = day_object.days
                if day_str not in ['MW', 'TuTh']:
                    expand_day_time.append(day_str + time_slots)
                else:
                    len_str = len(day_str)
                    expand_day_time.append(day_str[:len_str // 2] + time_slots)
                    expand_day_time.append(day_str[len_str // 2:] + time_slots)
            expand_day_times_list.append(expand_day_time)

    return expand_day_times_list


def organize_room_time(times_list, days_list):
    day_times_dict = {}
    for time_object in times_list:
        for day_object in days_list:
            time = str(day_object.days) + str(time_object.times)
            day_times_dict[time] = 1
    return day_times_dict


def organize_output(scheduled):
    ret_scheduled = []

    for item in scheduled:
        new_item = {
            'rname': item['rname'],
            'cname': item['cname'],
            'course_capacity': item['cattributes']['capacity'],
            'room_capacity': item['rattributes']['capacity'],
            'times': item['rattributes']['time']
        }
        ret_scheduled.append(new_item)

    return ret_scheduled
