#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Set, Tuple

Coord = Tuple[int, int]


@dataclass
class Shape:
    cells: Set[Coord]          # base shape, normalized
    variants: List[Set[Coord]] # all unique rotations/flips
    area: int                  # number of # cells


def normalize(cells: Set[Coord]) -> Set[Coord]:
    """Shift all cells so that min x and min y are 0."""
    xs = [x for x, y in cells]
    ys = [y for x, y in cells]
    min_x, min_y = min(xs), min(ys)
    return {(x - min_x, y - min_y) for x, y in cells}


def rotate90(cells: Set[Coord]) -> Set[Coord]:
    """Rotate 90 degrees around origin."""
    return { (y, -x) for (x, y) in cells }


def rotate180(cells: Set[Coord]) -> Set[Coord]:
    """Rotate 180 degrees around origin."""
    return { (-x, -y) for (x, y) in cells }


def rotate270(cells: Set[Coord]) -> Set[Coord]:
    """Rotate 270 degrees around origin."""
    return { (-y, x) for (x, y) in cells }


def flip_horizontal(cells: Set[Coord]) -> Set[Coord]:
    """Flip horizontally around y-axis."""
    return { (-x, y) for (x, y) in cells }


def generate_variants(base_cells: Set[Coord]) -> List[Set[Coord]]:
    """Generate all unique normalized rotations/flips of a shape."""
    variants = set()

    def add_variant(c: Set[Coord]):
        variants.add(frozenset(normalize(c)))

    # base, rotations, and flips
    base = base_cells
    add_variant(base)
    add_variant(rotate90(base))
    add_variant(rotate180(base))
    add_variant(rotate270(base))

    flipped = flip_horizontal(base)
    add_variant(flipped)
    add_variant(rotate90(flipped))
    add_variant(rotate180(flipped))
    add_variant(rotate270(flipped))

    return [set(v) for v in variants]


