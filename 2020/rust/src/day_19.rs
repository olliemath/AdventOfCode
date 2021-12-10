use std::collections::HashMap;

pub fn solve(input: &[String]) {
    println!("Part1: {}", part1(input));
    println!("Part2: {}", part2(input));
}

#[derive(Debug, Clone, PartialEq)]
enum Rule {
    And(Vec<Rule>),
    Match(char),
    Or(Vec<Rule>),
    Ref(usize),
}

#[derive(Debug, Clone, PartialEq)]
struct Message {
    text: Box<Vec<char>>,
    offset: usize,
}

impl Message {
    fn conforms_to_rule(&self, r: &Rule, lookup: &HashMap<usize, Rule>) -> bool {
        self._apply_rule(r, lookup)
            .iter()
            .any(|m| m.text.len() == m.offset)
    }

    fn _apply_rule(&self, r: &Rule, lookup: &HashMap<usize, Rule>) -> Vec<Message> {
        if self.offset == self.text.len() {
            vec![]
        } else {
            match r {
                Rule::And(sr) => self._apply_and(sr, lookup),
                Rule::Match(c) => self._apply_match(*c),
                Rule::Or(os) => self._apply_or(os, lookup),
                Rule::Ref(i) => self._apply_rule(lookup.get(i).unwrap(), lookup),
            }
        }
    }

    fn _apply_match(&self, c: char) -> Vec<Message> {
        if self.text[self.offset] == c {
            vec![Message {
                text: self.text.clone(),
                offset: self.offset + 1,
            }]
        } else {
            vec![]
        }
    }

    fn _apply_and(&self, and: &[Rule], lookup: &HashMap<usize, Rule>) -> Vec<Message> {
        let mut results: Vec<Message> = vec![self.clone()];

        for subrule in and {
            results = results
                .iter()
                .map(|m| m._apply_rule(subrule, lookup))
                .flatten()
                .collect();
        }

        results
    }

    fn _apply_or(&self, possibilities: &[Rule], lookup: &HashMap<usize, Rule>) -> Vec<Message> {
        possibilities
            .iter()
            .map(|p| self._apply_rule(p, lookup))
            .flatten()
            .collect()
    }
}

fn parse_rhs(rhs: &str) -> Rule {
    if rhs.contains('|') {
        Rule::Or(rhs.split(" | ").map(parse_rhs).collect())
    } else if rhs.starts_with('"') {
        Rule::Match(rhs.chars().skip(1).next().unwrap())
    } else {
        Rule::And(
            rhs.split(' ')
                .map(|s| Rule::Ref(s.parse().unwrap()))
                .collect(),
        )
    }
}

fn parse_line(line: &String) -> (usize, Rule) {
    let mut split = line.trim().split(": ");
    let idx = split.next().unwrap().parse().unwrap();
    let rhs = parse_rhs(split.next().unwrap());
    (idx, rhs)
}

fn parse_rules(input: &[String]) -> HashMap<usize, Rule> {
    input.iter().map(parse_line).collect()
}

fn parse_messages(input: &[String]) -> Vec<Message> {
    input
        .iter()
        .map(|s| Message {
            text: Box::new(s.trim().chars().collect()),
            offset: 0,
        })
        .collect()
}

fn parse(input: &[String]) -> (HashMap<usize, Rule>, Vec<Message>) {
    let mut split = input.split(|l| l.trim() == "");
    let rule = parse_rules(split.next().unwrap());
    let messages = parse_messages(split.next().unwrap());
    (rule, messages)
}

fn part1(input: &[String]) -> usize {
    let (rules, messages) = parse(input);
    let root = rules.get(&0).unwrap();
    messages
        .iter()
        .filter(|m| m.conforms_to_rule(&root, &rules))
        .count()
}

