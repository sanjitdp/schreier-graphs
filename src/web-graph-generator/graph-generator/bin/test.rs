use num_complex::Complex32 as Complex;
use graph_generator::*;

fn main() {
    let zero = 0.0 * Complex::i();
    let tree = BiColorTree {
        nodes: vec![
            vec![1], 
            vec![2, 3, 4],
            vec![],
            vec![],
            vec![],
        ],
    };
    let operators = get_operators(&tree);
    println!("{:?}", operators);
    let graph = get_graph(&operators, 0, 4, 1.0);
    for g in &graph.vertices {
        println!("({}, {})", g.re, g.im);
    }
    print!("[");
    for g in &graph.vertices {
        print!("{}, ", g.re);
    }
    println!("]");
    print!("[");
    for g in &graph.vertices {
        print!("{}, ", g.im);
    }
    println!("]");
    println!("{:?}", graph.edges);
}