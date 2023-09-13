import math


def e(a, b):
    # Basic implementation of the euclid algorithm for GCD
    if a % b == 0: return b
    return e(b, a % b)


def find_loops(v1, v2):
    """Math gives us a weird exploit here if any pair sums up to a power of two or is a multiple of any of those
    fractions then yeah it's good to use """
    if v1 == 0 or v2 == 0: return
    if math.log((v1 + v2) / e(v1, v2), 2) % 1:
        return True
    else:
        return False


def graphify(l):
    v = [0] * len(l)
    g = [[0 for i in range(len(l))] for j in range(len(l))]
    print(g)
    for i in range(len(l)):
        for j in range(len(l)):
            # print("finding loops for ", l[i], l[j])
            if find_loops(l[i], l[j]):
                # print((l[i], l[j]))
                v[i] = l[i]
                v[j] = l[j]
                g[i][j] = 1
                g[j][i] = 1
    return nodeify(g, v)


def nodeify(matrix, vert):
    graph = [] * len(matrix)
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
    for n in g:
        print("initializing node:", g[n], g[n].neighbors)
    return g


class Node:
    def __init__(self, v):
        self.matched_to = int()
        self.neighbors = []  # TODO get item for this
        self.value = v
        self.visited = False
        self.prev = None
        self.petals = []
        self.stem = None
        # blossom path and/or function to restore path

    def __repr__(self):
        return str(self.value)  # +", at "+str((id(self)))

    def augment(self):
        self.matched_to = self.prev
        self.prev.matched_to = self
        print("matching ", self.value, " to ", self.prev.value)
        if self.prev.prev == None:
            return
        else:
            self.prev.prev.augment()

    # def fold, def bloom #TODO
    def open(self):
        # put back all the nodes in the right place
        for n in self.petals:
            for neighbor in n:
                if neighbor not in self.petals:
                    neighbor.neighbors.append(n)

        # for each neighbor of each peatal, re-add edges to from neighbors to
        # if stem is matched to the same node as the blossom then we can keep the same matches,
        # #otherwise we alternate
        return

    # Runs a modified bloom bfs starting from self
    # TODO FIND CREATIVE SOLUTION TO KEEP A LIST OF BLOSSOMS ACCESSIBLE (OVERLOAD???)
    def path_finder(self, exposed):
        print('\n')
        q = []
        self.prev = None
        q.append(self)
        visited = {}

        while len(q) > 0:  # TODO update condition
            n1 = q.pop()
            print("bfsing from ", n1)
            if n1 in visited:
                print("visited n1 already", n1, visited[n1])
                continue  # TODO explore this more for both cases may be redundant
            if n1 == self:
                visited[n1] = 0
            else:
                visited[n1] = visited[n1.prev] + 1
            print(n1, n1.neighbors)

            for n2 in n1.neighbors:
                # 1/3 outcomes: Neighbor is "behind" us
                # for blossom we should a
                print('n2', n2, "is neighbor of", 'n1', n1)
                print(visited)
                print('p', n1.prev)

                # 1/4 outcomes: Neighbor is "behind" us
                if n2 == n1.prev or n2 == n1:  # TODO check to see if this can fuck us over maybe use visited
                    continue

                # 2/4 outcomes: we hit blossom or an inert loop
                if n2 in visited and n2.matched_to == n2.prev:  # TODO Account for non blossom condition if neccessary
                    # and if n2.prev == n2.match then for sure this is blossom
                    updated_nodes = None
                    blossom = bloomify(n1, n2, visited)
                    if blossom.stem == self:
                        updated_nodes = blossom.path_finder(exposed)
                    else:
                        updated_nodes = self.path_finder(exposed)
                    # open bloom blossom.open()
                    return updated_nodes

                # Inert loop
                elif n2 in visited:
                    continue

                # Guaranteed to progress, augment, or dead end here so define prev
                n2.prev = n1

                # 3/4 outcomes: path is an augmenting path
                if not n2.matched_to:
                    print("found aug path at:", n2)
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
                    print("moving forward added to q", n2, n2.matched_to)
                    print(visited)
                    visited[n2] = visited[n1] + 1
                    visited[n2.matched_to] = visited[n2] + 1
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
        print(">inbloom", v[m])
        if m not in blossom.petals:
            blossom.petals.append(m)
        m = m.prev

    # Until we find the stem we fold every node into the blossom
    while m != n:
        print("!=inbloom", v[n])
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
            print("petal ns", p.neighbors)
            print("edge ns", e.neighbors)
            if e not in blossom.petals:
                if p in e.neighbors:
                    e.neighbors.remove(p)
                e.neighbors.append(blossom)
                blossom.neighbors.append(e)

    blossom.value = "Bl stem: " + str(n.value) + " size: " + str(len(blossom.petals))
    print("petals", blossom.petals)
    print("b.n", blossom.neighbors)
    for e in blossom.neighbors:
        print("surounding edges", e, e.neighbors)

    # print(blossom, blossom.neighbors)
    return blossom  # TODO prob want to return a way to track # of blossoms
    # return pathfinder(self) #also unfold around here


def solution(l):
    g = graphify(l)
    exposed = set()
    for n in g:
        exposed.add(g[n])
    print(len(exposed))
    for n in g:
        if g[n] in exposed:
            exposed = g[n].path_finder(exposed)
            if len(exposed) == 0:
                return len(exposed)
        print ("Nodes left after bfs from ", g[n], ':', len(exposed))
    print(exposed)
    return len(exposed)


# Testing Zone
print(solution([1, 1]))
nums = [1, 7, 3, 21, 13, 8, 2]
g = solution(nums)
print("nums", g)
