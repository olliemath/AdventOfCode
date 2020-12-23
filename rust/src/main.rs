use std::env;
use std::fs;
use std::io::{self, BufRead};

mod day_01;
mod day_05;
mod day_06;
mod day_07;
mod day_08;
mod day_09;
mod day_10;
mod day_11;
mod day_12;
mod day_13;
mod day_14;
mod day_15;
mod day_16;
mod day_17;
mod day_18;
mod day_19;

fn load(filename: String) -> Vec<String> {
    match _load_impl(&filename) {
        Ok(v) => v,
        _ => panic!("Failed to open file {}", filename),
    }
}

fn _load_impl(filename: &str) -> Result<Vec<String>, io::Error> {
    let file = fs::File::open(filename)?;
    let mut result: Vec<String> = Vec::new();
    for line in io::BufReader::new(file).lines() {
        match line {
            Ok(s) => result.push(s),
            Err(e) => return Err(e),
        }
    }

    Ok(result)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    assert_eq!(
        args.len(),
        3,
        "Wrong number of args. Usage:\n    runner day input_dir\n"
    );

    let day = args[1].parse::<i32>().expect("day should be an integer");
    let input = format!("{}/day_{:02}.txt", args[2], day);

    match day {
        1 => day_01::solve(&load(input)),
        5 => day_05::solve(&load(input)),
        6 => day_06::solve(&load(input)),
        7 => day_07::solve(&load(input)),
        8 => day_08::solve(&load(input)),
        9 => day_09::solve(&load(input)),
        10 => day_10::solve(&load(input)),
        11 => day_11::solve(&load(input)),
        12 => day_12::solve(&load(input)),
        13 => day_13::solve(&load(input)),
        14 => day_14::solve(&load(input)),
        15 => day_15::solve(&load(input)),
        16 => day_16::solve(&load(input)),
        17 => day_17::solve(&load(input)),
        18 => day_18::solve(&load(input)),
        19 => day_19::solve(&load(input)),
        _ => panic!("No solution for {} provided", day),
    }
}
