import numpy as np
from chess.chess_enums import PieceType, PieceColor, MoveCode

# Move piece to (x,y) square
def move_vec(piece_color, piece_type, piece_x, piece_y, x, y):
	return np.array([MoveCode.MOVE_CODE,piece_color, piece_type, piece_x, piece_y, x, y])

def move(piece, x, y):
	return move_vec(piece.color, piece.type, piece.x, piece.y, x, y)

# Capture target at (x,y) with piece
def capture_vec(piece_color, piece_type, piece_x, piece_y, x, y):
	return np.array([MoveCode.CAPTURE_CODE, piece_color, piece_type, piece_x, piece_y, x, y])

def capture(piece, x, y):
	return capture_vec(piece.color, piece.type, piece.x, piece.y, x, y)

# Castle given side
def castle(piece, x, y, rook, x2, y2):
	return castle_vec(piece.color, piece.type, piece.x, piece.y, x, y, rook.x, rook.y, x2, y2)

def castle_vec(piece_color, piece_type, piece_x, piece_y, x, y, rook_x, rook_y, x2, y2):
	return np.array([MoveCode.CASTLE_CODE, piece_color, piece_type, piece_x, piece_y, x, y, rook_x, rook_y, x2, y2])

# Promote piece to promotion_type at (x,y)
def promotion_vec(piece_color, piece_type, piece_x, piece_y, x, y, promotion_type):
	return np.array([MoveCode.PROMOTION_CODE,piece_color, piece_type,  piece_x, piece_y, x, y, promotion_type])

def promotion(piece, x, y, promotion_type):
	return promotion_vec(piece.color, piece.type, piece.x, piece.y, x, y, promotion_type)

# PromotionList at (x,y)
def promotion_list(piece, x, y):
	return [
		promotion(piece, x, y, PieceType.QUEEN), 
		promotion(piece, x, y, PieceType.ROOK), 
		promotion(piece, x, y, PieceType.BISHOP), 
		promotion(piece, x, y, PieceType.KNIGHT)
	]

# En passant piece at (x2,y2) by moving to (x,y)
def en_passant_vec(piece_color, piece_type, piece_x, piece_y, x, y, x2, y2):
	return np.array([MoveCode.EN_PASSANT_CODE, piece_color, piece_type, piece_x, piece_y, x, y, x2, y2])

def en_passant(piece, x, y, x2, y2):
	return en_passant_vec(piece.color, piece.type, piece.x, piece.y, x, y, x2, y2)









