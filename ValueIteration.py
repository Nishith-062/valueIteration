import copy

REWARD = -0.01
DISCOUNT = 0.99
MAX_ERROR = 1e-3
ACTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]
NUM_ROWS = 3
NUM_COLS = 4
NUMS_ACTIONS = 4

U = [[0, 0, 0, 1], [0, 0, 0, -1], [0, 0, 0, 0]]

def printEnvironment(U, policy=False):
    for r in range(NUM_ROWS):
        print("|", end="")
        for c in range(NUM_COLS):
            if (r, c) == (1, 1):
                val = "WALL"
            elif c == 3 and r <= 1:
                val = "+1" if r == 0 else "-1"
            else:
                if policy:
                    val = ["Down", "Left", "Up", "Right"][U[r][c]]
                else:
                    val = f'{U[r][c]:.2f}'
            print(f"{str(val):^7}|", end="")
        print()

def getU(U, r, c, a):
    dr, dc = ACTIONS[a]
    nr, nc = r + dr, c + dc
    if (0 <= nr < NUM_ROWS and 0 <= nc < NUM_COLS) or (nr, nc) == (1, 1):
        return U[nr][nc]
    return U[r][c]

def calcU(U, r, c, a):
    u = REWARD
    u += 0.8 * DISCOUNT * getU(U, r, c, a)
    u += 0.1 * DISCOUNT * getU(U, r, c, (a - 1) % NUMS_ACTIONS)
    u += 0.1 * DISCOUNT * getU(U, r, c, (a + 1) % NUMS_ACTIONS)
    return u

def valueIteration(U):
    while True:
        newU = copy.deepcopy(U)
        err = 0
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if (r, c) in [(1, 1), (0, 3), (1, 3)]:
                    continue
                newU[r][c] = max(calcU(U, r, c, a) for a in range(4))
                err = max(err, abs(newU[r][c] - U[r][c]))
        U = newU
        printEnvironment(U)
        if err < MAX_ERROR * (1 - DISCOUNT) / DISCOUNT:
            break
    return U

def getoptimalPolicy(U):
    policy = [[-1] * NUM_COLS for _ in range(NUM_ROWS)]
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if (r, c) in [(1, 1), (0, 3), (1, 3)]:  
                continue
            maxAction, maxU = None, -float('inf')
            for a in range(NUMS_ACTIONS):
                u = calcU(U, r, c, a)
                if u > maxU:
                    maxAction, maxU = a, u
            policy[r][c] = maxAction
    return policy

print("iterations")
U = valueIteration(U)
print("Optimal soln:")
printEnvironment(getoptimalPolicy(U), True)
