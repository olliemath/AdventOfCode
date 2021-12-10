struct Tile {
    id: u64,
    pattern: Vec<String>,
}

pub fn solve(input: &[String]) {
    println!("Part1: {}", part1(input));
    println!("Part2: {}", part2(input).0);
}

fn parse(input: &[String]) -> Vec<Tile> {
    input.split(|l| l.trim() == "").map(parse_tile).collect()
}

fn parse_tile(input: &[String]) -> Tile {
    let id = input[0]
        .trim()
        .trim_start_matches("Tile ")
        .trim_end_matches(':')
        .parse()
        .unwrap();
    let pattern = input
        .iter()
        .skip(1)
        .map(|l| String::from(l.trim()))
        .collect();
    Tile { id, pattern }
}

fn edge_combos(tile: &Tile) -> [[String; 4]; 8] {
    let top = tile.pattern[0].clone();
    let bottom = tile.pattern[tile.pattern.len() - 1].clone();
    let left: String = tile
        .pattern
        .iter()
        .map(|s| s.chars().next().unwrap())
        .collect();
    let right: String = tile
        .pattern
        .iter()
        .map(|s| s.chars().last().unwrap())
        .collect();

    let edges = [top, right, bottom, left]; // We always list edges clockwise
    let r1 = rotate_clockwise(&edges);
    let r2 = rotate_clockwise(&r1);
    let r3 = rotate_clockwise(&r2);
    let flip = flip_lr(&edges);
    let rf1 = rotate_clockwise(&flip);
    let rf2 = rotate_clockwise(&rf1);
    let rf3 = rotate_clockwise(&rf2);

    [edges, r1, r2, r3, flip, rf1, rf2, rf3]
}

fn rotate_clockwise(edges: &[String; 4]) -> [String; 4] {
    let top = edges[3].chars().rev().collect();
    let right = edges[0].clone();
    let bottom = edges[1].chars().rev().collect();
    let left = edges[2].clone();

    [top, right, bottom, left]
}

fn flip_lr(edges: &[String; 4]) -> [String; 4] {
    let top = edges[0].chars().rev().collect();
    let right = edges[3].clone();
    let bottom = edges[2].chars().rev().collect();
    let left = edges[1].clone();

    [top, right, bottom, left]
}

fn rotate_tile_clockwise(tile: &Vec<String>) -> Vec<String> {
    (0..tile.len())
        .map(|i| {
            tile.iter()
                .map(|s| s.chars().nth(i).unwrap())
                .rev()
                .collect()
        })
        .collect()
}

fn flip_tile_lr(tile: &Vec<String>) -> Vec<String> {
    tile.iter().map(|s| s.chars().rev().collect()).collect()
}

fn permutations(tile: &Vec<String>) -> [Vec<String>; 8] {
    let normal = tile.clone();
    let flipped = flip_tile_lr(&normal);
    let r1 = rotate_tile_clockwise(tile);
    let r2 = rotate_tile_clockwise(&r1);
    let r3 = rotate_tile_clockwise(&r2);
    let rf1 = rotate_tile_clockwise(&flipped);
    let rf2 = rotate_tile_clockwise(&rf1);
    let rf3 = rotate_tile_clockwise(&rf2);
    [normal, r1, r2, r3, flipped, rf1, rf2, rf3]
}

#[derive(Debug, Clone, PartialEq)]
struct Arrangement {
    grid_size: usize,
    current: Vec<Vec<(usize, usize)>>,
}

