pub fn parse(input: &str) -> Vec<u32> {
    input.lines().map(|d| d.parse().unwrap()).collect()
}

pub fn solve_part1(input: &[u32]) -> u32 {
    input
        .windows(2)
        .map(|w| if w[0] < w[1] { 1 } else { 0 })
        .sum()
}

pub fn solve_part2(input: &[u32]) -> u32 {
    input
        .windows(4)
        .map(|w| if w[0] < w[3] { 1 } else { 0 })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(
            solve_part1(&parse("199\n200\n208\n210\n200\n207\n240\n269\n260\n263")),
            7
        )
    }

    #[test]
    fn test_part2() {
        assert_eq!(
            solve_part2(&parse("199\n200\n208\n210\n200\n207\n240\n269\n260\n263")),
            5
        )
    }
}
