# Team AI-Migos -- Loading/Unloading and Balancing of Containers on X2 Class Ship

# IMPORTS: libraries to use in code
import numpy as np #fast, efficient arrays, and calculations
import re # regex
import time # performance, error timeout
import datetime # for log file print

# Log file setup
log_file_to_write = "KeoghLongBeach" + str(datetime.datetime.now().year) + ".txt"
log_file = open(log_file_to_write, "a") # log file variable in use in all functions
user_name = "123" # user who signs in, "123" signifies no previous user signed in (first run)


#FUNCTION: all functions below
def write_to_log_file(message, file_name):
    log_file = open(file_name, "a")
    log_file.write(f"{get_date_time()} {message} \n")
    print("Log file written")

def count_containers(container_array):
    count = 0
    for rows in container_array:
        for container in rows:
            container_name = container[0]
            if container_name != "NAN" and container_name != "UNUSED":
                count += 1
    return count

#Any function with ## above it denotes that it isn't immediately required for integration
##
def log_file_init(): # determine if the user wants the log file restarted when programs starts
    global log_file
    choice = input("Do you want to restart the log file? y for yes, n for no\n-> ")
    while choice != "y" and choice != "n":
        choice = input("Do you want to restart the log file? y for yes, n for no\n-> ")
    if choice == "y":
        open(log_file_to_write, 'w').close() # clear file
    return

# Helper with log file printing [Month Day, Year:] (no appending space)
def get_date_time():
    return f"{datetime.datetime.now().strftime('%B')} {datetime.datetime.now().day}, {datetime.datetime.now().year}: {datetime.datetime.now().hour:0>2}:{datetime.datetime.now().minute:0>2}"

##
def log_file_change_user():
    global log_file, user_name
    if user_name != "123": # if there is a previous user, sign them out
        log_file.write(f"{get_date_time()} {user_name} signs out\n")
    user_name = input("Enter the name of the User to sign in\n-> ") # new user
    log_file.write(f"{get_date_time()} {user_name} signs in\n")
    return
##
def log_file_enter_comment():
    global log_file
    comment = input("Enter comment to append to log file\n-> ")
    log_file.write(f"{get_date_time()} {comment}\n")
    return

#initializing manifest by getting name
#We need this function in order to initialize array that is passed into ship_balance() argument within driver file
def manifest_init(file_name):
    #file_name = input("Enter the name of the manifest file. Example: SSMajestic.txt\n-> ")
    #new_filename = file_name.split(".")[0] + "OUTBOUND.txt" # for updated manifest file
    # file_name = "ship_unbalanceable.txt"

    with open(file_name) as f:
        lines = f.readlines()

    # [8x12] grid, bottom left [1,1], top right [8,12] ;; arr[i][j] = [Name, Weight]
    arr = np.empty([8,12], dtype='object') # Ship grid with Containers and weights
    # populate ship_arr with Container [Name, weight]
    # vals is list: [row, column, weight, name]
    container_cnt = 0 # for log file manifest open message
    for line in lines:
        vals = [int(s) for s in re.findall(r'\b\d+\b', line)] + [line.split(",")[-1].strip()]
        arr[r(vals[0])][c(vals[1])] = [vals[3], vals[2]]
        if vals[2] > 0:
            container_cnt += 1
    #pen(log_file_to_write, 'w').close()
    #log_file.write(f"{get_date_time()} Manifest {file_name} is opened, there are {container_cnt} containers on the ship\n") # log file open manifest message
    #print(arr)
    
    #return new_filename, arrs
    return arr

def write_new_manifest(f_to_write, arr):
    open(f_to_write, 'w').close() # clear file
    f = open(f_to_write, "a")
    for i in range(1, 9):
        for j in range(1, 13):
            col = "0" + str(j) if j < 10 else str(j)
            cell = arr[r(i)][c(j)]
            l_write = f"[0{i},{str(j):0>2}], {{{str(cell[1]):0>5}}}, {cell[0]}"
            f.write(l_write)
            if i != 8 or j != 12: # not last line
                f.write("\n")
    f.close()
    # log file manifest finished 
    #log_file.write(f"{get_date_time()} Finished a Cycle. Manifest {f_to_write} was written to desktop, and a reminder pop-up to operator to send file was displayed." + "\n")
    return

