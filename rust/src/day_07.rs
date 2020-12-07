use std::collections::{HashMap, HashSet};

pub fn solve(input: &Vec<String>) {
    let specs = parse_specs(input);
    let containers = find_containers(String::from("shiny gold"), &specs);
    println!("Shiny Gold can be put in {} bags", containers.len());
}

fn parse_raw_contains(raw: &str) -> (String, u8) {
    let pieces: Vec<&str> = raw.split(" ").collect();
    let color = pieces[1..pieces.len()-1].join(" ");
    let num: u8 = u8::from_str_radix(pieces[0], 10).expect(&format!("{} should be a number", pieces[0]));

    (color, num)
}


fn parse_specs(input: &Vec<String>) -> HashMap<String, HashMap<String, u8>> {
    let mut bags = HashMap::new();

    for line in input {
        let split: Vec<&str> = line.split(" bags contain ").collect();
        let color = String::from(split[0]);

        let raw_contains = split[1];
        if raw_contains == "no other bags." {
            bags.insert(color, HashMap::new());
        } else {
            let contains: HashMap<String, u8> = raw_contains.split(", ").map(parse_raw_contains).collect();
            bags.insert(color, contains);
        }
    }

    bags
}

// Reverse the (sparse) adjacency matrix for the 'contains' graph
fn reverse_adjacency_matrix(input: &HashMap<String, HashMap<String, u8>>) -> HashMap<String, HashSet<String>> {
    let mut result = HashMap::new();

    for (k, values) in input.iter() {
        for v in values.keys() {
            if !result.contains_key(v) {
                result.insert(v.clone(), HashSet::new());
            }

            result.get_mut(v).unwrap().insert(k.clone());
        }
    }

    result
}

// Find all containers that can contain the give color bag
fn find_containers(color: String, spec: &HashMap<String, HashMap<String, u8>>) -> HashSet<String> {
    let reversed = reverse_adjacency_matrix(spec);

    let mut result = reversed.get(&color).unwrap().clone();
    let mut to_check = result.clone();
    while to_check.len() > 0 {
        let mut parents = HashSet::new();
        for color in to_check.iter() {
            parents = parents.union(reversed.get(color).unwrap_or(&HashSet::new())).cloned().collect()
        }
        // Need to check parents of any we haven't seen before
        to_check = parents.difference(&result).cloned().collect();
        // Add current to result
        for new in to_check.iter() {
            result.insert(new.clone());
        }
    }

    result
}


#[cfg(test)]
mod tests {
    use super::*;

    fn fixture() -> Vec<String> {
        let raw = vec![
            "light red bags contain 1 bright white bag, 2 muted yellow bags.",
            "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
            "bright white bags contain 1 shiny gold bag.",
            "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
            "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
            "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
            "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
            "faded blue bags contain no other bags.",
            "dotted black bags contain no other bags.",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse_specs() {
        let specs = parse_specs(&fixture());
        assert_eq!(specs.len(), 9);

        let light_red: HashSet<String> = specs.get("light red").unwrap().keys().cloned().collect();
        let expected: HashSet<String> = vec![String::from("bright white"), String::from("muted yellow")].iter().cloned().collect();
        assert_eq!(light_red, expected);
        assert_eq!(specs.get("dotted black").unwrap().len(), 0);

    }

    #[test]
    fn test_find_containers() {
        let specs = parse_specs(&fixture());

        let gold_containers = find_containers(String::from("shiny gold"), &specs);
        assert_eq!(gold_containers.len(), 4);
    }


}
