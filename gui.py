import tkinter as tk
import numpy as np
from chess.chess_enums import MoveCode, PieceColor, PieceType

GUI_CONFIG_ENGINE_TITLE = "Anchovy v0.1" 
GUI_CONFIG_TILE_SIZE = 4
GUI_CONFIG_DARK_SQUARE_COLOR = "#cd8b62"
GUI_CONFIG_WHITE_SQUARE_COLOR = "#eed7a1"
GUI_CONFIG_HIGH_LIGHTED_DARK_SQUARE_COLOR = "#a52a2a"
GUI_CONFIG_HIGH_LIGHTED_WHITE_SQUARE_COLOR = "#ff6347"
GUI_CONFIG_AVAILABLE_SQUARE_COLOR = "#b9ce59"

# GUI_CONFIG_AVAILABLE_DARK_SQUARE_COLOR = "#008000"

GUI_CONFIG_BOARD_CANVAS_WIDTH = 640
GUI_CONFIG_BOARD_CANVAS_HEIGHT = 640

class GUI():

	def __init__(self, board):
		
		self.window = tk.Tk()
		self.window.title(GUI_CONFIG_ENGINE_TITLE)

		self.board = board

		self.board_canvas = tk.Canvas(self.window, width = GUI_CONFIG_BOARD_CANVAS_WIDTH, height = GUI_CONFIG_BOARD_CANVAS_HEIGHT)
		self.board_canvas.grid(row = 0, column = 0)

		
		self.tile_width = GUI_CONFIG_BOARD_CANVAS_WIDTH / (self.board.board_width + 1)
		self.tile_height = GUI_CONFIG_BOARD_CANVAS_HEIGHT / (self.board.board_height + 1)
		
		self.piece_images = []
		self.piece_views = []
		self.tile_views = []
		self.highlighted_tile_views = []
		
		self.available_moves = {}

		self.draw_board()
		self.render_board()

	def clear_highlighted_tiles(self):
		for tile_id in self.highlighted_tile_views:
			tile_original_color = GUI_CONFIG_WHITE_SQUARE_COLOR if (tile_id + tile_id // self.board.board_width) % 2 == 0 else GUI_CONFIG_DARK_SQUARE_COLOR
			self.board_canvas.itemconfig(self.tile_views[tile_id], fill=tile_original_color)	
		self.highlighted_tile_views = []
	
	def highlight_move(self, move):
		if move is not None:
			from_x, from_y = move[3], move[4]
			to_x, to_y = move[5], move[6]

			from_x,from_y = self.board.board_width-from_y-1,from_x
			to_x,to_y = self.board.board_width-to_y-1,to_x

			from_tile_id,to_tile_id = from_x + from_y * self.board.board_width, to_x + to_y * self.board.board_width
			from_tile, to_tile = self.tile_views[from_tile_id], self.tile_views[to_tile_id]
			
			self.clear_highlighted_tiles()
			
			to_highlighted_color = GUI_CONFIG_HIGH_LIGHTED_WHITE_SQUARE_COLOR if (to_tile_id + to_tile_id // self.board.board_width) % 2 == 0 else GUI_CONFIG_HIGH_LIGHTED_DARK_SQUARE_COLOR
			from_highlighted_color = GUI_CONFIG_HIGH_LIGHTED_WHITE_SQUARE_COLOR if (from_tile_id + from_tile_id // self.board.board_width) % 2 == 0 else GUI_CONFIG_HIGH_LIGHTED_DARK_SQUARE_COLOR

			self.board_canvas.itemconfig(from_tile, fill=from_highlighted_color)
			self.board_canvas.itemconfig(to_tile, fill=to_highlighted_color)
			self.highlighted_tile_views += [from_tile_id, to_tile_id]
		else:
			self.clear_highlighted_tiles()

	def on_key_press(self, event):
		
		if event.char == "r":
			legal_moves = self.board.get_legal_moves(self.board.get_turn_color())
			
			if len(legal_moves) == 0:
				raise Exception("No legal moves")
			random_move = legal_moves[np.random.randint(len(legal_moves))]

			self.board.make_move(random_move)
			self.highlight_move(self.board.get_last_move())
			self.render_board()

		if event.char == 'u':

			self.highlight_move(self.board.get_last_move())
			self.board.undo_last_move()
			self.render_board()

		if event.char == 'n':

			self.highlight_move(self.board.get_retrieve_move())
			self.board.retrieve_next_move()
			self.render_board()

		if event.char == 'd':
			self.board.reset_board()
			self.render_board()
			self.highlight_move(None)

		if event.char == 'q':
			self.window.destroy()

		if event.char == 'c':
			print("Number of legal moves:", len(self.board.get_legal_moves(self.board.get_turn_color())))


	def promote_move(self, move, promotion):
		move[7] = promotion
		self.board.make_move(move)
		self.promotion_window.destroy()

	def tile_on_click(self, tile_id):
		board_x, board_y = tile_id // self.board.board_width, self.board.board_height - tile_id % self.board.board_width - 1

		if len(self.available_moves.keys()) != 0 and tile_id in self.available_moves.keys():
			move = self.available_moves[tile_id]
			if move[0] == MoveCode.PROMOTION_CODE:
				# create 4 button for each promotion piece
				self.promotion_window = tk.Toplevel(self.window)
				self.promotion_window.title("Promote to")
				self.promotion_window.geometry("100x200")
				self.promotion_window.resizable(False, False)

				queen_button = tk.Button(self.promotion_window, height=2, text="Queen", command=lambda: self.promote_move(move, PieceType.QUEEN))
				queen_button.pack(fill=tk.X, expand=True)
				rook_button = tk.Button(self.promotion_window, height=2, text="Rook", command=lambda: self.promote_move(move, PieceType.ROOK))
				rook_button.pack(fill=tk.X, expand=True)
				bishop_button = tk.Button(self.promotion_window, height=2, text="Bishop", command=lambda: self.promote_move(move, PieceType.BISHOP))
				bishop_button.pack(fill=tk.X, expand=True)
				knight_button = tk.Button(self.promotion_window, height=2, text="Knight", command=lambda: self.promote_move(move, PieceType.KNIGHT))
				knight_button.pack(fill=tk.X, expand=True)

				#froze here until user click on a button
				self.window.wait_window(self.promotion_window)
				
			else:
				self.board.make_move(move)
			
			self.highlight_move(self.board.get_last_move())
			self.render_board()
			self.available_moves = {}

		else:
			piece = self.board.get_piece(board_x, board_y)
			if piece is not None and piece.color == self.board.get_turn_color():
				legal_moves = piece.get_legal_moves(self.board)
				for move in legal_moves:
					target_square = move[5], move[6]
					tile = self.board.board_width - target_square[1] - 1 + target_square[0] * self.board.board_width
					highlighted_color = GUI_CONFIG_AVAILABLE_SQUARE_COLOR
					self.board_canvas.itemconfig(self.tile_views[tile], fill=highlighted_color)
					self.highlighted_tile_views += [tile]
					
					self.available_moves[tile] = move

				# self.highlight_moves(s(piece))

			highlighted_color = GUI_CONFIG_HIGH_LIGHTED_WHITE_SQUARE_COLOR if (tile_id + tile_id // self.board.board_width) % 2 == 0 else GUI_CONFIG_HIGH_LIGHTED_DARK_SQUARE_COLOR
			self.board_canvas.itemconfig(self.tile_views[tile_id], fill=highlighted_color)
			self.highlighted_tile_views += [tile_id]


			self.render_board()

	def handle_tile_clicks(self, event):
		x,y = event.x, event.y
		
		tile_x, tile_y = int(x / self.tile_width), int(y / self.tile_height)
		# Convert to board coordinates

		if tile_x < 0 or tile_x >= self.board.board_width or tile_y < 0 or tile_y >= self.board.board_height:
			return

		tile_id = tile_y + tile_x * self.board.board_width
		self.tile_on_click(tile_id)
		
		# tile_x = int(x / self.tile_width)
		# tile_y = int(y / self.tile_height)

		# # Convert to board coordinates
		# tile_x, tile_y = tile_x, self.board.board_height - tile_y - 1



		

	def on_left_click(self, event):

		self.clear_highlighted_tiles()

		self.handle_tile_clicks(event)

	
	def on_right_click(self, event):

		self.clear_highlighted_tiles()

	def run(self):
		
		self.window.bind("<KeyPress>", self.on_key_press)
		self.board_canvas.bind('<Button-1>', self.on_left_click)
		# On right click
		self.board_canvas.bind('<Button-2>', self.on_right_click)
		self.window.mainloop()
		# Bind button R

	def render_board(self):

		# Clear the board
		for piece_view in self.piece_views:
			self.board_canvas.delete(piece_view)
		self.piece_views = []
		
		for i in range(self.board.board_width):
			for j in range(self.board.board_height):
				pos_x, pos_y = i, self.board.board_height - j - 1
				if self.board.get_piece(pos_x, pos_y) is not None:
					piece = self.board.get_piece(pos_x, pos_y)
					fen_char = piece.fen_char().lower()
					color_char = piece.color_char()
					piece_image_path = f"assets/sprites/chess_pieces/chess_piece_{fen_char}{color_char}.png"
					
					piece_image = tk.PhotoImage(file = piece_image_path)
					self.piece_images.append(piece_image)
					piece_view = self.board_canvas.create_image((i + 0.5) * self.tile_width, (j + 0.5) * self.tile_height, image = piece_image)
					self.piece_views.append(piece_view)


	def draw_board(self):

		for i in range(self.board.board_width + 1):
			for j in range(self.board.board_height + 1):

				tile_color = GUI_CONFIG_WHITE_SQUARE_COLOR if (i + j) % 2 == 0 else GUI_CONFIG_DARK_SQUARE_COLOR

				if i == self.board.board_width and j < self.board.board_height:
					coordinate_tile_horizontal = self.board_canvas.create_text((i + 0.5) * self.tile_width, (j + 0.5) * self.tile_height, text = str(self.board.board_width - j))
				elif j == self.board.board_height and i < self.board.board_width:
					coordinate_tile_vertical = self.board_canvas.create_text((i + 0.5) * self.tile_width, (j + 0.5) * self.tile_height, text = str(chr(ord('a') + i)))
				elif i < self.board.board_width and j < self.board.board_height:
					tile_view = self.board_canvas.create_rectangle(i * self.tile_width, j * self.tile_height, (i + 1) * self.tile_width, (j + 1) * self.tile_height, fill = tile_color)

					self.tile_views.append(tile_view)
					