# Load/Unload
# 1 minute within ship, 2 minutes to truck, 4 minutes ship/buffer
'''
def load_unload_ship(arr, op, name, weight=0):
    move_dict = {
        'coord_list': [],
        'name': '',
        'first': (),
        'next': (),
        'time_taken': 0,
        'time_to_move': 0
    }
    c_name = name
    c_weight = weight

    if op == "l": # load

        ##we don't need this
        #c_name = input("Enter exact name of container to load.\n-> ") # container name to move
        #c_weight = int(input("Enter weight of container\n-> ")) # container weight
        cell_to_insert = [c_name, c_weight]

        # search for least time to insert
        least_time = float('inf')
        best_loc = [-1,-1]
        for col in range(1, 13):
            i = 8
            if arr[r(8)][c(col)][0] != "UNUSED": # check if top of column is already full
                continue
            while i > 1 and arr[r(i-1)][c(col)][0] == "UNUSED":
                i -= 1
            curr_time = r(i) + c(col)
            if curr_time < least_time:
                least_time = curr_time
                best_loc = [i, col]
        arr[r(best_loc[0])][c(best_loc[1])] = cell_to_insert # optimal location to place container [time]
        print(f"The estimated time of this load operation is {least_time+2} minutes") # time estimation, +2 from truck -> ship
        print(f"Move {c_name} container with weight {c_weight} from the truck to [{best_loc[0]}, {best_loc[1]}] on the ship.") # instruction
        log_file.write(f"{get_date_time()} \"{c_name}\" is onloaded\n") # log file onloading
        move_dict = move_c(arr, cell_to_insert, 1, 1, least_time+2, coord_list=[])
    elif op == "u": # unload
        #c_name = input("Enter exact name of container to offload.\n-> ") # container name to move
        #needs to be rewritten
        #move_dict_R = move_c(arr, cell, 7, 1, 0, coord_list=[]) this is what it was in balancing
        move_dict = move_c(arr, [c_name, 0], -1, -1, 0,coord_list=[]) # loc == -1 to unload
        #print(f"The estimated time of this unload operation is {time_taken} minutes") # time estimation
        log_file.write(f"{get_date_time()} \"{c_name}\" is offloaded\n") # log file offloading

    return move_dict'''

def load(arr,name,weight=0):
    ##we don't need this
    # c_name = input("Enter exact name of container to load.\n-> ") # container name to move
    # c_weight = int(input("Enter weight of container\n-> ")) # container weight
    c_name = name
    c_weight = weight
    cell_to_insert = [c_name, c_weight]

    # search for least time to insert
    least_time = float('inf')
    best_loc = [-1, -1]
    for col in range(1, 13):
        i = 8
        if arr[r(8)][c(col)][0] != "UNUSED":  # check if top of column is already full
            continue
        while i > 1 and arr[r(i - 1)][c(col)][0] == "UNUSED":
            i -= 1
        curr_time = r(i) + c(col)
        if curr_time < least_time:
            least_time = curr_time
            best_loc = [i, col]
    arr[r(best_loc[0])][c(best_loc[1])] = cell_to_insert  # optimal location to place container [time]
    print(f"The estimated time of this load operation is {least_time + 2} minutes")  # time estimation, +2 from truck -> ship
    print(f"Move {c_name} container with weight {c_weight} from the truck to [{best_loc[0]}, {best_loc[1]}] on the ship.")  # instruction
    #log_file.write(f"{get_date_time()} \"{c_name}\" is onloaded\n")  # log file onloading
    return arr, best_loc

def unload(arr,name):
    c_name = name
    log_file.write(f"{get_date_time()} \"{c_name}\" is offloaded\n")
    unloadedContainer, coord_list = move_c(arr, [c_name, 0], -1, -1, 0, coord_list=[])

    return arr
    #return move_c(arr, [c_name, 0], -1, 0, 0, coord_list=[])

