# Mat K-V x K

from random import choice
from time import sleep
import tkinter as tk
from randomInputs import rand_inputs


class Piece:
    def __init__(self, x : int, y : int, color : str):
        self.x = x
        self.y = y
        self.sur = (self.x, self.y)
        self.color = color
        self.offset = [(self.x + 1) * 50 + 25, abs(500 - (self.y + 2) * 50) + 25]           # pre vykreslovanie v GUI
    
    
    def Move(self, x_n: int, y_n : int) -> None:
        """premiestni sa na nove suradnice x_n, y_n a refreshne dostupne polia ostatnych figrok"""
        sur_new = (x_n, y_n)

        self.sur = sur_new
        self.x, self.y = x_n, y_n
        self.offset = [(self.x + 1) * 50, abs(500 - (self.y + 2) * 50)]

        Refresh()  


class King(Piece):

    def __init__(self, x: int, y: int, color: str):
        super().__init__(x, y, color)

        self.AvalibleSquares = []
        
        for i in range(-1, 2):
            for j in range(-1, 2): 
                if self.x+i in range(0, 8) and self.y+j in range(0, 8) and i|j != 0:
                    self.AvalibleSquares.append((self.x+i, self.y+j)) 
        self.SurroundingSquares = self.AvalibleSquares.copy()

    def WhereToGo(self) -> None:
        """upravi premennu self.AvalibleSquares - zoznam policok na ktore sa vie dostat jednym tahom"""

        self.AvalibleSquares = []
        self.SurroundingSquares = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.x+i in range(0, 8) and self.y+j in range(0, 8) and i|j != 0:
                    new = (self.x+i, self.y+j)
                    self.SurroundingSquares.append(new)


class WhiteKing(King):      # player

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, "white")
        
    def WhereToGo(self) -> None:
        """upravi premennu self.AvalibleSquares - zoznam policok na ktore sa vie dostat jednym tahom"""

        super().WhereToGo()
        for square in self.SurroundingSquares:
            if square not in bk.SurroundingSquares:
                self.AvalibleSquares.append(square)


class BlackKing(King):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, "black")

    def WhereToGo(self) -> None:
        """upravi premennu self.AvalibleSquares - zoznam policok na ktore sa vie dostat jednym tahom"""

        super().WhereToGo()
        for square in self.SurroundingSquares:
            if square != br.sur and square not in wk.SurroundingSquares:
                self.AvalibleSquares.append(square)

                        
class BlackRook(Piece):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "black")
        self.AvalibleSquares = []

    def WhereToGo(self) -> None:
        """upravi premennu self.AvalibleSquares - zoznam policok na ktore sa vie dostat jednym tahom"""
        
        self.AvalibleSquares = []

        for s in ("x", "y"):                # "x" -> self.x, "y" -> self.y
            if s == "x":
                coordinate = self.x
            else:
                coordinate = self.y  

            for dir in (-1, 1):             # left/right, up/down v zavislosti od s

                i = 1
                while i < 8:                  
                    if coordinate + (dir * i) in range(8):
                        if s == "x":
                            if (self.x + (dir * i), self.y) == bk.sur:
                                break
                            self.AvalibleSquares.append((self.x + (dir * i), self.y))
                        elif s == "y":
                            if (self.x, (self.y + (dir * i))) == bk.sur:
                                break
                            self.AvalibleSquares.append((self.x, (self.y + (dir * i))))
                    i += 1
                        

    def Move(self, x_n: int, y_n: int) -> None:
        super().Move(x_n, y_n) 
        
        if wk.AvalibleSquares == []:
            global mat
            mat = True
                

def Refresh():
    """aktualizuje zoznamy kam kazda figurka moze ist (AvalibleSquares)"""
    br.WhereToGo()
    wk.WhereToGo()
    bk.WhereToGo()

    s1 = set(wk.AvalibleSquares)
    s2 = set(bk.AvalibleSquares)
    in_common = s1 & s2
    s1 -= in_common
    s2 -= in_common
    wk.AvalibleSquares = list(s1 - set(br.AvalibleSquares))
    bk.AvalibleSquares = list(s2)