def parse_input(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # Separate into shapes section and regions section
    # We assume that after the last shape block, we get a blank line and then the regions.
    i = 0
    n = len(lines)

    shapes_raw = []
    # Parse shapes until we hit something that doesn't look like "<int>:"
    while i < n and lines[i].strip():
        # Expect something like "0:" or "12:"
        header = lines[i].strip()
        if not header.endswith(":"):
            break
        idx_str = header[:-1]
        if not idx_str.isdigit():
            break
        idx = int(idx_str)
        i += 1
        shape_rows = []
        # read subsequent non-empty lines that are not another "k:" header
        while i < n:
            line = lines[i]
            if line.strip() == "":
                i += 1
                break
            # If it looks like another shape header, stop this shape
            if line.strip().endswith(":"):
                maybe_idx = line.strip()[:-1]
                if maybe_idx.isdigit():
                    break
            shape_rows.append(line)
            i += 1

        shapes_raw.append((idx, shape_rows))

    # Now skip any blank lines before regions
    while i < n and lines[i].strip() == "":
        i += 1

    regions_raw = lines[i:]

    # Build shapes
    max_idx = max(idx for idx, _ in shapes_raw) if shapes_raw else -1
    shapes_list: List[Shape] = [None] * (max_idx + 1)

    for idx, rows in shapes_raw:
        cells = set()
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == '#':
                    cells.add((x, y))
        cells = normalize(cells)
        variants = generate_variants(cells)
        area = len(cells)
        shapes_list[idx] = Shape(cells=cells, variants=variants, area=area)

    # Parse regions
    regions = []
    for line in regions_raw:
        line = line.strip()
        if not line:
            continue
        # Format: WxH: c0 c1 c2 ...
        left, right = line.split(":")
        left = left.strip()
        right = right.strip()
        wh = left.split("x")
        if len(wh) != 2:
            continue  # skip malformed
        W = int(wh[0])
        H = int(wh[1])

        if right:
            counts = [int(x) for x in right.split()]
        else:
            counts = []

        regions.append((W, H, counts))

    return shapes_list, regions


def build_placements_for_region(W: int, H: int, counts: List[int], shapes: List[Shape]):
    placements = []
    shape_count = len(counts)

    for k in range(shape_count):
        if counts[k] == 0:
            continue
        shape = shapes[k]
        if shape is None:
            continue
        for variant in shape.variants:
            # determine bounding box of the variant
            xs = [x for x, y in variant]
            ys = [y for x, y in variant]
            max_x, max_y = max(xs), max(ys)
            width = max_x + 1
            height = max_y + 1

            # try all positions where it fits
            for oy in range(H - height + 1):
                for ox in range(W - width + 1):
                    cells_covered = set()
                    for (x, y) in variant:
                        gx = ox + x
                        gy = oy + y
                        if not (0 <= gx < W and 0 <= gy < H):
                            break
                        cells_covered.add(gy * W + gx)
                    else:
                        # only add if we covered all shape cells
                        if len(cells_covered) == len(variant):
                            placements.append({"shape": k, "cells": cells_covered})

    return placements


def can_fill_region(W: int, H: int, counts: List[int], shapes: List[Shape]) -> bool:
    shape_count = len(counts)
    # quick area check
    total_cells = W * H
    target_area = 0
    for k in range(shape_count):
        if counts[k] > 0 and shapes[k] is not None:
            target_area += counts[k] * shapes[k].area
    if target_area != total_cells:
        return False

    placements = build_placements_for_region(W, H, counts, shapes)

    used_cells = [False] * total_cells
    remaining_counts = counts[:]  # mutable copy
    used_placement = [False] * len(placements)

    placements_by_cell = [[] for _ in range(total_cells)]
    for idx, p in enumerate(placements):
        for c in p["cells"]:
            placements_by_cell[c].append(idx)

    def backtrack(filled_cells: int) -> bool:
        if filled_cells == total_cells:
            # all cells are filled; check all counts
            return all(c == 0 for c in remaining_counts)

        # find first empty cell
        try:
            cell = next(i for i, used in enumerate(used_cells) if not used)
        except StopIteration:
            # no empty cell, but not all filled? shouldn't happen
            return False

        # try all placements that cover this cell
        for p_idx in placements_by_cell[cell]:
            if used_placement[p_idx]:
                continue
            p = placements[p_idx]
            k = p["shape"]
            if remaining_counts[k] == 0:
                continue

            # check overlap
            if any(used_cells[c] for c in p["cells"]):
                continue

            # place it
            used_placement[p_idx] = True
            remaining_counts[k] -= 1
            newly_filled = []
            for c in p["cells"]:
                if not used_cells[c]:
                    used_cells[c] = True
                    newly_filled.append(c)

            if backtrack(filled_cells + len(newly_filled)):
                return True

            # undo
            for c in newly_filled:
                used_cells[c] = False
            remaining_counts[k] += 1
            used_placement[p_idx] = False

        return False

    return backtrack(0)


def main():
    shapes, regions = parse_input("input.txt")

    # Ensure we have shapes for all indices referenced in regions
    max_shape_index = 0
    for _, _, counts in regions:
        if counts:
            max_shape_index = max(max_shape_index, len(counts) - 1)
    if max_shape_index >= len(shapes):
        # pad shapes with None if needed
        shapes.extend([None] * (max_shape_index + 1 - len(shapes)))

    solvable_count = 0
    for (W, H, counts) in regions:
        # pad counts to match shapes length if necessary
        if len(counts) < len(shapes):
            counts = counts + [0] * (len(shapes) - len(counts))
        elif len(counts) > len(shapes):
            # unlikely, but truncate if input has more counts than shapes
            counts = counts[:len(shapes)]

        if can_fill_region(W, H, counts, shapes):
            solvable_count += 1

    print(solvable_count)


if __name__ == "__main__":
    main()