fn build_grid(
    arrangement: &Arrangement,
    edge_lookup: &Vec<[[String; 4]; 8]>,
) -> Option<Arrangement> {
    if arrangement.current.len() == 0 {
        for i in 0..edge_lookup.len() {
            for j in 0..8 {
                let mut new = arrangement.clone();
                new.current.push(vec![(i, j)]);
                if new.grid_size == 1 {
                    return Some(new);
                } else {
                    let result = build_grid(&new, edge_lookup);
                    if result.is_some() {
                        return result;
                    }
                }
            }
        }
    } else {
        // Find the next item in the grid
        let mut row = arrangement.current.len() - 1;
        let mut col = arrangement.current[row].len();

        // We may need a new row
        if col == arrangement.grid_size {
            row += 1;
            col = 0;
        }

        for i in 0..edge_lookup.len() {
            if arrangement
                .current
                .iter()
                .any(|row| row.iter().any(|c| c.0 == i))
            {
                continue;
            }

            for j in 0..8 {
                // Determine if this square matches the one above
                if row > 0 {
                    let above = arrangement.current[row - 1][col];
                    let above_edge = &edge_lookup[above.0][above.1][2]; // Bottom of above tile
                    let this_edge = &edge_lookup[i][j][0]; // Top of this tile
                    if this_edge != above_edge {
                        continue;
                    }
                }
                if col > 0 {
                    let left = arrangement.current[row][col - 1];
                    let left_edge = &edge_lookup[left.0][left.1][1]; // Right of left tile
                    let this_edge = &edge_lookup[i][j][3]; // Left of this tile
                    if left_edge != this_edge {
                        continue;
                    }
                }

                let mut new = arrangement.clone();
                if col == 0 {
                    new.current.push(vec![(i, j)]);
                } else {
                    new.current[row].push((i, j));
                }

                if new.current.len() == new.grid_size
                    && new.current.last().unwrap().len() == new.grid_size
                {
                    return Some(new);
                } else {
                    let result = build_grid(&new, edge_lookup);
                    if result.is_some() {
                        return result;
                    }
                }
            }
        }
    }

    None
}

fn strip_edge(tile: &Tile) -> Vec<String> {
    tile.pattern
        .iter()
        .skip(1)
        .map(|r| String::from(&r[1..r.len() - 1]))
        .take(tile.pattern.len() - 2)
        .collect()
}

fn transform(tile: Vec<String>, variant: usize) -> Vec<String> {
    let mut variant = variant;
    let mut tile = tile;
    if variant > 3 {
        tile = flip_tile_lr(&tile);
        variant -= 3;
    }
    while variant > 0 {
        tile = rotate_tile_clockwise(&tile);
        variant -= 1;
    }

    tile
}

fn merge(tiles: &Vec<Vec<Vec<String>>>) -> Vec<String> {
    tiles
        .iter()
        .map(|row| {
            (0..row[0].len())
                .map(|i| {
                    row.iter()
                        .map(|t| t[i].clone())
                        .collect::<Vec<String>>()
                        .join("")
                })
                .collect::<Vec<String>>()
        })
        .flatten()
        .collect()
}

fn build_picutre_from_arrangement(arrangement: &Arrangement, tiles: &Vec<Tile>) -> Vec<String> {
    merge(
        &arrangement
            .current
            .iter()
            .map(|row| {
                row.iter()
                    .map(|(i, j)| transform(strip_edge(&tiles[*i]), *j))
                    .collect()
            })
            .collect(),
    )
}

fn spot_monsters(picture: &Vec<String>) -> (usize, usize) {
    let monster = vec![
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ];

    let required: Vec<(usize, usize)> = monster
        .iter()
        .enumerate()
        .map(|(i, row)| {
            row.chars()
                .enumerate()
                .filter(|(_, c)| *c == '#')
                .map(|(j, _)| (i, j))
                .collect::<Vec<(usize, usize)>>()
        })
        .flatten()
        .collect();

    let mut monsters = 0;
    for x in 0..picture.len() - 3 {
        for y in 0..picture.len() - 20 {
            if required
                .iter()
                .all(|(i, j)| picture[x + i].chars().nth(y + j).unwrap() == '#')
            {
                monsters += 1;
            }
        }
    }

    (
        picture
            .iter()
            .map(|s| s.chars().filter(|c| *c == '#').count())
            .sum::<usize>()
            - monsters * required.len(),
        monsters,
    )
}

fn part1(input: &[String]) -> u64 {
    let tiles = parse(input);
    let edge_combos: Vec<[[String; 4]; 8]> = tiles.iter().map(edge_combos).collect();
    // Work out grid size
    let grid_size = (tiles.len() as f64).sqrt() as usize;
    assert_eq!(grid_size * grid_size, tiles.len(), "Grid is not a square!");

    let arrangement = build_grid(
        &Arrangement {
            grid_size,
            current: vec![],
        },
        &edge_combos,
    )
    .unwrap();

    let debug: Vec<Vec<(u64, usize)>> = arrangement
        .current
        .iter()
        .map(|row| row.iter().map(|(i, j)| (tiles[*i].id, *j)).collect())
        .collect();

    // println!("{:?}", debug);
    let mut result = 1;
    result *= debug[0][0].0;
    result *= debug[0].last().unwrap().0;
    result *= debug.last().unwrap()[0].0;
    result *= debug.last().unwrap().last().unwrap().0;

    result
}

