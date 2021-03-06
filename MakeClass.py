import unittest
import argparse
import os.path

# Globals to set tab/indentation spacing
TAB = ' ' * 4

###################################### IO #####################################

# void --> cmd line args
# returns formatted command line args
def cmd_io():

    parser = argparse.ArgumentParser(description="Generates Class skeleton")

    # required args
    parser.add_argument('inFile', type = str,\
            help = "input file to style check")
    parser.add_argument('Name', type = str,\
            help = "Name of the class")
    parser.add_argument('-p', nargs = '*', type = str,\
            help = "Class arguments")

    # optional args
    parser.add_argument('-t', action = "store_true",\
            help = "include import unittest")

    return parser.parse_args()


################################## Classes #####################################

# a StrLst is one of
# - "mt" or
# - a Pair(first, rest)
class Pair:
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def __eq__(self, other):
        return type(self) == type(other)\
                and self.first == other.first\
                and self.rest == other.rest

    def __repr__(self):
        return "Pair({!r}, {!r})".format(self.first, self.rest)


# a ClassShape contains
# - a name (represented by a string)
# - a StrList of field names
class ClassShape:
    def __init__(self, name, field_names):
        self.name = name
        self.field_names = field_names

    def __eq__(self, other):
        return type(self) == type(other)\
                and self.name == other.name\
                and self.field_names == other.field_names

    def __repr__(self):
        return "ClassShape({!r}, {!r})".format(self.name, self.field_names)

################################## MY FUNCTIONS ###############################

# List --> StrList
# returns a StrList from a standard Python List
def list_to_linkedlist(inlist):
    if inlist:
        p = 'mt'
        for param in reversed(inlist):
            p = Pair(param, p)

        return p
    else:
        return 'mt'
# StrList string int --> StrList
# return a StrList where a string is added x times to the front of each Pair
def add_to_front(str_list, string, num = 1, skip_end = False):
    if str_list == 'mt':
        return 'mt'
    else:
        if skip_end:
            if str_list.rest == 'mt':
                return Pair(str_list.first,\
                        add_to_front(str_list.rest, string, num, skip_end))
            else:
                return Pair((string * num) + str_list.first,\
                        add_to_front(str_list.rest, string, num, skip_end))
        else:
            return Pair((string * num) + str_list.first,\
                    add_to_front(str_list.rest, string, num, skip_end))

# StrList --> StrList
# takes a StrList of field names and return s a StrList of lines type
# self.<field> == other.<field> for each field
def fields_to_eq(str_list):
    if str_list == 'mt':
        return Pair(TAB * 2 + ")", 'mt')
    else:
        temp_str = "self." + str_list.first + " == " + "other." + str_list.first
        if str_list.rest != 'mt':
            return Pair(temp_str, fields_to_eq(str_list.rest))
        else:
            return Pair(temp_str, fields_to_eq(str_list.rest))


# StrList --> StrList
# takes a StrList of field names and return a StrList of lines type
# self.<field> for each field
def fields_to_repr_format(str_list):
    if str_list == 'mt':
        return 'mt'
    else:
        temp_str = "self." + str_list.first
        return Pair(temp_str, fields_to_repr_format(str_list.rest))


# StrList --> StrList
# takes a StrList of field names and return a StrLst of type
# {!r}, {!r}, ... for every element in the StrList
def fields_to_repr_r(str_list):
    if str_list == 'mt':
        return 'mt'
    else:
        return Pair("{!r}", fields_to_repr_r(str_list.rest))


############################# REQUIRED FUNCTIONS ###############################

# StrList --> string
# takes a StrList type and converts it into a single string
# each item in the StrList is appended with a \n character and at the end
def join_lines(str_list, temp_str = ""):
    if str_list == 'mt':
        return ""
    else:
        if str_list.rest != 'mt':
            temp_str += str_list.first + '\n'
            return join_lines(str_list.rest, temp_str)
        else:
            return temp_str + str_list.first + '\n'


