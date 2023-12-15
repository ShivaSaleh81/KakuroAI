import time
start = time.time()

# matrix =[[-1, -1, [20, -1], [6, -1]],
#          [-1, [14, 11], 0, 0],
#          [[-1, 21], 0, 0, 0],
#          [[-1, 8], 0, 0, -1]]
# height = 4
# width = 4

# matrix = [[-1, [4, -1], [5, -1]],
#           [[-1, 9], 0, 0],
#           [-1, -1, -1]]
# height = 3
# width = 3

matrix=[[-1, -1, -1, [17,-1], [28,-1], -1, -1],
        [-1, -1, [27, 16], 0, 0, [17,-1], [17,-1]],
        [-1, [11,27], 0, 0, 0, 0, 0],
        [[-1,3], 0, 0, [14,19], 0, 0, 0],
        [[-1,34], 0, 0, 0, 0, 0, [17,-1]],
        [-1, [-1,30], 0, 0, 0, 0, 0],
        [-1, [-1,3], 0, 0, [-1,16], 0, 0]]
height = 7
width = 7

cells = {}
guides = {}    

class Cell: 
    def __init__(self, x, y, row_guide, col_guide):
        self.value = 0
        self.row_guide = row_guide
        self.col_guide = col_guide
        self.x = x
        self.y = y
        self.next_cell = None

    def set_next_cell(self, next_cell):
        self.next_cell = next_cell

    def __str__(self) -> str:
        return f'value: {self.value}, x: {self.x}, y: {self.y}'
    

class Guide:
    def __init__(self, value, is_row) :
        self.value = value
        self.is_row = is_row
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def __str__(self) -> str:
        if self.is_row:
            return f'row guide y: {self.cells[0].y} value: {self.value}'
        else:
            return f'col guide x: {self.cells[0].x} value: {self.value}'


def is_okay(cell_key):
    for c in cells[cell_key].col_guide.cells: 
        x = 0
        for t in cells[cell_key].col_guide.cells:
            if c.value == t.value and not c.value == 0:
                x += 1
        if x >= 2:
            return False
    
    for c in cells[cell_key].row_guide.cells: 
        x = 0
        for t in cells[cell_key].row_guide.cells:
            if c.value == t.value and not c.value == 0:
                x += 1
        if x >= 2:
            return False
          
    return True

def is_okay2(guide):
    sum = 0
    for j in range(len(guide.cells)):
        sum += guide.cells[j].value
    if not sum == guide.value:
        return False
    return True

def func(cell_key):
    for value in range(1, 10):
        cells[cell_key].value = value
        if is_okay(cell_key) and (cells[cell_key].next_cell is None or func(cells[cell_key].next_cell)): 
            count = 0
            for i in range(len(guides.values())):
                if is_okay2(list(guides.values())[i]):
                    count += 1
            if count == len(guides.values()) :   
                return True
                
    cells[cell_key].value = 0
    return False


def printKakuro(matrix):
    for i in range(width) :
        for j in range(height) :
            if matrix[i][j] == -1 :
                print("■\t",end="")
            elif isinstance(matrix[i][j], list) :
                if matrix[i][j][0] == -1 :
                    print("▲" + "\\" + str(matrix[i][j][1])+ "\t",end="")
                elif matrix[i][j][1] == -1 :
                    print(str(matrix[i][j][0]) + "\\" + "▼" + "\t",end="")
                else :
                    print(str(matrix[i][j][0]) + "\\" + str(matrix[i][j][1])+ "\t",end="")
            else :
                print(cells[f'{i},{j}'].value, end="\t")
        print()



def main(matrix):

    for i in range(width):
        for j in range(height):
            if isinstance(matrix[i][j], list):
                if not matrix[i][j][0] == -1:
                    guides[f'{i},{j},col'] = Guide(matrix[i][j][0], False)
                if not matrix[i][j][1] == -1:
                    guides[f'{i},{j},row'] = Guide(matrix[i][j][1], True)

    for i in range(width):
        for j in range(height):
            if matrix[i][j] == 0 :
                g_col = -1
                g_row = -1
                cell = Cell(i, j, None, None)
                for k in range(i-1, -1, -1) :
                    if isinstance(matrix[k][j], list) :
                        g_col = guides[f'{k},{j},col']
                        guides[f'{k},{j},col'].cells.append(cell)
                        break

                for k in range(j-1, -1, -1) :
                    if isinstance(matrix[i][k], list) :
                        g_row = guides[f'{i},{k},row']
                        guides[f'{i},{k},row'].cells.append(cell)
                        break


                cell.col_guide = g_col
                cell.row_guide = g_row
                
                cells[f'{cell.x},{cell.y}'] = cell

    for i in range(len(cells.keys()) - 1) :
        key = list(cells.keys())[i]
        next_key = list(cells.keys())[i + 1]
        cells[key].set_next_cell(next_key)

    printKakuro(matrix)
    print("***************************************************")   

    first_cell = list(cells.keys())[0]
        
    if func(first_cell):  
        printKakuro(matrix)
    else:
        print("NO ANSWER")

main(matrix)

end = time.time()
print(f"Time taken: {(end-start)*10**3:.03f}ms")