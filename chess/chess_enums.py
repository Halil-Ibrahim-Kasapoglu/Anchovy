from enum import Enum

class PieceColor(Enum):
	WHITE = 0
	BLACK = 1

class PieceType(Enum):
	PAWN = 0
	KNIGHT = 1
	BISHOP = 2
	ROOK = 3
	QUEEN = 4
	KING = 5

class MoveCode(Enum):
	MOVE_CODE = 0
	CAPTURE_CODE = 1
	CASTLE_CODE = 2
	PROMOTION_CODE = 3
	EN_PASSANT_CODE = 4
