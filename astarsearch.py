""" A* Search algorithm implementation to find the minimum path between 2 points"""

def astar(m, startp, endp):
    """ a* search """
    w, h = 10, 10		# 10x10(blocks) is the dimension of the input images
    sx, sy = startp  # Start Point
    ex, ey = endp  # End Point
    # [parent node, x, y, g, f]
    node = [None, sx, sy, 0, abs(ex-sx)+abs(ey-sy)]
    close_list = [node]
    created_list = {}
    created_list[sy*w+sx] = node
    k = 0
    while close_list:
        node = close_list.pop(0)
        x = node[1]
        y = node[2]
        l = node[3]+1
        k += 1
        # find neighbours
        if k != 0:
            neighbours = ((x, y+1), (x, y-1), (x+1, y), (x-1, y))
        else:
            neighbours = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        for nx, ny in neighbours:
            if nx == ex and ny == ey:
                path = [(ex, ey)]
                while node:
                    path.append((node[1], node[2]))
                    node = node[0]
                return list(reversed(path))
            if 0 <= nx < w and 0 <= ny < h and m[ny][nx] == 0:
                if ny*w+nx not in created_list:
                    nn = (node, nx, ny, l, l+abs(nx-ex)+abs(ny-ey))
                    created_list[ny*w+nx] = nn
                    # adding to close_list ,using binary heap
                    nni = len(close_list)
                    close_list.append(nn)
                    while nni:
                        i = (nni-1) >> 1
                        if close_list[i][4] > nn[4]:
                            close_list[i], close_list[nni] = nn, close_list[i]
                            nni = i
                        else:
                            break
    return []
