use std::collections::{HashMap, HashSet, VecDeque};
type BagSpec = HashMap<String, HashMap<String, u8>>;

pub fn solve(input: &[String]) {
    let specs = parse_specs(input);

    let containers = find_containers(String::from("shiny gold"), &specs);
    println!("Shiny Gold can be put in {} bags", containers.len());

    let contained = find_contained(&specs);
    let required = *contained.get("shiny gold").unwrap();
    println!(
        "Shiny Gold requires {} bags (not including itself)",
        required - 1
    );
}

fn parse_raw_contains(raw: &str) -> (String, u8) {
    let pieces: Vec<&str> = raw.split(' ').collect();
    let color = pieces[1..pieces.len() - 1].join(" ");
    let num: u8 = pieces[0].parse()
        .unwrap_or_else(|_| panic!("{} should be a number", pieces[0]));

    (color, num)
}

fn parse_specs(input: &[String]) -> BagSpec {
    let mut bags = HashMap::new();

    for line in input {
        let split: Vec<&str> = line.split(" bags contain ").collect();
        let color = String::from(split[0]);

        let raw_contains = split[1];
        if raw_contains == "no other bags." {
            bags.insert(color, HashMap::new());
        } else {
            let contains: HashMap<String, u8> =
                raw_contains.split(", ").map(parse_raw_contains).collect();
            bags.insert(color, contains);
        }
    }

    bags
}

// Reverse the (sparse) adjacency matrix for the 'contains' graph
fn reverse_adjacency_matrix(input: &BagSpec) -> HashMap<String, HashSet<String>> {
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
fn find_containers(color: String, spec: &BagSpec) -> HashSet<String> {
    let reversed = reverse_adjacency_matrix(spec);

    let mut result = reversed.get(&color).unwrap().clone();
    let mut to_check = result.clone();
    while !to_check.is_empty() {
        let mut parents = HashSet::new();
        for color in to_check.iter() {
            parents = parents
                .union(reversed.get(color).unwrap_or(&HashSet::new()))
                .cloned()
                .collect()
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

// Perform a topoligical sort on the bag graph into levels (we use Kahn's algo)
fn topological_sort(spec: &BagSpec) -> Vec<String> {
    let mut adjacency_matrix = spec.clone();
    let mut rev_matrix = reverse_adjacency_matrix(spec);

    // Begin by processing the root nodes
    let mut to_process: VecDeque<String> = spec
        .iter()
        .filter(|(_, v)| v.is_empty())
        .map(|(k, _)| k)
        .cloned()
        .collect();
    let mut processed = Vec::new();

    while !to_process.is_empty() {
        let subtree_root = to_process.pop_back().unwrap();
        processed.push(subtree_root.clone());

        if rev_matrix.contains_key(&subtree_root) {
            let contained_by = rev_matrix.get_mut(&subtree_root).unwrap();

            for parent in contained_by.iter() {
                // Remove the edge from the parent to this bag
                adjacency_matrix
                    .get_mut(parent)
                    .unwrap()
                    .remove(&subtree_root);
                if adjacency_matrix.get(parent).unwrap().is_empty() {
                    // This bag contains no bags not already processed or earlier in the to_process queue
                    to_process.push_front(parent.clone());
                }
            }
        }

        rev_matrix.remove(&subtree_root);
    }

    if !rev_matrix.is_empty() {
        panic!("Found an infinite loop for bags: it's bags all the way down?");
    }

    processed
}

// Find the number of containers required including this one
fn find_contained(spec: &BagSpec) -> HashMap<String, u32> {
    let mut result = HashMap::new();
    let order = topological_sort(spec);

    for color in order {
        let mut required = 1;
        let contains = spec.get(&color).unwrap();
        for (contained_color, number) in contains.iter() {
            // Topological ordering guarantees this exists
            required += *number as u32 * result.get(contained_color).unwrap();
        }
        result.insert(color, required);
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

    fn fixture2() -> Vec<String> {
        let raw = vec![
            "shiny gold bags contain 2 dark red bags.",
            "dark red bags contain 2 dark orange bags.",
            "dark orange bags contain 2 dark yellow bags.",
            "dark yellow bags contain 2 dark green bags.",
            "dark green bags contain 2 dark blue bags.",
            "dark blue bags contain 2 dark violet bags.",
            "dark violet bags contain no other bags.",
        ];
        raw.iter().map(|s| String::from(*s)).collect()
    }

    #[test]
    fn test_parse_specs() {
        let specs = parse_specs(&fixture());
        assert_eq!(specs.len(), 9);

        let light_red: HashSet<String> = specs.get("light red").unwrap().keys().cloned().collect();
        let expected: HashSet<String> =
            vec![String::from("bright white"), String::from("muted yellow")]
                .iter()
                .cloned()
                .collect();
        assert_eq!(light_red, expected);
        assert_eq!(specs.get("dotted black").unwrap().len(), 0);
    }

    #[test]
    fn test_find_containers() {
        let specs = parse_specs(&fixture());

        let gold_containers = find_containers(String::from("shiny gold"), &specs);
        assert_eq!(gold_containers.len(), 4);
    }

    #[test]
    fn test_find_contained() {
        let specs1 = parse_specs(&fixture());
        let contained1 = find_contained(&specs1);

        let required = *contained1.get("shiny gold").unwrap();
        assert_eq!(required, 33);

        let specs2 = parse_specs(&fixture2());
        let contained2 = find_contained(&specs2);

        let required = *contained2.get("shiny gold").unwrap();
        assert_eq!(required, 127);
    }
}