def WhitesCorner(cv_sur: list, bk_sur: list) -> int:
    """vracia pocet policok kvadrantu v ktorom sa nachadza b. kral (sachovnica je rozdelena podla suradnic veze)"""

    x = bk_sur[0] - cv_sur[0]
    y = bk_sur[1] - cv_sur[1]

    if x == 0 or y == 0:        # sach
        return 64

    if x > 0 and y > 0:
        return (7-cv_sur[0]) * (7-cv_sur[1])
    elif x > 0 and y < 0:
        return (7-cv_sur[0]) * (cv_sur[1])
    elif x < 0 and y > 0:
        return (cv_sur[0]) * (7-cv_sur[1])
    elif x < 0 and y < 0:
        return (cv_sur[0]) * (cv_sur[1])


def BlacksBestNextMove() -> tuple:
    """vyhodnoti najlepsi tah pre cierneho. Vracia tuple kde na indexe 0 je figurka, ktorou taha
    a na indexe 1 su suradnice tahu"""

    if (wk.x, br.x, bk.x) == (0, 1, 2) or (wk.x, br.x, bk.x) == (7, 6, 5):             # ked je b. kral na kraji (lavom / pravom...) 
        if (wk.x, br.x, bk.x) == (0, 1, 2):
            p = 0
        else:
            p = 7

        if (bk.y - wk.y) == 0 and abs(br.y - wk.y) != 1:
            return ("v", (p, br.y))     

        if abs(bk.y - wk.y) % 2 == 1:
            distance = [None, 0]
            for move in br.AvalibleSquares:
                if move[0] == br.x:
                    if abs(wk.y - move[1]) > distance[1]:
                        distance  = [move, abs(wk.y - move[1])]
            return ("v", distance[0])
        
        else:
            if br.sur in wk.SurroundingSquares:
                distance = [None, 0]
                for move in br.AvalibleSquares:
                    if move[0] == br.x:
                        if abs(wk.y - move[1]) > distance[1]:
                            distance  = [move, abs(wk.y - move[1])]
                return ("v", distance[0])
            while abs(bk.y - wk.y) % 2 == 0:
                direction = wk.y - bk.y 
                if direction < 0:
                    direction = -1
                else:
                    direction = 1
                return ("k", (abs(p-2), bk.y + direction))
    

    if (wk.y, br.y, bk.y) == (0, 1, 2) or (wk.y, br.y, bk.y) == (7, 6, 5):              # ked je b. kral na kraji (hore / dole...) 
        if (wk.y, br.y, bk.y) == (0, 1, 2):
            p = 0
        else:
            p = 7

        if (bk.x - wk.x) == 0 and abs(br.x - wk.x) != 1:
            return ("v", (br.x, p))     

        if abs(bk.x - wk.x) % 2 == 1:
            distance = [None, 0]
            for move in br.AvalibleSquares:
                if move[1] == br.y:
                    if abs(wk.x - move[0]) > distance[1]:
                        distance  = [move, abs(wk.x - move[0])]
            return ("v", distance[0])
        
        else:
            if br.sur in wk.SurroundingSquares:
                distance = [None, 0]
                for move in br.AvalibleSquares:
                    if move[1] == br.y:
                        if abs(wk.x - move[0]) > distance[1]:
                            distance  = [move, abs(wk.x - move[0])]
                return ("v", distance[0])
            while abs(bk.x - wk.x) % 2 == 0:
                direction = wk.x - bk.x 
                if direction < 0:
                    direction = -1
                else:
                    direction = 1
                return ("k", (bk.x + direction, abs(p-2)))


    if WhitesCorner(br.sur, wk.sur) == 2:               # zabranuje remize tym, ze by sa biely nemal kam pohnut, ale nebol by v sachu
        p = 1
        if br.x in (1, 6):
            p = 0
        for move in bk.AvalibleSquares:
            if move[p] in (2, 5) and move in br.AvalibleSquares:
                if move[abs(p-1)] in (0,7):
                    continue
                return ("k", move)
        for move in bk.AvalibleSquares:
            if move in br.AvalibleSquares:
                return ("k", move)


    if br.sur not in bk.SurroundingSquares:           # ak c. veza a c. kral nie su pri sebe, presunie c. vezu ku c. kralovi
        for move in br.AvalibleSquares:
            if move in bk.SurroundingSquares:
                return ("v", move)
        for move in br.AvalibleSquares:
            if move[0] == bk.sur[0] and move not in wk.SurroundingSquares:
                return ("v", move)
            elif move[1] == bk.sur[1] and move not in wk.SurroundingSquares:
                return ("v", move)

    
    if br.sur not in wk.SurroundingSquares:             # zmensi WhitesCorner alebo posunie c. krala blizsie k b. kralovi
        best = [None, 999]
        for move in br.AvalibleSquares:
            if ( WhitesCorner(br.sur, wk.sur) > WhitesCorner(move, wk.sur) ):
                if move in bk.SurroundingSquares:
                    if WhitesCorner(move, wk.sur) < best[1]:
                        best = [move, WhitesCorner(move, wk.sur)]
        if best[0] != None:
            return ("v", best[0])
        else:
            best = [None, 999]
            for k_move in bk.AvalibleSquares:
                distance = (wk.x - k_move[0])**2 + (wk.y - k_move[1])**2
                if distance < best[1]:
                    best = [k_move, distance]                    
            return ("k", best[0])


    if br.sur in wk.SurroundingSquares and br.sur in bk.SurroundingSquares:         # waiting move
        best = (None, 0)
        best_dis_bk = 0
        for move in bk.AvalibleSquares:
            distance = (br.x - move[0])**2 + (br.y - move[1])**2
            if distance == 1:
                dis_bk = wk.x**2 + wk.y**2
                if dis_bk > best_dis_bk:
                    best = ("k", move)
        return best


