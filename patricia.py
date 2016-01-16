#!/usr/bin/python3

class TNode:

    def __init__(self, children):
        self.children = children

    def is_leaf(self):
        return self.children is None

    def __repr__(self):
        return repr(self.children)

class PaTrie:

    def __init__(self):
        self.root = TNode(None)

    def find(self, word):
        cur = self.root
        i = 0
        while not cur.is_leaf():
            for label, child in cur.children.items():
                if word[i:i + len(label)] == label:
                    cur = child
                    i += len(label)
                    break
            else:
                return False
        return i == len(word)

    def insert(self, word):
        self._insert(word)
        if "" in self.root.children:
            del self.root.children[""]

    def _insert(self, word):
        cur = self.root
        i = 0
        while not cur.is_leaf():
            for label, child in cur.children.items():
                cl = self.common_prefix_len(word[i:], label)
                if cl:
                    if cl == len(label):
                        cur = child
                        i += len(label)
                        break

                    del cur.children[label]

                    cur.children[label[:cl]] = TNode({
                        label[cl:]: child,
                        word[i + cl:]: TNode(None),
                    })
                    return

            else:
                cur.children[word[i:]] = TNode(None)
                return

        cur.children = {
            "": TNode(None),
            word[i:]: TNode(None)
        }

    def __str__(self):
        s = []
        def _str(tnode, sofar, label, prepend):
            if tnode.is_leaf():
                if label:
                    s.append(prepend + "+ " + label)
                s.append(prepend + "  {"+sofar+"}")
            else:
                s.append(prepend + "+ " + label)
                for label, child in tnode.children.items():
                    _str(child, sofar + label, label, prepend + "  ")
        _str(self.root, "", "", "")

        return "PaTrie:\n" + "\n".join(s) + "\n"


    def common_prefix_len(self, a, b):
        i = 0
        for x, y in zip(a, b):
            if x == y:
                i += 1
            else:
                break
        return i


if __name__ == "__main__":
    t = PaTrie()
    words = "autobus", "auto", "abraka", "dabra", "abrakadabra", "honza", "honirna", "honicka", "hony", "ho"
    for w in words:
        t.insert(w)
        print(t)
        print(t.root)
