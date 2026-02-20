import time
import os
import heapq


# ━ ┃ ┏ ┓ ┗  ┛ ┣  ┫  ┳ ╋  ┻

class Cell:
    def __init__(self, x: int, y: int, hex_val: str):
        self.x = x
        self.y = y
        val = int(hex_val, 16)
        self.walls = {
            "top": bool(val & 1),
            "right": bool(val & 2),
            "bottom": bool(val & 4),
            "left": bool(val & 8),
        }
        self.g = float('inf')
        self.h = 0
        self.parent = None
        self.is_path = False
        self.is_end = False
        self.is_start = False


    def __lt__(self, other):
        return self.f < other.f

    @property
    def f(self):
        return self.g + self.h

def seed_to_objects_matrix_converter(seed: str, width: int, height: int):
    cells_list = []
    for y in range(height):
        row = []
        for x in range(width):
            cell = Cell(x, y, seed[y * width + x])
            row.append(cell)
        cells_list.append(row)
    return cells_list


def get_corner(matrix, y, x, width, height):
    up = False
    down = False
    left = False
    right = False

    if y > 0:
        if x < width:
            up = matrix[y - 1][x].walls["left"]
        else:
            up = matrix[y - 1][x - 1].walls["right"]

    if y < height:
        if x < width:
            down = matrix[y][x].walls["left"]
        else:
            down = matrix[y][x - 1].walls["right"]

    if x > 0:
        if y < height:
            left = matrix[y][x - 1].walls["top"]
        else:
            left = matrix[y - 1][x - 1].walls["bottom"]

    if x < width:
        if y < height:
            right = matrix[y][x].walls["top"]
        else:
            right = matrix[y - 1][x].walls["bottom"]

    index = (1 if up else 0) + (2 if down else 0) + (4 if right else 0) + (8 if left else 0)
    chars = " ┃┃┃━┗┏┣━┛┓┫━┻┳╋"
    return chars[index]


def render_maze(matrix, width, height):
    for y in range(height):
        top_line = ""
        mid_line = ""

        for x in range(width):
            cell = matrix[y][x]

            top_line += get_corner(matrix, y, x, width, height)
            top_line += "━━━" if cell.walls["top"] else "   "

            mid_line += "┃" if cell.walls["left"] else " "
            if cell.is_start:
                mid_line += " S "
            elif cell.is_end:
                mid_line += " F "
            elif cell.is_path:
                mid_line += " # "
            else:
                mid_line += "   "


        top_line += get_corner(matrix, y, width, width, height)
        mid_line += "┃" if matrix[y][width - 1].walls["right"] else " "

        print(top_line)
        #time.sleep(0.2)
        print(mid_line)
        #time.sleep(0.2)

    low_line = ""
    for x in range(width):
        low_line += get_corner(matrix, height, x, width, height)
        low_line += "━━━" if matrix[height - 1][x].walls["bottom"] else "   "

    low_line += get_corner(matrix, height, width, width, height)
    print(low_line)

def manhattan_distance(start_x,start_y, end_x, end_y):
    return abs(start_x - end_x) + abs(start_y - end_y)

def trace_path(end_cell):
    path = []
    current =  end_cell

    while current is not None:
        path.append((current.y, current.x))
        current = current.parent

    return path[::-1]


def solve_maze(matrix, width, height, start_x, start_y, end_x, end_y):
    directions = [
        ("top", 0, -1),
        ("right", 1, 0),
        ("bottom", 0, 1),
        ("left", -1, 0)
    ]


    start_cell = matrix[start_y][start_x]

    open_list = []
    heapq.heappush(open_list,(start_cell.f, start_cell))

    closed_list = set()

    while open_list:
        current_f, current_cell = heapq.heappop(open_list)

        if(current_cell.y, current_cell.x) in closed_list:
            continue
        closed_list.add((current_cell.y, current_cell.x))

        yield trace_path(current_cell)

        if current_cell.x == end_x and current_cell.y == end_y:
            return

        for wall_name, dx, dy in directions:
            if not current_cell.walls[wall_name]:
                nx,ny = current_cell.x + dx, current_cell.y + dy

                if 0 <= nx < width and 0 <= ny < height:
                    neighbor = matrix[ny][nx]

                    if (ny,nx) in closed_list:
                        continue


                    new_g = current_cell.g + 1
                    if new_g < neighbor.g:
                        neighbor.parent = current_cell
                        neighbor.g = new_g
                        neighbor.h = manhattan_distance(nx, ny, end_x, end_y)
                        heapq.heappush(open_list, (neighbor.f, neighbor))








