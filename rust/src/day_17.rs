use std::collections::VecDeque;
use std::iter;

type Grid = VecDeque<VecDeque<VecDeque<char>>>;

pub fn solve(input: &[String]) {
    let mut grid = parse(input);
    let final_grid = run(&mut grid);
    println!("Part 1: {}", num_active(&final_grid));

}

fn parse(input: &[String]) -> Grid {
    let mut result: Grid = VecDeque::new();

    result.push_front(input.iter().map(|r| r.trim().chars().collect()).collect());

    result
}

fn contrib(grid: &Grid, x: i32, y: i32, z: i32) -> i32 {
    if x < 0 || y < 0 || z < 0 {
        0
    } else {
        let x = x as usize;
        let y = y as usize;
        let z = z as usize;
        if x >= grid.len() || y >= grid[0].len() || z >= grid[0][0].len() || grid[x][y][z] == '.' {
            0
        } else {
            1
        }
    }
}

fn num_around(grid: &Grid, x: usize, y: usize, z: usize) -> i32 {
    let x = x as i32;
    let y = y as i32;
    let z = z as i32;

    let mut around = 0;
    for dx in -1..2 {
        for dy in -1..2 {
            for dz in -1..2 {
                if !(dx == 0 && dy == 0 && dz == 0) {
                    around += contrib(grid, x + dx, y + dy, z + dz);
                }
            }
        }
    }

    around
}

fn step(grid: &mut Grid) -> Grid {
    let zlen = grid[0][0].len() + 2;
    let ylen = grid[0].len() + 2;

    let row: VecDeque<char> = iter::repeat('.').take(zlen).collect();

    for plane in grid.iter_mut() {
        for k in 0..plane.len() {
            plane[k].push_front('.');
            plane[k].push_back('.');
        }

        plane.push_front(row.clone());
        plane.push_back(row.clone());
    }

    grid.push_front(iter::repeat(row.clone()).take(ylen).collect());
    grid.push_back(iter::repeat(row.clone()).take(ylen).collect());
    let mut new = Grid::new();

    for (i, plane) in grid.iter().enumerate() {
        let mut new_plane = VecDeque::new();
        for (j, row) in plane.iter().enumerate() {
            let mut new_row = VecDeque::new();
            for (k, state) in row.iter().enumerate() {
                let around = num_around(grid, i, j, k);

                if *state == '#' {
                    if around == 2 || around == 3 {
                        new_row.push_front('#');
                    } else {
                        new_row.push_front('.');
                    }
                } else {
                    if around == 3 {
                        new_row.push_front('#');
                    } else {
                        new_row.push_front('.');
                    }
                }
            }

            new_plane.push_front(new_row);
        }

        new.push_front(new_plane)
    }

    new
}

fn num_active(grid: &Grid) -> usize {
    grid.iter()
        .map(|p| {
            p.iter()
                .map(|r| r.iter().filter(|s| **s == '#').count())
                .sum::<usize>()
        })
        .sum()
}

fn run(grid: &mut Grid) -> Grid {
    let mut result = step(grid);
    for _ in 0..5 {
        result = step(&mut result);
    }

    result
}


#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![".#.\n", "..#\n", "###\n"];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse(&fixture());
        assert_eq!(parsed.len(), 1);

        let plane = &parsed[0];
        assert_eq!(plane.len(), 3);
        assert_eq!(plane[0].len(), 3);
    }

    #[test]
    fn test_num_around() {
        let parsed = parse(&fixture());
        assert_eq!(num_around(&parsed, 0, 0, 0), 1, "failed at (0, 0)");
        assert_eq!(num_around(&parsed, 0, 0, 1), 1, "failed at (0, 1)");
        assert_eq!(num_around(&parsed, 0, 0, 2), 2, "failed at (0, 2)");

        assert_eq!(num_around(&parsed, 0, 1, 0), 3, "failed at (1, 0)");
        assert_eq!(num_around(&parsed, 0, 1, 1), 5, "failed at (1, 1)");
        assert_eq!(num_around(&parsed, 0, 1, 2), 3, "failed at (1, 2)");

        assert_eq!(num_around(&parsed, 0, 2, 0), 1, "failed at (2, 0)");
        assert_eq!(num_around(&parsed, 0, 2, 1), 3, "failed at (2, 1)");
        assert_eq!(num_around(&parsed, 0, 2, 2), 2, "failed at (2, 2)");
    }

    #[test]
    fn test_step() {
        let mut parsed = parse(&fixture());
        let next = step(&mut parsed);

        assert_eq!(next.len(), 3);
        assert_eq!(next[0].len(), 5);
        assert_eq!(next[1].len(), 5);
        assert_eq!(next[1][0].len(), 5);
        assert_eq!(next[1][1].len(), 5);

        assert_eq!(num_active(&parsed), 5);
        assert_eq!(num_active(&next), 3 + 5 + 3);
    }

    #[test]
    fn test_run() {
        let mut parsed = parse(&fixture());
        let result = run(&mut parsed);
        assert_eq!(num_active(&result), 112);
    }
}
