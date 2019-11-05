from cspsolver import CSP, minConflicts

import random
import collections

"""
Takes in the data file and outputs class schedules for each weekday.
"""

MONDAY = 'mon' 
TUESDAY = 'tues' 
WEDNEWSDAY = 'wed' 
THURSDAY = 'thur' 
FRIDAY = 'fri'
WEEKDAYS = [MONDAY, TUESDAY, WEDNEWSDAY, THURSDAY, FRIDAY]

def pref_handler(rand_day):
    """Given a random day, return a list of days weighted by preference.

    Arguments:
        rand_day {string} -- A string representing a random day.

    Returns:
        [list] -- [A list of days weighted by preference]
    """
    days = [MONDAY, TUESDAY, WEDNEWSDAY, THURSDAY, FRIDAY]
    if rand_day == TUESDAY: 
        return [MONDAY, WEDNEWSDAY, THURSDAY, FRIDAY] 
    pref = [MONDAY, WEDNEWSDAY] if rand_day in (MONDAY, WEDNEWSDAY) else [THURSDAY, FRIDAY]
    return [day for day in (pref+days) if day != rand_day]

def assign_days_for_course(course_weekly_days):
    """Assign randomly the meetings days for a class given how many time it is held weekly.

    Arguments:
        course_weekly_days {int} -- how many days the class is held per week.

    Returns:
        [list] -- A list of days chosen for the class.
    """
    course_weekly_days = min(course_weekly_days, 5) 
    days_chosen = []
    if course_weekly_days == 1:
        workdays = [MONDAY, TUESDAY, WEDNEWSDAY, THURSDAY, FRIDAY]
    elif 2 <= course_weekly_days <= 4:
        # Pairs Mon-Wed and Thurs-Fri preferred if course is held 2 - 4 days per week.
        workdays = [MONDAY, WEDNEWSDAY, THURSDAY, FRIDAY] * 2 + [TUESDAY]
    else:
        return [MONDAY, TUESDAY, WEDNEWSDAY, THURSDAY, FRIDAY]
    for i in range(course_weekly_days):
        rand_day = random.choice(workdays)
        if i == 0:
            workdays = pref_handler(rand_day)
        else:
            workdays = list(set(workdays))
            workdays.remove(rand_day)
        days_chosen.append(rand_day)
    return days_chosen

#Soft constraint
def maps_day_to_class(course_days_weekly, courses):
    """Maps preferred days to classes.

    Arguments:
        course_days_weekly {dict} -- A map {class: how many days it's held per week}.
        courses {list} -- A list of classes.

    Returns:
        [dict] -- Returns a map {day: a list of classes on that day}.
    """
    weekdays = [MONDAY, TUESDAY, WEDNEWSDAY, THURSDAY, FRIDAY]
    courses_on_days = collections.defaultdict(list)
    for course in courses: 
        course_days = assign_days_for_course(course_days_weekly[course])
        for day in course_days:
            courses_on_days[day].append(course)
    return courses_on_days