def check_if_ship_is_balanced(arr):
        l_cells = []
        r_cells = []
        l_w = 0
        r_w = 0

        for i in range(1, 9):
            for j in range(1, 13):
                cell = arr[r(i)][c(j)]
                if (cell[1] > 0):
                    if j <= 6:  # left side
                        l_cells.append(cell + [j, i])
                        l_w += cell[1]
                    else:  # right side
                        r_cells.append(cell + [j])
                        r_w += cell[1]

        return check_unbalance(l_w, r_w)

# Balance ship: Heavier side of ship is no more than 10%
# weight of lighter side
def balance_ship(arr):
    # Get weight on both sides

    l_cells = []
    r_cells = []
    l_w = 0
    r_w = 0

    for i in range(1,9):
        for j in range(1,13):
            cell = arr[r(i)][c(j)] 
            if(cell[1] > 0):
                if j <= 6: # left side
                    l_cells.append(cell + [j,i])
                    l_w += cell[1] 
                else: # right side
                    r_cells.append(cell + [j])
                    r_w += cell[1]
    
    s_time = time.time()
    while (check_unbalance(l_w, r_w)): # while the ship is legally unbalanced
        if l_w > r_w: # move left -> right
            l_w -= l_cells[0][1]
            r_w += l_cells[0][1]
            temp = l_cells[0]
            l_cells.pop(0)
            r_cells.append(temp)
        else: # move right -> left
            r_w -= r_cells[0][1]
            l_w += r_cells[0][1]
            temp = r_cells[0]
            r_cells.pop(0)
            l_cells.append(temp)
        
        # check if timeout (balance not possible)
        if(time.time() - s_time >= 5):
            print("\n\nBalance not possible -_- PERFORM SIFT (put all containers in buffer zone, heaviest switch back and forth till row is filled, move up)\n")
            log_file.write(f"{get_date_time()} The ship is not able to be balanced according to the legal definition in its current state. The operator must perform SIFT.\n") # log file balancing fail
            sift_configuration, estimated_time = perform_sift(arr)
            #print(f"The estimated time of this SIFT operation is {time_taken} minutes") # time estimation
            log_file.write(f"{get_date_time()} SIFT has been completed.\n") # log file balancing fail
            return sift_configuration, estimated_time
    
    # Balance is possible, determine which cells have to move to the other side
    to_move_right = []
    for cell in r_cells:
        if cell[2] <= 6:
            cell.pop()
            to_move_right.append(cell)
            print(to_move_right)
    to_move_left = []
    for cell in l_cells:
        if cell[2] > 6:
            cell.pop()
            to_move_left.append(cell)
            print(to_move_left)

    total_time_taken = 0

    move_dict_L = {
        'coord_list': [],
        'name': '',
        'first': (),
        'next': (),
        'time_taken': 0,
        'time_to_move': 0
    }
    move_dict_R = {
        'coord_list': [],
        'name': '',
        'first': (),
        'next': (),
        'time_taken': 0,
        'time_to_move': 0
    }

    coord_listR = []
    coord_listL = []

    total_time = 0

    for cell in to_move_right:
        #total_time_taken += move_c(arr, cell, 7, 1, 0)
        move_dict_R, coord_listR = move_c(arr, cell, 7, 1, 0, coord_list=[])
        total_time_taken += total_time
    for cell in to_move_left:
        #total_time_taken += move_c(arr, cell, 6, -1,0)
        move_dict_L, coord_listL = move_c(arr, cell, 6, -1, 0, coord_list=[])
        total_time_taken += total_time

    #index 0 is left operations, index 1 is right, index 3 is total time


    coord_list = coord_listR + coord_listL
    balanceData = (move_dict_L, move_dict_R, total_time_taken)

    for data in balanceData:
        if type(data) == dict:
            coord_list.insert(0,data)

    print("\nContainers to move to the left [port]:",to_move_left)
    print("Containers to move to the right [starboard]:",to_move_right)
    # print("Moved Containers: \n\n",arr)
    print(f"The estimated time of this balancing operation is {total_time_taken} minutes") # time estimation balancing
    #log_file.write(f"{get_date_time()} The ship has been balanced according to the legal definition of balancing.\n") # log file balancing success

    print(balanceData)
    return arr
