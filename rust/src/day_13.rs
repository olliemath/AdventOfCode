pub fn solve(input: &[String]) {
    let parsed = parse(input);
    let next = next_bus_time(parsed.0, &parsed.1);
    println!("Part1: {}", next.0 * next.1);
    println!("Part2: {}", competition(&parsed.1));
}

fn parse(input: &[String]) -> (i64, Vec<(i64, i64)>) {
    let earliest = input[0].trim().parse().unwrap();
    let schedule = input[1]
        .trim()
        .split(',')
        .enumerate()
        .map(|s| (s.0 as i64, s.1.parse::<i64>()))
        .filter(|p| p.1.is_ok())
        .map(|p| (-p.0, p.1.unwrap()))
        .collect();

    (earliest, schedule)
}

fn next_bus_time(earliest: i64, schedule: &[(i64, i64)]) -> (i64, i64) {
    schedule
        .iter()
        .map(|(_, id)| ((id * (1 + earliest / id) - earliest), *id))
        .min().unwrap()
}


fn competition(schedule: &[(i64, i64)]) -> i64 {
    // This is basically solving chinese remainder problem
    // We use a seiving approach, but should probably use bezout etc.
    let mut schedule: Vec<(i64, i64)> = schedule.iter().copied().collect();
    schedule.sort_by(|(_, b), (_, c)| c.cmp(b));  // Order bus ids desc

    let mut modulus = schedule[0].1;
    let mut solution = schedule[0].0;

    for (k, b) in schedule[1..].iter() {
        let target = (b + k) % b;
        while solution % b != target {
            solution += modulus;
        }

        modulus *= b;
    }

    solution
}


#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        vec![String::from("939\n"), String::from("7,13,x,x,59,x,31,19\n")]
    }

    #[test]
    fn test_parse() {
        let input = fixture();
        let parsed = parse(&input);

        assert_eq!(parsed.0, 939);
        assert_eq!(parsed.1.len(), 5);
        assert_eq!(parsed.1[0], (0, 7));
        assert_eq!(parsed.1[2], (-4, 59));
    }

    #[test]
    fn test_next_bus_time() {
        let input = fixture();
        let parsed = parse(&input);
        let next = next_bus_time(parsed.0, &parsed.1);

        assert_eq!(next, (5, 59));
    }

    #[test]
    fn test_competition() {
        let input = fixture();
        let parsed = parse(&input);
        let solution = competition(&parsed.1);

        assert_eq!(solution, 1068781);
    }

    #[test]
    fn test_competition_2() {
        let input = vec![(0, 17),(-2, 13),(-3, 19)];
        let solution = competition(&input);
        assert_eq!(solution, 3417);
    }

    fn assert_competition_correct(input: &[String], expected: i64) {
        let parsed = parse(input);
        let actual = competition(&parsed.1);
        assert_eq!(actual, expected);
    }

    #[test]
    fn test_competition_3() {

        let input = vec![String::from("0\n"), String::from("67,7,59,61")];
        let expected = 754018;
        assert_competition_correct(&input, expected);

        let input = vec![String::from("0\n"), String::from("67,x,7,59,61")];
        let expected = 779210;
        assert_competition_correct(&input, expected);

        let input = vec![String::from("0\n"), String::from("67,7,x,59,61")];
        let expected = 1261476;
        assert_competition_correct(&input, expected);

        let input = vec![String::from("0\n"), String::from("1789,37,47,1889")];
        let expected = 1202161486;
        assert_competition_correct(&input, expected);

    }
}
