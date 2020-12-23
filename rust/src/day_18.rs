pub fn solve(input: &[String]) {
    let parsed = parse_many(input);
    let part1: u64 = parsed.iter().map(|p| eval(p)).sum();
    println!("Part1: {}", part1);
    let part2: u64 = parsed.iter().map(|p| advanced_eval(p)).sum();
    println!("Part2: {}", part2);
}

#[derive(Debug, PartialEq, Clone)]
enum Token {
    Num(u64),
    Add,
    Mul,
    Expr(Vec<Token>),
}

fn parse_many(input: &[String]) -> Vec<Vec<Token>> {
    input.iter().map(parse).collect()
}

fn parse(input: &String) -> Vec<Token> {
    let charvec: Vec<char> = input.trim().chars().collect();
    parse_subexpr(&charvec, 0).0
}

fn parse_num(input: Vec<u8>) -> Token {
    let n: u64 = String::from_utf8(input).unwrap().parse().unwrap();
    Token::Num(n)
}

fn parse_subexpr(input: &[char], offset: usize) -> (Vec<Token>, usize) {
    let mut result = Vec::new();
    let mut num = Vec::new();
    let mut k = offset;

    while k < input.len() {
        match input[k] {
            '(' => {
                let (parsed, new_k) = parse_subexpr(input, k + 1);
                result.push(Token::Expr(parsed));
                k = new_k;
            }
            ')' => {
                if num.len() > 0 {
                    result.push(parse_num(num.clone()));
                }
                return (result, k);
            }
            '+' => {
                result.push(Token::Add);
            }
            '*' => {
                result.push(Token::Mul);
            }
            ' ' => {
                if num.len() > 0 {
                    result.push(parse_num(num.clone()));
                    num.clear();
                }
            }
            c => {
                num.push(c as u8);
            }
        }
        k += 1;
    }

    if num.len() > 0 {
        result.push(parse_num(num));
    }

    (result, input.len())
}

fn expr_to_nums_and_ops(expr: &[Token], advanced: bool) -> (Vec<u64>, Vec<&Token>) {
    let mut numbers = Vec::new();
    let mut operators = Vec::new();

    for token in expr.iter() {
        match token {
            Token::Num(x) => numbers.push(*x),
            Token::Expr(v) => {
                if advanced {
                    numbers.push(advanced_eval(v))
                } else {
                    numbers.push(eval(v))
                }
            }
            t => operators.push(t),
        }
    }

    if numbers.len() != operators.len() + 1 {
        panic!(format!(
            "Syntax error: operator/number mismatch: {:?}",
            expr
        ));
    }

    (numbers, operators)
}

fn eval(expr: &[Token]) -> u64 {
    let (numbers, operators) = expr_to_nums_and_ops(expr, false);
    let mut answer = numbers[0];
    for (num, op) in numbers.iter().skip(1).zip(operators) {
        match op {
            Token::Add => answer += num,
            Token::Mul => answer *= num,
            _ => unreachable!(),
        }
    }

    answer
}

fn advanced_eval(expr: &[Token]) -> u64 {
    let (numbers, operators) = expr_to_nums_and_ops(expr, true);
    let mut answer = 1;
    let mut partial_result = numbers[0];

    for (num, op) in numbers.iter().skip(1).zip(operators) {
        match op {
            Token::Add => {
                partial_result += num;
            }
            Token::Mul => {
                answer *= partial_result;
                partial_result = *num;
            }
            _ => unreachable!(),
        }
    }
    answer *= partial_result;

    answer
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![
            "2 * 3 + (4 * 5)\n",
            "5 + (8 * 3 + 9 + 3 * 4 * 3)\n",
            "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n",
            "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2\n",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse() {
        let parsed = parse_many(&fixture());
        assert_eq!(parsed[0][0], Token::Num(2));
        assert_eq!(parsed[0][1], Token::Mul);
        assert_eq!(
            parsed[0][4],
            Token::Expr(vec![Token::Num(4), Token::Mul, Token::Num(5)])
        );
    }

    #[test]
    fn test_eval() {
        let parsed = parse_many(&fixture());
        assert_eq!(eval(&parsed[0]), 26);
        assert_eq!(eval(&parsed[1]), 437);
        assert_eq!(eval(&parsed[2]), 12240);
        assert_eq!(eval(&parsed[3]), 13632);
    }

    fn assert_eval(input: &str, exp: u64) {
        let parsed = parse(&String::from(input));
        assert_eq!(advanced_eval(&parsed), exp);
    }

    #[test]
    fn test_advanced_eval() {
        assert_eval("1 + 2 * 3 + 4 * 5 + 6", 231);

        let parsed = parse_many(&fixture());
        assert_eq!(advanced_eval(&parsed[0]), 46);
        assert_eq!(advanced_eval(&parsed[1]), 1445);
        assert_eq!(advanced_eval(&parsed[2]), 669060);
        assert_eq!(advanced_eval(&parsed[3]), 23340);
    }
}
