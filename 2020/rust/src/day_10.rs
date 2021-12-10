pub fn solve(input: &[String]) {
    let parsed = parse(input);
    let deltas = get_deltas(&parsed);
    println!("Part 1: {}", deltas.0 * deltas.1);
    let combos = get_combos(&parsed);
    println!("Part 2: {}", combos);
}

fn parse(input: &[String]) -> Vec<i64> {
    let mut parsed: Vec<i64> = input.iter().map(|s| s.trim().parse().unwrap()).collect();
    parsed.sort();
    parsed
}

fn device_rating(input: &[i64]) -> i64 {
    *input.iter().max().unwrap() + 3
}

fn get_deltas(input: &[i64]) -> (u32, u32) {
    let mut last_seen = 0;
    let mut one_deltas = 0;
    let mut tri_deltas = 0;

    for adapter in input.iter() {
        let delta = adapter - last_seen;
        if delta == 1 {
            one_deltas += 1;
        } else if delta == 3 {
            tri_deltas += 1;
        }
        last_seen = *adapter;
    }

    if device_rating(input) - last_seen == 1 {
        one_deltas += 1;
    } else if device_rating(input) - last_seen == 3 {
        tri_deltas += 1;
    }

    (one_deltas, tri_deltas)
}

fn tribonacci(len: &i64) -> i64 {
    if *len <= 0 {
        return 0;
    }

    let mut numbers = Vec::new();
    let len = *len as usize;

    for k in 0..len {
        if k <= 1 {
            numbers.push(1);
        } else if k == 2{
            numbers.push(2);
        } else {
            numbers.push(numbers[k-1] + numbers[k-2] + numbers[k-3]);
        }
    }

    *numbers.last().unwrap_or(&0)
}


fn get_combos(sorted_input: &[i64]) -> i64 {

    let mut chunk_sizes = Vec::new();
    let mut current_chunk_len = 1;

    for (k, item) in sorted_input.iter().enumerate() {
        if k == 0 {
            if *item == 3 {
                chunk_sizes.push(current_chunk_len);
                current_chunk_len = 0;
            }
        } else {
            if *item - sorted_input[k-1] == 3 {
                chunk_sizes.push(current_chunk_len);
                current_chunk_len = 0;
            }
        }
        current_chunk_len += 1;
    }

    chunk_sizes.push(current_chunk_len);
    chunk_sizes.iter().map(tribonacci).product()
}



#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![
            "16\n", "10\n", "15\n", "5\n", "1\n", "11\n", "7\n", "19\n", "6\n", "12\n", "4\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse(&fixture());
        assert_eq!(parsed.len(), 11);
    }

    #[test]
    fn test_device_rating() {
        let parsed = parse(&fixture());
        assert_eq!(device_rating(&parsed), 22);
    }

    #[test]
    fn test_get_deltas() {
        let parsed = parse(&fixture());
        assert_eq!(get_deltas(&parsed), (7, 5));
    }

    #[test]
    fn test_get_deltas_big() {
        let mut input = vec![
            28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
            8, 17, 7, 9, 4, 2, 34, 10, 3,
        ];
        input.sort();
        assert_eq!(get_deltas(&input), (22, 10));
    }

    #[test]
    fn test_get_combos() {
        let parsed = parse(&fixture());
        assert_eq!(get_combos(&parsed), 8);

        let mut big_input = vec![
            28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
            8, 17, 7, 9, 4, 2, 34, 10, 3,
        ];
        big_input.sort();
        assert_eq!(get_combos(&big_input), 19208);
    }
}
