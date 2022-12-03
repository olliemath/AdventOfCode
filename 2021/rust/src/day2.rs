pub enum Directions {
    Up,
    Down,
    Forward,
}


fn parse_line(line: &str) -> (Directions, u32) {
    let mut split = line.split_whitespace();
    let dir = match split.next().unwrap() {
        "up" => Directions::Up,
        "down" => Directions::Down,
        "forward" => Directions::Forward,
        _ => panic!("Bad direction!"),
    };
    let amt: u32 = split.next().unwrap().parse().unwrap();
    (dir, amt)
}


pub fn parse(input: &str) -> Vec<(Directions, u32)> {
    input.lines().map(parse_line).collect()
}

pub fn solve_part1(input: &[(Directions, u32)]) -> u32 {
    let mut x = 0;
    let mut y = 0;

    for (d, a) in input.iter() {
        match d {
            Directions::Up => y -= a,
            Directions::Down => y += a,
            Directions::Forward => x += a,
        };
    }

    x * y
}

pub fn solve_part2(input: &[(Directions, u32)]) -> u32 {
    let mut x = 0;
    let mut y = 0;
    let mut aim = 0;

    for (d, a) in input.iter() {
        match d {
            Directions::Up => aim -= a,
            Directions::Down => aim += a,
            Directions::Forward => {
                x += a;
                y += aim * a;
            },
        };
    }

    x * y
}