# StrList --> StrList
# takes a StrList of field names and returns a StrList of of lines type
# \t\tself.<field> = <field> for each field
def fields_to_assignments(str_list):
    if str_list == 'mt':
        return 'mt'
    else:
        temp_str = "self." + str_list.first + " = " + str_list.first
        return Pair(2 * TAB + temp_str, fields_to_assignments(str_list.rest))


# StrList --> string
# takes a StrList type and converts it into a single string
# each item in the StrList is seperated by commas
def commasep(str_list, temp_str = ""):
    if str_list == 'mt':
        return ""
    else:
        if str_list.rest != 'mt':
            temp_str += ', ' + str_list.first
            return commasep(str_list.rest, temp_str)
        else:
            return temp_str + ', ' + str_list.first



# StrList --> StrList
# accepts a list of field names, and
# returns a StrList representing the lines of the __init__ method
def init_method(field_strlist):
    # \tdef __init__ (self, test1, test2 ...):
    def_str = TAB + "def __init__(self" + commasep(field_strlist) + "):"

    # \t\tself.<field> = <field> StrLisit
    if field_strlist == 'mt':
        field_strlist = Pair(2 * TAB + "pass", 'mt')
    else:
        field_strlist = fields_to_assignments(field_strlist)

    # Put it all together
    return Pair(def_str, field_strlist)


# ClassShape --> StrList
# accepts a list of field names, and
# returns a StrList representing the lines of the __eq__ method
def eq_method(class_shape):
    field_strlist = class_shape.field_names
    name = class_shape.name

    # \tdef __eq__ (self, other):
    def_str = TAB + "def __eq__(self, other):"

    # return type(self) == type(other)
    ret_str = "return (type(other) == " + name

    # and self.<field> == other.<field>
    if field_strlist == 'mt':
        field_eq_strlist = fields_to_eq(field_strlist)
    else:
        field_eq_strlist = fields_to_eq(field_strlist)
        field_eq_strlist = add_to_front(field_eq_strlist,\
                "and ", skip_end = True)
        field_eq_strlist = add_to_front(field_eq_strlist,\
                TAB * 2, skip_end = True)

    # put it all together and add tabs
    return Pair(def_str, add_to_front(Pair(ret_str, field_eq_strlist), TAB, 2))


# ClassShape --> StrList
# accepts a list of field names, and
# returns a StrList representing the lines of the __repr__ method
def repr_method(class_shape):
    field_strlist = class_shape.field_names
    name = '"' + class_shape.name + "("

    # \tdef __repr__ (self):
    def_str = TAB + "def __repr__(self):"

    # return "Class({!r}, {!r}, ... )".format(self.<field>, self.<field> ...)
    str_r = commasep(fields_to_repr_r(field_strlist)).lstrip(', ')
    str_format = commasep(fields_to_repr_format(field_strlist)).lstrip(', ')
    str_tot = "return " + name + str_r + ')".format(' + str_format + ")"

    # put is all together and add tabs
    return Pair(def_str, add_to_front(Pair(str_tot, 'mt'), TAB, 2))


# ClassShape --> String
# returns a single string containing the entire Class boilerplate
def render_class(class_shape):
    name = class_shape.name
    fields = class_shape.field_names

    # construct class header
    class_str = "class " + name + ":\n"

    # add __init__ function
    class_str += join_lines(init_method(fields)) + '\n'

    # add __eq__ function
    class_str += join_lines(eq_method(class_shape)) + '\n'

    # add __repr__ function
    class_str += join_lines(repr_method(class_shape))

    # return completed biolerplate string
    return class_str


##################################### MAIN ####################################

def main(args):
    if args.t:
        line_1 = "import unittest\n\n"
    else:
        line_1 = ""

    class_str = render_class(ClassShape(args.Name, list_to_linkedlist(args.p)))

    # check if file exist and create it if it doesn't
    if os.path.isfile(args.inFile):
        with open(args.inFile, 'r') as original: data = original.read()
        with open(args.inFile, 'w') as\
                modified: modified.write(line_1 + class_str + "\n" + data)
    else:
        with open(args.inFile, 'w') as\
                modified: modified.write(line_1 + class_str + "\n")


if __name__ == '__main__':
    main(cmd_io())