def ValidInput(vstup : str) -> bool:
    """overi ci je vstup od uzivatela platny"""
    vstup = vstup.split()

    if len(vstup) != 3:
        return False

    for poz in vstup:
        if len(poz) != 2:
            return False
        elif poz[0] not in "abcdefgh":
            return False
        elif poz[1] not in "12345678":
            return False
    
    return True


def ValidPosition(wk : WhiteKing, br : BlackRook, bk : BlackKing) -> bool:
    """overi ci je zadana pozicia platna"""

    if wk.sur in bk.SurroundingSquares :
        return False

    if bk.sur == br.sur or wk.sur == bk.sur or wk.sur == br.sur:
        return False
    
    if wk.AvalibleSquares == []:
        return False

    return True


def TranslateInput(vstup : str) -> list:
    """prevedie vstup v sachovej notacii na zoznam suradnic"""

    vstup = vstup.split()

    output = [None] * 6

    for i in range(3):
        output[2*i] = ord(vstup[i][0])-97

    for i in range(3):
        output[2*i + 1] = int(vstup[i][1])-1

    return output


mat = False

#   GUI

root = tk.Tk()

canvas = tk.Canvas(height = 500, width = 500)
canvas.pack()

white_king = tk.PhotoImage(file = "biely_kral.png")
black_king = tk.PhotoImage(file = "cierny_kral.png")
black_rook = tk.PhotoImage(file = "cierna_veza.png")
board = tk.PhotoImage(file = "board.png")

canvas.create_image(250, 250, image = board)

submit =tk.StringVar()

l1 = tk.Label(text="Zadajte súradnice figúriek.\n\
    Postupne: biely kráľ, čierny kráľ, čierna veža.\n\
    Napríklad: b2 c5 e1")
l2 = None

