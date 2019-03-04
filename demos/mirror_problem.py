rows = 5
cols = 6

start_r = 1
start_c = 1

start = [1,1]
end = [5, 6]


def check_solution(M ,N):

    def block_no(i, j):
        return (i-1)*cols + (j-1)
    
    mirror_locs = {}

    for m in M:
        mirror_locs[block_no(m[0], m[1])] = -1

    for n in N:
        mirror_locs[block_no(n[0], n[1])] = 1

    ray_start = block_no(start[0], start[1])
    ray_end = block_no(end[0], end[1])

    curr_ray = ray_start

    curr_r = start[0]
    curr_c = start[1]

    col_inc = 1
    row_inc = 1

    move_horizontal=True

        
    for _ in range(rows*cols):

        if move_horizontal:
            curr_c += col_inc
        else:
            curr_r += row_inc

        if (curr_c > cols) or (curr_c < 0):
            curr_r += row_inc
            curr_c  = 1

        curr_ray =  block_no(curr_r, curr_c)

        # print( "row %d cols %d"%(curr_r, curr_c) )

        if curr_ray > ray_end:
            return True
        elif curr_ray == ray_end:
            return False

        # print("Check mirror at  %d"%curr_ray)
        # print (mirror_locs)

        try:
            val = mirror_locs[curr_ray]
            # print("Found mirror at %d %d"%(curr_r, curr_c))
        except Exception as e:
            val = None

        if val is not None:

            if val == 1 and move_horizontal:
                if col_inc == 1:
                    row_inc = 1
                else:
                    row_inc = -1
                move_horizontal = False
            elif val == 1 and not move_horizontal:
                if row_inc == 1:
                    col_inc = 1
                else:
                    col_inc = -1
                move_horizontal = True
            elif val == -1 and move_horizontal:
                if col_inc == 1:
                    row_inc = -1
                else:
                    row_inc = 1
                move_horizontal = False
            elif val== -1 and not move_horizontal:
                if row_inc == 1:
                    col_inc = -1
                else:
                    col_inc = 1
                move_horizontal = True



def test_case_1():
    M = [[2,3]]
    N = [[1,2],[2,5],[4,2], [5,5]]
    return check_solution(M,N)

def test_case_2():
    M = [[2,3]]
    N = [[1,2],[2,5],[4,2], [4, 5], [5,5]]
    return check_solution(M,N)

def test_case_3():
    M = [[2,3], [4,3]] #"/"
    N = [[1,2],[2,5],[4,2],[5,5]] #"\"
    return check_solution(M,N)


if __name__ == '__main__':
    
    soln1 = test_case_1()
    soln2 = test_case_2()
    soln3 = test_case_3()
    
    if soln1:
        print ("Test case 1 is impossible")
    else:
        print ("Test case 1 is possible")

    if soln2:
        print ("Test case 2 is impossible")
    else:
        print ("Test case 2 is possible")

    if soln3:
        print ("Test case 3 is impossible")
    else:
        print ("Test case 3 is possible")
