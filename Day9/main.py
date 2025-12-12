#!/usr/bin/env python3
# PyPy-optimized + coordinate compression

from collections import deque

# ------------------------------------------------------------
# Parse input
# ------------------------------------------------------------

def parse_input(path="input.txt"):
    pts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(","))
                pts.append((x, y))
    return pts


# ------------------------------------------------------------
# Part 1: largest rectangle using any red tiles
# ------------------------------------------------------------

def largest_rectangle_any(points):
    n = len(points)
    best = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i+1, n):
            x2, y2 = points[j]
            area = abs(x1 - x2) * abs(y1 - y2)
            if area > best:
                best = area
    return best


# ------------------------------------------------------------
# Coordinate compression
# ------------------------------------------------------------

def compress_coords(points):
    xs = sorted(set(x for x, _ in points))
    ys = sorted(set(y for _, y in points))

    x_index = {x:i for i, x in enumerate(xs)}
    y_index = {y:i for i, y in enumerate(ys)}

    return xs, ys, x_index, y_index


# ------------------------------------------------------------
# Build compressed grid + boundary greens
# ------------------------------------------------------------

def build_grid(points, x_index, y_index):
    n = len(points)
    W = len(x_index)
    H = len(y_index)

    # 0 = empty, 1 = red, 2 = green
    grid = [[0]*W for _ in range(H)]

    # mark reds
    for x, y in points:
        gx = x_index[x]
        gy = y_index[y]
        grid[gy][gx] = 1

    # connect consecutive red points
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]

        gx1 = x_index[x1]
        gy1 = y_index[y1]
        gx2 = x_index[x2]
        gy2 = y_index[y2]

        if gx1 == gx2:
            # vertical
            if gy2 >= gy1:
                step = 1
            else:
                step = -1
            y = gy1
            while True:
                if grid[y][gx1] == 0:
                    grid[y][gx1] = 2
                if y == gy2:
                    break
                y += step
        else:
            # horizontal
            if gx2 >= gx1:
                step = 1
            else:
                step = -1
            x = gx1
            while True:
                if grid[gy1][x] == 0:
                    grid[gy1][x] = 2
                if x == gx2:
                    break
                x += step

    return grid


# ------------------------------------------------------------
# Fill polygon interior with green (BFS from outside)
# ------------------------------------------------------------

def fill_interior_green(grid):
    H = len(grid)
    W = len(grid[0])

    EH = H + 2
    EW = W + 2

    ext = [[0]*EW for _ in range(EH)]
    for y in range(H):
        row = grid[y]
        erow = ext[y+1]
        for x in range(W):
            erow[x+1] = row[x]

    outside = [[False]*EW for _ in range(EH)]
    q = deque([(0, 0)])
    outside[0][0] = True

    while q:
        cy, cx = q.popleft()

        # 4-neighbour BFS
        ny = cy + 1
        if ny < EH and not outside[ny][cx] and ext[ny][cx] == 0:
            outside[ny][cx] = True
            q.append((ny, cx))

        ny = cy - 1
        if ny >= 0 and not outside[ny][cx] and ext[ny][cx] == 0:
            outside[ny][cx] = True
            q.append((ny, cx))

        nx = cx + 1
        if nx < EW and not outside[cy][nx] and ext[cy][nx] == 0:
            outside[cy][nx] = True
            q.append((cy, nx))

        nx = cx - 1
        if nx >= 0 and not outside[cy][nx] and ext[cy][nx] == 0:
            outside[cy][nx] = True
            q.append((cy, nx))

    # mark interior as green
    for y in range(H):
        row = grid[y]
        oy = outside[y+1]
        ey = ext[y+1]
        for x in range(W):
            if ey[x+1] == 0 and not oy[x+1]:
                row[x] = 2

    return grid


# ------------------------------------------------------------
# Prefix sum for fast rectangle validation
# ------------------------------------------------------------

def build_bad_prefix(grid):
    H = len(grid)
    W = len(grid[0])

    ps = [[0]*(W+1) for _ in range(H+1)]

    for y in range(1, H+1):
        row = grid[y-1]
        ps_row = ps[y]
        ps_above = ps[y-1]
        row_sum = 0
        for x in range(1, W+1):
            bad = 1 if row[x-1] == 0 else 0
            row_sum += bad
            ps_row[x] = ps_above[x] + row_sum

    return ps


def rect_ok(ps, x1, y1, x2, y2):
    # inclusive rectangle
    x1p = x1 + 1
    y1p = y1 + 1
    x2p = x2 + 1
    y2p = y2 + 1
    ps_y2 = ps[y2p]
    ps_y1m1 = ps[y1p - 1]
    total = ps_y2[x2p] - ps_y1m1[x2p] - ps_y2[x1p - 1] + ps_y1m1[x1p - 1]
    return total == 0


# ------------------------------------------------------------
# Part 2: largest rectangle using only red+green tiles
# ------------------------------------------------------------

def largest_rectangle_red_green(points):
    xs, ys, x_index, y_index = compress_coords(points)
    grid = build_grid(points, x_index, y_index)
    grid = fill_interior_green(grid)
    ps = build_bad_prefix(grid)

    # compressed red coords
    red = [(x_index[x], y_index[y]) for x, y in points]

    n = len(red)
    best = 0

    for i in range(n):
        x1, y1 = red[i]
        for j in range(i+1, n):
            x2, y2 = red[j]

            gx1 = x1 if x1 < x2 else x2
            gx2 = x2 if x2 > x1 else x1
            gy1 = y1 if y1 < y2 else y2
            gy2 = y2 if y2 > y1 else y1

            area = (gx2 - gx1) * (gy2 - gy1)
            if area <= best:
                continue

            if rect_ok(ps, gx1, gy1, gx2, gy2):
                best = area

    return best


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    points = parse_input("input.txt")

    print("Part 1:", largest_rectangle_any(points))
    print("Part 2:", largest_rectangle_red_green(points))


if __name__ == "__main__":
    main()
