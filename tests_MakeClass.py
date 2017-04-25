import unittest
from MakeClass import *


################################### TESTS ######################################

class TestCase(unittest.TestCase):
    # test the Pair(first, rest) class
    def test_Pair(self):
        a = Pair(1, 'mt')
        b = Pair(2.0, a)
        c = Pair(2.0, Pair(1, 'mt'))

        self.assertEqual(a == Pair(1, 'mt'), True)
        self.assertEqual(b == Pair(2.0, a), True)
        self.assertEqual(c == a, False)
        self.assertEqual(repr(a), "Pair(1, 'mt')")

    # test the ClassShape(name, StrList) class
    def test_ClassShape(self):
        a = ClassShape("", 'mt')
        b = ClassShape("test1", Pair("x", 'mt'))
        c = ClassShape("test2", Pair("x", Pair("y", 'mt')))

        self.assertEqual(a == ClassShape("", 'mt'), True)
        self.assertEqual(c == ClassShape("test2", \
                Pair("x", Pair("y", 'mt'))), True)
        self.assertEqual(a == b, False)
        self.assertEqual(repr(c),\
                "ClassShape('test2', Pair('x', Pair('y', 'mt')))")

    # tests for add_to_front(strlist, string) function
    def test_add_to_front_mt(self):
        self.assertEqual(add_to_front('mt', 'xy'), 'mt')
    def test_add_to_front_empty_string(self):
        self.assertEqual(add_to_front(Pair("a", 'mt'), ''), Pair("a", 'mt'))
    def test_add_to_front_mult_2(self):
        self.assertEqual(add_to_front(Pair("a", 'mt'), 'xy', 2),\
                Pair("xyxya", 'mt'))
    def test_add_to_front_mult_0(self):
        self.assertEqual(add_to_front(Pair("a", 'mt'), 'xy', 0),\
                Pair("a", 'mt'))
    def test_add_to_front_mult_neg_1(self):
        self.assertEqual(add_to_front(Pair("a", 'mt'),'xy', -1),\
                Pair("a", 'mt'))
    def test_add_to_front_2_pair(self):
        self.assertEqual(add_to_front(Pair("a", Pair("b", 'mt')), 'xy'),\
                Pair("xya", Pair("xyb", 'mt')))
    def test_add_to_front_skip_end_True(self):
        self.assertEqual(add_to_front(Pair("a", Pair("b", 'mt')),\
                'xy', skip_end = True), Pair("xya", Pair("b", 'mt')))

    # test fields_to_eq(strlist) function
    def test_fields_to_eq_mt(self):
        self.assertEqual(fields_to_eq('mt'), Pair(TAB * 2 + ")", 'mt'))
    def test_fields_to_eq_1_pair(self):
        self.assertEqual(fields_to_eq(Pair("x", 'mt')),\
                Pair("self.x == other.x", Pair(TAB * 2 + ")", 'mt')))
    def test_fields_to_eq_2_pair(self):
        self.assertEqual(fields_to_eq(Pair("x", Pair("y", 'mt'))),\
                Pair("self.x == other.x", Pair("self.y == other.y",\
                Pair(TAB * 2 + ")", 'mt'))))

    # test the fields_to_repr_format(strlist) function
    def test_fields_to_repr_format_mt(self):
        self.assertEqual(fields_to_repr_format('mt'), 'mt')
    def test_fields_to_repr_format_1_pair(self):
        self.assertEqual(fields_to_repr_format(Pair("x", 'mt')),\
                Pair("self.x", 'mt'))
    def test_fields_to_repr_format_2_pair(self):
        self.assertEqual(fields_to_repr_format(Pair("x", Pair("y", 'mt'))),\
                Pair("self.x", Pair("self.y", 'mt')))

    # test the fields_to_repr_r(strlist) function
    def test_fields_to_repr_r_mt(self):
        self.assertEqual(fields_to_repr_r('mt'), 'mt')
    def test_fields_to_repr_r_1_pair(self):
        self.assertEqual(fields_to_repr_r(Pair("x", 'mt')),\
                Pair("{!r}", 'mt'))
    def test_fields_to_repr_r_2_pair(self):
        self.assertEqual(fields_to_repr_r(Pair("x", Pair("y", 'mt'))),\
                Pair("{!r}", Pair("{!r}", 'mt')))

    # test join_lines(strlist) function
    def test_join_lines_mt(self):
        self.assertEqual(join_lines('mt'), "")
    def test_join_lines_1_pair(self):
        self.assertEqual(join_lines(Pair("x", 'mt')), "x\n")
    def test_join_lines_2_pair(self):
        self.assertEqual(join_lines(Pair("x", Pair("y", 'mt'))), "x\ny\n")

    # test fields_to_assingments(strlist) function
    def test_fields_to_assignemnts_mt(self):
        self.assertEqual(fields_to_assignments('mt'), 'mt')
    def test_fields_to_assignemnts_1_pair(self):
        self.assertEqual(fields_to_assignments(Pair("x", 'mt')),\
                Pair(2 * TAB + "self.x = x", 'mt'))
    def test_fields_to_assignemnts_2_pair(self):
        self.assertEqual(fields_to_assignments(Pair("x", Pair("y", 'mt'))),\
                Pair(2 * TAB + "self.x = x",\
                Pair(2 * TAB + "self.y = y", 'mt')))

    # test commasep(strlist) function
    def test_commasep_mt(self):
        self.assertEqual(commasep('mt'), "")
    def test_commasep_1_pair(self):
        self.assertEqual(commasep(Pair("x", 'mt')), ", x")
    def test_commasep_2_pair(self):
        self.assertEqual(commasep(Pair("x", Pair("y", 'mt'))), ", x, y")
    def test_commasep_3_pair(self):
        self.assertEqual(commasep(Pair("x", Pair("y", Pair("z", 'mt')))),\
                ", x, y, z")
    
    # test init_meathon(strlist) function
    def test_init_method_mt(self):
        self.assertEqual(init_method('mt'),\
                Pair(TAB + "def __init__(self):",\
                Pair(2 * TAB + "pass", 'mt')))
    def test_init_method_1_pair(self):
        self.assertEqual(init_method(Pair("x", 'mt')),\
                Pair(TAB + "def __init__(self, x):",\
                Pair(2 * TAB + "self.x = x", 'mt')))
    def test_init_method_2_pair(self):
        self.assertEqual(init_method(Pair("x", Pair("y", 'mt'))),\
                Pair(TAB + "def __init__(self, x, y):",\
                Pair(2 * TAB + "self.x = x",\
                Pair(2 * TAB + "self.y = y", 'mt'))))

    # test eq_meathon(classshape) function
    def test_eq_method_mt(self):
        self.assertEqual(eq_method(ClassShape("Name", 'mt')),\
                Pair(1 * TAB + "def __eq__(self, other):",\
                Pair(2 * TAB + "return (type(other) == Name",\
                Pair(4 * TAB + ")", 'mt'))))
    def test_eq_method_1_pair(self):
        self.assertEqual(eq_method(ClassShape("Name", Pair("x", 'mt'))),\
                Pair(1 * TAB + "def __eq__(self, other):",\
                Pair(2 * TAB + "return (type(other) == Name",\
                Pair(4 * TAB + "and self.x == other.x",\
                Pair(4 * TAB + ")", 'mt')))))
    def test_eq_method_2_pair(self):
        self.assertEqual(eq_method(ClassShape("Name",\
                Pair("x", Pair("y", 'mt')))),\
                    Pair(1 * TAB + "def __eq__(self, other):",\
                    Pair(2 * TAB + "return (type(other) == Name",\
                    Pair(4 * TAB + "and self.x == other.x",
                    Pair(4 * TAB + "and self.y == other.y",\
                    Pair(4 * TAB + ")", 'mt'))))))
    
    # test repr_meathon(classshape) function
    def test_repr_method_mt(self):
        self.assertEqual(repr_method(ClassShape("Name", 'mt')),\
                Pair(TAB + "def __repr__(self):",\
                Pair(2 * TAB + 'return "Name()".format()', 'mt')))
    def test_repr_method_1_pair(self):
        self.assertEqual(repr_method(ClassShape("Name", Pair("x", 'mt'))),\
                Pair(TAB + "def __repr__(self):",\
                Pair(2 * TAB + 'return "Name({!r})".format(self.x)', 'mt')))
    def test_repr_method_2_pair(self):
        self.assertEqual(repr_method(ClassShape("Nme",\
                Pair("x", Pair("y", 'mt')))),\
                    Pair(TAB + "def __repr__(self):",\
                    Pair(2 * TAB +\
                    'return "Nme({!r}, {!r})".format(self.x, self.y)', 'mt')))

    # test render_class(classshape)
    def test_render_class_mt(self):
        self.assertEqual(render_class(ClassShape("Name", 'mt')),\
'''
class Name:
    def __init__(self):
        pass

    def __eq__(self, other):
        return (type(other) == Name
                )

    def __repr__(self):
        return "Name()".format()
'''.lstrip('\n'))
    
    def test_render_class_1_pair(self):
        self.assertEqual(render_class(ClassShape("Name", Pair("x", 'mt'))),\
'''
class Name:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return (type(other) == Name
                and self.x == other.x
                )

    def __repr__(self):
        return "Name({!r})".format(self.x)
'''.lstrip('\n'))

    def test_render_class_2_pair(self):
        self.assertEqual(render_class(ClassShape("Name",\
                Pair("x", Pair("y", 'mt')))),\
'''
class Name:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (type(other) == Name
                and self.x == other.x
                and self.y == other.y
                )

    def __repr__(self):
        return "Name({!r}, {!r})".format(self.x, self.y)
'''.lstrip('\n'))


##################################### MAIN ####################################

if __name__ == '__main__':
    unittest.main()

