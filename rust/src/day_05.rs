pub fn solve(input: &Vec<String>) {
    let highest = parse_boarding_passes(input).iter().map(|t| t.2).max().unwrap();
    println!("Highest seat id: {}", highest);
}


fn parse_boarding_passes(input: &Vec<String>) -> Vec<(u8, u8, u16)> {
    input.iter().map(|s| parse_boarding_pass(s.clone())).collect()
}

fn parse_boarding_pass(input: String) -> (u8, u8, u16) {
    let (raw_row, raw_col) = input.split_at(7);
    let bin_row = raw_row.replace("F", "0").replace("B", "1");
    let bin_col = raw_col.replace("L", "0").replace("R", "1");

    let row = u8::from_str_radix(&bin_row, 2).unwrap();
    let col = u8::from_str_radix(&bin_col, 2).unwrap();

    let seat_id = row as u16 * 8 + col as u16;
    (row, col, seat_id)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_boarding_pass() {
        let pass = String::from("FBFBBFFRLR");
        assert_eq!(parse_boarding_pass(pass), (44, 5, 357));
    }

    #[test]
    fn test_parse_boarding_passes() {
        let passes = vec![
            String::from("BFFFBBFRRR"),
            String::from("FFFBBBFRRR"),
            String::from("BBFFBBFRLL"),
        ];

        let expected: Vec<(u8, u8, u16)> = vec![(70, 7, 567), (14, 7, 119), (102, 4, 820)];

        assert_eq!(parse_boarding_passes(&passes), expected);
    }
}
