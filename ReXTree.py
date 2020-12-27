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
                if isinstance(self.rex[i], Binary):  # Если оператор бинарный
                    pair = Pair(self.rex[i].value, self.max_of_pairs(pairs) + 1)  # Записывам ему максимально
                    pairs.append(pair)  # возможное значение
                    i = i + 1  # а следующему за ним на 1 больше
                    pair = Pair(self.rex[i].value, self.max_of_pairs(pairs) + 1)
                    current_literal = pair.value
                    pairs.append(pair)
                elif isinstance(self.rex[i], Unary):
                    pair = Pair(self.rex[i].value, current_literal)
                    for p in pairs:
                        p.value = p.value - 1
                    pairs.append(pair)
            i = i + 1
        self.tree = AVL_Tree()
        self.root = None
        for j in range(len(pairs)):
            self.root = self.tree.insert(self.root, pairs[j])

    def max_of_pairs(self, pairs):
        max = 0
        for p in pairs:
            if p.value > max:
                max = p.value
        return max

    def __str__(self):
        return self.tree.show(self.root)


class Pair:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value


class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.height = 1


class AVL_Tree(object):

    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key.value < root.data.value:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key.value < root.left.data.value:
            return self.rightRotate(root)

        if balance < -1 and key.value > root.right.data.value:
            return self.leftRotate(root)

        if balance > 1 and key.value > root.left.data.value:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and key.value < root.right.data.value:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def rightRotate(self, z):

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    def getBalance(self, root):
        if not root:
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right)

    def show(self, root):
        self.str = ""
        self.inOrder(root)
        return self.str

    def inOrder(self, root):

        if not root:
            return

        self.inOrder(root.left)
        self.str += ("{0}".format(root.data.symbol))
        self.inOrder(root.right)


tree = ReXTree("a*,b*|c*,h,f,s,t")
print(str(tree))
