from chess.chess_moves import move, capture, castle, promotion, en_passant, promotion_list
from chess.chess_enums import PieceType, PieceColor, MoveCode
import chess.utilities.fen as fen

class ChessPiece:

	def __init__(self, piece_color : PieceColor, piece_type : PieceType, x : int, y : int):
		self.color = piece_color
		self.type = piece_type
		self.x = x
		self.y = y

	def color_char(self):
		if self.color == PieceColor.WHITE:
			return "w"
		else:
			return "d"

	def fen_char(self):
		return fen.get_fen_char(self)

	def get_color(self):
		return self.color
	def get_type(self):
		return self.type

	def get_ascii(self):
		ascii_char = 0x265F
		if self.type == PieceType.KNIGHT:
			ascii_char = 0x265E
		elif self.type == PieceType.BISHOP:
			ascii_char = 0x265D
		elif self.type == PieceType.ROOK:
			ascii_char = 0x265C
		elif self.type == PieceType.QUEEN:
			ascii_char = 0x265B
		elif self.type == PieceType.KING:
			ascii_char = 0x265A
		
		if self.color == PieceColor.BLACK:
			ascii_char -= 6
		return chr(ascii_char)

	def get_legal_moves(self, board):
		# returns a list of legal moves for this piece on the given board
		if self.type == PieceType.PAWN:
			return self.get_legal_moves_pawn(board)
		
		elif self.type == PieceType.KNIGHT:
			return self.get_legal_moves_knight(board)

		elif self.type == PieceType.BISHOP:
			return self.get_legal_moves_bishop(board)
		elif self.type == PieceType.ROOK:
			return self.get_legal_moves_rook(board)
		elif self.type == PieceType.QUEEN:
			return self.get_legal_moves_queen(board)
		elif self.type == PieceType.KING:
			return self.get_legal_moves_king(board)
		else:
			raise Exception("Invalid piece type")


	# =================================
	# LEGAL KING MOVES
	# =================================
	def get_legal_moves_king(self, game_state):
		# returns a list of legal moves for a king on the given board
		legal_moves = []

		# check 8 directions

		unit_vectors = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

		for vec in unit_vectors:
			if self.x + vec[0] >= 0 and self.x + vec[0] <= 7 and self.y + vec[1] >= 0 and self.y + vec[1] <= 7:
				if game_state.get_piece(self.x + vec[0], self.y + vec[1]) == None:
					legal_moves.append(move(self, self.x + vec[0], self.y + vec[1]))
				elif game_state.get_piece(self.x + vec[0], self.y + vec[1]).color != self.color:
					legal_moves.append(capture(self, self.x + vec[0], self.y + vec[1]))
		
		if self.color == PieceColor.WHITE:
			if game_state.white_can_castle_kingside:
				if game_state.get_piece(5, 0) == None and game_state.get_piece(6, 0) == None:
					legal_moves.append(castle(self, 6, 0, game_state.get_piece(7, 0), 5, 0))
			if game_state.white_can_castle_queenside:
				if game_state.get_piece(3, 0) == None and game_state.get_piece(2, 0) == None and game_state.get_piece(1, 0) == None:
					legal_moves.append(castle(self, 2, 0, game_state.get_piece(0, 0), 3, 0))
		else:
			if game_state.black_can_castle_kingside:
				if game_state.get_piece(5, 7) == None and game_state.get_piece(6, 7) == None:
					legal_moves.append(castle(self, 6, 7, game_state.get_piece(7, 7), 5, 7))
			if game_state.black_can_castle_queenside:
				if game_state.get_piece(3, 7) == None and game_state.get_piece(2, 7) == None and game_state.get_piece(1, 7) == None:
					legal_moves.append(castle(self, 2, 7, game_state.get_piece(0, 7), 3, 7))

		return legal_moves

	# =================================
	# LEGAL QUEEN MOVES
	# =================================
	def get_legal_moves_queen(self, game_state):
		# returns a list of legal moves for a queen on the given board
		legal_moves = []

		# check 8 directions

		unit_vectors = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

		for vec in unit_vectors:
			for i in range(1, 8):
				if self.x + vec[0] * i >= 0 and self.x + vec[0] * i <= 7 and self.y + vec[1] * i >= 0 and self.y + vec[1] * i <= 7:
					if game_state.get_piece(self.x + vec[0] * i, self.y + vec[1] * i) == None:
						legal_moves.append(move(self, self.x + vec[0] * i, self.y + vec[1] * i))
					elif game_state.get_piece(self.x + vec[0] * i, self.y + vec[1] * i).color != self.color:
						legal_moves.append(capture(self, self.x + vec[0] * i, self.y + vec[1] * i))
						break
					else:
						break			
		
		return legal_moves

	# =================================
	# LEGAL ROOK MOVES
	# =================================
	def get_legal_moves_rook(self, board):
		# returns a list of legal moves for a rook on the given board
		legal_moves = []

		# check 4 directions

		unit_vectors = [[1, 0], [0, 1], [-1, 0], [0, -1]]

		for vec in unit_vectors:
			for i in range(1, 8):
				if self.x + vec[0] * i >= 0 and self.x + vec[0] * i <= 7 and self.y + vec[1] * i >= 0 and self.y + vec[1] * i <= 7:
					if board.get_piece(self.x + vec[0] * i, self.y + vec[1] * i) == None:
						legal_moves.append(move(self, self.x + vec[0] * i, self.y + vec[1] * i))
					elif board.get_piece(self.x + vec[0] * i, self.y + vec[1] * i).color != self.color:
						legal_moves.append(capture(self, self.x + vec[0] * i, self.y + vec[1] * i))
						break
					else:
						break			
		
		return legal_moves


	# =================================
	# LEGAL BISHOP MOVES
	# =================================
	
	def get_legal_moves_bishop(self, board):
		# returns a list of legal moves for a bishop on the given board
		legal_moves = []

		# check 4 diagonals

		unit_diagonals = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

		for vec in unit_diagonals:
			for i in range(1, 8):
				if self.x + vec[0] * i >= 0 and self.x + vec[0] * i <= 7 and self.y + vec[1] * i >= 0 and self.y + vec[1] * i <= 7:
					if board.get_piece(self.x + vec[0] * i, self.y + vec[1] * i) == None:
						legal_moves.append(move(self, self.x + vec[0] * i, self.y + vec[1] * i))
					elif board.get_piece(self.x + vec[0] * i, self.y + vec[1] * i).color != self.color:
						legal_moves.append(capture(self, self.x + vec[0] * i, self.y + vec[1] * i))
						break
					else:
						break			
		
		return legal_moves

	# =================================
	# LEGAL KNIGHT MOVES
	# =================================

	def get_legal_moves_knight(self, board):
		# returns a list of legal moves for a knight on the given board
		legal_moves = []
		for i in range(-2, 3):
			for j in range(-2, 3):
				if abs(i) + abs(j) == 3:
					if self.x + i >= 0 and self.x + i <= 7 and self.y + j >= 0 and self.y + j <= 7:
						if board.get_piece(self.x + i, self.y + j) == None:
							legal_moves.append(move(self, self.x + i, self.y + j))
						elif board.get_piece(self.x + i, self.y + j).color != self.color:
							legal_moves.append(capture(self, self.x + i, self.y + j))
		return legal_moves


	# =================================
	# LEGAL PAWN MOVES
	# =================================
	
	def get_legal_moves_pawn(self, board):
		if self.color == PieceColor.WHITE:
			return self.get_legal_moves_pawn_white(board)
		else:
			return self.get_legal_moves_pawn_black(board)

	def get_legal_moves_pawn_white(self, board):
		# returns a list of legal moves for a white pawn on the given board
		legal_moves = []
		
		# check promotion
		if self.y == 6:
			if board.get_piece(self.x, self.y + 1) == None:
				legal_moves += promotion_list(self, self.x, self.y + 1)
			if board.get_piece(self.x - 1, self.y + 1) != None and board.get_piece(self.x - 1, self.y + 1).color == PieceColor.BLACK:
				legal_moves += promotion_list(self, self.x - 1, self.y + 1)
			if board.get_piece(self.x + 1, self.y + 1) != None and board.get_piece(self.x + 1, self.y + 1).color == PieceColor.BLACK:
				legal_moves += promotion_list(self, self.x + 1, self.y + 1)
			
			return legal_moves

		# check if pawn can move forward one
		if self.y < 7 and board.get_piece(self.x, self.y + 1) == None:
			legal_moves.append(move(self, self.x, self.y + 1))
			# check if pawn can move forward two
			if self.y == 1 and board.get_piece(self.x, self.y + 2) == None and board.get_piece(self.x, self.y + 1) == None:
				legal_moves.append(move(self, self.x, self.y + 2))
		# check if pawn can capture diagonally
		if self.y < 7:
			if self.x > 0 and board.get_piece(self.x - 1, self.y + 1) != None and board.get_piece(self.x - 1, self.y + 1).color == PieceColor.BLACK:
				legal_moves.append(capture(self, self.x - 1, self.y + 1))
			if self.x < 7 and board.get_piece(self.x + 1, self.y + 1) != None and board.get_piece(self.x + 1, self.y + 1).color == PieceColor.BLACK:
				legal_moves.append(capture(self, self.x + 1, self.y + 1))

		# En passant
		en_passant_target = board.get_en_passant_target()
		if en_passant_target is not None and self.y == 4:
			if en_passant_target[0] == self.x - 1:
				legal_moves.append(en_passant(self, self.x - 1, self.y + 1, en_passant_target[0], en_passant_target[1]))
			elif en_passant_target[0] == self.x + 1:
				legal_moves.append(en_passant(self, self.x + 1, self.y + 1, en_passant_target[0], en_passant_target[1]))

		# last_move = board.get_last_move()
		# if last_move is not None and last_move[0] == MoveCode.MOVE_CODE and self.y == 4:
		# 	last_moved_color, last_moved_type, last_moved_from_x, last_moved_from_y, last_moved_to_x, last_moved_to_y = last_move[1:7]
		# 	if last_moved_type == PieceType.PAWN and last_moved_color == PieceColor.BLACK and last_moved_to_y == 4 and last_moved_from_y == 6:
		# 		if last_moved_to_x == self.x - 1:
		# 			legal_moves.append(en_passant(self, self.x - 1, self.y + 1, last_moved_to_x, last_moved_to_y))
		# 		elif last_moved_to_x == self.x + 1:
		# 			legal_moves.append(en_passant(self, self.x + 1, self.y + 1, last_moved_to_x, last_moved_to_y))

		return legal_moves

	def get_legal_moves_pawn_black(self, board):
		# returns a list of legal moves for a black pawn on the given board
		legal_moves = []

		# check promotion
		if self.y == 1:
			if board.get_piece(self.x, self.y - 1) == None:
				legal_moves += promotion_list(self, self.x, self.y - 1)
			if board.get_piece(self.x + 1, self.y - 1) != None and board.get_piece(self.x + 1, self.y - 1).color == PieceColor.WHITE:
				legal_moves += promotion_list(self, self.x + 1, self.y - 1)
			if board.get_piece(self.x - 1, self.y - 1) != None and board.get_piece(self.x - 1, self.y - 1).color == PieceColor.WHITE:
				legal_moves += promotion_list(self, self.x - 1, self.y - 1)
			return legal_moves

		# check if pawn can move forward one
		if self.y > 0 and board.get_piece(self.x, self.y - 1) == None:
			legal_moves.append(move(self, self.x, self.y - 1))
			# check if pawn can move forward two
			if self.y == 6 and board.get_piece(self.x, self.y - 2) == None and board.get_piece(self.x, self.y - 1) == None:
				legal_moves.append(move(self, self.x, self.y - 2))
		# check if pawn can capture diagonally
		if self.y > 0:
			if self.x > 0 and board.get_piece(self.x - 1, self.y - 1) != None and board.get_piece(self.x - 1, self.y - 1).color == PieceColor.WHITE:
				legal_moves.append(capture(self, self.x - 1, self.y - 1))
			if self.x < 7 and board.get_piece(self.x + 1, self.y - 1) != None and board.get_piece(self.x + 1, self.y - 1).color == PieceColor.WHITE:
				legal_moves.append(capture(self, self.x + 1, self.y - 1))

		# En passant
		en_passant_target = board.get_en_passant_target()
		if en_passant_target is not None and self.y == 3:
			if en_passant_target[0] == self.x - 1:
				legal_moves.append(en_passant(self, self.x - 1, self.y - 1, en_passant_target[0], en_passant_target[1]))
			elif en_passant_target[0] == self.x + 1:
				legal_moves.append(en_passant(self, self.x + 1, self.y - 1, en_passant_target[0], en_passant_target[1]))


		# last_move = board.get_last_move()
		# if last_move is not None and last_move[0] == MoveCode.MOVE_CODE and self.y == 3:
		# 	last_moved_color, last_moved_type, last_moved_from_x, last_moved_from_y, last_moved_to_x, last_moved_to_y = last_move[1:7]
		# 	if last_moved_type == PieceType.PAWN and last_moved_color == PieceColor.WHITE and last_moved_to_y == 3 and last_moved_from_y == 1:
		# 		if last_moved_to_x == self.x - 1:
		# 			legal_moves.append(en_passant(self, self.x - 1, self.y - 1, last_moved_to_x, last_moved_to_y))
		# 		elif last_moved_to_x == self.x + 1:
		# 			legal_moves.append(en_passant(self, self.x + 1, self.y - 1, last_moved_to_x, last_moved_to_y))

		return legal_moves




