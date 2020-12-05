use std::env;
use std::fs;
use std::io::{self, BufRead};

mod day_01;
mod day_05;


fn load(filename: String) -> Vec<String> {
    match _load_impl(&filename) {
        Ok(v) => v,
        Err(_) => panic!("Failed to open file {}", filename),
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
    assert_eq!(args.len(), 3, "Wrong number of args. Usage:\n    runner day input_dir\n");

    let day = args[1].parse::<i32>().expect("day should be an integer");
    let input = format!("{}/day_{:02}.txt", args[2], day);

    match day {
        1 => day_01::solve(&load(input)),
        5 => day_05::solve(&load(input)),
        _ => panic!("No solution for {} provided", day),
    }
}