def main():
    width  = 30
    height = 30

    my_seed = "953953D153A812844682C1286C4282852AC3A939515512AC07A852AC42852AC1445283C1552857C53A9553816A93952C5455"
    my_seed1 = "811113C55556911113C55556911113C44442"
    my_seed2 = "bd51553951153953915551517911557955139551511155555553951555115551393d513d153d5553c53a93aa9287c6906a95543c3ac2955293ac4112902e9551117aad4513ae9392aaa93ac12bc3953a97c6a842aac1396c3c0793e92abc45386a8516aa82c547940452c153c2c544682844283c6852c3aaa95144544056c693c3a96c3aeac5156abae96baea81539296b903854105115384693aaa93852928284129113969553a852a815283c1529568412d0696c296aa83846a8156812ad28112ac686c6b8282a83c02c2aaba93828546a83aac5296a9545041414156a9282c451404556aa83c4442c53c55386c02ec07a812a86aaac683916a82c112c3aad150569054512eaa8393c3c1557aaeab913ad3853baa952c3d69682ac696e851686c52c43c6c542c3e92d382953a856aac6abc3e9556a96aa86c3ac386aaad03a95692c6d3a93abc56917c13c13913ab856816a803ac0796a93841296d396ad02c53a87c43aac5002ad3a851382aaa85552a93aa90002c68057ac5686ac3c3abaac456ac53a81692c3baa813bc6a952aa838683ac2c42c6939406aea82c2c39285103d14783838682e91154156aaa96c3c68442c05146902aaaa92c69057a93ac696bc386abc3c6ac382c3a93eac4292c56a811415428457a9529529452b9682aea8429104396aa85783c52c7aa9693c386ad446c3a93c6c39502aa9453aa9556abc6b829502c52aa96c146c6baab846916a93c53ac052c3c4503d551442c1392ad2aa86956c469556879042c382d3846839291512c684796816ac53c412943813944151411416aaa83ac2e96b95116951292a9456ac52c3baac4443aa93c3941429693c116ac3a846c392bc3a856944686c1456d4696812d42c2c695143947c2e83d396aea85403c38692c7c07abac2d1542a83c6ab96953c53c1391538382a9543c3969696c115696816c3a90453a856c3ea951456ac3856b96c2c116c47814556b86e83c446c42d38386bc5293aa93ad0295284053aaa93945681451547a8116a97c52853916813d12c5104395393852c4450790444442c14041407abaec42869396c5381556ea816a93940382c16a856e95281443c6aa96d153c50039517a9296969456ac5392c3aaa93bc04551544012aaa92c2e94386939292841381542a956903d042c5296aac3c3c3d5017a80542842a87c5556d514286ac003856968140282ac56aac116a85142c56ba912c3a83ad29695281282916c3eaa95551153ad2c3c1444453c3e838442a9556a96e96c385695506aa856ac2c3ea92d06a8282839016ac11386d2c543afafbfffc569680116869556a93ad3a85105143a8293a943c56843a96ac6842a843c142ea93a93baafef857f9156946aad43c39146ac3c2814450386ac6aaa90553816ec1695294685412b852aac2ac42fffafffaa95051443bc3c0453c3c14281516a854396aaaa93c6a9178383ea91693ac003eac384552d3fafd52843a9053a814541143c5456a83c3841502bac6aaa93c0456c6c3a807ac6baaa92bc2d15016fafffa83842852aaa93bac3813d53aa8380543eaaa9386c6c56d51517aac696952c2ac443c143ac1505392a8692816aa82aa8542845382c2aaa93a96a86ac5539515143c3a853a943c52c517c543ac52bc3e802c3a84456c6aac6912a9104456aaea82c3aabc157a856943a94443aac1453c53c55392a95283c3a803aea9115552c516e86aac39554296e838282ba93c69143aa813b84696956d541392c2ac546abaae8043aaac511451695292abac5554693ac0286ac28394052ac2842c5143c513952ea87ac395528045447aa845100554169042c2a9555396c43c683812aea9412c3c69697852952c6941401696a956c293939428516c0793a90290146a9538293941386aaac12c3ac783943a96d6a96b9690382bc3aa9116aaa869683e93e96c6aa86ac512e90406ec3ae8542a90452813ac43aac5396c3aad282aa87a86ac296c6c169683aa9693d6aa943bac3c43e9556c385782ac554042c3b82853c697aa8128282c3aad696c555143e92c6ac52c53a82b802969383c139528552843d17c381002c294392968282a86c52aa93c55157c1456813815453ac2aaa868142ec54683ead1003c3c550286c07ac3c280382ac2c1794286c553c3954557c2c2e95140546aac5407a91553c03c3eac43c55382a9543c35696a86c683c3a96bac1579692c39555541452ba92913ac3d3c3aac13c3eaba96b969514004013c153c3ac393a8542a9043813c56abc03b91541382c6aaaaa969292a83ac3c5286a96abc52d443868381056a96aaac3946aa96c281178292aac4556c68512aac2c12aac2eac38392a9683a81783d54016c2a8396c56c6940152ec53ec6c506a8401515139296c2c38142ac145696ac6aaad2842838415384512c2ac13d553c56c3c1392955552928386929682c413a96a85045039569693aac3a87a82a9694055683a852c1392d513a96aaea9153c6a86a928690453aaea94694552869143ac6c56ec3aaaac38141556ac450386aa95428696c56aaba956ad42ec3ac13aac52ad3c1514456c52a93955152aea8542a929510515284568297c696d1556a84413a954150296ac2952c52941295553d6c6a811296c54297ac2aad68383a8555004555693c3916a952aaa93c544692baabc53aa96e853ba9517aac0445793c29696ec55682ac691542915116a904296a942c6ac13b956c06c453ac2c3903aac69456c7c55556c56c545555556ec556c5546c546d44456c56c5455456c6c555455556c547c6c444554557"

    #12 30
    my_seed3 = "D3915791579396EC53AC556AC3953AA9553ABC69686AD52A8396969693C6AEA96BC56C53A96C54393952AC393D2EAAD687C6C3C3AC53A95556BAC392AA97954696AEAAA96953C3C3AA86D294543AAAAF96EFFFAA86AFC5157FEAC3AFFFAFFF9696C3BFAFD503A97C2FAFFFAAAC55438393EAC553BC6AAC52953A8556A93EC3C6C393C6C3BAD53AAC3956AC396AC3AA9383AA9696AC6AAAAC43A9457AEAC3D46AB9529696953C6A96A96D43C39003C45556D46C46"
    #30 30
    my_seed4 = "B91553955393939391555555553D13AEC3BAC3BC6AAC6C6C55555553C3EAC396AC56857AAB95513953B956D056BC694553853AAC4396AAD2AA953E93A9545396C7AAC53EC3AC3C6C47C52AC69556C3952C53C53AC3C5179393EA93A95396C3C53A97AABA95296AAC52AAAA96C53C3D6AC52AAC696A96C396AAC2A93945693C53AA87947AC556ABAC3EAAEA953A83BAAA83879697956AC3C56C3AA96AAC2AC6AAA96945693A96955386AC3AAD2A97AC6C3AD152C2A96956ABABC6C3EAC54393AC3C783EC6969546A853FC56FFFAEAAD453EC393AD69556A96FD5157FA96C13BA952AC69569556C3FFFAFFFAA93EAC2A96C39693A9793C53FAFD546AC3C3C6AB96A96C6A96C53AFAFFF956BC3C13AAA9683B9469396A92D5529383C3EAAAAAD6AC2D16AC3AAC5156EC6C3C3AAAAC5383C3C7C3AAA97A95539547C6AA853AAC3C5556AAAC16C53AC395556AABC687A955516A83C7956A92C39792AC13A96AD55296EA95693AAE96C3AAC3AC6A92953EA93C693AC6C3C396AABAC396AEC3C3C6C556C6D1547A856AAC3AC3C55478555557913C5396C53AA96C7A95553A9555396A8556C5396AAAD156AD5546AD53C6BAE95517AE92C456D54555554554556C5457C5456E"

    #12 12
    my_seed5 = "D53951395513D3AABAEA956E92AC6C16C553AAC553C55796AC7FBC3FFFC3853FC5057F96E96FFFAFFFC396953FAFD5168547AFAFFF83AB93C3AD156AAAAC56C3C57AC6C555545556"
    os.system("clear")

    matrix = seed_to_objects_matrix_converter(my_seed4, width, height)


    start_x, start_y = 0,0
    end_x, end_y = 25,25

    matrix[start_y][start_x].g = 0
    matrix[start_y][start_x].is_start = True
    matrix[end_y][end_x].is_end = True


    for path in solve_maze(matrix, width, height, start_x, start_y, end_x, end_y):
        os.system("clear")
        for row in matrix:
            for cell in row:
                cell.is_path = False

        for py,px in path:
            matrix[py][px].is_path = True

        render_maze(matrix, width, height)

        time.sleep(0.1)


main()