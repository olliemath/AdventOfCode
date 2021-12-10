pub fn solve(input: &[String]) {
    let parsed = parse(input);
    println!("Pair: {:?}", find_product(&parsed, 2));
    println!("Triple: {:?}", find_product(&parsed, 3));
}

fn parse(input: &[String]) -> Vec<i32> {
    input.iter().map(|i| i.parse::<i32>().unwrap()).collect()
}

fn find_tuple(input: &[i32], size: usize) -> Option<Vec<i32>> {
    // TODO: support arbitrary sized loops (use a stack?)
    if size != 2 && size != 3 {
        panic!("Size {} tuples not supported", size);
    }

    for x in input.iter() {
        for y in input.iter() {
            if size == 2 {
                if x + y == 2020 {
                    return Some(vec!{*x, *y});
                }
            } else {
                for z in input.iter() {
                    if x + y + z == 2020 {
                        return Some(vec!{*x, *y, *z});
                    }
                }
            }
        }
    }

    None
}

fn find_product(input: &[i32], size: usize) -> Option<i32> {
    find_tuple(input, size).map(|tup| tup.iter().product())
}


#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let strvec = vec!{"1721", "979", "366", "299", "675", "1456"};
        strvec.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let input = fixture();
        let parsed = parse(&input);
        assert_eq!(parsed, vec!{1721, 979, 366, 299, 675, 1456});
    }

    #[test]
    fn test_find_tuple() {
        let input = fixture();
        let parsed = parse(&input);

        assert_eq!(find_tuple(&parsed, 2), Some(vec!{1721, 299}));
        assert_eq!(find_tuple(&parsed, 3), Some(vec!{979, 366, 675}));
    }

    #[test]
    fn test_find_product() {
        let input = fixture();
        let parsed = parse(&input);

        assert_eq!(find_product(&parsed, 2), Some(514579));
        assert_eq!(find_product(&parsed, 3), Some(241861950));
    }

}
