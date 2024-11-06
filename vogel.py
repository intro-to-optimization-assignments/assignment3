def diff_bw_min_and_next_to_min(vector):
    if len(vector) < 2:
        return None
    vector_copy = vector[:]
    min_value = min(vector_copy)
    vector_copy.remove(min_value)
    next_to_min_value = min(vector_copy)
    return abs(min_value - next_to_min_value)

def calculate_cell(table, i, j, rows_cnt, cols_cnt):
    row_sum = 0
    col_sum = 0
    for i_ in range(rows_cnt):
        col_sum += table[i_][j]
    for j_ in range(cols_cnt):
        row_sum += table[i][j_] 
    return row_sum, col_sum


def vogels_approximation(S_original, C_original, D_original):
    C = C_original[:]
    S = S_original[:]
    D = D_original[:]
    rows_cnt = len(C)
    cols_cnt = len(C[0])
    final_table = [[0 for i in range(len(C[0]))] for j in range(len(C))]
    under_considertion_r = [i for i in range(len(C))]
    under_considertion_c = [i for i in range(len(C[0]))]

    while len(under_considertion_c) > 1 and len(under_considertion_r) > 1:
        row_diff = []
        col_diff = []
        for i in range(rows_cnt):
            if i not in under_considertion_r:
                row_diff.append(None)
            else:
                vector = []
                for j in range(cols_cnt):
                    if j not in under_considertion_c:
                        pass
                    else:
                        vector.append(C[i][j])
                row_diff.append(diff_bw_min_and_next_to_min(vector))

        for i in range(cols_cnt):
            if i not in under_considertion_c:
                col_diff.append(None)
            else:
                vector = []
                for j in range(rows_cnt):
                    if j not in under_considertion_r:
                        pass
                    else:
                        vector.append(C[j][i])
                col_diff.append(diff_bw_min_and_next_to_min(vector))

        max_in_col = 0
        index_col = 0
        for i in range(cols_cnt): # finding max in col_diff
            if col_diff[i] == None:
                continue
            if col_diff[i] > max_in_col:
                max_in_col = col_diff[i]
                index_col = i
        
        max_in_row = 0
        index_row = 0
        for i in range(len(row_diff)): # finding max in row_diff
            if row_diff[i] == None:
                continue
            if row_diff[i] > max_in_row:
                max_in_row = row_diff[i]
                index_row = i
        
        if max_in_row < max_in_col: 
            min_value = None
            index_min = None
            for i in under_considertion_r:
                if min_value == None or C[i][index_col] < min_value:
                    min_value = C[i][index_col]
                    index_min = i
            insert = min(S[index_min], D[index_col])
            final_table[index_min][index_col] = insert
            if S[index_min] > D[index_col]:
                under_considertion_c.remove(index_col)
                S[index_min] -= insert
                D[index_col] -= insert
            else:
                under_considertion_r.remove(index_min)
                S[index_min] -= insert
                D[index_col] -= insert
        else:
            min_value = None
            index_min = None
            for i in under_considertion_c:
                if min_value == None or C[index_row][i] < min_value:
                    min_value = C[index_row][i]
                    index_min = i
            insert = min(S[index_row], D[index_min])
            final_table[index_row][index_min] = insert
            if S[index_row] > D[index_min]:
                under_considertion_c.remove(index_min)
                S[index_row] -= insert
                D[index_min] -= insert
            else:
                under_considertion_r.remove(index_row)
                S[index_row] -= insert
                D[index_min] -= insert

    for i in range(rows_cnt):
        for j in range(cols_cnt):
            if final_table[i][j] == 0:
                row_sum, col_sum = calculate_cell(final_table, i, j, rows_cnt, cols_cnt)
                if row_sum != S_original[i] and col_sum != D_original[j]:
                    if D[j] < S[i]:
                        final_table[i][j] = D[j]
                        D[j] = 0
                    else:
                        final_table[i][j] = S[i]
                        S[i] = 0
    return final_table

        

    


# S_cnt = 3
# D_cnt = 4
# Supply_vector = [float(x) for x in input().split()]
# Cost_matrix = []
# for i in range(S_cnt):
#     vector = [float(x) for x in input().split()]
#     Cost_matrix.append(vector)
# Demand_vector = [float(x) for x in input().split()]
# print(vogels_approximation(Supply_vector, Cost_matrix, Demand_vector))
