__author__ = 'RodXander'

MAX = 1
MIN = -1

NORTH = 'n'
SOUTH = 's'
WEST = 'w'
EAST ='e'

ENDING = 2048
NEW_NUMBER = 2

actions = [NORTH, EAST, SOUTH, WEST]
actions_number = len(actions)

SCORE_WEIGHT = 0.5
STABILITY_WEIGHT = 0.2
POSITION_WEIGHT = 0.3
BONUS_ENDGAME = 10000

from decimal import Decimal
class Node:
    def __init__(self, owner, parent, board, max_score, min_score, cause_action = None, points_gained = 0, board_full = None, is_finished = False, current_depth = 0):
        self.owner = owner
        self.board = board
        self.parent = parent
        self.children = []
        self.cause_action = cause_action
        self.board_full = board_full if not board_full is None else self.check_fullness()
        self.is_finished = is_finished
        self.points_gained = points_gained
        self.minimax_value = Decimal('Infinity') if owner == MIN else Decimal('-Infinity')
        self.max_score = max_score
        self.min_score = min_score
        self.dif_score = max_score - min_score

        self.stability = 0 if parent is None else (parent.stability + \
                         0 if Decimal.is_signed(Decimal(self.dif_score)) != Decimal.is_signed(Decimal(parent.dif_score)) else current_depth)

    def check_fullness(self):
        for r in range(board_dimension):
            for c in range(board_dimension):
                if self.board[r][c] == 0:
                    return False
        return True

    def available_actions(self):
        if not self.board_full:
            return actions

        available_actions = []
        breaking = False
        for r in range(board_dimension):
            for c in range(board_dimension):
                if c > 0 and self.board[r][c] == self.board[r][c - 1]:
                    available_actions.extend([EAST, WEST])
                    breaking = True
                    break
            if breaking:
                break

        breaking = False
        for c in range(board_dimension):
            for r in range(board_dimension):
                if r > 0 and self.board[r][c] == self.board[r - 1][c]:
                    available_actions.extend([NORTH, SOUTH])
                    breaking = True
                    break
            if breaking:
                break

        return available_actions

    def evaluate(self, leaf = False):
        if leaf:
            return (self.max_score - self.min_score) * BONUS_ENDGAME

        position = self.position()
        sign = (-1 if Decimal.is_signed(Decimal(self.dif_score)) else 1) if self.max_score != self.min_score else (-1 if Decimal.is_signed(Decimal(position)) else 1)

        return SCORE_WEIGHT * self.dif_score + POSITION_WEIGHT * position + STABILITY_WEIGHT * sign * self.stability

    def position(self):
        previous_value = -1
        points_horizontal = 0
        for r in range(board_dimension):
            for c in range(board_dimension):
                if self.board[r][c] == 0:
                    continue
                if self.board[r][c] == previous_value:
                    points_horizontal += 2 * self.board[r][c]
                    previous_value = -1
                else:
                    previous_value = self.board[r][c]

        previous_value = -1
        points_vertical = 0
        for c in range(board_dimension):
            for r in range(board_dimension):
                if self.board[r][c] == 0:
                    continue
                if self.board[r][c] == previous_value:
                    points_vertical += 2 * self.board[r][c]
                    previous_value = -1
                else:
                    previous_value = self.board[r][c]

        return max(points_horizontal, points_vertical) if self.owner == MAX else -max(points_horizontal, points_vertical)

def dfs_limited(node, current_depth, max_depth, alpha, beta):
    possible_actions = node.available_actions() if node == root else actions

    if not possible_actions:
        node.minimax_value = node.evaluate(leaf = True)
        return
    if node.is_finished:
        node.minimax_value = node.evaluate(leaf = True)
        return
    if current_depth == max_depth:
        node.minimax_value = node.evaluate()
        return

    children = []
    for i in possible_actions:
        # Defino que hijo analizar primero teniendo en cuenta aquel con la mayor ganancia para mi
        # No obstante, si esta es una segunda iteracion del algoritmo con una profundidad mayor, entonces utilizo los valores minimax previamente calculados.
        children.append(get_child(node, i, current_depth))

    if not node.children:
        node.children = children


    if all(child.minimax_value == Decimal('Infinity') or child.minimax_value == Decimal('-Infinity') for child in children):
        list.sort(children, key = lambda n: n.points_gained, reverse = True)
    else:
        list.sort(children, key = lambda n: n.minimax_value, reverse = True)

    for i in range(len(possible_actions)):
        dfs_limited(children[i], current_depth + 1, max_depth, alpha, beta)

        if node.owner == MAX:
            node.minimax_value = max(node.minimax_value, children[i].minimax_value)
            if node.minimax_value > beta:
                return
            alpha = max(alpha, node.minimax_value)
        else:
            node.minimax_value = min(node.minimax_value, children[i].minimax_value)
            if node.minimax_value < alpha:
                return
            beta = min(beta, node.minimax_value)

def get_child(parent, action, current_depth):
    if parent.children:
        for child in parent.children:
            if child.cause_action == action:
                return child
    else:
        new_board, points_earned, board_full, is_finished = move(parent.board, action)
        if parent.owner == MAX:
            return Node(MIN, parent, new_board, parent.max_score + points_earned, parent.min_score, action, points_earned, board_full, is_finished, current_depth + 1)
        else:
            return Node(MAX, parent, new_board, parent.max_score, parent.min_score + points_earned, action, points_earned, board_full, is_finished, current_depth + 1)

