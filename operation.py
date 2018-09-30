import getopt
import sys
import random

operator_precedence = {
    '(': 0,
    ')': 0,
    '+': 1,
    '-': 1,
    '×': 2,
    '÷': 2
}


def postfix_convert(exp):
    '''
    将表达式字符串，转为后缀表达式
    如exp = "1+2*(3-1)-4"
    转换为：postfix = ['1', '2', '3', '1', '-', '*', '+', '4', '-']
    '''
    stack = []  # 运算符栈，存放运算符
    postfix = []  # 后缀表达式栈
    for char in exp:
        #        print char, stack, postfix
        if char not in operator_precedence:  # 非符号，直接进栈
            postfix.append(char)
        else:
            if len(stack) == 0:  # 若是运算符栈啥也没有，直接将运算符进栈
                stack.append(char)
            else:
                if char == "(":
                    stack.append(char)
                elif char == ")":  # 遇到了右括号，运算符出栈到postfix中，并且将左括号出栈
                    while stack[-1] != "(":
                        postfix.append(stack.pop())
                    stack.pop()

                elif operator_precedence[char] > operator_precedence[stack[-1]]:
                    # 只要优先级数字大，那么就继续追加
                    stack.append(char)
                else:
                    while len(stack) != 0:
                        if stack[-1] == "(":  # 运算符栈一直出栈，直到遇到了左括号或者长度为0
                            break
                        postfix.append(stack.pop())  # 将运算符栈的运算符，依次出栈放到表达式栈里面
                    stack.append(char)  # 并且将当前符号追放到符号栈里面

    while len(stack) != 0:  # 如果符号站里面还有元素，就直接将其出栈到表达式栈里面
        postfix.append(stack.pop())
    return postfix


