from board import Board

def play_game():
    board = Board()
    turn = 'x'
    while True:
        print(board)
        if turn == 'x':
            position = input("Enter your move (row column): ")
            try:
                position = tuple(map(int, position.split()))
                board.make_move(position, turn)
                status = board.get_status()
                if status == 'x':
                    print("Congratulations! You win!")
                    break
                elif status == 'draw':
                    print("It's a draw!")
                    break
                turn = '0'
            except ValueError:
                print("Invalid input. Please enter row and column as integers.")
            except IndexError as e:
                print(str(e))
        else:
            print("Computer is making its move...")
            position = board.make_computer_move()
            print("Computer placed its move at position:", position)
            status = board.get_status()
            if status == '0':
                print("Sorry! Computer wins!")
                break
            elif status == 'draw':
                print("It's a draw!")
                break
            turn = 'x'

if __name__ == "__main__":
    play_game()
    