fn part2(input: &[String]) -> usize {
    let (mut rules, messages) = parse(input);
    // Patch rules 8 and 11
    rules.insert(
        8,
        Rule::Or(vec![
            Rule::Ref(42),
            Rule::And(vec![Rule::Ref(42), Rule::Ref(8)]),
        ]),
    );
    rules.insert(
        11,
        Rule::Or(vec![
            Rule::And(vec![Rule::Ref(42), Rule::Ref(31)]),
            Rule::And(vec![Rule::Ref(42), Rule::Ref(11), Rule::Ref(31)]),
        ]),
    );

    let root = rules.get(&0).unwrap();
    messages
        .iter()
        .filter(|m| m.conforms_to_rule(&root, &rules))
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn from_raw(raw: &[&str]) -> Vec<String> {
        raw.iter().map(|s| String::from(*s)).collect()
    }

    fn fixture1() -> Vec<String> {
        let raw = vec!["0: 1 2\n", "1: \"a\"\n", "2: 1 3 | 3 1\n", "3: \"b\"\n"];
        from_raw(&raw)
    }

    fn fixture2() -> Vec<String> {
        let raw = vec![
            "0: 4 1 5\n",
            "1: 2 3 | 3 2\n",
            "2: 4 4 | 5 5\n",
            "3: 4 5 | 5 4\n",
            "4: \"a\"\n",
            "5: \"b\"\n",
            "\n",
            "ababbb\n",
            "bababa\n",
            "abbbab\n",
            "aaabbb\n",
            "aaaabbb\n",
        ];
        from_raw(&raw)
    }

    fn fixture3() -> Vec<String> {
        let raw = vec![
            "42: 9 14 | 10 1\n",
            "9: 14 27 | 1 26\n",
            "10: 23 14 | 28 1\n",
            "1: \"a\"\n",
            "11: 42 31\n",
            "5: 1 14 | 15 1\n",
            "19: 14 1 | 14 14\n",
            "12: 24 14 | 19 1\n",
            "16: 15 1 | 14 14\n",
            "31: 14 17 | 1 13\n",
            "6: 14 14 | 1 14\n",
            "2: 1 24 | 14 4\n",
            "0: 8 11\n",
            "13: 14 3 | 1 12\n",
            "15: 1 | 14\n",
            "17: 14 2 | 1 7\n",
            "23: 25 1 | 22 14\n",
            "28: 16 1\n",
            "4: 1 1\n",
            "20: 14 14 | 1 15\n",
            "3: 5 14 | 16 1\n",
            "27: 1 6 | 14 18\n",
            "14: \"b\"\n",
            "21: 14 1 | 1 14\n",
            "25: 1 1 | 1 14\n",
            "22: 14 14\n",
            "8: 42\n",
            "26: 14 22 | 1 20\n",
            "18: 15 15\n",
            "7: 14 5 | 1 21\n",
            "24: 14 1\n",
            "\n",
            "abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa\n",
            "bbabbbbaabaabba\n",
            "babbbbaabbbbbabbbbbbaabaaabaaa\n",
            "aaabbbbbbaaaabaababaabababbabaaabbababababaaa\n",
            "bbbbbbbaaaabbbbaaabbabaaa\n",
            "bbbababbbbaaaaaaaabbababaaababaabab\n",
            "ababaaaaaabaaab\n",
            "ababaaaaabbbaba\n",
            "baabbaaaabbaaaababbaababb\n",
            "abbbbabbbbaaaababbbbbbaaaababb\n",
            "aaaaabbaabaaaaababaa\n",
            "aaaabbaaaabbaaa\n",
            "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa\n",
            "babaaabbbaaabaababbaabababaaab\n",
            "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba\n",
        ];
        from_raw(&raw)
    }

    #[test]
    fn test_apply_rule() {
        let parsed = parse_rules(&fixture1());
        let message = Message {
            text: Box::new(vec!['a', 'a', 'b']),
            offset: 0,
        };

        let result = message._apply_rule(&parsed.get(&0).unwrap(), &parsed);
        assert_eq!(result.len(), 1);
        assert_eq!(result[0].offset, 3);
    }

    #[test]
    fn test_conforms_to_rule() {
        let parsed = parse_rules(&fixture1());
        let messages = parse_messages(&vec![
            String::from("aab"),
            String::from("aba"),
            String::from("a"),
            String::from("aaba"),
            String::from("abc"),
        ]);

        let result: Vec<bool> = messages
            .iter()
            .map(|m| m.conforms_to_rule(parsed.get(&0).unwrap(), &parsed))
            .collect::<Vec<bool>>();

        assert_eq!(result, vec![true, true, false, false, false]);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&fixture2()), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part1(&fixture3()), 3);
        assert_eq!(part2(&fixture3()), 12);
    }
}