def move(old_board, action):
    new_board = []
    for i in range(board_dimension):
        new_board.append([0] * board_dimension)

    points_earned = 0
    is_full = True
    is_finished = False
    new_number_located = False

    # Este simulador de movimientos funciona creando un nuevo tablero donde pondrá los resultados de aplicarle
    # el movimiento especificado al tablero actual.
    # Para esto recorre el tablero en la direccion opuesta al movimiento. E.g. si es SOUTH va de abajo hacia arriba
    # en cada una de las columnas, mientras obvia los ceros del tablero actual y determina si sumar o no los numeros
    #
    # En adicion, al final establece la posicion del nuevo numero, para esto se apoya en que el nuevo numero aparece
    # en la fila o columna contraria a la del movimiento siguiendo las manceillas del reloj y luego baja.
    # E.g. si la direccion del movimiento es SOUTH, entonces el numero intentaria aparecer en la primera columna en
    # la fila mas superior; asi que aprovechando que mi modo de obtener el nuevo tablero para este movimiento termina
    # en la fila superior, solo tengo que arreglar el orden de como se procesan las columnas para analizarlas de primera
    # a ultima. Observese que si esta columna esta llena, entonces el numero intentara aparecer en la parte superior
    # de la proxima. Tambien entiendase que si no puede ponerse en la fila superior, entonces no puede ubicarse en mas
    # ningun lado, pues esto significaria que todas las demas casillas estan ocupadas, recuerdese que todo esto es bajo
    # la asuncion de un movimiento SOUTH. Un poco tricky!!! Verdad?
    #
    # Ademas el algoritmo se encarga de decirme si el tablero se encuentra lleno, en cuyo caso es cuando se presentan
    # las siruaciones donde es posible dar un movimiento que no modifique el tablero. Esta informacion la uso para
    # saber que en estos casos debo comprobar los tableros, sin tener que hacerlo en todos los nodos.
    #
    # Tambien determina si el juego ha terminado con este movimiento.

    if action == SOUTH:
        for column in range(board_dimension):
            new_row = board_dimension - 1
            for row in range(board_dimension - 1, -1, -1):

                if old_board[row][column] == 0:
                    continue
                elif new_board[new_row][column] == old_board[row][column]:
                    new_board[new_row][column] *= 2
                    points_earned += new_board[new_row][column]

                    if new_board[new_row][column] == ENDING:
                        is_finished = True

                    new_row -= 1
                else:
                    new_row = new_row if new_board[new_row][column] == 0 else new_row - 1
                    new_board[new_row][column] = old_board[row][column]

            if not new_number_located and new_board[0][column] == 0:
                new_board[0][column] = NEW_NUMBER
                new_number_located = True

        for column in range(board_dimension):
            if new_board[0][column] == 0:
                is_full = False
                break

    elif action == NORTH:
        for column in range(board_dimension - 1, -1, -1):
            new_row = 0
            for row in range(board_dimension):

                if old_board[row][column] == 0:
                    continue
                elif new_board[new_row][column] == old_board[row][column]:
                    new_board[new_row][column] *= 2
                    points_earned += new_board[new_row][column]

                    if new_board[new_row][column] == ENDING:
                        is_finished = True

                    new_row += 1
                else:
                    new_row = new_row if new_board[new_row][column] == 0 else new_row + 1
                    new_board[new_row][column] = old_board[row][column]

            if not new_number_located and new_board[board_dimension - 1][column] == 0:
                new_board[board_dimension - 1][column] = NEW_NUMBER
                new_number_located = True

        for column in range(board_dimension):
            if new_board[board_dimension - 1][column] == 0:
                is_full = False
                break

    elif action == EAST:
        for row in range(board_dimension - 1, -1, -1):
            new_column = board_dimension - 1
            for column in range(board_dimension - 1, -1, -1):

                if old_board[row][column] == 0:
                    continue
                elif new_board[row][new_column] == old_board[row][column]:
                    new_board[row][new_column] *= 2
                    points_earned += new_board[row][new_column]

                    if new_board[row][new_column] == ENDING:
                        is_finished = True

                    new_column -= 1
                else:
                    new_column = new_column if new_board[row][new_column] == 0 else new_column - 1
                    new_board[row][new_column] = old_board[row][column]

            if not new_number_located and new_board[row][0] == 0:
                new_board[row][0] = NEW_NUMBER
                new_number_located = True

        for row in range(board_dimension):
            if new_board[row][0] == 0:
                is_full = False
                break

    else:
        for row in range(board_dimension):
            new_column = 0
            for column in range(board_dimension):

                if old_board[row][column] == 0:
                    continue
                elif new_board[row][new_column] == old_board[row][column]:
                    new_board[row][new_column] *= 2
                    points_earned += new_board[row][new_column]

                    if new_board[row][new_column] == ENDING:
                        is_finished = True

                    new_column += 1
                else:
                    new_column = new_column if new_board[row][new_column] == 0 else new_column + 1
                    new_board[row][new_column] = old_board[row][column]

            if not new_number_located and new_board[row][board_dimension - 1] == 0:
                new_board[row][board_dimension - 1] = NEW_NUMBER
                new_number_located = True

        for row in range(board_dimension):
            if new_board[row][board_dimension - 1] == 0:
                is_full = False
                break

    return new_board, points_earned, is_full, is_finished

from sys import argv
my_score = int(argv[3])
his_score = int(argv[4])
board = eval(argv[1])
board_dimension = len(board)
root = Node(MAX, None, board, my_score, his_score)   # Creo la raiz

max_depth = 7 if my_score - his_score > 0 else 8
dfs_limited(root, 0, max_depth, Decimal('-Infinity'), Decimal('Infinity'))

action = ''
max_minimax = Decimal('-Infinity')
for child in root.children:
    if child.minimax_value > max_minimax:
        max_minimax = child.minimax_value
        action = child.cause_action

print (action)
