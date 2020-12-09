use std::collections::HashSet;

#[derive(Clone, Debug, PartialEq)]
enum Instruction {
    Nop,
    Acc,
    Jmp,
}

#[derive(Clone, Debug, PartialEq)]
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


struct History {
    history: Vec<StateMachine>,
    instructions_run: HashSet<usize>,
    revision: i32,
}

impl History {

    fn run_until_repeat_or_terminate(&mut self, code: &[(Instruction, i32)]) -> Result<i32, i32> {
        let mut state = if self.history.is_empty() {
            StateMachine{position: 0, accumulator: 0}
        } else {
            self.history.pop().unwrap()
        };

        let mut result: Result<i32, i32> = Err(-1);
        for _ in 0..code.len() {
            self.instructions_run.insert(state.position);
            self.history.push(state.clone());
            state.step(code);

            if self.instructions_run.contains(&state.position) {
                result = Err(self.history.last().unwrap().accumulator);
                break;
            }
            if state.position >= code.len() {
                result = Ok(state.accumulator);
                self.history.push(state);
                break;
            }
        }

        result
    }

    // Revise the code by walking back over history
    fn revise(&mut self, code: &Vec<(Instruction, i32)>) -> Result<Vec<(Instruction, i32)>, &'static str> {
        let mut seen = 0;
        while !self.history.is_empty() {
            let last = self.history.pop().unwrap();
            self.instructions_run.remove(&last.position);

            if code[last.position].0 == Instruction::Nop || code[last.position].0 == Instruction::Jmp {
                seen += 1;
                if seen == self.revision {
                    let mut cloned = (*code).clone();
                    if cloned[last.position].0 == Instruction::Nop {
                        cloned[last.position] = (Instruction::Jmp, cloned[last.position].1);
                    } else {
                        cloned[last.position] = (Instruction::Nop, cloned[last.position].1);
                    }

                    return Ok(cloned)
                }
            }
        }

        Err("No revisions to make")
    }

    // Iteratively revise the code by walking back over history until we succeed
    fn find_good_path(&mut self, code: &Vec<(Instruction, i32)>) -> i32 {
        let mut new_code = (*code).clone();
        let mut result = self.run_until_repeat_or_terminate(&new_code);
        let orig_history = self.history.clone();

        while result.is_err() {
            self.revision += 1;
            self.history = orig_history.clone();
            new_code = self.revise(code).unwrap();
            // Revising the code also winds back history to the correct starting point
            result = self.run_until_repeat_or_terminate(&new_code);
        }

        result.unwrap()
    }
}


pub fn solve(input: &[String]) {
    let code = parse(input);
    let mut machine = StateMachine{position: 0, accumulator: 0};
    let result = machine.run_until_repeat(&code);
    println!("Value was {} at first repeat", result);

    let mut history = History{history: Vec::new(), instructions_run: HashSet::new(), revision: 0};
    let result = history.find_good_path(&code);
    println!("Corrected run gave {}", result);
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

    fn fixture2() -> Vec<String> {
        let raw = vec![
            "nop +0",
            "acc +1",
            "jmp +4",  // This needs changing to nop
            "acc +3",
            "jmp +6",
            "acc -99",
            "acc +1",
            "jmp +1",
            "jmp -8",
            "jmp -9",
            "acc +6",
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

    #[test]
    fn test_find_good_path() {
        let parsed = parse(&fixture());
        let mut history = History{history: Vec::new(), instructions_run: HashSet::new(), revision: 0};
        let result = history.find_good_path(&parsed);
        assert_eq!(result, 8);
    }

    #[test]
    fn test_find_good_path_2() {
        let parsed = parse(&fixture2());
        let mut history = History{history: Vec::new(), instructions_run: HashSet::new(), revision: 0};
        let result = history.find_good_path(&parsed);
        assert_eq!(result, 10);
    }
}
