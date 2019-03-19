from fractions import Fraction 
  
def identity(n): 
    m=[[0 for x in range(n)] for y in range(n)] 
    for i in range(0,n): 
        m[i][i] = 1 
    return m 
  
def transposeMatrix(m): 
    return list(map(list,zip(*m))) 
  
def getMatrixMinor(m,i,j): 
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])] 
  
def getMatrixDeternminant(m): 
    #base case for 2x2 matrix 
    if len(m) == 2: 
        return m[0][0]*m[1][1]-m[0][1]*m[1][0] 
  
    determinant = 0 
    for c in range(len(m)): 
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c)) 
    return determinant 
  
def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m) 
    #special case for 2x2 matrix: 
    if len(m) == 2: 
        return [[m[1][1]/determinant, -1*m[0][1]/determinant], 
               [-1*m[1][0]/determinant, m[0][0]/determinant]] 
  
    #find matrix of cofactors 
    cofactors = [] 
    for r in range(len(m)): 
        cofactorRow = [] 
        for c in range(len(m)): 
            minor = getMatrixMinor(m,r,c) 
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor)) 
        cofactors.append(cofactorRow) 
    cofactors = transposeMatrix(cofactors) 
    for r in range(len(cofactors)): 
        for c in range(len(cofactors)): 
            cofactors[r][c] = cofactors[r][c]/determinant 
    return cofactors 
  
def matmult(a,b): 
    zip_b = zip(*b) 
    zip_b = list(zip_b) 
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in zip_b] for row_a in a]

def get_lcm(x, y):
   if x > y:
       greater = x
   else:
       greater = y
   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1
   return lcm
  
def get_probabilities(state_matrix): 
    for row in state_matrix: 
        row_sum = sum(row) 
        for i, val in enumerate(row): 
            if row_sum != 0: 
                row[i] = val/row_sum 
    return state_matrix

def get_qr_mat_zeros(state_matrix):
    r_dim = list(range(0,len(state_matrix)))
    q_dim = []
    for i, row in enumerate(state_matrix):
        for j, column in enumerate(row):
            if column != 0 and state_matrix[j][i] != 0:
                if i in r_dim:
                    r_dim.remove(i)
                    q_dim.append(i)
    q_mat = [[0 for x in range(len(q_dim))] for y in range(len(q_dim))]
    r_mat = [[0 for x in range(len(q_dim))] for y in range(len(r_dim))]
    for i, i_val in enumerate(q_dim):
        for j, j_val in enumerate(q_dim):
            q_mat[i][j] = state_matrix[i_val][j_val]/sum(state_matrix[i_val])
    for i, i_val in enumerate(q_dim):
        for j, j_val in enumerate(r_dim):
            r_mat[i][j] = state_matrix[i_val][j_val]/sum(state_matrix[i_val])
    return q_mat, r_mat
  
def get_qr_mat(state_matrix): 
    state_matrix = get_probabilities(state_matrix) 
    count = 0 
    for row in state_matrix: 
        if sum(row) == 0:
            count += 1
    for i, row in enumerate(state_matrix):
        if sum(row) == 0:
            for next_row in state_matrix[i+1:]:
                if sum(next_row) != 0:
                    return get_qr_mat_zeros(state_matrix)
    q_dim = (len(state_matrix[0])-count,len(state_matrix[0])-count) 
    r_dim = (len(state_matrix[0])-count, len(state_matrix[0])-q_dim[0]) 
    q_mat = [state_matrix[i][:q_dim[1]] for i in range(q_dim[0])]
    r_mat = [state_matrix[i][r_dim[0]:] for i in range(q_dim[0])]
    return q_mat, r_mat
  
def get_f_mat(q_mat): 
    i_mat = identity(len(q_mat)) 
    diff_mat = [[a-b for a, b in zip(xrow, yrow)] for xrow, yrow in zip(i_mat,q_mat)]
    return getMatrixInverse(diff_mat) 
  
def get_fr_mat(f_mat, r_mat):
    fr_mat = matmult(f_mat, r_mat)
    print(fr_mat)
    fr_vec = fr_mat[0]
    return fr_vec

def get_answer(fr_vec):
    answer_list = []
    for i in range(0,len(fr_vec)):
        answer_list.append(Fraction(fr_vec[i]).limit_denominator())
    answer_list.append(0)
    denom = 0
    for i, val in enumerate(answer_list):
        if denom == 0 and val != 0:
            denom = val.denominator
        if val != 0 and answer_list[i+1] != 0:
            denom = get_lcm(denom, answer_list[i+1].denominator)
    for i, val in enumerate(answer_list):
        answer_list[i] = int(val.numerator*(denom/val.denominator))
    answer_list[-1] = denom
    return answer_list
  
def answer(state_matrix):
    if len(state_matrix[0]) == 1:
        return [1,1]
    else:
        state_matrix = get_probabilities(state_matrix) 
        q_mat, r_mat = get_qr_mat(state_matrix) 
        f_mat = get_f_mat(q_mat) 
        fr_vec = get_fr_mat(f_mat, r_mat)
        print(get_answer(fr_vec))
        return get_answer(fr_vec)



assert(answer([[0,2,1,0,0],[0,0,0,3,4],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])==[7,6,8,21])
assert(answer([[0,1,0,0,0,1],[4,0,0,3,2,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])==[0,3,2,9,14])
assert(answer([[0]])==[1,1])
assert(answer([[1,2,3,0,0,0],[4,5,6,0,0,0],[7,8,9,1,0,0],[0,0,0,0,1,2],[0,0,0,0,0,0],[0,0,0,0,0,0]])==[1,2,3])
assert(answer([[0,0,12,0,15,0,0,0,1,8],[0,0,60,0,0,7,13,0,0,0],[0,15,0,8,7,0,0,1,9,0],[23,0,0,0,0,1,0,0,0,0],[37,35,0,0,0,0,3,21,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])==[1,2,3,4,5,15])
assert(answer([[0,7,0,17,0,1,0,5,0,2],[0,0,29,0,28,0,3,0,16,0],[0,3,0,0,0,1,0,0,0,0],[48,0,3,0,0,0,17,0,0,0],[0,6,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])==[4,5,5,4,2,20])
assert(answer([[1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0]])==[1,1,1,1,1,5])
assert(answer([[1,1,1,0,1,0,1,0,1,0],[0,0,0,0,0,0,0,0,0,0],[1,0,1,1,1,0,1,0,1,0],[0,0,0,0,0,0,0,0,0,0],[1,0,1,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,0,0,0],[1,0,1,0,1,0,1,1,1,0],[0,0,0,0,0,0,0,0,0,0],[1,0,1,0,1,0,1,0,1,1],[0,0,0,0,0,0,0,0,0,0]])==[2,1,1,1,1,6])
assert(answer([[0,86,61,189,0,18,12,33,66,39],[0,0,2,0,0,1,0,0,0,0],[15,187,0,0,18,23,0,0,0,0],[1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])==[6,44,4,11,22,13,100])
assert(answer([[0,0,0,0,3,5,0,0,0,2],[0,0,4,0,0,0,1,0,0,0],[0,0,0,4,4,0,0,0,1,1],[13,0,0,0,0,0,2,0,0,0],[0,1,8,7,0,0,0,1,3,0],[1,7,0,0,0,0,0,2,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])==[1,1,1,2,5])