fn get_picture(input: &[String]) -> Vec<String> {
    let tiles = parse(input);
    let edge_combos: Vec<[[String; 4]; 8]> = tiles.iter().map(edge_combos).collect();
    // Work out grid size
    let grid_size = (tiles.len() as f64).sqrt() as usize;
    assert_eq!(grid_size * grid_size, tiles.len(), "Grid is not a square!");

    let arrangement = build_grid(
        &Arrangement {
            grid_size,
            current: vec![],
        },
        &edge_combos,
    )
    .unwrap();

    let debug: Vec<Vec<(u64, usize)>> = arrangement
        .current
        .iter()
        .map(|row| row.iter().map(|(i, j)| (tiles[*i].id, *j)).collect())
        .collect();

    build_picutre_from_arrangement(&arrangement, &tiles)
}

fn part2(input: &[String]) -> (usize, usize) {
    let picture = get_picture(input);
    for permutation in permutations(&picture).iter() {
        let (choppiness, monsters) = spot_monsters(&permutation);
        if monsters > 0 {
            return (choppiness, monsters);
        }
    }

    unreachable!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        let raw = fixture();
        let parsed = parse(&raw);
        assert_eq!(parsed.len(), 9);
        assert_eq!(parsed[0].id, 2311);
        assert_eq!(parsed[0].pattern.len(), 10);
        assert_eq!(parsed[0].pattern[0].len(), 10);
    }

    #[test]
    fn test_edge_combos() {
        let raw = fixture();
        let parsed = parse(&raw);
        let combos = edge_combos(&parsed[0]);
        assert_eq!(
            combos[0],
            ["..##.#..#.", "...#.##..#", "..###..###", ".#####..#."]
        );
        assert_eq!(
            combos[1],
            [".#..#####.", "..##.#..#.", "#..##.#...", "..###..###"]
        );
    }

    #[test]
    fn test_rotate_tile_clockwise() {
        let tile = vec![String::from("ab"), String::from("cd")];
        let expected = vec![String::from("ca"), String::from("db")];
        let rotated = rotate_tile_clockwise(&tile);
        assert_eq!(rotated, expected);
    }

    #[test]
    fn test_merge() {
        let row1 = vec![
            vec![String::from("ab"), String::from("cd")],
            vec![String::from("ab"), String::from("cd")],
        ];
        let row2 = vec![
            vec![String::from("pq"), String::from("rs")],
            vec![String::from("xy"), String::from("zw")],
        ];
        let tiles = vec![row1, row2];
        let expected = vec![
            String::from("abab"),
            String::from("cdcd"),
            String::from("pqxy"),
            String::from("rszw"),
        ];
        let actual = merge(&tiles);
        assert_eq!(actual, expected);
    }

    #[test]
    fn test_build_picture_from_arrangement() {
        let picture = get_picture(&fixture());
        let variations = permutations(&picture);

        let expected = vec![
            ".#.#..#.##...#.##..#####",
            "###....#.#....#..#......",
            "##.##.###.#.#..######...",
            "###.#####...#.#####.#..#",
            "##.#....#.##.####...#.##",
            "...########.#....#####.#",
            "....#..#...##..#.#.###..",
            ".####...#..#.....#......",
            "#..#.##..#..###.#.##....",
            "#.####..#.####.#.#.###..",
            "###.#.#...#.######.#..##",
            "#.####....##..########.#",
            "##..##.#...#...#.#.#.#..",
            "...#..#..#.#.##..###.###",
            ".#.#....#.##.#...###.##.",
            "###.#...#..#.##.######..",
            ".#.#.###.##.##.#..#.##..",
            ".####.###.#...###.#..#.#",
            "..#.#..#..#.#.#.####.###",
            "#..####...#.#.#.###.###.",
            "#####..#####...###....##",
            "#.##..#..#...#..####...#",
            ".#.###..##..##..####.##.",
            "...###...##...#...#..###",
        ];
        assert_eq!(variations.iter().filter(|v| *v == &expected).count(), 1);
    }

    #[test]
    fn test_part1() {
        let result = part1(&fixture0());
        assert_eq!(result, 2311 * 2311 * 2311 * 2311);
        let result = part1(&fixture());
        assert_eq!(result, 20899048083289);
    }

    #[test]
    fn test_part2() {
        let result = part2(&fixture());
        assert_eq!(result, (273, 2));
    }

    fn fixture0() -> Vec<String> {
        let raw = vec![
            "Tile 2311:\n",
            "..##.#..#.\n",
            "##..#.....\n",
            "#...##..#.\n",
            "####.#...#\n",
            "##.##.###.\n",
            "##...#.###\n",
            ".#.#.#..##\n",
            "..#....#..\n",
            "###...#.#.\n",
            "..###..###\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    fn fixture() -> Vec<String> {
        let raw = vec![
            "Tile 2311:\n",
            "..##.#..#.\n",
            "##..#.....\n",
            "#...##..#.\n",
            "####.#...#\n",
            "##.##.###.\n",
            "##...#.###\n",
            ".#.#.#..##\n",
            "..#....#..\n",
            "###...#.#.\n",
            "..###..###\n",
            "\n",
            "Tile 1951:\n",
            "#.##...##.\n",
            "#.####...#\n",
            ".....#..##\n",
            "#...######\n",
            ".##.#....#\n",
            ".###.#####\n",
            "###.##.##.\n",
            ".###....#.\n",
            "..#.#..#.#\n",
            "#...##.#..\n",
            "\n",
            "Tile 1171:\n",
            "####...##.\n",
            "#..##.#..#\n",
            "##.#..#.#.\n",
            ".###.####.\n",
            "..###.####\n",
            ".##....##.\n",
            ".#...####.\n",
            "#.##.####.\n",
            "####..#...\n",
            ".....##...\n",
            "\n",
            "Tile 1427:\n",
            "###.##.#..\n",
            ".#..#.##..\n",
            ".#.##.#..#\n",
            "#.#.#.##.#\n",
            "....#...##\n",
            "...##..##.\n",
            "...#.#####\n",
            ".#.####.#.\n",
            "..#..###.#\n",
            "..##.#..#.\n",
            "\n",
            "Tile 1489:\n",
            "##.#.#....\n",
            "..##...#..\n",
            ".##..##...\n",
            "..#...#...\n",
            "#####...#.\n",
            "#..#.#.#.#\n",
            "...#.#.#..\n",
            "##.#...##.\n",
            "..##.##.##\n",
            "###.##.#..\n",
            "\n",
            "Tile 2473:\n",
            "#....####.\n",
            "#..#.##...\n",
            "#.##..#...\n",
            "######.#.#\n",
            ".#...#.#.#\n",
            ".#########\n",
            ".###.#..#.\n",
            "########.#\n",
            "##...##.#.\n",
            "..###.#.#.\n",
            "\n",
            "Tile 2971:\n",
            "..#.#....#\n",
            "#...###...\n",
            "#.#.###...\n",
            "##.##..#..\n",
            ".#####..##\n",
            ".#..####.#\n",
            "#..#.#..#.\n",
            "..####.###\n",
            "..#.#.###.\n",
            "...#.#.#.#\n",
            "\n",
            "Tile 2729:\n",
            "...#.#.#.#\n",
            "####.#....\n",
            "..#.#.....\n",
            "....#..#.#\n",
            ".##..##.#.\n",
            ".#.####...\n",
            "####.#.#..\n",
            "##.####...\n",
            "##..#.##..\n",
            "#.##...##.\n",
            "\n",
            "Tile 3079:\n",
            "#.#.#####.\n",
            ".#..######\n",
            "..#.......\n",
            "######....\n",
            "####.#..#.\n",
            ".#...#.##.\n",
            "#.#####.##\n",
            "..#.###...\n",
            "..#.......\n",
            "..#.###...\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }
}
