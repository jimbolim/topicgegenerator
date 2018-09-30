import random


operator_precedence = {
    '(' : 0,
    ')' : 0,
    '+' : 1,
    '-' : 1,
    '×' : 2,
    '÷' : 2
}


def postfix_convert(exp):
    '''
    将表达式字符串，转为后缀表达式
    如exp = "1+2*(3-1)-4"
    转换为：postfix = ['1', '2', '3', '1', '-', '*', '+', '4', '-']
    '''
    stack = []          #运算符栈，存放运算符
    postfix = []        #后缀表达式栈
    for char in exp:
#        print char, stack, postfix
        if char not in operator_precedence:#非符号，直接进栈
            postfix.append(char)
        else:
            if len(stack) == 0:#若是运算符栈啥也没有，直接将运算符进栈
                stack.append(char)
            else:
                if char == "(":
                    stack.append(char)           
                elif char == ")":#遇到了右括号，运算符出栈到postfix中，并且将左括号出栈
                    while stack[-1]!="(":
                        postfix.append(stack.pop())
                    stack.pop()
                    
                elif operator_precedence[char] > operator_precedence[stack[-1]]:
                    #只要优先级数字大，那么就继续追加
                    stack.append(char)
                else:
                    while len(stack)!=0:
                        if stack[-1]=="(":#运算符栈一直出栈，直到遇到了左括号或者长度为0
                            break
                        postfix.append(stack.pop())#将运算符栈的运算符，依次出栈放到表达式栈里面
                    stack.append(char)#并且将当前符号追放到符号栈里面
                    
    while len(stack)!=0:#如果符号站里面还有元素，就直接将其出栈到表达式栈里面
        postfix.append(stack.pop())
    return postfix
#===========================这部分用于构造表达式树，不涉及计算================================#
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
    #print postfix
    for char in postfix:
        if char not in operator_precedence:
            #非操作符，即叶子节点
            node = Node(char)   
            stack.append(node)
        else:
            #遇到了运算符，出两个，进一个。
            node = Node(char)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    #将最后一个出了即可。
    return stack.pop()

#递归遍历树
def inorder(tree):
    if tree:
        inorder(tree.left)
        print(tree.val)
        inorder(tree.right)

#避免出现负数，假分数
def check(tree):
    if tree:
        if tree.left==None:
            return tree.val
        num1 = check(tree.left)
        num2 = check(tree.right)
        if tree.val == '-':
            if eval(num1 + '-' + num2)<0:
                supporter = tree.left
                tree.left = tree.right
                tree.right = supporter
                return calculate(num2,num1,'-')
            else:
                return calculate(num1,num2,'-')
        elif tree.val == '÷':
            if eval(num1 + '/' + num2)>1:
                supporter = tree.left
                tree.left = tree.right
                tree.right = supporter
                return calculate(num2,num1,'÷')
            else:
                return calculate(num1,num2,'÷')
        elif tree.val == '+':
            return calculate(num1,num2,'+')
        elif tree.val == '×':
            return calculate(num1,num2,'×')

#将树输出为字符串
def exchangetree(tree,equation):
    if tree:
        if tree.left==None:
            equation.append(tree.val)
        else:
            equation.append('(')
            exchangetree(tree.left,equation)
            equation.append(tree.val)
            exchangetree(tree.right,equation)
            equation.append(')')
    


#此方法用于产生分数
def proper_fraction(maxnum):
    interger = str(random.randint(0,maxnum))
    numerator = str(random.randint(0,maxnum))
    if numerator=='0':
        minnum = 1
    else: 
        minnum = int(numerator)
    denominator = str(random.randint(minnum,maxnum))
    if interger=='0':
        proper_fraction = numerator + '/' + denominator
    else:
        proper_fraction = interger + '’' + numerator + '/' + denominator
    return proper_fraction


