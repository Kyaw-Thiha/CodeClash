class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getAvailableMoves(self, state) -> list[(int, bool)]:
        return []


class King(Piece):
    def getAvailableMoves(self, state) -> list[(int, bool)]:
        '''
        King available moves:
        - 0-9 (excluding 4): tiles row-wise from top-left
        '''
        availableMoves = []
        for i in range(0, 9):
            if (i == 4 
                or not 0 <= self.x - i%3 - 1 <= 4 
                or not 0 <= self.y + i//3  - 1<= 4
                or (state["board"][self.y + i//3 - 1][self.x - i%3 - 1] != None
                    and state["board"][self.y + i//3 - 1][self.x - i%3 - 1]["color"] == state["playerColor"])):
                continue
            b = (state["board"][self.y + i//3 - 1][self.x - i%3 - 1] != None 
                 and state["board"][self.y + i//3 - 1][self.x - i%3- 1]["color"] != state["playerColor"])
            availableMoves.append((i, b))
        return availableMoves
    
class Pawn(Piece):
    def getAvailableMoves(self, state) -> list[(int, bool)]:
        '''
        Pawn available moves:
        - 0: up-left attack
        - 1: one tile up
        - 2: up-right attack
        '''
        availableMoves = []
        inc = -1 if state["playerColor"] == "black" else 1
        if 0 <= self.y + inc <= 4:
            if (self.x > 0 
                and state["board"][self.y+inc][self.x-1] != None 
                and state["board"][self.y+inc][self.x-1]["color"] != state["playerColor"]):
                availableMoves.append((0, True))
            if (state["board"][self.y+inc][self.x] == None):
                availableMoves.append((1, False))
            if (self.x < 4 
                and state["board"][self.y+inc][self.x+1] != None
                and state["board"][self.y+inc][self.x+1]["color"] != state["playerColor"]):
                availableMoves.append((2, True))
        return availableMoves
    
class Bishop(Piece):
    def getAvailableMoves(self, state) -> list[(int, bool)]:
        '''
        Bishop available moves:
        - list of 4 tuples (n, b): (# of tiles moveable in direction clockwise
                                    from up-left diagonal, attack available?)
        '''
        availableMoves = []
        for inc in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            n = 0
            b = False
            cX = self.x + inc[0]
            cY = self.y + inc[1]
            while (0 <= cX <= 4 
                   and 0 <= cY <= 4
                   and state["board"][cY][cX] == None):
                n += 1
                cX += inc[0]
                cY += inc[1]

            if (0 <= cX <= 4 
                and 0 <= cY <= 4
                and state["board"][cY][cX] != None
                and state["board"][cY][cX]["color"] != state["playerColor"]):
                n += 1
                b = True
            availableMoves.append((n, b))
            
        return availableMoves

class Rook(Piece):
    def getAvailableMoves(self, state) -> list[(int, bool)]:
        '''
        Rook available moves:
        - list of 4 tuples (n, b): (# of tiles moveable in direction clockwise
                                    from up vertical, attack available?)
        '''
        availableMoves = []
        for inc in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            n = 0
            b = False
            cX = self.x + inc[0]
            cY = self.y + inc[1]
            while (0 <= cX <= 4 
                   and 0 <= cY <= 4
                   and state["board"][cY][cX] == None):
                n += 1
                cX += inc[0]
                cY += inc[1]

            if (0 <= cX <= 4 
                and 0 <= cY <= 4
                and state["board"][cY][cX] != None 
                and state["board"][cY][cX]["color"] != state["playerColor"]):
                n += 1
                b = True
            availableMoves.append((n, b))
        
        return availableMoves