# Helper to balance_ship function
# Returns false if the two sides of ship are balanced;; true otherwise.
def check_unbalance(l_w, r_w): 
    if l_w == r_w:
        return False
    max_side = max(l_w,r_w)
    min_side = min(l_w,r_w)
    return (((max_side - min_side) / max_side) > 0.1)

#define getters
def getName(name):
    return name
def getFirst(first):
    return first

def getTime_taken(time_taken):
    return time_taken

def getTime_to_move(time_to_move):
    return time_to_move

def getPrev_coords(prev_coords):
    return prev_coords

def getDict(name,first,next,time_taken,time_to_move,prev_coords):
    moveDict = {
        "prev_coords": prev_coords, #list
        "name": name, #string
        "first": first, #tuple
        "next": next, #tuple
        "time_taken": time_taken, #int
        "time_to_move": time_to_move #int
    }
    return moveDict


# Helper for balance/unload optimal move for container [recursive]
# cell is to be moved, loc is column to start with, mod is to either move right (+1) or move left (-1)
# if loc is -1, cell is to be unloaded (removed from ship array)
# time_taken is minutes the operation has taken so far, saved and added to in recursive calls.
# 1 minute within ship, 2 minutes ship <-> truck, 4 minutes ship <-> buffer
# coord list is a list of coords this container has moved through
# returns a movement dictionary for a cell
def move_c(arr, cell, loc, mod, time_taken, coord_list):
    row_c,cell_c = find_cell(arr, cell) # get cell's index
    j = cell_c # orginal cell column
    i = 8 # current row number

    time_to_move = 0
    moveDict = {
        #"prev_coords": coord_list,
        "name": cell[0],
        "first": (row_c, j),
        "next": (i, cell_c),
        "time_taken": time_taken,
        "time_to_move": time_to_move
    }
    currCoord = moveDict.copy()
    while i != row_c: # loop down row to cell, move other containers out of the way
        curr_cell = arr[r(i)][c(cell_c)]
        if curr_cell[0] != "UNUSED" and curr_cell[0] != "NAN":
            out_bound = -1
            if (cell_c - mod <= 0) or (cell_c - mod >= 13): # so recurs loc doesn't go out of bounds
                out_bound = 1
            currCoord,coord_list = move_c(arr, curr_cell, cell_c + (mod * out_bound), mod * out_bound, time_taken, coord_list)
            coord_list.append(currCoord)
        i -= 1
    # here, access to container with nothing above, time to move to loc column
    # make current cell UNUSED
    cell_weight = arr[r(i)][c(cell_c)][1]
    arr[r(i)][c(cell_c)] = ["UNUSED", 0]
    #UNLOAD
    if loc == -1: # if container is to be unloaded
        print(f"Move {cell[0]} container with weight {cell_weight} from [{i}, {cell_c}] in the ship to the truck.") # instruction
        moveDict['name']=cell[0]
        #return statement just returns time
        #return time_taken + r(i) + c(cell_c) + 2 # take previous time taken + current container movement + (2 ship->truck)
        return moveDict, coord_list
    # check that no column from cell_c to loc is completely full
    # if any are, move the top container out of the way
    for col in range(cell_c + mod, loc + mod, mod):
        curr_cell = arr[r(8)][c(col)]
        if curr_cell[0] != "UNUSED":
            coord_list, time_taken = move_c(arr, curr_cell, col + mod, mod, time_taken, coord_list)
    # get to loc column
    time_to_move = 0 # for minute calculations
    print(f"Move {cell[0]} container with weight {cell[1]} from [{i}, {cell_c}] in the ship to ", end = '') # instruction
    name = cell[0]
    while cell_c != loc:
        if arr[r(i)][c(cell_c + mod)][0] == "UNUSED": # move mod column if possible
            cell_c += mod
        else: # move up, because can't move column
            i += 1
        time_to_move += 1 # +1 minute either case
    # then move as far down as possible, meaning when the cell below is not UNUSED
    while i > 1 and (arr[r(i-1)][c(cell_c)][0] == "UNUSED"):
        i -= 1
        time_to_move += 1 # +1 minute each row gone down
    # place the cell at [i, cell_c]
    arr[r(i)][c(cell_c)] = cell
    moveDict["next"] = (i,cell_c)

    total_time = time_taken + time_to_move

    #moveDict['prev_coords'] = coord_list.append(move_c())
    print(f"[{i}, {cell_c}] in the ship.") # instruction
    #return moveDict #coord_list + (row_c, j) + (i, cell_c), time_taken + time_to_move # cell has been successfully moved, return time
    return moveDict, coord_list

