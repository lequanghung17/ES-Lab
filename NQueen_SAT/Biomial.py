from pysat.solvers import Glucose3

def solve_nqueens(n):
    with Glucose3() as g:
        vars = [[(i * n + j + 1) for j in range(n)] for i in range(n)]
        
        # Constraint 1
        for i in range(n):
            g.add_clause(vars[i])  
            for j in range(n):
                for k in range(j + 1, n):
                    g.add_clause([-vars[i][j], -vars[i][k]])  
        
        # Constraint 2
        for j in range(n):
            col = [vars[i][j] for i in range(n)]
            g.add_clause(col) 
            for i in range(n):
                for k in range(i + 1, n):
                    g.add_clause([-vars[i][j], -vars[k][j]])  
        
        # Constraint 3
        for i1 in range(n):
            for j1 in range(n):
                for i2 in range(n):
                    for j2 in range(n):
                        if (i1 != i2 and j1 != j2) and (abs(i1 - i2) == abs(j1 - j2)):
                            g.add_clause([-vars[i1][j1], -vars[i2][j2]])
        
       
        if g.solve():
            model = g.get_model()
            board = [['.' for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if vars[i][j] in model:
                        board[i][j] = 'Q'
            for row in board:
                print(' '.join(row))
        else:
            print("UNSATISFIABLE")


solve_nqueens(4)
