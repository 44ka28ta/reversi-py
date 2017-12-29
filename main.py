import numpy as np

MAX_INDEX = 8

WHITE_DISK = -1
BLACK_DISK = 1
EMPTY_STATE = 0

def flip_disks(board, start, end):

	src = start
	dst = end

	first_diff = src[0] - dst[0]
	second_diff = src[1] - dst[1]
	
	if (first_diff == 0):

		if src[1] > dst[1]:
			src, dst = dst, src

		for i in range(src[1] + 1, dst[1]):
			board[src[0], i] *= -1

	elif (second_diff == 0):

		if src[0] > dst[0]:
			src, dst = dst, src

		for j in range(src[0] + 1, dst[0]):
			board[j, src[1]] *= -1

	elif (abs(first_diff) - abs(second_diff)) == 0:

		if first_diff < 0:
			f_sign = 1
		else:
			f_sign = -1

		if second_diff < 0:
			s_sign = 1
		else:
			s_sign = -1
			
		for k in range(1, abs(first_diff)):
			board[src[0] + f_sign * k, src[1] + s_sign * k] *= -1
	
	return

def is_included_in_board(pivot):
	return (pivot[0] >= 0 and pivot[0] < MAX_INDEX) and (pivot[1] >= 0 and pivot[1] < MAX_INDEX)

def check_flipability(board, pivot, direction):

	j, i = pivot

	for k in range(0, MAX_INDEX):
		j += direction[0]
		i += direction[1]

		if is_included_in_board((j, i)):
			if board[j, i] == EMPTY_STATE:
				return []
			elif board[j, i] == - board[pivot[0], pivot[1]]:
				return [(j, i)]
		else:
			break
				
	
	return []

def check_one_grid(board, pivot, position, grids, disk_dict):

	j = pivot[0] + position[0]
	i = pivot[1] + position[1]

	if board[j, i] == EMPTY_STATE:
		flipables = check_flipability(board, pivot, (-position[0], -position[1]))

		if flipables:
			terminal_grid = (j, i)
			grids.append(terminal_grid)
			if terminal_grid in disk_dict:
				disk_dict[terminal_grid] += flipables
			else:
				disk_dict[terminal_grid] = flipables

	return

def get_effective_grids_on_moore(board, pivot, disk_dict):

	grids = []

	if is_included_in_board(pivot):
	
		if pivot[0] > 0:

			if pivot[1] > 0:
				check_one_grid(board, pivot, (-1, -1), grids, disk_dict)

			check_one_grid(board, pivot, (-1, 0), grids, disk_dict)

			if pivot[1] < MAX_INDEX - 1:
				check_one_grid(board, pivot, (-1, 1), grids, disk_dict)


		if pivot[1] < MAX_INDEX - 1:
			check_one_grid(board, pivot, (0, 1), grids, disk_dict)

			if pivot[0] < MAX_INDEX - 1:
				check_one_grid(board, pivot, (1, 1), grids, disk_dict)

		if pivot[1] > 0:
			check_one_grid(board, pivot, (0, -1), grids, disk_dict)

			if pivot[0] < MAX_INDEX - 1:
				check_one_grid(board, pivot, (1, -1), grids, disk_dict)


		if pivot[0] < MAX_INDEX - 1:
			check_one_grid(board, pivot, (1, 0), grids, disk_dict)

	return grids

def get_available_grids(board, turned_state, disk_dict):

	grids = []

	for j in range(0, MAX_INDEX):
		for i in range(0, MAX_INDEX):

			if board[j, i] == - turned_state:
				grids += get_effective_grids_on_moore(board, (j, i), disk_dict)

	return grids

def calc_score(board):

	black_score = 0
	white_score = 0

	for j in range(0, MAX_INDEX):
		for i in range(0, MAX_INDEX):

			if board[j, i] == BLACK_DISK:
				black_score += 1

			elif board[j, i] == WHITE_DISK:
				white_score += 1

	return black_score, white_score

def play_game(board):

	# first player
	player = BLACK_DISK

	pair_dict = {}

	next_grids = get_available_grids(board, player, pair_dict)

	while next_grids:

		print(":", next_grids)
		print("Score:", calc_score(board))
		print(board)

		input_grid = tuple(map(int, input().split(',')))

		while input_grid not in next_grids:
			input_grid = tuple(map(int, input().split(',')))

		board[input_grid[0], input_grid[1]] = player

		for pair in pair_dict[input_grid]:
			flip_disks(board, input_grid, pair)

		pair_dict = {}

		player *= -1
		next_grids = get_available_grids(board, player, pair_dict)
		

	return calc_score(board)

def create_init_board():

	board = np.zeros((MAX_INDEX, MAX_INDEX), dtype=int)

	board[3,3] = WHITE_DISK
	board[4,4] = WHITE_DISK

	board[3,4] = BLACK_DISK
	board[4,3] = BLACK_DISK

	return board

def main():

	board = create_init_board()

	b, w = play_game(board)

	if b > w:
		print("BLACK win! (", b, ",", w, ")")
	elif b == w:
		print("Draw.")
	else:
		print("WHITE win! (", b, ",", w, ")")

	return


if __name__ == '__main__':
	main()
