use std::fs;
use std::path::PathBuf;

fn main() {
    // Get input file path relative to this file
    let mut input_path = PathBuf::from(file!());
    input_path.pop();
    input_path.push("input.txt");
    
    let input = fs::read_to_string(&input_path)
        .expect("Failed to read input file");
    
    // Part 1
    let part1 = solve_part1(&input);
    println!("Part 1: {}", part1);
    
    // Part 2
    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
}

fn has_repeating_pattern(number: i64) -> bool {
    // convert number to string
    let num_str = number.to_string();

    // remove leading zeros
    let num_str = num_str.trim_start_matches('0');

    // if number has odd number of digits,
    // it can't have repeating pattern
    if num_str.len() % 2 != 0 {
        return false;
    }
    // for n-digit number (where n is even), we compare
    // first half (num_str[0..n/2]) with second half (num_str[n/2..n])
    // if they are equal, then it has repeating pattern
    let first_half = &num_str[0..num_str.len()/2];
    let second_half = &num_str[num_str.len()/2..num_str.len()];
    return first_half == second_half;
}

fn solve_part1(input: &str) -> i64 {
    let lines = input.lines();
    let mut count = 0;
    for line in lines {
        for id_range in line.split(",") {
            let (start_str, end_str) = id_range.split_once("-").unwrap();
            let start = start_str.parse::<i64>().unwrap();
            let end = end_str.parse::<i64>().unwrap();
            
            for i in start..=end {
                if has_repeating_pattern(i) {
                    count += i;
                }
            }
        }
    }
    return count;
}

fn solve_part2(input: &str) -> i64 {
    // TODO: Implement part 2
    0
}
