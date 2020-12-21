use std::collections::{HashMap, HashSet};

#[derive(Debug, PartialEq)]
struct NumberSpec {
    name: String,
    range1: (i64, i64),
    range2: (i64, i64),
}

struct TicketSpec {
    ticket: Vec<i64>,
    nearby_tickets: Vec<Vec<i64>>,
    spec: Vec<NumberSpec>,
}

impl TicketSpec {
    fn conforms_to_spec(&self, spec: &NumberSpec, num: &i64) -> bool {
        (spec.range1.0 <= *num && *num <= spec.range1.1)
            || (spec.range2.0 <= *num && *num <= spec.range2.1)
    }

    fn valid_number(&self, num: &i64) -> bool {
        self.spec.iter().any(|s| self.conforms_to_spec(s, num))
    }

    fn invalid_numbers(&self) -> Vec<i64> {
        self.nearby_tickets
            .iter()
            .flatten()
            .filter(|n| !self.valid_number(n))
            .copied()
            .collect()
    }

    // Get the valid fields for the nearby tickets
    fn valid_fields(&self) -> Vec<Vec<i64>> {
        let mut fields = Vec::new();
        for _ in 0..self.ticket.len() {
            fields.push(Vec::new());
        }

        for ticket in self.nearby_tickets.iter() {
            if !ticket.iter().all(|n| self.valid_number(n)) {
                continue;
            }

            for (k, f) in ticket.iter().enumerate() {
                fields[k].push(*f);
            }
        }

        fields
    }

    fn get_field_name(&self, field_values: &Vec<i64>) -> HashSet<String> {
        let mut possible = HashMap::new();
        for number_spec in self.spec.iter() {
            possible.insert(number_spec.name.clone(), number_spec);
        }

        for value in field_values.iter() {
            let mut to_remove = Vec::new();
            for (k, s) in possible.iter() {
                if !self.conforms_to_spec(s, value) {
                    to_remove.push(k.clone());
                }
            }

            for k in to_remove {
                possible.remove(&k);
            }
        }

        possible.keys().cloned().collect()
    }

    fn get_field_names(&self) -> Vec<String> {
        let mut names = Vec::new();
        let mut allocated = 0;
        for _ in 0..self.ticket.len() {
            names.push(String::from(""));
        }

        let mut all_choices: Vec<HashSet<String>> = self.valid_fields().iter().map(|f| self.get_field_name(f)).collect();
        while allocated < self.ticket.len() {
            let mut to_remove = Vec::new();
            for (k, choices) in all_choices.iter().enumerate() {
                if choices.len() == 0 {
                    continue
                } else if choices.len() == 1 {
                    allocated += 1;
                    let name = choices.iter().next().unwrap();
                    names[k] = name.clone();
                    to_remove.push(name.clone());
                }
            }

            for name in to_remove {
                for choices in all_choices.iter_mut() {
                    choices.remove(&name);
                }
            }

        }

        names
    }

    fn departure_values(&self) -> Vec<i64> {
        self.get_field_names()
            .iter()
            .zip(self.ticket.iter())
            .filter(|(f, _)| f.starts_with("departure"))
            .map(|(_, v)| *v)
            .collect()
    }
}

pub fn solve(input: &[String]) {
    let ticket_spec = parse(input);
    let invalid = ticket_spec.invalid_numbers();
    println!("Part 1: {}", invalid.iter().sum::<i64>());

    let departure_values = ticket_spec.departure_values();
    println!("{:?}", departure_values);
    println!("Part 2: {}", departure_values.iter().product::<i64>());
}

fn parse_hilo(s: &str) -> (i64, i64) {
    let mut splat = s.split('-');
    let min = splat.next().unwrap().parse().unwrap();
    let max = splat.next().unwrap().parse().unwrap();
    (min, max)
}

fn parse_number_spec(line: &String) -> NumberSpec {
    let mut split = line.split(": ");
    let name = String::from(split.next().unwrap());
    let mut splat = split.next().unwrap().trim().split(" or ").map(parse_hilo);
    let range1 = splat.next().unwrap();
    let range2 = splat.next().unwrap();
    NumberSpec {
        name,
        range1,
        range2,
    }
}

fn parse(input: &[String]) -> TicketSpec {
    let mut chunks = input.split(|line| line.trim() == "");
    let spec = chunks
        .next()
        .unwrap()
        .iter()
        .map(parse_number_spec)
        .collect();
    let ticket = chunks
        .next()
        .unwrap()
        .last()
        .unwrap()
        .trim()
        .split(',')
        .map(|s| s.parse().unwrap())
        .collect();
    let nearby_tickets = chunks
        .next()
        .unwrap()
        .iter()
        .skip(1)
        .map(|line| line.trim().split(",").map(|s| s.parse().unwrap()).collect())
        .collect();

    TicketSpec {
        ticket: ticket,
        nearby_tickets: nearby_tickets,
        spec: spec,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![
            "class: 1-3 or 5-7\n",
            "row: 6-11 or 33-44\n",
            "seat: 13-40 or 45-50\n",
            "\n",
            "your ticket:\n",
            "7,1,14\n",
            "\n",
            "nearby tickets:\n",
            "7,3,47\n",
            "40,4,50\n",
            "55,2,20\n",
            "38,6,12\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    fn fixture2() -> Vec<String> {
        let raw = vec![
            "class: 0-1 or 4-19\n",
            "row: 0-5 or 8-19\n",
            "seat: 0-13 or 16-19\n",
            "\n",
            "your ticket:\n",
            "11,12,13\n",
            "\n",
            "nearby tickets:\n",
            "3,9,18\n",
            "15,1,5\n",
            "5,14,9\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse(&fixture());
        assert_eq!(parsed.ticket, vec![7, 1, 14]);
        assert_eq!(parsed.nearby_tickets.len(), 4);
        assert_eq!(parsed.spec.len(), 3);
        assert_eq!(
            parsed.spec[0],
            NumberSpec {
                name: String::from("class"),
                range1: (1, 3),
                range2: (5, 7)
            }
        );
    }

    #[test]
    fn test_invalid_numbers() {
        let parsed = parse(&fixture());
        let invalid = parsed.invalid_numbers();
        assert_eq!(invalid, vec![4, 55, 12]);
    }

    #[test]
    fn test_get_field_names() {
        let parsed = parse(&fixture2());
        let field_names = parsed.get_field_names();
        let expected = vec![
            String::from("row"),
            String::from("class"),
            String::from("seat"),
        ];
        assert_eq!(field_names, expected);
    }
}
