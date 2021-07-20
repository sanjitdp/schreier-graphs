let wasm_exports;
let wasm;
let wasm_module;

let here = {};

export function init() {
    let wasm = fetch('./generator.wasm');

    var imports = {
        
    };

    let WasmParams = {
        mem: new WebAssembly.Memory({initial: 16, maximum: 128}),
        env: imports,
    };

    let result;

    if (false && typeof WebAssembly.instantiateStreaming === 'function') {
        result = WebAssembly.instantiateStreaming(wasm, WasmParams).then(({module, instance}) => {
            wasm_exports = instance.exports;
            wasm_module = module;
            wasm = instance;
            mem = fns.memory;

            return 0;
        });
    } else {
        result = wasm.then(response => response.arrayBuffer()).then(mod =>
            WebAssembly.instantiate(mod, WasmParams)
        ).then(({instance, module}) => {
            wasm_module = module;
            wasm_exports = instance.exports;
            here.wasm_exports = wasm_exports;
            wasm = instance;

            return 0;
        });
    }

    result = result.then(x => {

        return 0;
    });

    return result;
}

var mode = 0;
var bwTree = [
    {x: 0, y: 0, black: true, grabbed: false, index: 0, next: []},
];

var graph_ptr;
var graph_edges;
var graph_verts;
var graph_transforms;
var graph_vert_list;
var graph_dir_list;
var graph_edge_list;

var depth = 4;

var buttons = [
    {x: 1, y: 1, w: 150, h: 50, name: "Draw Graph", active: true, pressed: false, press: () => {
        mode = 1;
        buttons[1].active = true;
        buttons[0].active = false;
        buttons[2].active = false;
        buttons[3].active = false;
        let tree = here.wasm_exports.get_bw_tree(bwTree.length);
        copy_tree(tree, bwTree[0], Math.PI);
        graph_ptr = here.wasm_exports.generate_graph(tree, 0, depth, 1);
        here.wasm_exports.delete_tree(tree);
        let graph_data = here.wasm_exports.get_graph_data(graph_ptr);
        let view = new Uint32Array(here.wasm_exports.memory.buffer, graph_data, 5);
        graph_verts = view[0];
        graph_transforms = view[1];
        graph_edges = graph_verts * graph_transforms;
        graph_vert_list = new Float32Array(here.wasm_exports.memory.buffer, view[2], 2 * graph_verts);
        graph_dir_list = new Float32Array(here.wasm_exports.memory.buffer, view[3], 2 * graph_verts);
        graph_edge_list = new Uint32Array(here.wasm_exports.memory.buffer, view[4], graph_edges);
        here.wasm_exports.delete_graph_data(graph_data);
    }},
    {x: 1, y: 1, w: 150, h: 50, name: "Back to Tree", active: false, pressed: false, press: () => {
        mode = 0;
        buttons[1].active = false;
        buttons[0].active = true;
        buttons[2].active = true;
        buttons[3].active = true;
        here.wasm_exports.delete_graph(graph_ptr);
    }},
    {x: 280, y: 1, w: 35, h: 25, name: "∧", active: true, pressed: false, press: () => {
        depth += 1;
    }},
    {x: 280, y: 26, w: 35, h: 25, name: "∨", active: true, pressed: false, press: () => {
        depth -= 1;
    }}
];

function copy_tree(tree, node, prev_dir) {
    let c = Math.cos(prev_dir);
    let s = Math.sin(prev_dir);
    node.next.sort((a, b) => {
        let dxa = bwTree[a].x - node.x;
        let dxb = bwTree[b].x - node.x;
        let dya = bwTree[a].y - node.y;
        let dyb = bwTree[b].y - node.y;
        let angle_a = Math.atan2(dya * c - dxa * s, dxa * c + dya * s);
        let angle_b = Math.atan2(dyb * c - dxb * s, dxb * c + dyb * s);
        angle_a - angle_b
    });
    for (let v of node.next) {
        let test = here.wasm_exports.add_tree_edge(tree, node.index, v);
        let dx = v.x - node.x;
        let dy = v.y - node.y
        copy_tree(tree, bwTree[v], Math.atan2(dy, dx));
    }
}

var drag = -1;

var width = 0;
var height = 0;

var mouseX = 0;
var mouseY = 0;
var mouseDown = false;

var panning = false;
var pan_start;