e1 = tk.Entry(root, bg="#F0F0F0")
b1 = tk.Button(root, text = "Odoslať", command = lambda : submit.set(e1.get()), fg="blue")
b2 = tk.Button(text = "Náhodná pozícia", command = lambda : submit.set(choice(rand_inputs)))

l1.pack()
e1.pack()
b1.pack()
b2.pack()

while True:         # cakanie na platny vstup

    root.wait_variable(submit)

    vstup = submit.get()

    if not ValidInput(vstup):
        if l2:
            l2.destroy()
        l2 = tk.Label(text="Neplatný vstup. Skúste znova.")
        l2.pack()
        e1.delete(0, "end")
        continue

    vstup = TranslateInput( submit.get() )

    wk = WhiteKing(vstup[0], vstup[1])
    bk = BlackKing(vstup[2], vstup[3])
    br = BlackRook(vstup[4], vstup[5])
    Refresh()


    if ValidPosition(wk, br, bk):
        break

    else:
        if l2:
            l2.destroy()
        l2 = tk.Label(text="Neplatná pozícia. Skúste znova.")
        l2.pack()
        e1.delete(0, "end")
        

e1.destroy()
b1.destroy()
l1.destroy()
b2.destroy()
if l2:
    l2.destroy()



wk_img = canvas.create_image(wk.offset[0], wk.offset[1], image = white_king)
bk_img = canvas.create_image(bk.offset[0], bk.offset[1], image = black_king)
br_img = canvas.create_image(br.offset[0], br.offset[1], image = black_rook)

dots = []
for move in wk.AvalibleSquares:             # nakresli cerveny kruzok na kazde policko, kam sa moze b. kral presunut (zaciatok hry)
    x = (move[0] + 1) * 50 + 25
    y = abs(500 - (move[1] + 2) * 50 + 25)
    dots.append(canvas.create_oval(x-5, y-5, x+5, y+5, fill = "red", outline=""))


def BlackMove() -> None:
    """tah cierneho. (vykonava pocitac)"""

    Refresh()

    where = BlacksBestNextMove()
    if where[0] == "v":
        piece = br
        img = br_img
    else:
        piece = bk
        img = bk_img
    
    piece.Move(where[1][0], where[1][1])
    canvas.moveto(img, piece.offset[0], piece.offset[1])

    Refresh()

    for move in wk.AvalibleSquares:         # nakresli cerveny kruzok na kazde policko, kam sa moze b. kral presunut
        x = (move[0] + 1) * 50 + 25
        y = abs(500 - (move[1] + 2) * 50 + 25)
        dots.append(canvas.create_oval(x-5, y-5, x+5, y+5, fill = "red", outline=""))
    
    if mat == True:                         # koniec hry
        canvas.create_rectangle(200, 230, 300, 270, fill = "red")
        canvas.create_text(250, 250, text = "MAT!")
        l2 = tk.Label(text="Kliknite kdekoľvek pre ukončenie hry")
        l2.pack()


def WhiteMove(e) -> None:
    """tah bieleho. (vykonava hrac)"""
    Refresh()

    if mat == True:
        root.destroy()
        return

    if wk.AvalibleSquares == []:     # remiza v pripade ze biely kral sa nema kam pohnut (len teoreticky)
        canvas.create_rectangle(200, 230, 300, 270, fill = "red")
        canvas.create_text(250, 250, text = "REMÍZA!")

    where = (e.x//50-1, abs(9 - e.y//50)-1)
    
    if where not in wk.AvalibleSquares:
        return

    wk.Move(where[0], where[1])
    canvas.moveto(wk_img, wk.offset[0], wk.offset[1])

    if where == br.sur:             # remiza ak ostanu len krali (len teoreticky)
        canvas.create_rectangle(200, 230, 300, 270, fill = "red")
        canvas.create_text(250, 250, text = "REMÍZA!")

    for dot in dots:
        canvas.delete(dot)
        
    root.update()
    sleep(0.5)
    BlackMove()
    
        
root.bind("<Button-1>", WhiteMove)

root.mainloop()