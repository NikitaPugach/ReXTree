from abc import ABC

class Operator(ABC):
    def __init__(self):
        self.value = ''

class Unary(Operator, ABC):
    def __init__(self):
        self.value = ''

class Binary(Operator, ABC):
    def __init__(self):
        self.value = ''

class Repeat(Unary):
    def __init__(self):
        self.value = '*'

class Or(Binary):
    def __init__(self):
        self.value = '|'

class Concat(Binary):
    def __init__(self):
        self.value = ','

class Plus(Unary):
    def __init__(self):
        self.value = '+'

class Literal:
    def __init__(self, s):
        self.value = s

class ReXTree:
    def __init__(self, str):
        self.str = str
        self.tree = None
        self.rex = []
        self.create()

    def create(self):
        for s in self.str:
            if s == '*':
                self.rex.append(Repeat())
            elif s == '|':
                self.rex.append(Or())
            elif s == '+':
                self.rex.append(Plus())
            elif s == ',':
                self.rex.append(Concat())
            else:
                self.rex.append(Literal(s))
        self.createTree()

    def createTree(self):
        current_literal = 0
        pairs = []
        i = 0
        while i < len(self.rex):
            if i == 0:
                pair = Pair(self.rex[i].value, 1)  # Первому элементу устанавливаем значение 1
                pairs.append(pair)
                current_literal = 1
            else:
                if isinstance(self.rex[i], Binary):   # Если оператор бинарный
                    pair = Pair(self.rex[i].value, self.max_of_pairs(pairs) + 1)   # Записывам ему максимально
                    pairs.append(pair)      # возможное значение
                    i = i + 1         # а следующему за ним на 1 больше
                    pair = Pair(self.rex[i].value, self.max_of_pairs(pairs) + 1)
                    current_literal = pair.value
                    pairs.append(pair)
                elif isinstance(self.rex[i], Unary):
                    pair = Pair(self.rex[i].value, current_literal)
                    for p in pairs:
                        p.value = p.value - 1
                    pairs.append(pair)
            i = i + 1
        for j in range(len(pairs)):
            if j == 0:
                self.tree = Node(pairs[j])
            else:
                self.tree.insert(pairs[j])

    def max_of_pairs(self, pairs):
        max = 0
        for p in pairs:
            if p.value > max:
                max = p.value
        return max

    def inorder(self, node):
        str = ""
        if not node is None:
            str = str + self.inorder(node.left)
            str = node.data.symbol
            str = str + self.inorder(node.right)
        return str

    def __str__(self):
        return self.inorder(self.tree)


class Pair:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data:
            if data.value < self.data.value:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data.value > self.data.value:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data


tree = ReXTree("a*,b*|c*,h,f,s,t")
print(str(tree))