var transform_origin_x = 500;
var transform_origin_y = 500;
var transform_scale = 10;

const colors = [
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FF0080",
    "#FF8000",
    "#00FF80",
    "#80FF00",
    "#0080FF",
    "#8000FF"
];

function transform(x, y) {
    return {
        x: transform_origin_x + transform_scale * x,
        y: transform_origin_y - transform_scale * y,
    };
}

export function draw(ctx) {
    ctx.fillStyle = "#FFFFFF";
    ctx.strokeStyle = "#000000";

    if (depth < 1) {
        depth = 1;
    }

    while (bwTree.length ** depth >= 2 ** 20) {
        depth -= 1;
    }
    
    ctx.fillRect(0, 0, width, height);
    if (mode == 0) {
        ctx.lineWidth = 3;
        for (let v of bwTree) {
            for (let i of v.next) {
                let other = bwTree[i];
                ctx.beginPath();
                ctx.moveTo(v.x, v.y);
                ctx.lineTo(other.x, other.y);
                ctx.stroke();
            }
        }
        ctx.lineWidth = 1;
        for (let v of bwTree) {
            if (v.grabbed) {
                v.x = mouseX;
                v.y = mouseY;
                ctx.beginPath();
                ctx.arc(v.x, v.y, 14, 0, 2 * Math.PI);
                ctx.fillStyle = "#FFFF99";
                ctx.fill();
            }
            ctx.beginPath();
            ctx.arc(v.x, v.y, 12, 0, 2 * Math.PI);
            let dx = mouseX - v.x;
            let dy = mouseY - v.y;
            if (dx * dx + dy * dy < 12 * 12) {
                if (v.black) {
                    ctx.fillStyle = "#000000";
                    if (v.index == 0) {
                        ctx.fillStyle = "#001040";
                    }
                } else {
                    ctx.fillStyle = "#FFFFFF";
                }
            } else {
                v.grabbed = false;
                if (v.black) {
                    ctx.fillStyle = "#404040";
                    if (v.index == 0) {
                        ctx.fillStyle = "#002880";
                    }
                } else {
                    ctx.fillStyle = "#E0E0E0";
                }
            };
            ctx.fill();
            ctx.stroke();
        }
    } else if (mode == 1) {
        for (var i = 0;i<graph_verts;i += 1) {
            ctx.fillStyle = "#000000";
            let x = graph_vert_list[2 * i];
            let y = graph_vert_list[2 * i + 1];
            let p = transform(x, y);
            if (p.x >= 0 && p.y >= 0 && p.x <= width && p.y <= height) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, 2, 0, 2 * Math.PI);
                ctx.fill();
            }
        }
        ctx.lineWidth = 2;
        for (var i = 0;i<graph_verts;i += 1) {
            let x = graph_vert_list[2 * i];
            let y = graph_vert_list[2 * i + 1];
            let p = transform(x, y);
            for (var k = 0;k<graph_transforms;k += 1) {
                ctx.strokeStyle = colors[k];
                let other = graph_edge_list[i * graph_transforms + k];
                let ox = graph_vert_list[2 * other];
                let oy = graph_vert_list[2 * other + 1];
                let op = transform(ox, oy);
                let dx = (p.x - op.x);
                let dy = (p.y - op.y);
                if (dx * dx + dy * dy >= 3 * 3) {
                    if ((op.x >= 0 || p.x >= 0) && (op.y >= 0 || p.y >= 0)) {
                        if ((op.x <= width || p.x <= width) && (op.y <= height || p.y <= height)) {
                            ctx.beginPath();
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(op.x, op.y);
                            ctx.stroke();
                        }
                    }
                }
            }
        }
    }

    ctx.font = "20px Arial";
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#000000";
    ctx.fillStyle = "#000000";

    if (mode == 0) {
        ctx.fillText("Depth: " + depth, 170, 31);
    }

    for (let b of buttons) {
        if (b.active) {
            ctx.fillStyle = "#FFFFFF";
            if (mouseX >= b.x && mouseX <= b.x + b.w && mouseY >= b.y && mouseY <= b.y + b.h) {
                ctx.fillStyle = "#FFFF99";
                if (b.pressed) {
                    ctx.fillStyle = "#8080FF";
                }
            } else if (b.pressed) {
                b.pressed = false;
            }
            ctx.beginPath();
            ctx.fillRect(b.x, b.y, b.w, b.h);
            ctx.strokeRect(b.x, b.y, b.w, b.h);
            ctx.fillStyle = "#000000";
            ctx.fillText(b.name, b.x + 10, b.y + b.h / 2 + 5);
        }
    }
}

