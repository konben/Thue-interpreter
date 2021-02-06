"""A small Thue interpreter."""

import sys
import re
import random
import time


class Rule:
    """Represents a rule of the form:
        <lhs> ::= <rhs>
    """
    def __init__(self, lhs, rhs):
        self.lhs, self.rhs = lhs, rhs


def read_program(filename):
    """Reads a Thue program from file and returns the rulebase as well as the initial string."""
    # Try to open file.
    try:
        file = open(filename)
    except:
        error(f'could not open "{filename}"')
    rulebase = read_rulebase(file)
    # Read initial string.
    init_str = ''
    for line in file:
        init_str += line.rstrip()
    return rulebase, init_str


def read_rulebase(file):
    """Reads the rulebase from file."""
    rulebase = []
    lineno = 1
    for line in file:
        line = line.rstrip()
        # Discard empty lines.
        if line == '' or line.isspace():
            pass
        elif m := re.match(r'(.*)::=(.*)', line):
            lhs, rhs = m.groups()
            # Exit if rulebase is finished.
            if lhs == '':
                return rulebase
            # Add rule to rulebase.
            rulebase.append(Rule(lhs, rhs))
        else:
            error(f'Expected "<lhs> ::= <rhs>", got {line}', lineno)
        # Increase line count.
        lineno += 1
    error('Expected "::=", got "EOF"', lineno)


def error(msg, lineno=-1):
    """Prints an error message and exits program.
       If lineno is equal to -1, then the linenumber is omitted.
    """
    if lineno != -1:
        sys.stderr.write(f'error, line {lineno}: {msg}!\n')
    else:
        sys.stderr.write(f'error: {msg}!\n')
    exit(1)


def execute(rulebase, string, is_verbose):
    """Executes the Thue program."""
    while (rules := applicable_rules(rulebase, string)) != []:
        # Output string.
        if is_verbose:
            time.sleep(0.25)
            print('string:', string)
        # Compute next string.
        r = random.choice(rules)
        string = apply(r, string)
    print(string)


def applicable_rules(rulebase, s):
    """Finds all to s applicable rules in the rulebase."""
    ret = []
    for rule in rulebase:
        if s.find(rule.lhs) != -1:
            ret.append(rule)
    return ret


def find_occurences(s, substr):
    """Returns a list of indexes indicating occurences of substr in str."""
    offset = 0
    occurences = []
    while (i := s.find(substr)) != -1:
        occurences.append(i + offset)
        s = s[i + len(substr):]
        offset += i + len(substr)
    return occurences


def apply(rule, string):
    """Applies rule to string."""
    # Edge case
    occurences = find_occurences(string, rule.lhs)
    i = random.choice(occurences)
    left, right = string[:i], string[i + len(rule.lhs):]
    # Input
    if rule.rhs == ':::':
        in_between = input()
    # Output
    elif rule.rhs != '' and rule.rhs[0] == '~':
        in_between = ''
        print(rule.rhs[1:], flush=True, end='')
    # Vanilla rule.
    else:
        in_between = rule.rhs
    return left + in_between + right


def print_help():
    """Prints a help message and exits program."""
    print('usage: python3 thue.py [-v] <path-to-file>')
    exit()


# Main program.
if __name__ == '__main__':
    # Get arguments.
    if len(sys.argv) == 2:        
        filename = sys.argv[1]
        is_verbose = False
    elif len(sys.argv) == 3:
        if sys.argv[1] not in ['-v', '-verbose']:
            print_help()
        filename = sys.argv[2]
        is_verbose = True
    else:
        print_help()
    # Read & execute program.
    rulebase, init_str = read_program(filename)
    execute(rulebase, init_str, is_verbose)