'''
topicnum 题目的数量
maxnum 题目中的最大数字（不等于）
减法运算不能为负
除法运算不能产生假分数
'''
def create_equation(topicnum, maxnum):
    operational_characters = ['+', '-', '×', '÷']
    #项目要求不等于
    maxnum = maxnum-1
    equations = []
    for i in range(1,topicnum+1):

        #生成的运算符的数量，最多为三个
        operatornum = random.randint(1,3) 
        #当只有一个运算符时，只需要注意减法和除法
        '''
        if operatornum==1:
            equation = []
            operational_character = operational_characters[random.randint(0,3)]
            equation.append(random.randint(0,maxnum))
            equation.append(operational_character)
            #使用负值来从末尾取列表值
            if operational_character=='-':
                equation.append(random.randint(0,equation[-2]))
            elif operational_character=='÷':
                equation.append(random.randint(equation[-2],maxnum))
            equation.append('=')
        #两个运算符时,可以出现括号
        elif operatornum==2:
            #拆分为e1和e2，先生成e2，使用上面的方法即可
            e2 = []
            operational_character = operational_characters[random.randint(0,3)]
            e2.append(random.randint(0,maxnum))
            e2.append(operational_character)
            #使用负值来从末尾取列表值
            if operational_character=='-':
                e2.append(random.randint(0,equation[-2]))
            elif operational_character=='÷':
                e2.append(random.randint(equation[-2],maxnum))

            #加括号的情况
            if random.randint(1,2)==1:


        else:

            pass
        '''        
        equation=[]
        for k in range(0,operatornum+1):
            '''
            if random.randint(1,3)==1:
                equation.append(proper_fraction(maxnum))
            else:    
            '''    
            equation.append(random.randint(1,maxnum))
            if k==operatornum:
                #equation.append('=')
                continue
            else:
                equation.append(operational_characters[random.randint(0,3)])
        #print('%s. '%i, end='')
        #for a in equation:
            #print(a, end='')
        #print()
        #calculate(equation)
        equations.append(equation)
    return equations
     
def calculate(a,b,c):
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
        Fz = int(fzm)*int(fmn) + int(fmm)*int(fzn)
        Fm = int(fmm)*int(fmn)
        return str(Fz) + '/' + str(Fm)
    if c == '-':
        Fz = int(fzm)*int(fmn) - int(fmm)*int(fzn)
        Fm = int(fmm)*int(fmn)
        return str(Fz) + '/' + str(Fm)
    if c == '×':
        Fz = int(fzm)*int(fzn)
        Fm = int(fmm)*int(fmn)
        return str(Fz) + '/' + str(Fm)
    if c == '÷':
        Fz = int(fzm) * int(fmn)
        Fm = int(fmm) * int(fzn)
        return str(Fz) + '/' + str(Fm)

def a(g):#分数（包括假分数，整数，真分数）转化成真分数
    m = g.split('/')
    c = int(m[0]) // int(m[1])
    d = int(m[0]) % int(m[1])
    if int(m[0]) > int(m[1]) :
        if d == 0:
            return str(c)
        else:
            return str(c) + "’" + str(d) + "/" + str(m[1])
    if int(m[0]) == int(m[1]):
        return 1
    else:
        return str(m[0]) + "/" + str(m[1])




if __name__ == '__main__':
    '''equations = [] 
    with open("Exercises.txt") as f:
        contents = f.readlines()
        for equation in contents:
            equation = equation.strip('\n')
                i.replace('\\','')
            equations.append(equation)
'''
    b=[]
    a =['5/19', '-', '(', '17', '-', '16', '+', '5', ')']
   
    #a = equations[0]
    #print(a)
    tree =create_expression_tree(postfix_convert(a))
    #inorder(tree)
    check(tree)
    exchangetree(tree,b)
    print(b)
    
    '''for equation in equations:
        print(equation)
        tree = create_expression_tree(postfix_convert(equation))
        a = check(tree)
        b=[]
        exchangetree(tree,b)
        print(b,end='')
        print('=' + str(a))'''