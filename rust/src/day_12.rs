#[derive(Debug, PartialEq, Clone)]
enum Instruction {
    North(i32),
    South(i32),
    East(i32),
    West(i32),
    Left(i32),
    Right(i32),
    Forward(i32),
}

struct Ship {
    direction: i32, // As degrees e.g. on a compass
    lattitude: i32, // N-S component
    longitude: i32, // E-W component
    waypoint:  Waypoint,
}

impl Ship {
    fn new() -> Self {
        Self {
            direction: 90,
            lattitude: 0,
            longitude: 0,
            waypoint: Waypoint::new()
        }
    }

    fn go(&mut self, ins: &Instruction) {
        match ins {
            Instruction::North(x) => self.lattitude += x,
            Instruction::South(x) => self.lattitude -= x,
            Instruction::East(x) => self.longitude += x,
            Instruction::West(x) => self.longitude -= x,
            Instruction::Left(x) => self.direction = (self.direction - x) % 360,
            Instruction::Right(x) => self.direction = (self.direction + x) % 360,
            Instruction::Forward(x) => self.forward(*x),
        }
    }

    fn go_with_waypoint(&mut self, ins: &Instruction) {
        self.waypoint.go(ins);
        match ins {
            Instruction::Forward(x) => {
                self.lattitude += x * self.waypoint.lattitude;
                self.longitude += x * self.waypoint.longitude;
            },
            _ => (),  // Only moves waypoint
        }
    }

    fn forward(&mut self, dist: i32) {
        if self.direction < 0 {
            self.direction += 360;
        }
        match self.direction {
            0 => self.lattitude += dist,
            90 => self.longitude += dist,
            180 => self.lattitude -= dist,
            270 => self.longitude -= dist,
            _ => todo!("use trig for {}", self.direction),
        }
    }

    fn goto(&mut self, instructions: &[Instruction]) {
        for ins in instructions {
            self.go(ins)
        }
    }

    fn goto_with_waypoint(&mut self, instructions: &[Instruction]) {
        for ins in instructions {
            self.go_with_waypoint(ins)
        }
    }

    fn dist_travelled(self) -> i32 {
        self.lattitude.abs() + self.longitude.abs()
    }
}

struct Waypoint {
    lattitude: i32, // N-S component relative to ship
    longitude: i32, // E-W component relative to ship
}

impl Waypoint {
    fn new() -> Self {
        Self {
            lattitude: 1,
            longitude: 10,
        }
    }

    fn go(&mut self, ins: &Instruction) {
        match ins {
            Instruction::North(x) => self.lattitude += x,
            Instruction::South(x) => self.lattitude -= x,
            Instruction::East(x) => self.longitude += x,
            Instruction::West(x) => self.longitude -= x,
            Instruction::Left(x) => self.rotate(-x),
            Instruction::Right(x) => self.rotate(*x),
            _ => (), // Only affects ship
        }
    }

    fn rotate(&mut self, amnt: i32) {
        let mut amnt = amnt % 360;
        if amnt < 0 {
            amnt += 360;
        }

        match amnt {
            0 => (),
            90 => {
                let tmp = self.lattitude;
                self.lattitude = -self.longitude;
                self.longitude = tmp;
            }
            180 => {
                self.lattitude = -self.lattitude;
                self.longitude = -self.longitude;
            }
            270 => {
                let tmp = self.lattitude;
                self.lattitude = self.longitude;
                self.longitude = -tmp;
            }
            _ => todo!("use trig / matrix multiplication for {}", amnt),
        }
    }
}

pub fn solve(input: &[String]) {
    let parsed = parse(input);
    let mut ship = Ship::new();
    ship.goto(&parsed);
    println!("Part1: {}", ship.dist_travelled());

    ship = Ship::new();
    ship.goto_with_waypoint(&parsed);
    println!("Part2: {}", ship.dist_travelled());
}

fn parse_line(line: &String) -> Instruction {
    let mut line = line.trim().chars();
    match line.next().unwrap() {
        'N' => Instruction::North(line.as_str().parse().unwrap()),
        'S' => Instruction::South(line.as_str().parse().unwrap()),
        'E' => Instruction::East(line.as_str().parse().unwrap()),
        'W' => Instruction::West(line.as_str().parse().unwrap()),
        'L' => Instruction::Left(line.as_str().parse().unwrap()),
        'R' => Instruction::Right(line.as_str().parse().unwrap()),
        'F' => Instruction::Forward(line.as_str().parse().unwrap()),
        _ => panic!("Bad instruction"),
    }
}

fn parse(input: &[String]) -> Vec<Instruction> {
    input.iter().map(parse_line).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec!["F10\n", "N3\n", "F7\n", "R90\n", "F11\n"];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse(&fixture());
        assert_eq!(parsed.len(), 5);
        assert_eq!(parsed[0], Instruction::Forward(10));
    }

    #[test]
    fn test_go() {
        let parsed = parse(&fixture());
        let mut ship = Ship::new();
        for ins in parsed.iter() {
            ship.go(ins)
        }
        assert_eq!(ship.dist_travelled(), 25);
    }

    #[test]
    fn test_go_with_waypoint() {
        let parsed = parse(&fixture());
        let mut ship = Ship::new();
        for ins in parsed.iter() {
            ship.go_with_waypoint(ins)
        }
        assert_eq!(ship.dist_travelled(), 286);
    }
}
