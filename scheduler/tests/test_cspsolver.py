"""
This is the test suite for cspsolver.py.
"""
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase, main, skip
from cspsolver import CSP, minConflicts


def create_csp1():
    csp = CSP()
    csp.add_node(("physics", "John Smith"), [("648", "physics")])
    return csp


def create_csp2():
    csp = CSP()
    csp.add_node("class1", ["domain1"])
    csp.add_node("class2", ["domain2", "domain3", "domain4"])
    csp.add_node("class3", ["domain5", "domain6"])
    return csp


def create_user_data():
    courses = ["physics", "chemistry"]
    professors = ['John Smith', 'Lisa Jones', 'Mike Williams']
    rooms = ["648","649"]
    room_capacities = {'648': 30, '649': 40}
    course_no_students = {'physics': 35, 'chemistry': 26}
    course_mins = {'physics': 60, 'chemistry': 90}
    course_no_sections = {'physics': 2, 'chemistry': 2}
    course_days_weekly = {'physics': 3, 'chemistry': 2}
    prof_info = {'John Smith': {'courses': ['physics', 'chemistry'], 'start_time': 8, 'end_time': 17},
                 'Lisa Jones': {'courses': ['physics'],'start_time': 9,'end_time': 18},
                 'Mike Williams': {'courses': ['biology 1'], 'start_time': 9, 'end_time': 15}}
    user_data = professors, prof_info, rooms, room_capacities, courses, \
                course_no_students, course_no_sections, course_mins, course_days_weekly
    return user_data


class CspTestCase(TestCase):
    def setUp(self):
        self.csp = create_csp1()
        self.data = create_user_data()

    def tearDown(self):
        self.csp = None

    def test_nodes(self):
        self.assertEqual(self.csp.nodes[0], ("physics", "John Smith"))
        self.assertEqual(self.csp.node_domains[("physics", "John Smith")], [("648", "physics")])

    def test_add(self):
        """
        Test if add node to CSP work.
        """
        self.assertFalse(self.csp.add_node(("physics", "John Smith"), [("648", "physics")]))
        self.assertFalse(self.csp.add_node(("physics", "John Smith"), ["domain2"]))
        self.assertEqual(len(self.csp.nodes), 1)
        self.csp.add_node("class2", ["domain2"])
        self.assertEqual(len(self.csp.nodes), 2)

    def room_has_capacity(self, val):
        """
            Constraint function for unary
        """
        room = val[0]
        course = val[1]
        no_students = self.data[5][course]
        return bool(self.data[3][room] >= no_students)

    def test_unary_constraint(self):
        """
            Test unary constraint function
        """
        result = self.room_has_capacity(("648", "physics"))
        self.assertFalse(result)
        result = self.room_has_capacity(("649", "physics"))
        self.assertTrue(result)

    def test_add_unary_constraint(self):
        """
        Test if add unary constraint work.
        """
        self.assertRaises(ValueError, lambda: self.csp.add_unary_constraint
        ("class2", constraint_func=1))
        domain = self.csp.node_domains[("physics", "John Smith")]
        factor = {val: self.room_has_capacity(val) for val in domain}
        self.csp.add_unary_constraint(("physics", "John Smith"), self.room_has_capacity)
        constraint = self.csp.unary_constraints[("physics", "John Smith")]
        self.assertEqual(constraint, factor)


    def no_class_overlap(self, val1, val2, course1, course2):
        """
            Class constraint function for binary
        """
        course_min = self.data[5]
        hours1, mins1 = val1[1]
        hours2, mins2 = val2[1]
        course_start1 = hours1 * 6 + mins1 // 10
        course_end1 = course_start1 + \
                      course_min[course1] // 10
        course_start2 = hours2 * 6 + mins2 // 10
        course_end2 = course_start2 + \
                      course_min[course2] // 10
        # conditions to check if one class starts during other
        if course_start1 <= course_start2 < course_end1:
            return bool(False)
        if course_start2 <= course_start1 < course_end2:
            return bool(False)
        # soft constraint: non-sequential classes
        # get higher weight
        if course_start1 == course_end2 or course_start2 == course_end1:
            return 2
        return bool(True)

    def test_binary_class(self):
        """
        Test if binary constraint of class work.
        """
        val1 = ["648",(5,60)]
        val2 = ["648", (5,60)]
        self.assertFalse(self.no_class_overlap(val1, val2, "physics", "chemistry"))
        val1[1] = (6,10)
        self.assertFalse(self.no_class_overlap(val1, val2, "physics", "chemistry"))
        val1[1] = (6, 60)
        self.assertTrue(self.no_class_overlap(val1, val2, "physics", "chemistry"))
        val1[1] = (6, 20)
        self.assertEqual(2, self.no_class_overlap(val1, val2, "physics", "chemistry"))


    def no_time_clash(self, val1, val2, course):
        """
            Class constraint function for binary
        """
        course_min = self.data[5]
        room1, time1 = val1
        room2, time2 = val2
        if room1 != room2:
            return bool(True)
        hours1, mins1 = time1
        hours2, mins2 = time2
        start_time1 = hours1 * 6 + mins1 // 10
        end_time1 = start_time1 + course_min[course] // 10
        start_time2 = hours2 * 6 + mins2 // 10
        if start_time1 <= start_time2 < end_time1:
            return bool(False)
        return bool(True)

    def test_binary_time(self):
        """
        Test if binary constraint of time work.
        """
        val1 = ["648",(5,60)]
        val2 = ["649", (5,60)]
        self.assertTrue(self.no_time_clash(val1, val2, "physics"))
        val1[0] = "649"
        self.assertFalse(self.no_time_clash(val1, val2, "physics"))
        val2[1] = (3,60)
        self.assertTrue(self.no_time_clash(val1, val2, "physics"))


    def test_add_binary_constraint(self):
        """
        Test if add binary constraint work.
        """
        self.assertRaises(ValueError, lambda: self.csp.add_binary_constraint
        ("class2", "class1", constraint_func=1))


class MinConflictsTestCase(TestCase):
    def setUp(self):
        csp = create_csp2()
        self.minC = minConflicts(csp)

    def tearDown(self):
        self.minC.csp = None
        self.minC = None

    def test_assigner(self):
        assignment = self.minC.initial_var_assignment()
        self.assertTrue(assignment["class1"] == "domain1")
        self.assertTrue(assignment["class2"] in ["domain2", "domain3", "domain4"])
        self.assertFalse(assignment["class3"] == "domain10")

    def test_conflicted(self):
        assignment = self.minC.initial_var_assignment()
        conflict = self.minC.conflicted(assignment)
        self.assertEqual(conflict, set())

    def test_solve(self):
        result = self.minC.solve(100)
        self.assertEqual(result["class1"], "domain1")
        self.assertTrue(result["class2"] in ["domain2", "domain3", "domain4"])
        self.assertNotEqual(result["class3"], "domin5")


if __name__ == '__main__':
    main()
