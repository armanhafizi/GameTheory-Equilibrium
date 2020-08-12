from scipy.optimize import linprog
def state(i, n): #returns string of support set
    s = "{0:b}".format(i)
    m = len(s)
    for k in range(n - m):
        s = "0" + s
    return s
#main
u = eval(input())
m = len(u)
n = len(u[0])
#pure section
pure = []
for j in range(m):
    for k in range(n):
        flag = 1 #assume to be pure nash
        for j2 in range(len(u)):
            if u[j2][k][0] > u[j][k][0]: #cannot be pure nash
                flag = 0
                break
        if flag != 0:
            for k2 in range(len(u[0])):
                if u[j][k2][1] > u[j][k][1]: #cannot be pure nash
                    flag = 0
                    break
        if flag == 1: #pure nash
            pure.append([j, k])
print("Pure strategies:")
for l in pure:
    print("     " + str(l) + " : " + str(u[l[0]][l[1]]))
if len(pure) == 0:
    print("     None")
print("************************************")
#mixed section
mixedFound = 0 #is mixed nash found
for sup1_it in range(1, 2**m):
    for sup2_it in range(1, 2**n):
        #print("Set number ", sup1_it, " * ",sup2_it)
        sup1 = state(sup1_it, m) #support set of plater 1
        sup2 = state(sup2_it, n) #support set of plater 2
        #row player
        A_ub = [] #upper bound matrix
        b_ub = [] #upper bound vector
        A_eq = [] #equality matrix
        b_eq = [] #equality vector
        b = [] #variable bound
        c = [] #coef vector
        for j in range(m):
            row = [] #the row that will be attached to the matrix containing utilities
            for k in range(n):
                if int(sup2[k]) > 0:
                    row.append(u[j][k][0])
            row.append(-1) #coef for U1*
            if int(sup1[j]) > 0:
                A_eq.append(row)
                b_eq.append(0)
            else:
                A_ub.append(row)
                b_ub.append(0)
        sum_row = [] #the row that satisfies the sum = 1
        for k in range(n):
            if int(sup2[k]) > 0:
                sum_row.append(1)
                c.append(0)
                b.append((0, None))
        sum_row.append(0) #coef for U1* in sum
        c.append(1) #coef for U1* in min function
        b.append((None, None))
        A_eq.append(sum_row)
        b_eq.append(1)
        #print(A_eq, b_eq, A_ub, b_ub, c, b)
        if len(A_ub) == 0:
            res2 = linprog(c = c, A_eq = A_eq, b_eq = b_eq, bounds = b, method = 'revised simplex')
        else:
            res2 = linprog(c = c, A_ub = A_ub, b_ub = b_ub, A_eq = A_eq, b_eq = b_eq, bounds = b, method = 'revised simplex')
        #print(res2.success, res2.x)
        if res2.success == False: #optimization terminated unsuccessfully
            mixedFound = 0
            continue
        mixedFound = 1
        for l in res2.x:
            if l == 0 or l == 1: #strategy in support set is 0 or pure
                mixedFound = 0
                break
        if mixedFound == 0: #did not find valid answer
            continue
        #column player
        A_ub = []  # upper bound matrix
        b_ub = []  # upper bound vector
        A_eq = []  # equality matrix
        b_eq = []  # equality vector
        b = []  # variable bound
        c = []  # coef vector
        for k in range(n):
            row = []  # the row that will be attached to the matrix containing utilities
            for j in range(m):
                if int(sup1[j]) > 0:
                    row.append(u[j][k][1])
            row.append(-1)  # coef for U2*
            if int(sup2[k]) > 0:
                A_eq.append(row)
                b_eq.append(0)
            else:
                A_ub.append(row)
                b_ub.append(0)
        sum_row = []  # the row that satisfies the sum = 1
        for j in range(m):
            if int(sup1[j]) > 0:
                sum_row.append(1)
                c.append(0)
                b.append((0, None))
        sum_row.append(0)  # coef for U2* in sum
        c.append(1)  # coef for U2* in min function
        b.append((None, None))
        A_eq.append(sum_row)
        b_eq.append(1)
        #print(A_eq, b_eq, A_ub, b_ub, c, b)
        if len(A_ub) == 0:
            res1 = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=b, method='revised simplex')
        else:
            res1 = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=b, method='revised simplex')
        #print(res1.success, res1.x)
        if res1.success == False:  # optimization terminated unsuccessfully
            mixedFound = 0
            continue
        for l in res1.x:
            if l == 0 or l == 1: #strategy in support set is 0 or pure
                mixedFound = 0
                break
        if mixedFound == 1: #found mixed nash
            print("One mixed strategy:")
            print("     Strategy profile for player 1:", end= " ")
            r1 = 0
            for j in range(m):
                if int(sup1[j]) > 0:
                    print(round(res1.x[r1], 3), end=" ")
                    r1 += 1
                else:
                    print("0", end= " ")
            print("\n", end="")
            print("     Strategy profile for player 2:", end=" ")
            r2 = 0
            for k in range(n):
                if int(sup2[k]) > 0:
                    print(round(res2.x[r2],3), end=" ")
                    r2 += 1
                else:
                    print("0", end=" ")
            break
    if mixedFound == 1:
        break
if mixedFound == 0:
    print("Mixed strategy:")
    print("     None")