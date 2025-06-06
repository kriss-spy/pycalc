from rich import print as rprint


def debug_log(*args):
    print("[DEBUG]", end="")
    rprint(*args)


def print_error(*args):  # TODO rich
    if len(args) == 0:
        print("something is wrong")
        return
    prompt = args[0]
    start_msg = "[ERROR]"
    extra_msg = ""
    if len(args) > 1:
        extra_msg = args[1]
    msgs = {
        "not num": "input is not a number",
        "missing op": "op missing",
        "missing a": "first operand missing",
        "invalid input": "input is invalid",
        "ans none": "answer doesn't exist",
        "zero division": "zero division",
        "parenthesis": "parenthesis error in input",
    }
    if prompt not in msgs.keys():
        print("something is wrong")
        return

    print(start_msg + msgs[prompt] + ";" + extra_msg)


def print_welcome():  # TODO rich
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


class parenthesis_elem:
    is_open = True
    idx = 0

    def __init__(self, p, idx):
        self.is_open = p == "("
        self.idx = idx

    def open(self):
        return self.is_open

    def get_idx(self):
        return self.idx


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

    def empty(self):
        return len(self.li) == 0


class parenthesis_stack:  # TODO check
    st = stack()

    def __init__(self):
        self.st = stack()

    def push(self, p, idx):
        if self.empty() and p == ")":
            return None, False
        elif self.empty():
            self.st.push(parenthesis_elem(p, idx))
            return None, True
        elif p == ")" and self.top().open():
            return self.pop(), True
        else:
            self.st.push(parenthesis_elem(p, idx))
            return None, True

    def top(self):
        return self.st.top()

    def pop(self):
        return self.st.pop()

    def empty(self):
        return self.st.empty()

    def get_str(self):
        return "".join([("(" if p.open() else ")") for p in self.st.get_li()])


def get_input():
    print("> ", end="")
    s = input()
    return s


def print_ans(*args):
    rprint(*args)


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
