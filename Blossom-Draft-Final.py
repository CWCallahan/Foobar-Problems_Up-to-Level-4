import math


# Basic implementation of the euclid algorithm for GCD
def e(a, b):
    if a % b == 0: return b
    return e(b, a % b)


# I solved for the looping rule by plotting loop and match relations and noticed that while most pairs appeared
#  to loop, the ones that went to a match appeared on specific slopes and periodicities, doing some math, I derived
#  the following rule and function
def find_loops(v1, v2):
    if v1 == 0 or v2 == 0: return
    if math.log((v1 + v2) / e(v1, v2), 2) % 1:
        return True
    else:
        return False

# Here we read in our list and generate a graph using our rule. I worked with matrices and nodes for ease of debugging
def graphify(l):
    v = [0] * len(l)
    g = [[0 for i in range(len(l))] for j in range(len(l))]
    for i in range(len(l)):
        for j in range(len(l)):
            if find_loops(l[i], l[j]):
                v[i] = l[i]
                v[j] = l[j]
                g[i][j] = 1
                g[j][i] = 1
    return nodeify(g, v)

# Converts any graph matrix and index list to a node object graph
def nodeify(matrix, vert):
    g = {}
    for i in range(len(vert)):
        g[i] = Node(vert[i])

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                if i == j:
                    continue
                else:
                    g[i].neighbors.append(g[j])
    return g

# Our Node class we will use this for
class Node:
    def __init__(self, v):
        self.matched_to = int()
        self.neighbors = []
        self.value = v
        self.visited = False
        self.prev = None
        self.petals = []
        self.stem = None

    def __repr__(self):
        return str(self.value)

    def augment(self):
        self.matched_to = self.prev
        self.prev.matched_to = self
        if self.prev.prev == None:
            return
        else:
            self.prev.prev.augment()

    def open_blossom(self):
        for n in self.petals:
            for neighbor in n:
                if neighbor not in self.petals:
                    neighbor.neighbors.append(n)
        # for each neighbor of each petal, re-add edges to from neighbors to
        # if stem is matched to the same node as the blossom then we can keep the same matches,
        # #otherwise we alternate
        return


    def path_finder(self, exposed):
        q = []
        self.prev = None
        q.append(self)
        visited = {}

        while len(q) > 0:
            n1 = q.pop()
            if n1 in visited:
                continue
            if n1 == self:
                visited[n1] = 0
            else:
                visited[n1] = visited[n1.prev] + 1

            for n2 in n1.neighbors:

                # 1/4 outcomes: Neighbor is "behind" us
                if n2 == n1.prev or n2 == n1:
                    continue

                # 2/4 outcomes: we hit blossom or an inert loop
                if n2 in visited and n2.matched_to == n2.prev:
                    # and if n2.prev == n2.match then for sure this is blossom
                    updated_nodes = None
                    blossom = bloomify(n1, n2, visited)
                    if blossom.stem == self:
                        updated_nodes = blossom.path_finder(exposed)
                    else:
                        updated_nodes = self.path_finder(exposed)
                    return updated_nodes

                # Inert loop
                elif n2 in visited:
                    continue

                # Guaranteed to progress, augment, or dead end here so define prev
                n2.prev = n1

                # 3/4 outcomes: path is an augmenting path
                if not n2.matched_to:
                    # ie. if n2 exposed. This ends our bfs for this node
                    n2.augment()
                    if self in exposed:
                        exposed.remove(self)
                    elif len(self.petals) > 0:
                        exposed.remove(self.stem)
                    exposed.remove(n2)
                    return exposed

                # 4/4 move forward along established path or reach dead end
                else:
                    visited[n2] = visited[n1] + 1
                    n2.matched_to.prev = n2
                    q.append(n2.matched_to)

        # didn't find any exposed so return
        return exposed


# m path should always be longer or equal
# we take in two nodes and their distance from
def bloomify(n, m, v):  # fold_blossom
    # n1 is always lower so:
    blossom = Node(None)
    blossom.petals = [m, n]

    # Get the two paths to be equal distance from the stem folding nodes into blossom
    while v[m] > v[n]:
        if m not in blossom.petals:
            blossom.petals.append(m)
        m = m.prev

    # Until we find the stem we fold every node into the blossom
    while m != n:
        if m not in blossom.petals:
            blossom.petals.append(m)
        m = m.prev
        if n not in blossom.petals:
            blossom.petals.append(n)
        n = n.prev

    # Count stem as a petal for code simplicity later
    if n not in blossom.petals:
        blossom.petals.append(n)
    blossom.stem = n
    blossom.matched_to = n.matched_to

    # Set up our outgoing and incoming edges
    for p in blossom.petals:
        for e in p.neighbors:  # optomize?
            if e not in blossom.petals:
                if p in e.neighbors:
                    e.neighbors.remove(p)
                e.neighbors.append(blossom)
                blossom.neighbors.append(e)

    blossom.value = "Blossom with stem: " + str(n.value) + " size: " + str(len(blossom.petals))
    return blossom  # TODO prob want to return a way to track # of blossoms


def solution(l):
    g = graphify(l)
    exposed = set()
    for n in g:
        exposed.add(g[n])

    for n in g:
        if g[n] in exposed:
            exposed = g[n].path_finder(exposed)
            if len(exposed) == 0:
                return len(exposed)
    return len(exposed)
