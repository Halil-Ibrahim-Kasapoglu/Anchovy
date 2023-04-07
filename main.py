import gym
import numpy as np
import argparse
import chess.chess_board as chess_board
from chess.chess_enums import PieceColor, PieceType, MoveCode
import gui

def run_cli():

	board = chess_board.ChessBoard()
	board.display_board()
	simulate = False
	while True:
		if not simulate:
			command = input("").lower()
		if command == "s":
			simulate = True
		if command == "r" or simulate:
			legal_moves = board.get_legal_moves(board.get_turn_color())
			# print(legal_moves)
			# if len(legal_moves) == 0:
				# raise Exception("No legal moves")
			random_move = legal_moves[np.random.randint(len(legal_moves))]
			# print("Move Played : ", random_move)

			
			# last_move = board.get_last_move()
			# if last_move is not None:
			# 	last_move_code, last_moved_color, last_moved_type, last_moved_from_x, last_moved_from_y, last_moved_to_x, last_moved_to_y = last_move[0:7]
			# 	print(f"Last move {last_move_code} {board.get_coordinate_string(last_moved_from_x, last_moved_from_y)} {board.get_coordinate_string(last_moved_to_x, last_moved_to_y)}")

			board.make_move(random_move)
			board.display_board()
		
def run_gui():

	board = chess_board.ChessBoard()	
	chess_gui = gui.GUI(board)
	chess_gui.run()


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument("-v", "--visualize", action="store")
	args = parser.parse_args()

	if args.visualize == "gui":
		run_gui()
	elif args.visualize == "cli":
		run_cli()
	else:
		run_gui()

