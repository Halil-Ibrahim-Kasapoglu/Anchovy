from chess.chess_enums import PieceType, PieceColor, MoveCode
import chess.chess_moves
import chess.chess_piece
from chess.chess_piece import ChessPiece
import copy
import chess.utilities.fen as fen

class ChessBoard():

	def __init__(self):

		self.board_width = 8
		self.board_height = 8
		
		self.reset_board()

		self.initialize_board()

		
	def reset_board(self):

		self.round = 0
		self.half_move_clock = 0
		self.en_passant_target = None
		self.white_can_castle_kingside = True
		self.white_can_castle_queenside = True
		self.black_can_castle_kingside = True
		self.black_can_castle_queenside = True

		self.move_history = []
		self.previous_board_states = []
		self.removed_board_states = []
		self.removed_move_history = []

		fen.load_fen_to_board(self, "r2qkbnr/pP1bpppp/2n5/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5")

	def get_en_passant_target(self):
		return self.en_passant_target

	def initialize_board(self):
		fen.load_fen_to_board(self, fen.FEN_DEFAULT)

	def get_coordinate_string(self, x, y):
		return chr(x + 97) + str(y + 1)

	def get_turn_color(self):
		return PieceColor.WHITE if self.round % 2 == 0 else PieceColor.BLACK


	def get_piece(self, x, y):
		if x < 0 or x >= self.board_width or y < 0 or y >= self.board_height:
			return None
		return self.board[x][y]

	def get_legal_moves(self, color):
				
		legal_moves = []

		for i in range(self.board_width):
			for j in range(self.board_height):
				if self.board[i][j] == None:
					continue
				
				if self.board[i][j].color == color:
					moves = self.board[i][j].get_legal_moves(self)
					legal_moves += moves # self.board[i][j].get_legal_moves(self)

		return legal_moves

	def undo_last_move(self):
		if len(self.move_history) == 0:
			return

		last_move = self.move_history.pop()
		self.round -= 1
		
		self.removed_move_history.append(last_move)
		self.removed_board_states.append(copy.deepcopy(self.board))
		self.board = self.previous_board_states.pop()


	def retrieve_next_move(self):
		if len(self.removed_move_history) == 0:
			return

		retrived_move = self.removed_move_history.pop()
		self.round += 1

		self.move_history.append(retrived_move)
		self.previous_board_states.append(copy.deepcopy(self.board))
		self.board = self.removed_board_states.pop()
		

	def update_castle_rights(self):

		a1_rook = self.get_piece(0,0)
		h1_rook = self.get_piece(7,0)
		a8_rook = self.get_piece(0,7)
		h8_rook = self.get_piece(7,7)

		white_king = self.get_piece(4,0)
		black_king = self.get_piece(4,7)

		if a1_rook == None or a1_rook.type != PieceType.ROOK or a1_rook.color != PieceColor.WHITE:
			self.white_can_castle_queenside = False
		if h1_rook == None or h1_rook.type != PieceType.ROOK or h1_rook.color != PieceColor.WHITE:
			self.white_can_castle_kingside = False
		if a8_rook == None or a8_rook.type != PieceType.ROOK or a8_rook.color != PieceColor.BLACK:
			self.black_can_castle_queenside = False
		if h8_rook == None or h8_rook.type != PieceType.ROOK or h8_rook.color != PieceColor.BLACK:
			self.black_can_castle_kingside = False

		if white_king == None or white_king.type != PieceType.KING or white_king.color != PieceColor.WHITE:
			self.white_can_castle_kingside = False
			self.white_can_castle_queenside = False

		if black_king == None or black_king.type != PieceType.KING or black_king.color != PieceColor.BLACK:
			self.black_can_castle_kingside = False
			self.black_can_castle_queenside = False

	def make_move(self, move):

		# SAVE PREVIOUS BOARD STATE

		self.removed_move_history = []
		self.removed_board_states = []
		self.previous_board_states.append(copy.deepcopy(self.board))

		# UPDATE BOARD STATE

		# clear en passant target on new move
		self.en_passant_target = None

		move_code = move[0]

		if move_code == MoveCode.MOVE_CODE:
			# get piece
			piece_x,piece_y,target_x,target_y = move[3:7]
			piece = self.get_piece(piece_x, piece_y)
			target = self.get_piece(target_x, target_y)
			
			if target != None:
				raise Exception(f"Invalid action! Piece on {self.get_coordinate_string(piece_x,piece_y)} cannot move to {self.get_coordinate_string(target_x,target_y)}") 
			if piece == None:
				raise Exception(f"Invalid action! No piece on {self.get_coordinate_string(piece_x,piece_y)}")

			# If piece is a pawn and moves two spaces, set en passant target
			if piece.type == PieceType.PAWN and abs(target_y - piece_y) == 2:
				self.en_passant_target = (target_x, (target_y + piece_y) // 2)
				print("en passant target square ", self.en_passant_target)

			# Swap places on board
			self.board[piece_x][piece_y] = None
			piece.x = target_x
			piece.y = target_y
			self.board[target_x][target_y] = piece
			
			print(f"Move {self.get_coordinate_string(piece_x,piece_y)} to {self.get_coordinate_string(target_x,target_y)}")
			

		elif move_code == MoveCode.CAPTURE_CODE:

			piece_x,piece_y,target_x,target_y = move[3:7]
			piece = self.get_piece(piece_x, piece_y)
			target = self.get_piece(target_x, target_y)

			if target == None:
				raise Exception(f'Invalid action! Piece on {self.get_coordinate_string(piece_x,piece_y)} cannot capture {self.get_coordinate_string(target_x,target_y)}. Nothing there')
			if piece == None:
				raise Exception(f"Invalid action! No piece on {self.get_coordinate_string(piece_x,piece_y)}")

			self.board[piece_x][piece_y] = None
			piece.x = target_x
			piece.y = target_y
			self.board[target_x][target_y] = piece

			print(f"Capture {self.get_coordinate_string(piece_x,piece_y)} to {self.get_coordinate_string(target_x,target_y)}")
			
		elif move_code == MoveCode.PROMOTION_CODE:

			piece_x,piece_y,target_x,target_y,promotion_type = move[3:8]
			piece = self.get_piece(piece_x, piece_y)
			target = self.get_piece(target_x, target_y)

			if piece == None:
				raise Exception(f"Invalid action! No piece on {self.get_coordinate_string(piece_x,piece_y)}")

			self.board[piece_x][piece_y] = None

			promoted_piece = ChessPiece(piece.color, promotion_type, target_x, target_y)
			self.board[target_x][target_y] = promoted_piece

			print(f"Promote {self.get_coordinate_string(piece_x,piece_y)} to {self.get_coordinate_string(target_x,target_y)} to {promotion_type}")

		elif move_code == MoveCode.EN_PASSANT_CODE:

			piece_x,piece_y,target_x,target_y, capture_x, capture_y = move[3:9]
			piece = self.get_piece(piece_x, piece_y)
			move_target = self.get_piece(target_x, target_y)
			capture_target = self.get_piece(capture_x, capture_y)

			if piece == None:
				raise Exception(f"Invalid action! No piece on {self.get_coordinate_string(piece_x,piece_y)}")
			if move_target != None:
				raise Exception(f"Invalid action! Piece on {self.get_coordinate_string(piece_x,piece_y)} cannot move to {self.get_coordinate_string(target_x,target_y)}. Square is occupied")
			if capture_target == None:
				raise Exception(f"Invalid action! Piece on {self.get_coordinate_string(piece_x,piece_y)} cannot capture {self.get_coordinate_string(capture_x,capture_y)}. Nothing there")

			self.board[piece_x][piece_y] = None
			self.board[capture_x][capture_y] = None
			piece.x = target_x
			piece.y = target_y
			self.board[target_x][target_y] = piece

			print(f"En passant {self.get_coordinate_string(piece_x,piece_y)} to {self.get_coordinate_string(target_x,target_y)} and captured {self.get_coordinate_string(capture_x,capture_y)}")
		
		elif move_code == MoveCode.CASTLE_CODE:

			piece_x,piece_y,target_x,target_y,rook_x, rook_y, rook_target_x, rook_target_y = move[3:11]
			piece = self.get_piece(piece_x, piece_y)
			rook = self.get_piece(rook_x, rook_y)
			move_target = self.get_piece(target_x, target_y)
			rook_target = self.get_piece(rook_target_x, rook_target_y)

			if piece == None:
				raise Exception(f"Invalid action! No piece on {self.get_coordinate_string(piece_x,piece_y)}")
			if rook == None:
				raise Exception(f"Invalid action! No piece on {self.get_coordinate_string(rook_x,rook_y)}")
			if move_target != None:
				raise Exception(f"Invalid action! Piece on {self.get_coordinate_string(piece_x,piece_y)} cannot move to {self.get_coordinate_string(target_x,target_y)}. Square is occupied")
			if rook_target != None:
				raise Exception(f"Invalid action! Piece on {self.get_coordinate_string(rook_x,rook_y)} cannot move to {self.get_coordinate_string(rook_target_x,rook_target_y)}. Square is occupied")

			self.board[piece_x][piece_y] = None
			self.board[rook_x][rook_y] = None
			piece.x = target_x
			piece.y = target_y
			rook.x = rook_target_x
			rook.y = rook_target_y
			self.board[target_x][target_y] = piece
			self.board[rook_target_x][rook_target_y] = rook

			print(f"Castle {self.get_coordinate_string(piece_x,piece_y)} to {self.get_coordinate_string(target_x,target_y)} and {self.get_coordinate_string(rook_x,rook_y)} to {self.get_coordinate_string(rook_target_x,rook_target_y)}")

		# Update board stats
		self.update_castle_rights()
		self.round += 1
		self.move_history.append(move)


	def get_retrieve_move(self):
		if len(self.removed_move_history) == 0:
			return None
		return self.removed_move_history[-1]

	def get_last_move(self):
		if len(self.move_history) == 0:
			return None
		return self.move_history[-1]

	def display_board(self):

		# display coordinates too
		
		tile_horizontal_separator = "-"
		tile_vertical_separator = "|"
		tile_corner = "+"
		tile_display_width = 3
		tile_display_height = 1

		board_str_width = (self.board_width + 1) * (tile_display_width + 1)
		board_str_height = (self.board_height + 1) * (tile_display_height + 1)

		board_string = [[" " for i in range(board_str_width)] for j in range(board_str_height)]

		for i in range(board_str_height):
			for j in range(board_str_width):
				if (i - 1) / (tile_display_height + 1) < 8 and (j - 1) / (tile_display_width + 1) < 8:
					if i % (tile_display_height + 1) == 0:
						if j % (tile_display_width + 1) == 0:
							board_string[i][j] = tile_corner
						else:
							board_string[i][j] = tile_horizontal_separator
					else:
						if j % (tile_display_width + 1) == 0:
							board_string[i][j] = tile_vertical_separator
						else:
							board_string[i][j] = " "
				

		# Display coordinates numbers at the rightmost
		for i in range(self.board_height):
			board_string[i * (tile_display_height + 1) + 1][board_str_width - 2] = str(self.board_height - i)

		# Display coordinates letters at the bottom
		for i in range(self.board_width):
			board_string[board_str_height - 1][i * (tile_display_width + 1) + 2] = chr(ord('a') + i)

		# Display pieces
		for i in range(self.board_height):
			for j in range(self.board_width):
				if self.board[j][7-i] != None:
					board_string[i * (tile_display_height + 1) + 1][j * (tile_display_width + 1) + 2] = self.board[j][7-i].get_ascii()
					
		for i in range(board_str_height):
			for j in range(board_str_width):
				print(board_string[i][j], end="")
			print()