export function mouse_press(event, time) {
    if (event.button == 0) {
        for (let b of buttons) {
            if (b.active) {
                if (mouseX >= b.x && mouseX <= b.x + b.w && mouseY >= b.y && mouseY <= b.y + b.h) {
                    b.pressed = true;
                    return;
                }
            }
        }
        mouseDown = true;
    } else {
        return;
    }
    if (mode == 0) {
        for (let v of bwTree) {
            let dx = mouseX - v.x;
            let dy = mouseY - v.y;
            if (dx * dx + dy * dy < 12 * 12) {
                if (event.shiftKey) {
                    v.next.push(bwTree.length);
                    drag = bwTree.length;
                    bwTree.push({x: mouseX, y: mouseY, black: !v.black, grabbed: true, index: drag, next: []});
                } else {
                    bwTree[v.index].grabbed = true;
                    drag = v.index;
                }
                return;
            }
        }
    } else if (mode == 1) {
        panning = true;
        pan_start = {x: mouseX, y: mouseY};
    }
}

export function mouse_release(event, time) {
    if (event.button != 0) {
        return;
    }
    panning = false;
    for (let b of buttons) {
        if (b.active) {
            if (mouseX >= b.x && mouseX <= b.x + b.w && mouseY >= b.y && mouseY <= b.y + b.h) {
                if (b.pressed) {
                    b.pressed = false;
                    b.press();
                    return;
                }
            }
        }
    }
    mouseDown = false;
    if (mode == 0) {
        if (drag >= 0) {
            for (let v of bwTree) {
                if (v.grabbed) continue;
                let dx = bwTree[drag].x - v.x;
                let dy = bwTree[drag].y - v.y;
                if (drag > 0 && v.next.indexOf(drag) >= 0 && dx * dx + dy * dy < 14 * 14) {
                    remove_from_tree(drag);
                    drag = -1;
                    return;
                } else if (dx * dx + dy * dy < 30 * 30) {
                    let dist = Math.sqrt(dx * dx + dy * dy);
                    bwTree[drag].x = v.x + 70 * dx / dist;
                    bwTree[drag].y = v.y + 70 * dy / dist;
                    break;
                }
            }
            bwTree[drag].grabbed = false;
            drag = -1;
            return;
        }
    }
}

function remove_from_tree(idx) {
    let o = bwTree[idx];
    while (o.next.length > 0) {
        remove_from_tree(o.next[0]);
    }

    let v = o.index;

    bwTree.splice(v, 1);
    for (var i = 0;i<bwTree.length;i += 1) {
        let w = bwTree[i];
        if (w.index > v) {
            w.index -= 1;
        }
        var k = 0;
        while (k < w.next.length) {
            if (w.next[k] == v) {
                w.next.splice(k, 1);
            } else {
                if (w.next[k] > v) w.next[k] -= 1;
                k += 1;
            }
        }
    }
}

export function on_resize(w, h) {
    width = w;
    height = h;
    let dx = w / 2 - bwTree[0].x;
    let dy = h / 2 - bwTree[0].y;
    for (let v of bwTree) {
        v.x += dx;
        v.y += dy;
    }
    transform_origin_x = w / 2;
    transform_origin_y = h / 2;
}

export function mouse_move(event, time) {
    mouseX = event.pageX;
    mouseY = event.pageY;
    if (mode == 1 && panning) {
        transform_origin_x += mouseX - pan_start.x;
        transform_origin_y += mouseY - pan_start.y;
        pan_start.x = mouseX;
        pan_start.y = mouseY;
    }
}

export function mouse_wheel(event, time) {
    let factor;
    if (event.deltaMode == 0) {
        factor = 1.001 ** -event.deltaY;
    } else if (event.deltaMode == 1) {
        factor = 1.2 ** -event.deltaY;
    } else {
        factor = 2 ** -event.deltaY;
    }
    transform_scale *= factor;
    let dx = mouseX - transform_origin_x;
    let dy = mouseY - transform_origin_y;
    transform_origin_x = mouseX - dx * factor;
    transform_origin_y = mouseY - dy * factor;
}