# Helper for move_c to return arr index of cell
# cell is guaranteed to be in arr
def find_cell(arr, cell):
    for i in range(1,9):
        for j in range(1,13):
            if arr[r(i)][c(j)][0] == cell[0]: # match
                return i,j
    return None # not possible to reach

# i is row user space, return row matrix space
def r(i):
    return 8-i

# i is column user space, return column matrix space
def c(i):
    return i-1

# perform SIFT on the ship
# put all containers in buffer zone, heaviest switch back and forth till row is filled, move up
# 1 minute within ship, 2 minutes ship <-> truck, 4 minutes ship <-> buffer
def perform_sift(arr):
    # add all containers to buffer zone
    time_taken = 0
    buffer = []
    coord_list = []

    for col in range(1, 13):
        for row in range(8, 0, -1):
            cell = arr[r(row)][c(col)]
            if cell[1] > 0: # if it's a container
                buffer.append(cell)
                arr[r(row)][c(col)] = ["UNUSED", 0] # clear out cell
                time_taken += 8 # ship -> buffer and buffer -> ship
                print(f"Move {cell[0]} container with weight {cell[1]} from [{row}, {col}] in the ship to the buffer zone.") # instruction
                coord_list.append({
                    "name": cell[0],
                    "first": (row,col),
                    "next": (-1, -1),
                    "time_taken": time_taken,
                })

    # sort them by weight [descending]
    buffer.sort(key = lambda x: x[1], reverse = True)

    # place heaviest container, alternate port and starboard sides
    mod = -1 # to alternate 
    for cell in buffer:
        row = 1
        col = int(6.5 + mod * 0.5) # 6 for port, 7 for starboard
        while arr[r(row)][c(col)][0] != "UNUSED":
            col += mod
            if col < 1 or col > 12:
                row += 1
                col = int(6.5 + mod * 0.5) # reset col
        arr[r(row)][c(col)] = cell # place the cell
        time_taken += r(row) + c(col)
        print(f"Move {cell[0]} container with weight {cell[1]} from the buffer zone to [{row}, {col}] in the ship.") # instruction
        mod *= -1 # switch side
    return arr, time_taken

# MAIN: method below
# Log file initialization

"""

log_file_init()
log_file_change_user()

# READ: the manifest file
new_filename, arr = manifest_init()

while(1):
    op = input("l for load, u for unload, b for balance, s for change user, c for adding user comment to log file, p for finishing the current manifest and open a new one, q for quit.\n-> ")
    if op == "l" or op == "u":
        load_unload_ship(arr, op)
    elif op == "b":
        balance_ship(arr)
    elif op == "s":
        log_file_change_user()
    elif op == "c":
        log_file_enter_comment()
    elif op == "p":
        write_new_manifest(new_filename, arr)
        new_filename, arr = manifest_init()
    elif op == "q":
        # create updated manifest file
        # log file write that cycle has finished
        write_new_manifest(new_filename, arr)
        log_file.write(f"{get_date_time()} {user_name} signs out\n")
        log_file.close()
        break

    print(arr)

"""