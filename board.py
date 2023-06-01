class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.last_move = None

    def get_status(self):
        for i in range(3):
            # Перевірка рядків
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            
            # Перевірка стовпців
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        
        # Перевірка діагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        # Перевірка на нічию
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'draw'
        
        return 'continue'

    def make_move(self, position, turn):
        if position[0] < 0 or position[0] > 2 or position[1] < 0 or position[1] > 2:
            raise IndexError("Invalid move. Position is out of range.")

        if self.board[position[0]][position[1]] != ' ':
            raise IndexError("Invalid move. Position is already occupied.")

        self.board[position[0]][position[1]] = turn
        self.last_move = (turn, position)


    def make_computer_move(self):
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    available_moves.append((i, j))

        # Знайдемо найкращий хід для комп'ютера
        best_score = float('-inf')
        best_move = None
        for move in available_moves:
            self.board[move[0]][move[1]] = '0'
            score = self.minimax(self.board, False)
            self.board[move[0]][move[1]] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        self.make_move(best_move, '0')
        return best_move

    def minimax(self, board, is_maximizing):
        status = self.get_status()
        if status == 'x':
            return -1
        elif status == '0':
            return 1
        elif status == 'draw':
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = '0'
                        score = self.minimax(board, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'x'
                        score = self.minimax(board, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def __str__(self):
        rows = []
        for row in self.board:
            row_str = "[" + ", ".join([f"'{cell}'" for cell in row]) + "]"
            rows.append(row_str)
        return "\n".join(rows)


