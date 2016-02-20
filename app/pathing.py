# Creates a 2D list of the given side initialized with value in each slot
def make_grid(width, height, value):
	return [[value for x in range(width)] for x in range(height)]
	
def next_point(Q, dist):
	min_dist = None
	min_point = None
	for point in Q:
		distance_for_point = dist[point[0]][point[1]]
		
		if distance_for_point is None:
				continue
		
		# in the none case anything is lower than us
		if min_dist is None:
			min_dist = distance_for_point
			min_point = point
			continue
		
		if distance_for_point < min_dist:
			min_dist = distance_for_point
			min_point = point
	
	return min_point
	
def analyze_point( original, point, grid, dist, prev ):
	terrain_at_point = grid[point[0]][ point[1]]
	terrain_at_original = grid[original[0] ][ original[1]]
	
	if terrain_at_original is None:
		return
	if terrain_at_point is None:
		return
		
	best_distance_to_original = dist[original[0]][original[1]]
	best_distance_to_point = dist[point[0]][point[1]]
	
	alternate_distance = best_distance_to_original + terrain_at_point + terrain_at_original
	if best_distance_to_point is None or alternate_distance < best_distance_to_point:
		dist[ point[0] ][ point[1] ] = alternate_distance
		prev[ point[0] ][ point[1] ] = original

# Given a grid of costs, find the best path between start[x,y] and end[x,y]
def find_path(grid, width, height, start, end):
	prev = find_paths(grid, width, height, start)
	
	# print(end)
	last_point = None
	point = end
	while not point is None:
		if point[0] == start[0] and point[1] == start[1]:
			return last_point
		
		next = prev[point[0]][point[1]]
		# print( next )
		last_point = point
		point = next
	
	return None

def find_paths(grid, width, height, start):
	dist = make_grid(width, height, None)
	prev = make_grid(width, height, None)
	
	Q = []
	
	for x in range(0, width):
		for y in range(0, height):
			Q.append( [x,y] )
			
	dist[ start[0] ][ start[1] ] = 0
	
	while len(Q) > 0:
		u = next_point(Q, dist)
		if u is None:
			break
			
		Q.remove(u)
		
		if u[0] > 0:
			analyze_point( u, [u[0] - 1, u[1]], grid, dist, prev )
			
		if u[0] < width - 1:
			analyze_point( u, [u[0] + 1, u[1]], grid, dist, prev )
			
		if u[1] > 0:
			analyze_point( u, [u[0], u[1] - 1], grid, dist, prev )
			
		if u[1] < height - 1:
			analyze_point( u, [u[0], u[1] + 1], grid, dist, prev )
			
	return prev
	
# g = make_grid(10, 10, 1)
# g[0][1] = None
# g[1][0] = 5
# print find_path(g, 10, 10, [0,0], [2,2])