def assigner(user_data):
    """Takes in data provided by the user and creates class schedule.

    Arguments:
        user_data {tuple} -- A tuple of lists containing the user's data information.

    Returns:
        [dict] -- Returns a map {day: a list of classes taught by professors with room numbers and times}.
    """

    def add_nodes():
        """Adds nodes (course, professor) and its list of domains (rooms, hours) to node domains.
        """
        for course in courses:
            # This enforces room consistency
            if rooms_chosen.get(course) is None:
                # rooms_course = rooms for course
                rooms_course = rooms
            else:
                rooms_course = rooms_chosen[course]
            professor = full_prof_assignment[course]
            if professor is None:
                continue
            domain = [(room, hour) for room in rooms_course for hour in hours_for_prof(professor)]
            node_name = (course, professor)
            csp.add_node(node_name, domain)

    def profs_for_courses(courses):
        """Assign professors to given list of courses.

    	Arguments:
    	    courses {list} -- A list of classes.

    	Returns:
    	    [dict] -- Returns a map {course : professor}.
    	"""
        profs_chosen = {course: None for course in courses}
        for course in courses:
            hits = []
            for professor in professors:
                their_courses = prof_info[professor]['courses']
                if course in their_courses:
                    hits.append(professor)
            if hits:
                profs_chosen[course] = random.choice(hits)
        return profs_chosen

    def hours_for_prof(professor):
        """Assigns a professor time for their class based on their preferences

        Arguments:
            professor {string} -- A professor's name.

        Returns:
            [dict] -- A tuple of times for the professor's courses.
        """
        start = prof_info[professor]['start_time']
        end = prof_info[professor]['end_time']
        # in format (hours,minutes) in 30min intervals
        return {(i, j * 30) for i in range(start, end) for j in range(2)}

    def add_unary():
        """Adds an unary constraint to list of nodes
        """
        for node in csp.nodes:
            course, professor = node

            def room_has_capacity(val, course=course, prof=professor):
                """Checks to see if given room has room for all students in course.

                Arguments:
                    val {tuple} -- Contains values for room and time of class.
                    Course {string} -- Name of course.
                    Professor {string} -- Name of professor.

                Returns:
                    [bool] -- Whether or not the room has capacity for all students in course.
                """
                room, hour_and_min = val
                no_students = course_no_students[course]
                return bool(room_capacities[room] >= no_students)

            csp.add_unary_constraint((course, professor), room_has_capacity)

    def add_binary():
        nodes = csp.nodes
        for i, n in enumerate(nodes):
            course_n, prof_n = n
            for m in nodes[i:]:
                course_m, prof_m = m
                if prof_n == prof_m:
                    if course_n == course_m:
                        continue
                    '''first binary constraint'''

                    # c1 = course_1, c2 = course_2
                    def no_class_overlap(val1, val2, c1=course_n, c2=course_m):
                        # makes the math easy: calculate course times in
                        # 10min intervals e.g. 120min is 12 intervals
                        hours1, mins1 = val1[1]
                        hours2, mins2 = val2[1]
                        course_start1 = hours1 * 6 + mins1 // 10
                        course_end1 = course_start1 + \
                            course_mins[c1] // 10
                        course_start2 = hours2 * 6 + mins2 // 10
                        course_end2 = course_start2 + \
                            course_mins[c2] // 10
                        # conditions to check if one class starts during other
                        if course_start1 <= course_start2 < course_end1:
                            return bool(False)
                        if course_start2 <= course_start1 < course_end2:
                            return bool(False)
                        # soft constraint: non-sequential classes
                        # get higher weight
                        if course_start1 == course_end2 \
                                or course_start2 == course_end1:
                            return 2
                        return bool(True)

                    csp.add_binary_constraint(n, m, no_class_overlap)
                '''second binary constraint'''

                def no_time_clash(val1, val2, course1=course_n):
                    room1, time1 = val1
                    room2, time2 = val2
                    if room1 != room2:
                        return bool(True)
                    hours1, mins1 = time1
                    hours2, mins2 = time2
                    start_time1 = hours1 * 6 + mins1 // 10
                    end_time1 = start_time1 + course_mins[course1] // 10
                    start_time2 = hours2 * 6 + mins2 // 10
                    if start_time1 <= start_time2 < end_time1:
                        return bool(False)
                    return bool(True)

                csp.add_binary_constraint(n, m, no_time_clash)

    # get the professor-course-room data from the function argument
    professors, prof_info, rooms, room_capacities, courses, \
        course_no_students, course_mins, course_days_weekly = user_data

    # enforce professor-course consistency among different days
    full_prof_assignment = profs_for_courses(courses)
    rooms_chosen = {}  # rooms are consistent
    solution = {d: None for d in WEEKDAYS}
    retries = 0
    # will retry max 3 times to get a solution
    while retries < 3:
        daily_courses = maps_day_to_class(course_days_weekly, courses)
        # upon retry increase maximum iterations
        max_iters = 100 * (retries + 1)
        for d in WEEKDAYS:
            csp = CSP()
            courses = daily_courses[d]
            add_nodes()
            add_unary()
            add_binary()
            minconf = minConflicts(csp)
            solved = minconf.solve(max_iters)
            if solved is None:
                retries += 1
                if retries < 3:
                    break
            solution[d] = solved
        break
    return solution