use std::collections::HashMap;

pub fn solve(input: &[String]) {
    let mut program = parse(input);
    program.run();
    println!("Part1: {}", program.sum());

    let mut program = parse(input);
    program.run_v2();
    println!("Part2: {}", program.sum());
}

#[derive(Debug, PartialEq)]
enum Instruction {
    Mask(u64, u64),
    Mem(u64, u64),
}

#[derive(Debug, PartialEq)]
enum InstructionV2 {
    Mask(u64, u64, Vec<u64>),
    Mem(u64, u64),
}


struct Program {
    instructions_v1: Vec<Instruction>,
    instructions_v2: Vec<InstructionV2>,
    memory: HashMap<u64, u64>,
}

impl Program {
    fn run(&mut self) {
        let mut bitmask = None;

        for ins in self.instructions_v1.iter() {
            match ins {
                Instruction::Mask(a, o) => bitmask = Some((*a, *o)),
                Instruction::Mem(l, v) => {
                    match bitmask {
                        Some(b) => self.memory.insert(*l, self.apply_bitmask(b, *v)),
                        None => self.memory.insert(*l, *v),
                    };
                },
            }
        }
    }

    fn run_v2(&mut self) {
        let mut bitmask = None;

        for ins in self.instructions_v2.iter() {
            match ins {
                InstructionV2::Mask(a, o, p) => bitmask = Some((*a, *o, p)),
                InstructionV2::Mem(l, v) => {
                    match bitmask {
                        Some(b) => {
                            for new_l in self.apply_v2_bitmask(b, *l) {
                                self.memory.insert(new_l, *v);
                            }
                        },
                        None => {self.memory.insert(*l, *v);},
                    };
                },
            }
        }
    }

    fn apply_bitmask(&self, bitmask: (u64, u64), value: u64) -> u64 {
        let (and, or) = bitmask;
        (value & and) | or
    }

    fn apply_v2_bitmask(&self, bitmask: (u64, u64, &Vec<u64>), loc: u64) -> Vec<u64> {
        let mut result = Vec::new();
        let (and, or, floating) = bitmask;
        for modifier in floating.iter() {
            result.push((loc & and) | or | modifier);
        }

        result
    }

    fn sum(&self) -> u64 {
        self.memory.values().sum()
    }
}

fn parse_bitmask(bitmask: &str) -> (u64, u64) {
    // Create integers to AND + OR with
    let mut and = 0;
    let mut or = 0;

    for (n, c) in bitmask.chars().enumerate() {
        let exponent = bitmask.len() - 1 - n;
        match c {
            '0' => {}
            '1' => {
                or += 2u64.pow(exponent as u32);
                and += 2u64.pow(exponent as u32);
            }
            _ => {
                and += 2u64.pow(exponent as u32);
            }
        }
    }

    (and, or)
}

fn parse_bitmask_v2(bitmask: &str) -> (u64, u64, Vec<u64>) {
    // Parse for an and, an or, and all possibilites
    // The idea is we map to (addr & and) | or | pos
    let mut and = 0;
    let mut or = 0;
    let mut possibilites = vec![0];

    for (n, c) in bitmask.chars().enumerate() {
        let exponent = bitmask.len() - 1 - n;
        let bit = 2u64.pow(exponent as u32);
        match c {
            '0' => {
                // Address unchanged
                and += bit;
            }
            '1' => {
                // Flip to a 1
                or += bit;
                and += bit;
            }
            _ => {
                // Floating
                if possibilites.len() < 4092 {
                    // Arbitrary limit, just to ensure we don't run forever
                    for k in 0..possibilites.len() {
                        possibilites.push(possibilites[k] + bit);
                    }
                }
            }
        }
    }

    (and, or, possibilites)
}

fn parse_instruction(line: &String) -> Instruction {
    if &line[..4] == "mask" {
        let raw = line.trim().trim_start_matches("mask = ");
        let (and, or) = parse_bitmask(raw);
        Instruction::Mask(and, or)
    } else {
        let mut pieces = line.trim().split(" = ");
        let mem = pieces
            .next()
            .unwrap()
            .trim_start_matches("mem[")
            .trim_end_matches(']')
            .parse()
            .unwrap();
        let val = pieces.next().unwrap().parse().unwrap();
        Instruction::Mem(mem, val)
    }
}

fn parse_instruction_v2(line: &String) -> InstructionV2 {
    if &line[..4] == "mask" {
        let raw = line.trim().trim_start_matches("mask = ");
        let (and, or, floating) = parse_bitmask_v2(raw);
        InstructionV2::Mask(and, or, floating)
    } else {
        let mut pieces = line.trim().split(" = ");
        let mem = pieces
            .next()
            .unwrap()
            .trim_start_matches("mem[")
            .trim_end_matches(']')
            .parse()
            .unwrap();
        let val = pieces.next().unwrap().parse().unwrap();
        InstructionV2::Mem(mem, val)
    }
}



fn parse(input: &[String]) -> Program {
    Program {
        instructions_v1: input.iter().map(parse_instruction).collect(),
        instructions_v2: input.iter().map(parse_instruction_v2).collect(),
        memory: HashMap::new(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        vec![
            String::from("mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X\n"),
            String::from("mem[8] = 11\n"),
            String::from("mem[7] = 101\n"),
            String::from("mem[8] = 0\n"),
        ]
    }

    fn fixture2() -> Vec<String> {
        vec![
            String::from("mask = 000000000000000000000000000000X1001X\n"),
            String::from("mem[42] = 100\n"),
            String::from("mask = 00000000000000000000000000000000X0XX\n"),
            String::from("mem[26] = 1\n"),
        ]
    }

    #[test]
    fn test_parse() {
        let program = parse(&fixture());
        assert_eq!(program.instructions_v1.len(), 4);
        assert_eq!(program.instructions_v1[1], Instruction::Mem(8, 11));
    }

    #[test]
    fn test_parse_v2() {
        let program = parse(&fixture2());
        assert_eq!(program.instructions_v2.len(), 4);

        let (and, or, floating) = match &program.instructions_v2[0] {
            InstructionV2::Mask(a, o, f) => (a, o, f),
            _ => panic!("Expected mask"),
        };
        assert_eq!(*and & 1, 0);
        assert_eq!(*and & 2, 2);
        assert_eq!(*and & 4, 4);
        assert_eq!(*and & 8, 8);
        assert_eq!(*and & 16, 16);
        assert_eq!(*and & 32, 0);
        assert_eq!(*and & 64, 64);
        assert_eq!(*or, 2 + 16);
        assert_eq!(floating.len(), 4);
    }

    #[test]
    fn test_apply_bitmask() {
        let program = parse(&fixture());
        let mask = match program.instructions_v1[0] {
            Instruction::Mask(x, y) => (x, y),
            _ => panic!("Expected a mask"),
        };
        assert_eq!(program.apply_bitmask(mask, 11), 73);
        assert_eq!(program.apply_bitmask(mask, 101), 101);
        assert_eq!(program.apply_bitmask(mask, 0), 64);
    }

    #[test]
    fn test_run() {
        let mut program = parse(&fixture());
        program.run();
        assert_eq!(program.sum(), 165);
    }

    #[test]
    fn test_run_v2() {
        let mut program = parse(&fixture2());
        program.run_v2();
        assert_eq!(program.sum(), 208);
    }
}
