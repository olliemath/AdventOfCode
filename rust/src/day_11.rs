type Grid = Vec<Vec<u8>>;

#[derive(Clone, Copy)]
enum Version {
    One,
    Two,
}

pub fn solve(input: &[String]) {
    let parsed = parse(input);
    println!("Part1: {}", get_stable_seat_count(&parsed, Version::One));
    println!("Part2: {}", get_stable_seat_count(&parsed, Version::Two));
}

fn parse(input: &[String]) -> Grid {
    input
        .iter()
        .map(|r| r.trim().as_bytes().iter().cloned().collect())
        .collect()
}

fn contrib(grid: &Grid, x: i32, y: i32) -> i32 {
    if x < 0 || y < 0 {
        0
    } else {
        let x = x as usize;
        let y = y as usize;
        if x >= grid.len()
            || y >= grid[0].len()
            || grid[x][y] == 'L' as u8
            || grid[x][y] == '.' as u8
        {
            0
        } else {
            1
        }
    }
}

fn is_seat(grid: &Grid, x: usize, y: usize) -> bool {
    let square = grid[x][y];
    square == 'L' as u8 || square == '#' as u8
}

fn num_around(grid: &Grid, x: usize, y: usize) -> i32 {
    let x = x as i32;
    let y = y as i32;

    contrib(grid, x - 1, y - 1)
        + contrib(grid, x - 1, y)
        + contrib(grid, x - 1, y + 1)
        + contrib(grid, x, y - 1)
        + contrib(grid, x, y + 1)
        + contrib(grid, x + 1, y - 1)
        + contrib(grid, x + 1, y)
        + contrib(grid, x + 1, y + 1)
}

fn contrib_in_direction(grid: &Grid, x: i32, y: i32, p: i32, q: i32) -> i32 {
    let mut contrib = 0;
    let mut x = x;
    let mut y = y;
    loop {
        x += p;
        y += q;

        if x < 0 || y < 0 || x as usize >= grid.len() || y as usize >= grid[0].len() {
            break;
        }
        let seat = grid[x as usize][y as usize];

        if seat == 'L' as u8 {
            break; // Empty seat spotted
        }
        if seat == '#' as u8 {
            contrib = 1; // Occupied seat spotted
            break;
        }
    }

    contrib
}

fn num_visible_around(grid: &Grid, x: usize, y: usize) -> i32 {
    let x = x as i32;
    let y = y as i32;

    contrib_in_direction(grid, x, y, -1, -1)
        + contrib_in_direction(grid, x, y, -1, 0)
        + contrib_in_direction(grid, x, y, -1, 1)
        + contrib_in_direction(grid, x, y, 0, -1)
        + contrib_in_direction(grid, x, y, 0, 1)
        + contrib_in_direction(grid, x, y, 1, -1)
        + contrib_in_direction(grid, x, y, 1, 0)
        + contrib_in_direction(grid, x, y, 1, 1)
}

fn should_flip_square(grid: &Grid, x: usize, y: usize, version: Version) -> bool {
    match version {
        Version::One => {
            is_seat(grid, x, y)
                && ((contrib(grid, x as i32, y as i32) == 0 && num_around(grid, x, y) == 0)
                    || contrib(grid, x as i32, y as i32) != 0 && num_around(grid, x, y) >= 4)
        }
        Version::Two => {
            is_seat(grid, x, y)
                && ((contrib(grid, x as i32, y as i32) == 0 && num_visible_around(grid, x, y) == 0)
                    || contrib(grid, x as i32, y as i32) != 0
                        && num_visible_around(grid, x, y) >= 5)
        }
    }
}

fn step(grid: &Grid, version: Version) -> Grid {
    let mut new = Vec::new();
    for (i, row) in grid.iter().enumerate() {
        let mut new_row: Vec<u8> = row.iter().cloned().collect();
        for (j, seat) in row.iter().enumerate() {
            if should_flip_square(grid, i, j, version) {
                match *seat as char {
                    '#' => new_row[j] = 'L' as u8,
                    'L' => new_row[j] = '#' as u8,
                    _ => unreachable!(),
                };
            }
        }
        new.push(new_row);
    }

    new
}

