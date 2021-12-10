use std::collections::HashSet;

pub fn solve(input: &[String]) {
    println!("Part1: {}", total_yeses_any(&parse(input)));
    println!("Part2: {}", total_yeses_all(&parse(input)));
}

pub fn parse(input: &[String]) -> Vec<Vec<String>> {
    let mut parsed = Vec::new();
    let mut group: Vec<String> = Vec::new();

    for line in input.iter() {
        let stripped = line.trim();
        if stripped != "" {
            group.push(String::from(stripped));
        } else if !group.is_empty() {
            parsed.push(group);
            group = Vec::new();
        }
    }

    // Possible final group
    if !group.is_empty() {
        parsed.push(group);
    }

    parsed
}

fn num_of_yeses(input: &[String]) -> usize {
    let mut yeses = HashSet::new();
    for row in input {
        for b in row.as_bytes().iter() {
            yeses.insert(b);
        }
    }
    yeses.len()
}

fn num_common_yeses(input: &[String]) -> usize {
    let mut yeses: HashSet<u8> = b"abcdefghijklmnopqrstuvwxyz"
        .iter()
        .cloned()
        .collect();

    for row in input {
        let lookup: HashSet<u8> = row.as_bytes().iter().copied().collect();
        yeses = yeses.intersection(&lookup).cloned().collect();
    }

    yeses.len()
}

fn total_yeses_any(input: &[Vec<String>]) -> usize {
    input.iter().map(|v| num_of_yeses(v)).sum()
}

fn total_yeses_all(input: &[Vec<String>]) -> usize {
    input.iter().map(|v| num_common_yeses(v)).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn _test_data() -> Vec<String> {
        let raw = vec![
            "abc\n", "\n", "a\n", "b\n", "c\n", "\n", "ab\n", "ac\n", "\n", "a\n", "a\n", "a\n",
            "a\n", "\n", "b\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let groups = parse(&_test_data());
        let expected_lens = vec![1, 3, 2, 4, 1];
        let actual_lens: Vec<usize> = groups.iter().map(|v| v.len()).collect();
        assert_eq!(expected_lens, actual_lens);
    }

    #[test]
    fn test_total_yeses() {
        let groups = parse(&_test_data());
        let yeses = total_yeses_any(&groups);
        assert_eq!(11, yeses);
    }

    #[test]
    fn test_total_yeses_all() {
        let groups = parse(&_test_data());
        let yeses = total_yeses_all(&groups);
        assert_eq!(6, yeses);
    }
}
