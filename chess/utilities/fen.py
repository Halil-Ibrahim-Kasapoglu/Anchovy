import chess.chess_piece as chess_piece
from chess.chess_enums import PieceType, PieceColor, MoveCode

FEN_DEFAULT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def get_piece_from_fen_char(fen_char):
	piece_color = PieceColor.WHITE
	piece_type = PieceType.PAWN
	if fen_char.islower():
		piece_color = PieceColor.BLACK
	if fen_char.lower() == "p":
		piece_type = PieceType.PAWN
	elif fen_char.lower() == "n":
		piece_type = PieceType.KNIGHT
	elif fen_char.lower() == "b":
		piece_type = PieceType.BISHOP
	elif fen_char.lower() == "r":
		piece_type = PieceType.ROOK
	elif fen_char.lower() == "q":
		piece_type = PieceType.QUEEN
	elif fen_char.lower() == "k":
		piece_type = PieceType.KING
	else:
		raise Exception("Invalid fen character: " + fen_char)
	return chess_piece.ChessPiece(piece_color, piece_type, 0, 0)

def get_fen_char(piece):
	fen_char = "p"
	if piece.type == PieceType.KNIGHT:
		fen_char = "n"
	elif piece.type == PieceType.BISHOP:
		fen_char = "b"
	elif piece.type == PieceType.ROOK:
		fen_char = "r"
	elif piece.type == PieceType.QUEEN:
		fen_char = "q"
	elif piece.type == PieceType.KING:
		fen_char = "k"
	if piece.color == PieceColor.BLACK:
		fen_char = fen_char.upper()
	return fen_char

def get_fen_parts(fen):
	return fen.split(" ")

def convert_board_to_fen(chess_board):
	# PART 1
	board_fen = ""
	for y in range(chess_board.board_height):
		empty_tile_count = 0
		for x in range(chess_board.board_width):
			piece = chess_board.board[x][y]
			if piece is None:
				empty_tile_count += 1
			else:
				if empty_tile_count > 0:
					board_fen += str(empty_tile_count)
					empty_tile_count = 0
				board_fen += piece.get_fen()
		if empty_tile_count > 0:
			board_fen += str(empty_tile_count)
		if y < chess_board.board_height - 1:
			board_fen += "/"
	# PART 2
	turn_fen = "w" if chess_board.round % 2 == 0 else "b"
	# PART 3
	castling_fen = ""
	if chess_board.white_can_castle_kingside:
		castling_fen += "K"
	if chess_board.white_can_castle_queenside:
		castling_fen += "Q"
	if chess_board.black_can_castle_kingside:
		castling_fen += "k"
	if chess_board.black_can_castle_queenside:
		castling_fen += "q"
	# PART 4
	en_passant_target_fen = "-"
	if chess_board.en_passant_target is not None:
		en_passant_target_fen = chess_board.get_coordinate_string(chess_board.en_passant_target[0], chess_board.en_passant_target[1])
	# PART 5
	half_move_fen = str(chess_board.half_move_clock)
	# PART 6
	full_move_number_fen = str(chess_board.round // 2 + 1)



def load_fen_to_board(chess_board, fen):

	board_fen, turn_fen, castling_fen, en_passant_target_fen, half_move_fen, full_move_number_fen = get_fen_parts(fen)
	# PART 1
	board_rows = board_fen.split("/")
	chess_board.board = [[None for i in range(chess_board.board_width)] for j in range(chess_board.board_height)]
	position = (0, chess_board.board_height)
	for row in board_rows:
		position = (0, position[1] - 1)
		for char in row:
			if char.isdigit():
				position = (position[0] + int(char), position[1])
			else:
				piece = get_piece_from_fen_char(char)
				piece.x = position[0]
				piece.y = position[1]
				chess_board.board[piece.x][piece.y] = piece
				position = (position[0] + 1, position[1])

	# PART 2
	chess_board.round = 0 if turn_fen == "w" else 1
	# PART 3
	chess_board.white_can_castle_kingside = "K" in castling_fen
	chess_board.white_can_castle_queenside = "Q" in castling_fen
	chess_board.black_can_castle_kingside = "k" in castling_fen
	chess_board.black_can_castle_queenside = "q" in castling_fen
	# PART 4
	if en_passant_target_fen != "-":
		chess_board.en_passant_target = (ord(en_passant_target_fen[0]) - 97, int(en_passant_target_fen[1]) - 1)
	else:
		chess_board.en_passant_target = None
	# PART 5
	chess_board.half_move_clock = int(half_move_fen)
	# PART 6
	chess_board.round += (int(full_move_number_fen) - 1) * 2

	
