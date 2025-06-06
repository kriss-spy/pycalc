# v3.0
# argparse design
# no arg: enter REPL
# -h or --help: print help
# -v or --version: print version
# -d or --debug: print debug info
# --verbose: print intermediate process, not only the result of calc() # TODO
# several strings: calc() and print_ans() each

# import sys

DEBUG = False
operators = ["+", "-", "*", "/"]
priorities = {"*": 1, "/": 1, "+": 2, "-": 2}
use_parenthesis = False  # add support to ()
separate_cli = (
    False  # always display the equation on top, always input at the bottom line)
)

from helper import (
    bye,
    get_input,
    print_ans,
    print_error,
    print_welcome,
    debug_log,
    stack,
    parenthesis_stack,
    test_case,
)


def print_help():
    help_msg = """
    this is a simple cli calculator
    input in the order of operand1, op, operand2
    supported op:
    """
    for op in operators:
        help_msg += " " + op

    print(help_msg)


def atom_calc(a, b, op):  # TODO fix float
    # assuming params are valid
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0 or b == "0":
            print_error("zero division")
            return None
        return a / b


def equation_split(s):
    res = []
    s = s.replace(" ", "")
    l = 0
    while l < len(s):
        if str_is_number(s[l]):
            r = l + 1
            while r < len(s) and (str_is_number(s[r]) or s[r] == "."):
                r += 1
            res.append(s[l:r])
            l = r - 1
        elif s[l] == "-":
            r = l + 1
            while r < len(s) and (str_is_number(s[r]) or s[r] == "."):
                r += 1
            if l >= 1 and str_is_number(s[l - 1]):
                res.append("+")
            res.append(s[l:r])
            l = r - 1
        else:
            res.append(s[l])

        l += 1

    return res


def calc(s):
    ans = 0
    st = stack()

    # process parenthesis
    pst = parenthesis_stack()
    i = 0
    while i < len(s):
        if s[i] in "()":
            match_p, flag = pst.push(s[i], i)
            if not flag:
                print_error("parenthesis")
                return ans, False
            if match_p != None:
                sub_ans, flag = calc(s[match_p.idx + 1 : i])
                if not flag:
                    return ans, False
                s = s[: match_p.idx] + str(sub_ans) + s[i + 1 :]
                i = match_p.idx - 1

        i += 1
    if DEBUG:
        debug_log("parenthesis processing finished for " + s)

    # calculate simple equation
    symbols = equation_split(s)
    if DEBUG:
        debug_log(symbols)
    prev_is_number = str_is_op(symbols[0])

    # check input validity
    for i in range(len(symbols)):
        if not prev_is_number and str_is_number(symbols[i]):
            prev_is_number = True
            symbols[i] = to_number(symbols[i])
        elif prev_is_number and str_is_op(symbols[i]):
            prev_is_number = False
        else:
            return ans, False

    for sym in symbols:
        if st.size() == 0 and str_is_op(sym) and priorities[sym] == 1:
            return ans, False
        elif st.size() == 0:
            st.push(sym)
        else:
            if str_is_op(sym):
                st.push(sym)
            else:
                if priorities[st.top()] == 1:
                    op = st.pop()
                    a = st.pop()
                    atom_ans = atom_calc(a, sym, op)
                    if atom_ans == None:
                        return ans, False
                    st.push(atom_ans)
                elif priorities[st.top()] == 2:
                    st.push(sym)
    li = st.get_li()
    if DEBUG:
        debug_log(li)
    i = 0
    while i + 1 < len(li):
        if li[i] == "-":
            if li[i + 1] == "-":
                # li = li[:i] + li[i + 2 :]
                # i -= 1
                i += 1
            elif isinstance(li[i + 1], (int, float)):
                li[i + 1] *= -1

        i += 1
    nums = [sym for sym in li if not str_is_op(sym)]
    if len(nums) == 0:
        print_error("invalid input")
        return ans, False
    if DEBUG:
        debug_log(nums)
    ans = sum(nums)

    return ans, True


def str_is_number(s):
    # supported number:
    # integer
    # float

    return str_is_integer(s) or str_is_float(s)


def str_is_pos_integer(s):
    if len(s) == 0:
        return False
    if len(s) > 1 and s[0] == "0":
        return False
    for c in s:
        if not ("0" <= c <= "9"):
            return False

    return True


def str_is_integer(s):
    if len(s) == 0:
        return False
    if s[0] == "-":
        return str_is_pos_integer(s[1:])
    if len(s) > 1 and s[0] == "0":
        return False
    for c in s:
        if not ("0" <= c <= "9"):
            return False

    return True


def str_is_float(s):
    # xxx.xxxx ok
    # .xxx not ok
    if len(s) == 0:
        return False
    if s[0] == "-":
        return str_is_float(s[1:])
    dot_cnt = 0
    for c in s:
        if c == ".":
            dot_cnt += 1
        elif "0" <= c <= "9":
            pass
        else:
            return False
    if dot_cnt != 1:
        return False

    return True


def str_is_op(s):
    return s in operators


def to_number(s):
    if str_is_integer(s):
        return int(s)
    elif str_is_float(s):
        return float(s)
    else:
        print_error()


def main_loop(ans):
    s = get_input()
    if s == "":
        print_ans(ans)
        return ans
    elif s == "h" or s == "help":
        print_help()
        return ans
    elif s == "ans":
        if ans != None:
            print_ans(ans)
            return ans
        else:
            print_error("ans none")
            return None
    elif s == "q" or s == "quit":
        bye()
    else:
        old_ans = ans
        ans, is_valid = calc(s)
        if not is_valid:
            print_error("invalid input")
            return old_ans
        print_ans(ans)
        return ans


def test():
    cases = test_case.split("\n")
    print(cases)
    cases = [case for case in cases if case != ""]
    for case in cases:
        print_ans(case, " = ", calc(case))


def parenthesis_stack_test():
    pst = parenthesis_stack()
    s = ")(())"
    for i in range(len(s)):
        print(pst.push(s[i], i))
        print(pst.get_str())
        print()


def main():
    print_welcome()
    ans = None
    while True:
        ans = main_loop(ans)


from typing import List
import argparse

parser = argparse.ArgumentParser(description="simple python cli program")
# __version_info__ = ("2013", "03", "14")
# __version__ = "-".join(__version_info__)
__version__ = "3.0"
parser.add_argument(
    "-v", "--version", action="version", version="%(prog)s " + __version__
)

parser.add_argument(
    "input",
    metavar="input",
    type=str,
    nargs="+",
    help="one or several optional input strings to calculate",
)

parser.add_argument(
    "-d", "--debug", default=False, type=bool, help="toggle debug output"
)

args = parser.parse_args()

DEBUG = args.debug

if args.input:
    for s in args.input:
        ans, flag = calc(s)
        if flag:
            print_ans(s, " = ", ans)
        else:
            print_error("invalid input", " " + s)
else:
    # test()
    main()
