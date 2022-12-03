use std::fs::read_to_string;

pub fn input_data(day: &str) -> String {
    read_to_string(format!(
        "/home/oliver/Projects/Advent/2021/data/{}.txt",
        day
    ))
    .unwrap()
}
