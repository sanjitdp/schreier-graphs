use num_complex::Complex32 as Complex;

fn main() {
    let zero = 0.0 * Complex::i();
    let tree = BiColorTree {
        nodes: vec![
            (zero, 0, vec![1, 2, 3, 4]),
            (zero, 0, vec![]),
            (zero, 0, vec![]),
            (zero, 0, vec![]),
            (zero, 0, vec![]),
        ],
    };
    let operators = get_operators(&tree);
    println!("{:?}", operators);
    let graph = get_graph(4, &operators);
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

#[derive(Debug)]
struct Operator {
    alphabet: usize,
    cycle_len: usize,
    permutation: Vec<usize>,
    repeat: usize,
}

impl Operator {
    fn apply(&self, word: &mut [usize]) {
        let mut w = word;
        while w.len() > 0 {
            let first = w[0];
            w[0] = self.permutation[w[0]];
            if first == self.repeat {
                w = &mut w[1..];
            } else {
                break;
            }
        }
    }

    fn apply_index(&self, word: usize, length: usize) -> usize {
        let mut w = word;
        let mut front = 0;
        let mut scale = 1;
        let mut len = length;
        while len > 0 {
            let first = w % self.alphabet;
            w = w - first + self.permutation[first];
            if first == self.repeat {
                front += self.permutation[first] * scale;
                scale *= self.alphabet;
                w /= self.alphabet;
                len -= 1;
            } else {
                break;
            }
        }
        front + w * scale
    }

    fn cycle_digits(&self, word: usize, length: usize) -> usize {
        let mut w = word;
        let mut depth = 0;
        let mut len = length;
        while len > 0 {
            let first = w % self.alphabet;
            if self.permutation[first] != first {
                w /= self.alphabet;
                len -= 1;
                depth += 1;
            } else {
                break;
            };
        }
        depth
    }

    fn get_cycle_len(&self, word: usize, length: usize) -> usize {
        self.cycle_len.pow(self.cycle_digits(word, length) as u32)
    }

    fn with_next_level_indices<F: FnMut(usize)>(&self, word: usize, length: usize, mut f: F) {
        let mut w = word;
        let mut front = 0;
        let mut scale = 1;
        let mut depth = 0;
        let mut len = length;
        let mut first = 0;
        let mut letter = 0;
        while len > 0 {
            first = w % self.alphabet;
            if self.permutation[first] != first {
                letter = first;
                front += first * scale;
                scale *= self.alphabet;
                w /= self.alphabet;
                len -= 1;
                depth += 1;
            } else {
                break;
            };
        }
        if depth == 0 {
            return;
        }
        let fscale = scale / self.alphabet;
        front -= letter * fscale;
        for _ in 1..self.cycle_len {
            letter = self.permutation[letter];
            f(front + letter * fscale + w * scale);
        }
    }

    fn apply_at_depth(&self, depth: usize, word: usize, length: usize) -> usize {
        let skip = self.cycle_digits(word, length) - depth;
        let mut depth_factor = self.alphabet.pow(skip as u32);
        let mut w = word / depth_factor;
        let mut front = 0;
        let mut scale = 1;
        let mut len = length - skip;
        while len > 0 {
            let first = w % self.alphabet;
            w = w - first + self.permutation[first];
            if first == self.repeat {
                front += self.permutation[first] * scale;
                scale *= self.alphabet;
                w /= self.alphabet;
                len -= 1;
            } else {
                break;
            }
        }
        (front + w * scale) * depth_factor + word % depth_factor
    }

    fn inverse_at_depth(&self, depth: usize, word: usize, length: usize) -> usize {
        let mut w = word;
        for d in 1..=depth {
            for _ in 1..self.cycle_len {
                w = self.apply_at_depth(d, w, length);
            }
        }
        w
    }
}

struct BiColorTree {
    // adjacent edges in CCW order from the
    // connection to the root
    nodes: Vec<(Complex, usize, Vec<usize>)>,
}

fn get_operators(tree: &BiColorTree) -> Vec<Operator> {
    let mut n = 0;
    let mut label_num = 1;
    let mut label = 0;
    let mut operator_num = 0;
    let mut branch_num = 0;
    let mut white = false;
    let mut stack = Vec::new();
    let mut operator_builders = Vec::<Vec<usize>>::new();

    loop {
        let node = &tree.nodes[n];
        if node.2.len() > branch_num {
            stack.push((n, branch_num + 1, operator_num, label));
            n = node.2[branch_num];
            branch_num = 0;
            if white {
                // next we visit the next black vertex
                // for the first time
                label = label_num;
                label_num += 1;
                operator_builders[operator_num].push(label);
            } else {
                // next we are visiting a white vertex for the first time
                // don't assign a label yet, but we create a list
                // to start storing its cycle
                operator_num = operator_builders.len();
                operator_builders.push(vec![label]);
            };
        } else if stack.len() > 0 {
            if white {
                // leaving a white vertex for the last time
                operator_builders[operator_num].push(label_num);
                label_num += 1;
            }
            let (next, bn, on, ln) = stack.pop().unwrap();
            branch_num = bn;
            n = next;
            operator_num = on;
            label = ln;
        } else {
            break;
        }

        white = !white;
    }

    let mut operators = Vec::with_capacity(operator_builders.len());

    for b in operator_builders {
        let mut p = vec![0; label_num];
        for i in 0..label_num {
            p[i] = i;
        }
        for i in 0..b.len() - 1 {
            p[b[i]] = b[i + 1];
        }
        p[b[b.len() - 1]] = b[0];
        operators.push(Operator {
            alphabet: label_num,
            cycle_len: b.len(),
            permutation: p,
            repeat: b[b.len() - 1],
        });
    }

    return operators;
}

struct SGraph {
    vertices: Vec<Complex>,
    edges: Vec<usize>,
}

#[derive(Clone, Copy)]
struct Mobius {
    a: Complex,
    b: Complex,
    c: Complex,
    d: Complex,
}

impl Mobius {
    fn apply(&self, z: Complex) -> Complex {
        (self.a * z + self.b) / (self.c * z + self.d)
    }

    fn deriv(&self, z: Complex) -> Complex {
        let denom = self.c * z + self.d;
        self.a / denom - (self.a * z + self.b) * self.c / (denom * denom)
    }

    fn identity() -> Mobius {
        let one = Complex::new(1.0, 0.0);
        let zero = Complex::new(0.0, 0.0);
        Mobius {
            a: one,
            b: zero,
            c: zero,
            d: one,
        }
    }

    fn inverse(&self) -> Mobius {
        Mobius {
            a: self.d,
            b: -self.b,
            c: -self.c,
            d: self.a,
        }
    }

    fn compose(&self, other: Mobius) -> Mobius {
        Mobius {
            a: self.a * other.a + self.b * other.c,
            b: self.a * other.b + self.b * other.d,
            c: self.c * other.a + self.d * other.c,
            d: self.c * other.b + self.d * other.d,
        }
    }

    fn from_points(
        z1: Complex,
        z2: Complex,
        z3: Complex,
        z1_img: Complex,
        z2_img: Complex,
        z3_img: Complex,
    ) -> Mobius {
        let f1 = (z3 - z2) / (z3 - z1);
        let m1 = Mobius {
            a: f1,
            b: -f1 * z1,
            c: Complex::new(1.0, 0.0),
            d: -z2,
        };
        let f2 = (z3_img - z2_img) / (z3_img - z1_img);
        let m2 = Mobius {
            a: f2,
            b: -f2 * z1_img,
            c: Complex::new(1.0, 0.0),
            d: -z2_img,
        };
        m2.inverse().compose(m1)
    }

    fn ortho(z1: Complex, z2: Complex, z1_img: Complex, z2_img: Complex) -> Mobius {
        let f = (z1_img - z2_img) / (z1 - z2);
        Mobius {
            a: f,
            b: z1_img - z1 * f,
            c: Complex::new(0.0, 0.0),
            d: Complex::new(1.0, 0.0),
        }
    }
}

const PI: f32 = std::f32::consts::PI;

fn get_graph(depth: usize, operators: &[Operator]) -> SGraph {
    let alphabet = operators[0].alphabet;
    let n_vertices = alphabet.pow(depth as u32);
    let zero = 0.0 * Complex::i();
    let mut vertices = vec![zero; n_vertices];
    let mut edges = Vec::with_capacity(n_vertices * operators.len());
    for i in 0..n_vertices {
        for k in 0..operators.len() {
            edges.push(operators[k].apply_index(i, depth));
        }
    }

    let angle_num = 0.5 * operators.len() as f32;
    let leaf_angle = 2.0 * PI / operators.len() as f32;

    let rel_scale = (0.5f32).sqrt();

    let get_point_norm = |angle: f32| {
        let r = (angle_num * angle).cos();
        let rot = (angle * Complex::i()).exp();
        let p = rot * r;
        let dr = -angle_num * (angle_num * angle).sin();
        let dlen = (dr * dr + r * r).sqrt();
        let norm = -Complex::i() * rot *
            Complex::new(dr, r) / dlen;

        (p, norm)
    };

    let mut build_stack = Vec::new();

    for i in 0..operators.len() {
        let dir = (Complex::i() * i as f32 * leaf_angle).exp();
        let mut angle = -leaf_angle / 2.0;
        let scale = operators[i].get_cycle_len(0, depth) as f32;
        operators[i].with_next_level_indices(0, depth, |next| {
            angle += leaf_angle / operators[i].cycle_len as f32;
            let (p, norm) = get_point_norm(angle);
            vertices[next] = p * dir * scale;
            build_stack.push((next, norm * dir, i, 1));
        });
    }

    while let Some((vert, dir, op, op_depth)) = build_stack.pop() {
        let p1 = operators[op].apply_at_depth(op_depth, vert, depth);
        let p2 = operators[op].inverse_at_depth(op_depth, vert, depth);
        let op_scale = operators[op].get_cycle_len(vert, depth) as f32;

        let map = if p1 == p2 {
            // degenerate case - not enough points to specify map
            Mobius::ortho(
                vertices[vert],
                vertices[vert] - dir * op_scale,
                vertices[vert],
                vertices[p1],
            )
        } else {
            let step_angle = leaf_angle / operators[op].cycle_len.pow(op_depth as u32) as f32;
            let angle = -leaf_angle / 2.0 + step_angle;
            let (p, _) = get_point_norm(angle);
            let pa = p * dir * op_scale;
            let pb = p.conj() * dir * op_scale;
            Mobius::from_points(
                vertices[vert],
                vertices[vert] - pa,
                vertices[vert] - pb,
                vertices[vert],
                vertices[p1],
                vertices[p2],
            )
        };

        if op_depth < operators[op].cycle_digits(vert, depth) {
            let mut w = p2;
            let step_angle = leaf_angle / operators[op].cycle_len.pow(op_depth as u32 + 1) as f32;
            let mut angle = leaf_angle / 2.0 - step_angle * operators[op].cycle_len as f32 + step_angle;

            for _ in 0..2 {
                for _ in 1..operators[op].cycle_len {
                    w = operators[op].apply_at_depth(op_depth + 1, w, depth);
                    let (p, norm) = get_point_norm(angle);
                    let p = p * dir * op_scale;
                    let new_point = vertices[vert] - p;
                    vertices[w] = map.apply(new_point);
                    let new_dir = -dir * norm;
                    build_stack.push((w, new_dir * map.deriv(new_point), op, op_depth + 1));
                    angle += step_angle;
                }
                angle = -leaf_angle / 2.0 + step_angle;
                w = operators[op].apply_at_depth(op_depth + 1, w, depth);
            }
        }

        for i in 0..operators.len() {
            if i == op {
                continue;
            }
            let op_dir = -dir * (Complex::i() * (i as f32 - op as f32) * leaf_angle).exp();
            let mut angle = -leaf_angle / 2.0;
            let scale = operators[i].get_cycle_len(vert, depth) as f32 * rel_scale;
            operators[i].with_next_level_indices(vert, depth, |next| {
                angle += leaf_angle / operators[i].cycle_len as f32;
                let (p, norm) = get_point_norm(angle);
                let new_point = vertices[vert] + p * op_dir * scale;
                vertices[next] = map.apply(new_point);
                let next_dir = norm * op_dir * rel_scale;
                build_stack.push((next, next_dir * map.deriv(new_point), i, 1));
            });
        }
    };

    SGraph {
        vertices: vertices,
        edges: edges,
    }
}
