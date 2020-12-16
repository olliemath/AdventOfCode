use std::collections::HashMap;

pub fn solve(input: &[String]) {
    let parsed = parse(input);
    let (_, part1) = game(&parsed, 2020);
    println!("Part 1: {}", part1);

    let (_, part2) = game(&parsed, 30000000);
    println!("Part 2: {}", part2);
}

fn parse(input: &[String]) -> Vec<usize> {
    let line = &input[0];
    line.trim().split(',').map(|s| s.parse().unwrap()).collect()
}

fn game(input: &[usize], turns: usize) -> (HashMap<usize, usize>, usize) {
    // We record the numbers and the turn they were spoken
    let mut seen = HashMap::new();
    let mut last_value = input[0];

    for (k, x) in input[1..].iter().enumerate() {
        seen.insert(last_value, k);
        last_value = *x;
    }

    for k in input.len()-1..turns-1 {
        if !seen.contains_key(&last_value) {
            seen.insert(last_value, k);
            last_value = 0;
        } else {
            let next_value = (k - seen.get(&last_value).unwrap()) as usize;
            seen.insert(last_value, k);
            last_value = next_value;
        }
    }

    (seen, last_value)
}


#[cfg(test)]
mod tests {
    use super::*;
    use std::iter::FromIterator;

    fn fixture() -> Vec<String> {
        vec![String::from("0,3,6\n")]
    }

    #[test]
    fn test_parse() {
        assert_eq!(parse(&fixture()), vec![0, 3, 6]);
    }

    #[test]
    fn test_game() {
        let parsed = parse(&fixture());
        let (seen, last) = game(&parsed, 4);
        let expected = vec![(0, 0), (3, 1), (6, 2)];
        assert_eq!(seen, HashMap::from_iter(expected));
        assert_eq!(last, 0);

        let (_, last) = game(&parsed, 5);
        assert_eq!(last, 3);

        let (_, last) = game(&parsed, 6);
        println!("{:?}", seen);
        assert_eq!(last, 3);

        let (_, last) = game(&parsed, 7);
        assert_eq!(last, 1);

        let (_, last) = game(&parsed, 10);
        assert_eq!(last, 0);

        let (_, last) = game(&parsed, 2020);
        assert_eq!(last, 436);
    }

    #[test]
    fn test_games() {

        let input = vec![1, 3, 2];
        let (_, last) = game(&input, 2020);
        assert_eq!(last, 1);

        let input = vec![2, 1, 3];
        let (_, last) = game(&input, 2020);
        assert_eq!(last, 10);

        let input = vec![1, 2, 3];
        let (_, last) = game(&input, 2020);
        assert_eq!(last, 27);

        let input = vec![2, 3, 1];
        let (_, last) = game(&input, 2020);
        assert_eq!(last, 78);

        let input = vec![3, 2, 1];
        let (_, last) = game(&input, 2020);
        assert_eq!(last, 438);

        let input = vec![3, 1, 2];
        let (_, last) = game(&input, 2020);
        assert_eq!(last, 1836);
    }

    #[test]
    fn test_long_game() {
        let input = vec![0,3,6];
        let (_, last) = game(&input, 30000000);
        assert_eq!(last, 175594);
    }

    #[test]
    fn test_long_games() {
        let input = vec![1,3,2];
        let (_, last) = game(&input, 30000000);
        assert_eq!(last, 2578);

        // The following pass, they just take ages
        // let input = vec![2,1,3];
        // let (_, last) = game(&input, 30000000);
        // assert_eq!(last, 3544142);

        // let input = vec![1,2,3];
        // let (_, last) = game(&input, 30000000);
        // assert_eq!(last, 261214);

        // let input = vec![2,3,1];
        // let (_, last) = game(&input, 30000000);
        // assert_eq!(last, 6895259);

        //let input = vec![3,2,1];
        //let (_, last) = game(&input, 30000000);
        //assert_eq!(last, 18);

        // let input = vec![3,1,2];
        // let (_, last) = game(&input, 30000000);
        // assert_eq!(last, 362);
    }
}
