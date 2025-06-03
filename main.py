# v2
# 1+2*3-5
# use stack

operators = ["+", "-", "*", "/"]
priorities = {"*": 1, "/": 1, "+": 2, "-": 2}
use_parenthesis = False  # add support to ()
separate_cli = (
    False  # always display the equation on top, always input at the bottom line)
)


class stack:
    li = list()

    def __init__(self):
        pass

    def get_li(self):
        return stack.li

    def push(self, val):
        self.li.append(val)

    def top(self):
        return self.li[-1]

    def pop(self):
        foo = self.li[-1]
        del self.li[-1]
        return foo

    def size(self):
        return len(self.li)


def print_help():
    help_msg = """
    this is a simple cli calculator
    input in the order of operand1, op, operand2
    supported op:
    """
    for op in operators:
        help_msg += " " + op

    print(help_msg)


def print_error(*args):
    if len(args) == 0:
        print("something is wrong")
        return
    prompt = args[0]
    start_msg = "[ERROR]"
    msgs = {
        "not num": "input is not a number",
        "missing op": "op missing",
        "missing a": "first operand missing",
        "invalid input": "input is invalid",
        "ans none": "answer doesn't exist",
        "zero division": "zero division",
    }
    if prompt not in msgs.keys():
        print("something is wrong")
        return

    print(start_msg + msgs[prompt])


def print_welcome():
    welcome_msg = """
welcome to pycalc, a simple cli calculator app
    """
    print(welcome_msg)


def bye():
    bye_msg = """
bye!
    """
    print(bye_msg)
    exit()


def atom_calc(a, b, op):
    # assuming params are valid
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        print(a, "/", b, "=")
        if b == 0 or b == "0":
            print_error("zero division")
            return None


def equation_split(s):
    res = []
    l = 0
    while l < len(s):
        if is_digit(s[l]):
            r = l + 1
            while r < len(s) and (is_digit(s[r]) or s[r] == "."):
                r += 1
            res.append(s[l:r])
            l = r - 1
        else:
            r = l + 1
            while r < len(s) and not is_digit(s[r]):
                r += 1
            res.append(s[l:r])
            l = r - 1

        l += 1

    return res


def calc(s):
    is_valid = True
    ans = 0
    st = stack()
    symbols = equation_split(s)
    prev_is_digit = False

    # check input validity
    for i in range(len(symbols)):
        if not prev_is_digit and is_digit(symbols[i]):
            prev_is_digit = True
            symbols[i] = to_digit(symbols[i])
        elif prev_is_digit and is_op(symbols[i]):
            prev_is_digit = False
        else:
            return ans, False

    for sym in symbols:
        if st.size() == 0 and is_op(sym):
            return ans, False
        elif st.size() == 0:
            st.push(sym)
        else:
            if is_op(sym):
                st.push(sym)
            else:
                if priorities[st.top()] == 1:
                    op = st.pop()
                    a = st.pop()
                    atom_ans = atom_calc(a, sym, op)
                    if atom_ans == None:
                        return ans, False
                    st.push(atom_ans)
    nums = [sym for sym in st.get_li() if not is_op(sym)]
    if __debug__:
        print(nums)
    ans = sum(nums)

    return ans, is_valid


def is_digit(s):
    # supported number:
    # integer
    # float

    return is_integer(s) or is_float(s)


def is_pos_integer(s):
    if len(s) == 0:
        return False
    if len(s) > 1 and s[0] == "0":
        return False
    for c in s:
        if not ("0" <= c <= "9"):
            return False

    return True


def is_integer(s):
    if len(s) == 0:
        return False
    if s[0] == "-":
        return is_pos_integer(s[1:])
    if len(s) > 1 and s[0] == "0":
        return False
    for c in s:
        if not ("0" <= c <= "9"):
            return False

    return True


def is_float(s):
    # xxx.xxxx ok
    # .xxx not ok
    if len(s) == 0:
        return False
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


def is_op(s):
    return s in operators


def to_digit(s):
    if is_integer(s):
        return int(s)
    elif is_float(s):
        return float(s)
    else:
        print_error()


def get_input():
    print("> ", end="")
    s = input()
    return s


def print_ans(ans):
    print(ans)


def main_loop(ans):
    s = get_input()
    if s == "":
        return ans
    elif s == "h" or s == "help":
        print_help()
        return ans
    elif s == "ans":
        if ans != None:
            return ans
        else:
            print_error("ans none")
            return None
    elif s == "q" or s == "quit":
        bye()
    # elif is_digit(s):
    #     if a == None:
    #         a = to_digit(s)
    #     elif op != None:
    #         b = to_digit(s)
    #         ans = calc(a, b, op)
    #         a = None
    #         b = None
    #         op = None
    #         print(ans)
    #     else:
    #         print_error("missing op")
    # elif is_op(s):
    #     if a != None:
    #         op = s
    #     else:
    #         print_error("missing a")

    else:
        old_ans = ans
        ans, is_valid = calc(s)
        if not is_valid:
            print_error("invalid input")
            return old_ans
        return ans


def main():
    print_welcome()
    ans = None
    while True:
        ans = main_loop(ans)
        if ans != None:
            print_ans(ans)


main()