# ===========================这部分用于构造表达式树================================#
class Node(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def create_expression_tree(postfix):
    """
    利用后缀表达式，构造二叉树
    "1+2*(3-1)-4"
    ['1', '2', '3', '1', '-', '*', '+', '4', '-']
    """
    stack = []
    # print postfix
    for char in postfix:
        if char not in operator_precedence:
            # 非操作符，即叶子节点
            node = Node(char)
            stack.append(node)
        else:
            # 遇到了运算符，出两个，进一个。
            node = Node(char)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    # 将最后一个出了即可。
    return stack.pop()

# 避免出现负数，假分数
def check(tree):
    if tree:
        if tree.left == None:
            return tree.val
        num1 = check(tree.left)
        num2 = check(tree.right)
        if tree.val == '-':
            if eval(num1 + '-' + num2) < 0:
                supporter = tree.left
                tree.left = tree.right
                tree.right = supporter
                return calculate(num2, num1, '-')
            else:
                return calculate(num1, num2, '-')
        elif tree.val == '÷':
            if eval(num1 + '/' + num2) > 1:
                supporter = tree.left
                tree.left = tree.right
                tree.right = supporter
                return calculate(num2, num1, '÷')
            else:
                return calculate(num1, num2, '÷')
        elif tree.val == '+':
            return calculate(num1, num2, '+')
        elif tree.val == '×':
            return calculate(num1, num2, '×')


# 将树输出为字符串
def exchangetree(tree, equation):
    if tree:
        if tree.left == None:
            equation.append(tree.val)
        else:
            equation.append('(')
            exchangetree(tree.left, equation)
            equation.append(tree.val)
            exchangetree(tree.right, equation)
            equation.append(')')


def calculate(a, b, c):
    if len(a.split('/')) == 2:
        m = a.split('/')
        fzm = m[0]
        fmm = m[1]
    else:
        fzm = int(a)
        fmm = 1
    if len(b.split('/')) == 2:
        n = b.split('/')
        fzn = n[0]
        fmn = n[1]
    else:
        fzn = int(b)
        fmn = 1
    if c == '+':
        Fz = int(fzm) * int(fmn) + int(fmm) * int(fzn)
        Fm = int(fmm) * int(fmn)
        return str(Fz) + '/' + str(Fm)
    if c == '-':
        Fz = int(fzm) * int(fmn) - int(fmm) * int(fzn)
        Fm = int(fmm) * int(fmn)
        return str(Fz) + '/' + str(Fm)
    if c == '×':
        Fz = int(fzm) * int(fzn)
        Fm = int(fmm) * int(fmn)
        return str(Fz) + '/' + str(Fm)
    if c == '÷':
        Fz = int(fzm) * int(fmn)
        Fm = int(fmm) * int(fzn)
        return str(Fz) + '/' + str(Fm)


def main(n, r):
    z = 1
    ex = []
    answer = []
    while (int(z) < int(n) + 1):
        m = exercise(r)
        tree = create_expression_tree(postfix_convert(m))
        try:
            aa = check(tree)
        except:
            continue
        b = []
        exchangetree(tree, b)
        del b[0]
        b.pop()
        aa = exchangesize(aa)
        answer.append('%s'%aa)
        c = ''
        bb = c.join('%s' % id for id in b)
        ex.append(bb)
        z = z + 1
    with open('Exercises.txt', 'w+') as f:
        for i in range(len(ex)):
            f.write(str(i + 1) + '. ' + str(ex[i]) + ' = ' + '\n')  # 存放题目
    with open('Answers.txt', 'w+') as f:
        for i in range(len(answer)):
            f.write(str(i + 1) + '. ' + str(answer[i]) + '\n')  # 存放答案



def number(r):  # 随机生成一个分数或者整数
    m = [random.randint(2, int(r)) for _ in range(3)]
    for i in range(2, m[1]):
        while (m[0] % i == 0 and m[1] % i == 0):
            m[0] = m[0] // i
            m[1] = m[1] // i
    if m[1] > m[2]:
        return str(m[0]) + "/" + str(m[1])
    else:
        return str(m[2])


def opt():  # 随机生成一个运算符
    ops = ['+', '-', '×', '÷']  # 运算符
    op = random.randint(0, 3)
    return ops[op]


def exercise(r):  # 随机生成题目放在列表里
    list = []
    if random.randint(1, 4) == 1:
        list.append(number(r))
        list.append(opt())
        list.append(number(r))
    elif random.randint(1, 4) == 2:
        start = random.randint(0, 2)
        end = 0
        if start == 0:
            end == 0
        else:
            end = start + 1
        for i in range(1, 4):
            if i == start:
                list.append("(")
            list.append(number(r))
            if i == end:
                list.append(")")
            list.append(opt())
        list.pop()

    else:
        start = random.randint(0, 3)
        end = 0
        if start == 0:
            end == 0
        else:
            end = start + 1 + random.randint(0, 1)
            if end >= 4:
                end = 4
        for i in range(1, 5):
            if i == start:
                list.append("(")
            list.append(number(r))
            if i == end:
                list.append(")")
            list.append(opt())
        list.pop()
    return list


def exchangesize(g):  # 分数（包括假分数，整数，真分数）转化成真分数
    m = g.split('/')
    c = int(m[0]) // int(m[1])
    d = int(m[0]) % int(m[1])
    if int(m[0]) > int(m[1]):
        if d == 0:
            return str(c)
        else:
            return str(c) + "’" + str(d) + "/" + str(m[1])
    if int(m[0]) == int(m[1]):
        return 1
    if int(m[0])==0:
        return 0
    else:
        for i in range(2, int(m[1])):
            while (int(m[0]) % i == 0 and int(m[1]) % i == 0):
                m[0] = int(m[0])// i
                m[1] = int(m[1]) // i
        return str(m[0]) + "/" + str(m[1])


def b(k):  # 带分数转化成假分数
    m = k.split('’')  # 带分数的点是中文’
    mm = m[1].split('/')
    c = int(m[0]) * int(mm[1]) + int(mm[0])
    return str(c) + "/" + str(mm[1])


def compare(exercisefile ,answerfile ):
    correct = []
    wrong = []
    with open(answerfile, 'r') as a:
        text = a.readlines()
        hangshu = len(text)
    for i in range(hangshu):  # 读取答案文件的行数，循环对比
      # 第i行
        with open(exercisefile, 'r') as problem:
            timuhang = problem.readlines()
            a = []
            question = timuhang[i].split()
            b=''
            for size in question[1]:    
                if size not in "+-×÷()":
                    b=b+size
                else:
                    if b!='':
                        a.append(b)
                        b=''
                    a.append(size)
            if b!='':
                a.append(b)             
        with open(answerfile, 'r') as filea:
            text = filea.readlines()
            l = len(text)
            answer=text[i].split()
            result = answer[1]
        if str(result) == str(exchangesize(check(create_expression_tree(postfix_convert(a))))):
            correct.append(i + 1)
        else:
            wrong.append(i + 1)
    print('Correct: {}{}'.format(len(correct), tuple(correct)) + '\n' + 'Wrong: {}{}'.format(len(wrong), tuple(wrong)))



if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hr:n:e:a:")
    if '-r' in opts[0]:
        r = opts[0][1]
        if '-n' in opts[1]:
            n = opts[1][1]
            main(n,r)
    if '-e' in opts[0]:
        exercisefile = opts[0][1]
        if '-a' in opts[1]:
            answerfile = opts[1][1]
            compare(exercisefile ,answerfile )