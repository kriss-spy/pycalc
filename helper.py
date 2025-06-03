def debug_log(s):
    print("[DEBUG]", end="")
    print(s)


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


class stack:
    li = []

    def __init__(self):
        self.li = []

    def get_li(self):
        return self.li

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


def get_input():
    print("> ", end="")
    s = input()
    return s


def print_ans(ans):
    print(ans)


test_case = """
1 + 1
5 + 0
-3 + 2
10 + -4
0.1 + 0.2
5 - 3
10 - 0
2 - 5
-7 - 3
0.5 - 0.1
2 * 3
7 * 0
-4 * 2
0.5 * 4
10 / 2
7 / 1
6 / -3
5 / 2
5 / 0
999999 + 1
1000000000 * 2
0.001 * 0.002
0.005 / 2
2 - 10
5 * -2
2 + 3 * 4
10 - 4 / 2
5 + 2 - 1
8 / 2 * 3
"""