fn get_stable_state(grid: &Grid, version: Version) -> Grid {
    let mut prev_state = step(grid, version);

    loop {
        let state = step(&prev_state, version);
        if state == prev_state {
            break;
        }
        prev_state = state;
    }

    prev_state
}

fn get_stable_seat_count(grid: &Grid, version: Version) -> i32 {
    let state = get_stable_state(grid, version);
    let mut count = 0;

    for row in state.iter() {
        for seat in row.iter() {
            if *seat == '#' as u8 {
                count += 1;
            }
        }
    }

    count
}

#[cfg(test)]
mod tests {
    use super::*;

    fn round0() -> Vec<&'static str> {
        vec![
            "L.LL.LL.LL\n",
            "LLLLLLL.LL\n",
            "L.L.L..L..\n",
            "LLLL.LL.LL\n",
            "L.LL.LL.LL\n",
            "L.LLLLL.LL\n",
            "..L.L.....\n",
            "LLLLLLLLLL\n",
            "L.LLLLLL.L\n",
            "L.LLLLL.LL\n",
        ]
    }

    fn round1() -> Vec<&'static str> {
        vec![
            "#.##.##.##\n",
            "#######.##\n",
            "#.#.#..#..\n",
            "####.##.##\n",
            "#.##.##.##\n",
            "#.#####.##\n",
            "..#.#.....\n",
            "##########\n",
            "#.######.#\n",
            "#.#####.##\n",
        ]
    }

    fn round2() -> Vec<&'static str> {
        vec![
            "#.LL.L#.##\n",
            "#LLLLLL.L#\n",
            "L.L.L..L..\n",
            "#LLL.LL.L#\n",
            "#.LL.LL.LL\n",
            "#.LLLL#.##\n",
            "..L.L.....\n",
            "#LLLLLLLL#\n",
            "#.LLLLLL.L\n",
            "#.#LLLL.##\n",
        ]
    }

    fn fixture(n: i32) -> Vec<String> {
        match n {
            0 => round0(),
            1 => round1(),
            2 => round2(),
            _ => panic!("Round not implemented"),
        }
        .iter()
        .map(|s| String::from(*s))
        .collect()
    }

    #[test]
    fn test_parse() {
        let state = parse(&fixture(0));
        assert_eq!(state.len(), 10);
        assert_eq!(state[0].len(), 10);
    }

    #[test]
    fn test_step() {
        let state = parse(&fixture(0));
        let expected = parse(&fixture(1));
        let actual = step(&state, Version::One);

        assert_eq!(expected, actual);
    }

    #[test]
    fn test_twostep() {
        let state = parse(&fixture(0));
        let expected = parse(&fixture(2));
        let actual = step(&step(&state, Version::One), Version::One);

        assert_eq!(expected, actual);
    }

    #[test]
    fn test_get_stable_seat_count() {
        let state = parse(&fixture(0));
        assert_eq!(get_stable_seat_count(&state, Version::One), 37);
    }

    #[test]
    fn test_step_two() {
        let step1: Grid = vec![
            "#.##.##.##",
            "#######.##",
            "#.#.#..#..",
            "####.##.##",
            "#.##.##.##",
            "#.#####.##",
            "..#.#.....",
            "##########",
            "#.######.#",
            "#.#####.##",
        ]        .iter()
        .map(|r| r.as_bytes().iter().cloned().collect())
        .collect();

        let step2: Grid = vec![
            "#.LL.LL.L#",
            "#LLLLLL.LL",
            "L.L.L..L..",
            "LLLL.LL.LL",
            "L.LL.LL.LL",
            "L.LLLLL.LL",
            "..L.L.....",
            "LLLLLLLLL#",
            "#.LLLLLL.L",
            "#.LLLLL.L#",
        ]        .iter()
        .map(|r| r.trim().as_bytes().iter().cloned().collect())
        .collect();

        let actual1 = step(&parse(&fixture(0)), Version::Two);
        let actual2 = step(&actual1, Version::Two);

        assert_eq!(actual1, step1);
        assert_eq!(actual2, step2);
    }

    #[test]
    fn test_get_stable_seat_count_two() {
        let state = parse(&fixture(0));
        assert_eq!(get_stable_seat_count(&state, Version::Two), 26);
    }
}
