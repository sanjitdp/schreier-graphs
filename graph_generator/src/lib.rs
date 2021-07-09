use num_complex::Complex32 as Complex;

#[derive(Debug)]
pub struct Operator {
    alphabet: usize,
    cycle_len: usize,
    permutation: Vec<usize>,
    repeat: usize,
}

impl Operator {
    pub fn apply(&self, word: &mut [usize]) {
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
        let mut first;
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
        if depth == 0 {
            return word;
        }
        let skip = self.cycle_digits(word, length) - depth;
        let depth_factor = self.alphabet.pow(skip as u32);
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
        if depth == 0 {
            return word;
        }
        let mut w = word;
        for d in 1..=depth {
            for _ in 1..self.cycle_len {
                w = self.apply_at_depth(d, w, length);
            }
        }
        w
    }
}

pub struct BiColorTree {
    // adjacent edges in CCW order from the
    // connection to the root
    pub nodes: Vec<Vec<usize>>,
}

pub fn get_operators(tree: &BiColorTree) -> Vec<Operator> {
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
        if node.len() > branch_num {
            stack.push((n, branch_num + 1, operator_num, label));
            n = node[branch_num];
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

pub struct SGraph {
    pub vertices: Vec<Complex>,
    pub vert_dirs: Vec<Complex>,
    pub edges: Vec<usize>,
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
        z3_img: Complex
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

fn circ_between_points(z1: Complex, z2: Complex, z3: Complex) -> (Complex, Complex) {
    let mid1 = 0.5 * (z1 + z2);
    let mid2 = 0.5 * (z2 + z3);
    let m = mid2 - mid1;
    let i = Complex::new(0.0, 1.0);
    let d1 = i * (z2 - z1);
    let d2 = i * (z3 - z2);
    let t = (m.conj() * d2).im / (d1.conj() * d2).im;
    let center = mid1 + d1 * t;

    let radius = (z1 - center).norm();

    let norm = - d2 / d2.norm();

    let dir = if t > 0.0 {
        norm
    } else {
        -norm
    };

    (center + dir * radius, norm)
}

const PI: f32 = std::f32::consts::PI;

pub fn get_graph(operators: &[Operator], root_vert: usize, depth: usize, rel_scale: f32) -> SGraph {
    let alphabet = operators[0].alphabet;
    let n_vertices = alphabet.pow(depth as u32);
    let zero = 0.0 * Complex::i();
    let mut vertices = vec![zero; n_vertices];
    let mut vert_dirs = vec![zero; n_vertices];
    let mut edges = Vec::with_capacity(n_vertices * operators.len());
    for i in 0..n_vertices {
        for k in 0..operators.len() {
            edges.push(operators[k].apply_index(i, depth));
        }
    }

    let (leaf_angle, angle_num) = if operators.len() == 1 {
        (PI, 1.0)
    } else {
        (2.0 * PI / operators.len() as f32, 0.5 * operators.len() as f32)
    };

    let func = |angle: f32| {
        (
            (angle_num * angle).cos(),
            -angle_num * (angle_num * angle).sin()
        )
        /*let c = (angle_num * angle).cos();
        let dc = -angle_num * (angle_num * angle).sin();
        (
            c * c,
            2.0 * c * dc,
        )*/
    };

    let get_point_norm = |angle: f32| {
        let (r, dr) = func(angle);
        let rot = (angle * Complex::i()).exp();
        let p = rot * r;
        let dlen = (dr * dr + r * r).sqrt();
        let norm = - Complex::i() * rot * 
            Complex::new(dr, r) / dlen;

        (p, norm)
    };

    vert_dirs[root_vert] = Complex::new(1.0, 0.0);
    let mut build_stack = vec![(root_vert, 0, 0, 0, 0)];

    let mut chain_sets = vec![Vec::new(); depth];
    let mut lowest_depth = depth + 1;

    while let Some((vert, from_root, op_num, op, op_depth)) = build_stack.pop() {
        let p1 = operators[op].apply_at_depth(op_depth, vert, depth);
        let p2 = operators[op].inverse_at_depth(op_depth, vert, depth);
        let op_scale = operators[op].get_cycle_len(vert, depth) as f32;

        let op_digits = operators[op].cycle_digits(vert, depth);

        let (step_p1, step_p2, map_angle_1, map_angle_2) = if op_depth < op_digits {
            let step_angle = leaf_angle / operators[op].cycle_len.pow(op_depth as u32) as f32;
            let off_step_angle = step_angle - step_angle / operators[op].cycle_len as f32;

            let (sp1, map_angle_1) = if op_num == operators[op].cycle_len - 1 {
                (operators[op].inverse_at_depth(op_depth + 1, p1, depth), off_step_angle)
            } else {
                (p1, step_angle)
            };

            let (sp2, map_angle_2) = if op_num == 1 {
                (operators[op].apply_at_depth(op_depth + 1, p2, depth), off_step_angle)
            } else {
                (p2, step_angle)
            };

            (sp1, sp2, map_angle_1, map_angle_2)
        } else {
            let map_angle = leaf_angle / operators[op].cycle_len.pow(op_depth as u32) as f32;
            (p1, p2, map_angle, map_angle)
        };

        let map = if op_depth == 0 {
            Mobius::identity()
        } else if step_p1 == step_p2 {
            // degenerate case - not enough points to specify map
            Mobius::ortho(
                vertices[vert],
                vertices[vert] + op_scale,
                vertices[vert],
                vertices[step_p1],
            )
        } else {
            let angle_1 = -leaf_angle / 2.0 + map_angle_1;
            let angle_2 = -leaf_angle / 2.0 + map_angle_2;
            let (point_1, _) = get_point_norm(angle_1);
            let (point_2, _) = get_point_norm(angle_2);
            let pa = point_1 * op_scale;
            let pb = point_2.conj() * op_scale;
            Mobius::from_points(
                vertices[vert],
                vertices[vert] + pa,
                vertices[vert] + pb,
                vertices[vert],
                vertices[step_p1],
                vertices[step_p2],
            )
        };

        for i in 0..operators.len() {
            let op_dir = (Complex::i() * (i as f32 - op as f32) * leaf_angle).exp();
            let next_depth = if i == op {
                op_depth + 1
            } else {
                1
            };

            let clen = operators[i].cycle_len;

            let remaining_depth = if i == op {
                operators[i].cycle_digits(vert, depth) - op_depth
            } else {
                operators[i].cycle_digits(vert, depth)
            };

            let scale = operators[i].get_cycle_len(vert, depth) as f32;
            let angle = -leaf_angle / 2.0;
            let mut step_angle = leaf_angle / clen.pow(next_depth as u32) as f32;
            let next_from = from_root + 1;
            let next_scale = rel_scale.powi(next_from);

            for k in 0..remaining_depth {
                let v1 = operators[i].apply_at_depth(next_depth + k, vert, depth);
                let v2 = operators[i].inverse_at_depth(next_depth + k, vert, depth);

                let (p, norm) = get_point_norm(angle + step_angle);

                let new_1 = vertices[vert] + p * op_dir * scale;
                let new_2 = vertices[vert] + p.conj() * op_dir * scale;

                let dir_1 = map.deriv(new_1) * norm;
                let dir_2 = map.deriv(new_2) * norm;

                let new_1 = map.apply(new_1);
                let new_2 = map.apply(new_2);

                if lowest_depth > next_depth + k {
                    lowest_depth = next_depth + k;
                }
                chain_sets[next_depth + k - 1].push((vert, i));

                if k > 0 || clen > 2 {
                    vertices[v1] = new_1;
                    vertices[v2] = new_2;
                    vert_dirs[v1] = dir_1;
                    vert_dirs[v2] = dir_2; 
                } else if i != op || op_depth == 0 {
                    vertices[v1] = new_1;
                    vert_dirs[v1] = dir_1;
                }

                step_angle /= clen as f32;
            }
        }

        if build_stack.len() == 0 {
            while lowest_depth <= chain_sets.len() && chain_sets[lowest_depth - 1].len() == 0 {
                lowest_depth += 1;
            }

            if lowest_depth <= chain_sets.len() {
                let next_chains = std::mem::replace(&mut chain_sets[lowest_depth - 1], Vec::new());
                for (start, next_op) in next_chains {
                    let op_len = operators[next_op].cycle_len;
                    let step_angle = leaf_angle / op_len.pow(lowest_depth as u32) as f32;
                    let mut point = start;
                    let mut points = Vec::with_capacity(op_len + 1);
                    for i in 0..op_len {
                        points.push(point);
                        point = operators[next_op].apply_at_depth(lowest_depth, point, depth);
                    }
                    points.push(point);
                    for i in 1..(op_len - 1) / 2 {
                        let p1 = points[i];
                        let p2 = points[op_len - i];

                        let prev_1 = points[i - 1];
                        let prev_2 = points[op_len - i + 1];

                        let next_1 = points[i + 1];
                        let next_2 = points[op_len - i - 1];

                        let steps = op_len - 2 * i;
                        let angle = -leaf_angle / 2.0 + step_angle * i as f32;
                        let prev_angle = angle - step_angle;
                        let across_angle = angle + step_angle * steps as f32;
                        let next_angle = angle + step_angle;

                        let (prev, _) = get_point_norm(prev_angle);
                        let (point, _) = get_point_norm(angle);
                        let (across, _) = get_point_norm(across_angle);
                        let (next_point, next_dir) = get_point_norm(next_angle);

                        let map_1 = Mobius::from_points(
                            vertices[p1],
                            vertices[p1] + across - point,
                            vertices[p1] + prev - point,
                            vertices[p1],
                            vertices[p2],
                            vertices[prev_1],
                        );

                        let map_2 = Mobius::from_points(
                            vertices[p2],
                            vertices[p2] + (across - point).conj(),
                            vertices[p2] + (prev - point).conj(),
                            vertices[p2],
                            vertices[p1],
                            vertices[prev_2],
                        );

                        vertices[next_1] = map_1.apply(vertices[p1] + next_point - point);
                        vertices[next_2] = map_2.apply(vertices[p2] + (next_point - point).conj());
                    }

                    if op_len % 2 == 0 && op_len > 2 {
                        let prev = points[op_len / 2 - 2];
                        let p1 = points[op_len / 2 - 1];
                        let p2 = points[op_len / 2 + 1];
                        let next = points[op_len / 2];

                        let (v, norm) = circ_between_points(vertices[prev], vertices[p1], vertices[p2]);
                        vertices[next] = v;
                        vert_dirs[next] = norm;
                    }

                    for i in 1..op_len {
                        build_stack.push((points[i], 0, i, next_op, lowest_depth));
                    }
                }
            }
        }
    }

    SGraph {
        vertices: vertices,
        vert_dirs: vert_dirs,
        edges: edges,
    }
}
