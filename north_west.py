def apply_nw(vector_s, matrix_c, vector_d):
    # Check if the method is applicable by ensuring the dimensions are correct
    if len(vector_s) != len(matrix_c) or len(vector_d) != len(matrix_c[0]):
        print("The method is not applicable!")
        exit(0)
    # elif ():
    #     ....
    else:
        # Check if the problem is balanced
        if sum(vector_s) != sum(vector_d):
            print("The problem is not balanced!")
            exit(0)
        else:

            # Initialize the solution matrix with zeros
            x0 = [[0] * len(vector_d) for _ in range(len(vector_s))]

            # Apply the Northwest Corner Method
            i, j = 0, 0
            while i < len(vector_s) and j < len(vector_d):
                # Determine the allocation amount for cell (i, j)
                allocation = min(vector_s[i], vector_d[j])
                x0[i][j] = allocation
                vector_s[i] -= allocation
                vector_d[j] -= allocation

                # Move to the next cell based on remaining supply or demand
                if vector_s[i] == 0:
                    i += 1
                elif vector_d[j] == 0:
                    j += 1

            # Display the initial basic feasible solution
            print()
            print("Vectors of Initial Basic Feasible Solution (x0) using Northwest Corner Method:")
            for row in x0:
                print(" ".join(map(str, row)))
