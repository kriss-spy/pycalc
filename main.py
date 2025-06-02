# v1

operators = ["+", "-", "*", "/"]


def print_help():
    help_msg = """
    this is a simple cli calculator
    input in the order of operand1, operator, operand2
    supported operator:
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
        "missing op": "operator missing",
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


def calc(a, b, operator):
    # assuming params are valid
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        print(a, "/", b, "=")
        if b == 0 or b == "0":
            print_error("zero division")
            return None
        else:
            return a / b


def is_digit(s):
    # supported number:
    # integer
    # float

    return is_integer(s) or is_float(s)


def is_pos_integer(s):
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
    s = input()
    return s


def main_loop(a, b, operator, ans):
    print("> ", end="")
    s = get_input()
    if s == "":
        pass
    elif s == "h" or s == "help":
        print_help()
    elif s == "ans":
        if ans != None:
            print(ans)
        else:
            print_error("ans none")

    elif is_digit(s):
        if a == None:
            a = to_digit(s)
        elif operator != None:
            b = to_digit(s)
            ans = calc(a, b, operator)
            a = None
            b = None
            operator = None
            print(ans)
        else:
            print_error("missing op")
    elif is_op(s):
        if a != None:
            operator = s
        else:
            print_error("missing a")

    else:
        print_error("invalid input")

    return a, b, operator, ans


def main():
    print_welcome()
    ans = None
    a = None
    b = None
    operator = None
    while True:
        a, b, operator, ans = main_loop(a, b, operator, ans)


main()
