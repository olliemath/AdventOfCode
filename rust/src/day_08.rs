use std::collections::HashSet;

#[derive(Debug, PartialEq)]
enum Instruction {
    Nop,
    Acc,
    Jmp,
}

#[derive(Clone, PartialEq)]
struct StateMachine {
    position: usize,
    accumulator: i32,
}

impl StateMachine {

    fn run_until_repeat(&mut self, code: &[(Instruction, i32)]) -> i32 {
        let mut instructions_run = HashSet::new();
        let mut prev_value = 0;

        while !instructions_run.contains(&self.position) {
            instructions_run.insert(self.position);
            prev_value = self.accumulator;
            self.step(code);
        }

        prev_value
    }

    fn step(&mut self, code: &[(Instruction, i32)]) {
        let current = &code[self.position];
        match current.0 {
            Instruction::Nop => self.nop(),
            Instruction::Acc => self.acc(current.1),
            Instruction::Jmp => self.jmp(current.1),
        };
    }

    #[inline]
    fn nop(&mut self) {
        self.position += 1;
    }

    #[inline]
    fn acc(&mut self, amnt: i32) {
        self.position += 1;
        self.accumulator += amnt;
    }

    #[inline]
    fn jmp(&mut self, size: i32) {
        self.position = (self.position as i32 + size) as usize;
    }
}


pub fn solve(input: &[String]) {
    let code = parse(input);
    let mut machine = StateMachine{position: 0, accumulator: 0};
    let result = machine.run_until_repeat(&code);
    println!("Value was {} at first repeat", result);
}

fn parse(input: &[String]) -> Vec<(Instruction, i32)> {
    let mut result = Vec::new();
    for line in input {
        let mut pieces = line.trim().split(' ');
        let ins = match pieces.next().unwrap() {
            "nop" => Instruction::Nop,
            "acc" => Instruction::Acc,
            "jmp" => Instruction::Jmp,
            _ => panic!("Bad instruction"),
        };
        let num = pieces.next().unwrap().parse::<i32>().unwrap();
        result.push((ins, num))
    }

    result
}


#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![
            "nop +0\n",
            "acc +1\n",
            "jmp +4\n",
            "acc +3\n",
            "jmp -3\n",
            "acc -99\n",
            "acc +1\n",
            "jmp -4\n",
            "acc +6\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse(&fixture());
        assert_eq!(parsed.len(), 9);
        assert_eq!(parsed[0], (Instruction::Nop, 0));
        assert_eq!(parsed[5], (Instruction::Acc, -99));
    }

    #[test]
    fn test_run_until_repeat() {
        let parsed = parse(&fixture());
        let mut machine = StateMachine{position: 0, accumulator: 0};

        let result = machine.run_until_repeat(&parsed);
        assert_eq!(result, 5);
    }
}
