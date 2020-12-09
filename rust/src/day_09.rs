use std::collections::VecDeque;
use std::cmp::Ordering;

pub fn solve(input: &[String]) {
    let parsed = parse(input);
    let target = check_sums(&parsed, 25).unwrap();
    let minmax = add_minmax_summands(&parsed, target);

    println!("Part 1: {}", target);
    println!("Part 2: {}", minmax);
}

fn parse(input: &[String]) -> Vec<i64> {
    input.iter().map(|s| s.trim().parse().unwrap()).collect()
}

fn check_sums(input: &[i64], lookback: usize) -> Result<i64, &'static str> {
    let mut candidates = VecDeque::new();

    for (k, num) in input.iter().enumerate() {
        if k < lookback {
            candidates.push_front(*num)
        } else {
            let mut found = false;

            for first in candidates.iter() {
                if candidates.contains(&(num - first)) {
                    candidates.pop_back();
                    candidates.push_front(*num);
                    found = true;
                    break;
                }
            }

            if !found {
                return Ok(*num);
            }
        }
    }

    Err("All the numbers looked OK")
}

fn find_contiguous_sumands(input: &[i64], target: i64) -> Result<&[i64], &'static str> {
    for j in 0..input.len() - 1 {
        let mut sum_ = input[j];

        for k in j + 1..input.len() {
            sum_ += input[k];
            match sum_.cmp(&target) {
                Ordering::Equal => return Ok(&input[j..=k]),
                Ordering::Greater => break,  // Assumption here is that inputs are all positive
                _ => (),
            }
        }
    }

    Err("Could not find summands")
}

fn add_minmax_summands(input: &[i64], target: i64) -> i64 {
    let summands = find_contiguous_sumands(input, target).unwrap();
    let min_summand = summands.iter().min().unwrap();
    let max_summand = summands.iter().max().unwrap();
    min_summand + max_summand
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![
            "35\n", "20\n", "15\n", "25\n", "47\n", "40\n", "62\n", "55\n", "65\n", "95\n",
            "102\n", "117\n", "150\n", "182\n", "127\n", "219\n", "299\n", "277\n", "309\n",
            "576\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse(&fixture());
        assert_eq!(parsed.len(), 20);
    }

    #[test]
    fn test_check_sums() {
        let parsed = parse(&fixture());
        let found = check_sums(&parsed, 5);
        assert_eq!(found, Ok(127));
    }

    #[test]
    fn test_find_contiguous_summands() {
        let parsed = parse(&fixture());
        let target = 127;
        let expected = vec![15, 25, 47, 40];
        let actual: Vec<i64> = find_contiguous_sumands(&parsed, target)
            .unwrap()
            .iter()
            .copied()
            .collect();
        assert_eq!(actual, expected);
    }

    #[test]
    fn test_add_minmax_summands() {
        let parsed = parse(&fixture());
        let target = 127;
        let result = add_minmax_summands(&parsed, target);
        assert_eq!(result, 62);
    }
}
