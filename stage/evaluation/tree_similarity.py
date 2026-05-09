

def select_tree(t, i, m=0):
    n = m
    v = None
    for c in t[1]:
        nv, n = select_tree(c, i, m=n)
        if nv:
            v = nv

    if i == n + 1:
        return t, n + 1
    return v, n + 1

def tree_index(t, i):
    return select_tree(t, i)[0]


def leaf(tree):
    if not tree[1]:
        return tree[0]
    return leaf(tree[1][0])


def post_order(t, f, m=0):
    n=m
    for c in t[1]:
        n = post_order(c, f, n)

    n += 1
    f(n, t)
    return n

def tree_size(t):
    return post_order(t, lambda x, y: None)


def lr_keyroots(t):
    roots = []
    post_order(t, lambda x, y: roots.append((x, leaf(y))))

    selected = []

    for i, (x, y) in enumerate(roots):
        if not any(xn > x and yn == y for xn, yn in roots[i:]):
            selected.append(x)

    return selected


def insert_cost(n1, n2):
    return 1


def delete_cost(n1, n2):
    return 1


def update_cost(n1, n2):
    if n1[0] == n2[0]:
        return 0
    return 2


def tree_dist(treedist, t1, t2, i, j):
    q1 = tree_index(t1, i)
    q2 = tree_index(t2, j)

    tp = [[0 for _ in range(tree_size(q2) + 1)] for _ in range(tree_size(q1) + 1)]

    for q in range(len(tp)):
        tp[q][0] = q

    for q in range(len(tp[0])):
        tp[0][q] = q

    idif = i - (len(tp) - 1)
    jdif = j - (len(tp[0]) - 1)

    for q in range(1, len(tp)):

        qn = tree_index(t1, q + idif)

        for w in range(1, len(tp[0])):

            wn = tree_index(t2, w + jdif)

            if leaf(qn) == leaf(q1) and leaf(wn) == leaf(q2):
                tp[q][w] = min(
                    tp[q - 1][w] + delete_cost(qn, wn),
                    tp[q][w - 1] + insert_cost(qn, wn),
                    tp[q - 1][w - 1] + update_cost(qn, wn)
                )

                treedist[q + idif - 1][w + jdif - 1] = tp[q][w]
            else:
                tp[q][w] = min(
                    tp[q - 1][w] + delete_cost(qn, wn),
                    tp[q][w - 1] + insert_cost(qn, wn),
                    tp[q - 1][w - 1] + treedist[q + idif - 1][w + jdif - 1]
                )


def ted(t1, t2):
    treedist = [[0 for _ in range(tree_size(t2))] for _ in range(tree_size(t1))]
    for i in lr_keyroots(t1):
        for j in lr_keyroots(t2):
            tree_dist(treedist, t1, t2, i, j)

    return treedist[-1][-1]


def tree_sim(t1, t2):
    return 1 - ted(t1, t2) / (tree_size(t1) + tree_size(t2))
