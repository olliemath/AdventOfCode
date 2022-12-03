mod day1;
mod day2;
mod day6;
mod util;

fn main() {
    let data = util::input_data("01");
    println!("Day 01");
    println!("  {}", day1::solve_part1(&day1::parse(&data)));
    println!("  {}", day1::solve_part2(&day1::parse(&data)));

    let data = util::input_data("02");
    println!("Day 02");
    println!("  {}", day2::solve_part1(&day2::parse(&data)));
    println!("  {}", day2::solve_part2(&day2::parse(&data)));

    let data = util::input_data("06");
    println!("Day 06");
    println!("  {}", day6::solve_part1(&day6::parse(&data)));
    println!("  {}", day6::solve_part2(&day6::parse(&data)));
}
