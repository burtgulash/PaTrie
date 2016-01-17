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
        self.root = None

    def __contains__(self, word):
        cur = self.root
        if cur is None:
            return False

        i = 0
        while cur is not None and not cur.is_leaf():
            for label, child in cur.children.items():
                if len(label) == 0 and i < len(word):
                    continue

                if word[i:i + len(label)] == label:
                    cur = child
                    i += len(label)
                    break
            else:
                return False
        return i == len(word)

    def insert(self, word):
        cur = self.root
        if cur is None:
            self.root = TNode({ word: None })
            return

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
            if tnode is None:
                return
            if tnode.is_leaf():
                if label:
                    s.append(prepend + "+ " + label)
                s.append(prepend + "  {"+sofar+"}")
            else:
                s.append(prepend + "+ " + label)
                for label, child in tnode.children.items():
                    _str(child, sofar + label, label, prepend + "  ")

        if self.root is not None:
            _str(self.root, "", "", "")

        return "\n".join(s)


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
    words = "autobus", "auto", "abraka", "dabra", "abrakadabra", "honza", "honirna", "honicka", "hony", "ho", "h"
    for w in words:
        t.insert(w)
        print("AFTER INSERTING", w)
        print(t.root)
        print(t)
        print()
