pub fn parse(input: &str) -> Vec<usize> {
    input
        .strip_suffix("\n")
        .unwrap()
        .split(",")
        .map(|c| c.parse().unwrap())
        .collect()
}

pub fn solve(input: &[usize], steps: usize) -> u64 {
    let mut fish: [u64; 9] = [0; 9];

    for i in input.iter() {
        fish[*i] += 1;
    }

    for _ in 0..steps {
        let zfish = fish[0];
        for i in 1..9 {
            fish[i - 1] = fish[i];
        }
        fish[8] = zfish;
        fish[6] += zfish;
    }

    fish.iter().sum()
}

pub fn solve_part1(input: &[usize]) -> u64 {
    solve(input, 80)
}

pub fn solve_part2(input: &[usize]) -> u64 {
    solve(input, 256)
}
