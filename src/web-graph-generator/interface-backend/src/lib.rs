use graph_generator::*;



#[no_mangle]
pub fn get_bw_tree(verts: usize) -> Box<BiColorTree> {
    let mut nodes = Vec::with_capacity(verts);
    for _ in 0..verts {
        nodes.push(Vec::new());
    }
    Box::new(BiColorTree {
        nodes: nodes,
    })
}

#[no_mangle]
pub fn add_tree_edge(tree: &mut BiColorTree, vert: usize, edge: usize) {
    tree.nodes[vert].push(edge);
}

#[no_mangle]
pub fn generate_graph(tree: &BiColorTree, root: usize, depth: usize, scale: f32) -> Box<SGraph> {
    let transforms = get_operators(tree);
    Box::new(
        get_graph(&transforms, root, depth, scale)
    )
}

#[repr(C)]
pub struct GraphData {
    verts: usize,
    transforms: usize,
    vert_ptr: *const f32,
    dir_ptr: *const f32,
    edge_ptr: *const usize,
}

#[no_mangle]
pub fn get_graph_data(graph: &SGraph) -> Box<GraphData> {
    Box::new(GraphData {
        verts: graph.vertices.len(),
        transforms: graph.edges.len() / graph.vertices.len(),
        vert_ptr: graph.vertices.as_ptr() as *const f32,
        dir_ptr: graph.vert_dirs.as_ptr() as *const f32,
        edge_ptr: graph.edges.as_ptr(),
    })
}

#[no_mangle]
pub fn delete_tree(_: Box<BiColorTree>) {

}

#[no_mangle]
pub fn delete_graph(_: Box<SGraph>) {

}

#[no_mangle]
pub fn delete_graph_data(_: Box<GraphData>) {

}