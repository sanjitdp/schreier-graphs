"""
These files are for use with the library Manim:
https://www.manim.community/

Use
py -m manim *filename *scenename -p
to generate and preview a scene.
"""

from manim import *
import networkx as nx
import itertools as it

AutomorphismSet = []


class Automorphism:
    def __init__(self, symbol, action, color=WHITE):
        # symbol is one character string
        # action is dictionary from letters to pairs of letters and automorphism symbols
        # color is what color you want this symbol to appear as universally
        self.symbol = symbol
        self.action = action
        self.color = color
        AutomorphismSet.append(self)

    def apply_to_string(self, string):
        output = ""
        current_action = self.action
        for i in range(len(string)):
            output_letter, next_layer = current_action[string[i]]
            output = output + output_letter
            current_action = self.find_auto_with_symbol(next_layer).action
        return output

    def __repr__(self):
        return self.symbol

    def tex(self):
        return MathTex(self.symbol, color=self.color)

    def find_auto_with_symbol(self, symbol):
        for auto in AutomorphismSet:
            if auto.symbol == symbol:
                return auto
        return False


id_auto = Automorphism(
    "1",
    {"0": ("0", "1"), "1": ("1", "1"), "2": ("2", "1")},
    color=GRAY
)

a = Automorphism(
    "a",
    {"0": ("1", "1"), "1": ("0", "a"), "2": ("2", "1")},
    color=RED
)

b = Automorphism(
    "b",
    {"0": ("2", "1"), "1": ("1", "1"), "2": ("0", "b")},
    color=GREEN
)


def all_strings(n):
    return [''.join(x) for x in it.product('012', repeat=n)]


# Testing
# print(b.apply_to_string("220102"))
# print(a.apply_to_string("120102"))


class Tree(Graph):
    def __init__(self, alphabet_size=3, depth=2, width=3, layout="straight", **kwargs):
        A = list(range(alphabet_size))
        G = nx.Graph()
        G.add_node("")
        if layout == "straight":
            tree_layout = {"": [width / 2, 0, 0]}
            for d in range(1, depth + 1):
                for i, s in enumerate(all_strings(d)):
                    G.add_node(s)
                    G.add_edge(s[:-1], s)
                    tree_layout[s] = [width * (2 * i + 1) / (2 * alphabet_size ** d), -1.5 * d, 0]
        if layout == "circular":
            tree_layout = {"": [0, 0, 0]}
            for d in range(1, depth + 1):
                for i, s in enumerate(all_strings(d)):
                    G.add_node(s)
                    G.add_edge(s[:-1], s)
                    tree_layout[s] = polar_to_cartesian(d, (2 * i + 1) / (2 * alphabet_size ** d))

        super().__init__(list(G.nodes), list(G.edges), layout=tree_layout, **kwargs)
        self.center()

    def apply_permutation(self, p):
        new_layout = {v: self[p(v)].get_center() for v in self.vertices}
        self.change_layout(new_layout)


class Generated(Scene):
    def construct(self):
        self.apply_permutation_sequence([a, b, a, b, a, b, a], "1011")

    def apply_permutation(self, p, s):
        G = Tree(3, 4, width=13.5, vertex_config={s: {"fill_color": RED}})

        string_eq = MathTex("x(", s, ")", "=", p(s)).to_edge(DOWN)

        self.add(G)
        self.play(FadeIn(string_eq[:3]))
        self.wait()
        self.play(G.animate.change_layout(layout={v: G[p(v)].get_center() for v in G.vertices}), run_time=5)
        self.play(FadeIn(string_eq[3:]))
        self.wait()
        self.clear()
        # self.play(G.animate.change_layout(layout={v : G[p(v)].get_center() for v in G.vertices}), run_time=1)
        # self.wait()

    def staggered_permutation(self, p, p_name, s):
        G = Tree(3, len(s), width=13.5, vertex_config={s: {"fill_color": RED}}).to_edge(UP)
        G_original = G.copy()

        string_eq = MathTex(p_name, "(", s, ")", "=", p(s)).to_edge(DOWN)

        self.add(G)
        self.play(Write(string_eq[:4]))
        self.wait()
        for n in range(1, len(s) + 1):
            self.play(
                G.animate.change_layout(layout={v: G_original[partial_perm(p, v, n)].get_center() for v in G.vertices}),
                run_time=1)
        self.play(Write(string_eq[4:]))
        self.wait()
        self.clear()

    def apply_permutation_sequence(self, p_sequence, s):
        G = Tree(3, len(s), width=13.5, layout="straight", vertex_config={s: {"fill_color": RED}}).to_edge(UP)
        G_original = G.copy()
        string = s
        string_eq = MathTex(p_sequence[0].symbol, "(", s, ")", "=", p_sequence[0].apply_to_string(s)).to_edge(DOWN)
        string_eq[0].set_color(p_sequence[0].color)

        self.add(G)
        self.play(Write(string_eq[:4]))
        self.wait()
        for i in range(len(p_sequence)):
            if i == 0:
                pass
            else:
                self.play(*[Write(string_eq[j]) for j in [0, 1, 3]])
            p = p_sequence[i]
            for n in range(1, len(s) + 1):
                self.play(G.animate.change_layout(
                    layout={v: G_original[partial_perm(p, v, n)].get_center() for v in G.vertices}), run_time=1)
            self.play(Write(string_eq[-2:]))
            self.wait(0.75)
            if i != len(p_sequence) - 1:
                new_string = p.apply_to_string(string)
                new_string_eq = MathTex(p_sequence[i + 1].symbol, "(", new_string, ")", "=",
                                        p_sequence[i + 1].apply_to_string(new_string)).to_edge(DOWN)
                self.play(
                    FadeOut(string_eq[:-1]),
                    ReplacementTransform(string_eq[-1], new_string_eq[2])
                )
                string = new_string
                string_eq = new_string_eq
                string_eq[0].set_color(p_sequence[i + 1].color)
                self.remove(G)
                G = Tree(3, len(s), width=13.5, vertex_config={new_string: {"fill_color": RED}}).to_edge(UP)
                G_original = G.copy()
                self.add(G)

        self.wait()


class CircularTest(Scene):
    def construct(self):
        p = x
        p_name = "x"
        s = "1021"

        C = Tree(3, 4, layout="circular", vertex_config={s: {"fill_color": RED}})
        self.add(C)
        C.scale(0.9)

        C_original = C.copy()

        string_eq = MathTex(p_name, "(", s, ")", "=", p(s)).to_corner(DR)

        self.play(Write(string_eq[:4]))
        self.wait()
        for n in range(1, len(s) + 1):
            self.play(
                C.animate.change_layout(layout={v: C_original[partial_perm(p, v, n)].get_center() for v in C.vertices}),
                run_time=1)
        self.play(Write(string_eq[4:]))
        self.wait()


def polar_to_cartesian(r, theta):
    # theta from 0 to 1
    # now clockwise from bottom lol
    return [-r * np.sin(2 * PI * theta), -r * np.cos(2 * PI * theta), 0]


def partial_perm(p, s, n):  # will apply permutation up to n characters in
    if n >= len(s):
        return p.apply_to_string(s)
    else:
        return p.apply_to_string(s)[:n] + s[n:]
