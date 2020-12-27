class Transition(object):
    def __init__(self, s1, t, s2):
        self.s1 = s1
        self.s2 = s2
        self.t = t


class LTS(object):
    def __init__(self):
        self.tokens = ['a', 'b', 'c', ' ']
        self.states = ['start', 'even', 'odd', 'finish']
        self.s_first = self.states[0]
        self.s_finish = self.states[3]
        self.transitions = [Transition(self.s_first, self.tokens[3], self.states[1]),
                            Transition(self.states[1], self.tokens[3], self.s_finish),
                            Transition(self.states[1], self.tokens[0], self.states[2]),
                            Transition(self.states[1], self.tokens[1], self.states[1]),
                            Transition(self.states[2], self.tokens[0], self.states[1]),
                            Transition(self.states[2], self.tokens[1], self.states[2])]

    def accept(self, c):
        i = 0
        j = 0
        w = []
        clos = closure(self, self.s_first)
        for cl in clos:
            w.append([cl, 0, i])  # Третий элемент равняется глобальным индексом в массиве w
            i = i + 1
        while j <= i:
            for z in w:
                if z[2] == j:
                    x = z
                    break

            if len(w) != 0:
                w.remove(x)
            else:
                break

            if x[1] == len(c):
                if x[0] == self.s_finish:
                    return True
                j = j + 1
                continue
            for t in self.transitions:          # W ← W ∪ {<s, X_snd + 1> | <X_fst, c[X_snd], s> ∈ T};
                if t.s1 == x[0] and t.t == c[x[1]]:
                    w.append([t.s2, x[1] + 1, i])
                    i = i + 1

            states = []
            for h in w:
                states.append(h[0])

            states = closure(self, states)    # W ← closure(T , W)
            new_W = []
            for h in w:
                if h[0] in states:
                    new_W.append(h)

            w = new_W

            j = j + 1

        return False


def closure(lts, x):
    if isinstance(x, list):
        w = x
    else:
        w = [x]
    w1 = None
    if x is None:
        return x
    while w != w1:
        w1 = w
        for t in lts.transitions:
            if t.s1 in w1:
                if t.t == ' ':
                    if not t.s2 in w:
                        w.append(t.s2)
    return w


lts = LTS()
print(lts.accept(" baa "))