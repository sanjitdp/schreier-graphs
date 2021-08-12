from manim import *

A = ["a","b","i"]
L = ["0","1","2"]

Swap_dict = {
    "a0" : "1i",
    "a1" : "0a",
    "a2" : "2i",
    "b0" : "2i",
    "b1" : "1i",
    "b2" : "0b",
    "i0" : "0i",
    "i1" : "1i",
    "i2" : "2i",
}

Colors = {
    "i" : YELLOW,
    "a" : RED_D,
    "b" : GREEN_D,
    "0" : LIGHT_GREY,
    "1" : RED_A,
    "2" : GREEN_A,
}

class MagicStringTest(Scene):
    def construct(self):
        M = MagicString("abababa1011")
        self.play(Create(M.VGroup))
        self.wait()
        self.full_march(M)
        self.wait(3)
        
        
    def letter_travel(self,M,i_min,i_max):
        self.add(M.VGroup)
        for i in range(i_min,i_max+1):
            self.wait()
            self.letter_swap(M,i)
    
    def letter_swap(self,M,i):
        M.swap_index(i)
        self.play(
                Transform(M.VGroup[i],M.new_VGroup[i+1]),
                Transform(M.VGroup[i+1],M.new_VGroup[i])
            )
        self.remove(M.VGroup, M.new_VGroup)
        M.reset()
        self.add(M.VGroup)
    
    def multi_letter_swap(self,M,i_list):
        start_string = M.string
        start_VGroup = M.VGroup
        for i in i_list:
            M.swap_index(i)
            M.reset()
        self.play(
                *[Transform(start_VGroup[i],M.new_VGroup[i+1]) for i in i_list],
                *[Transform(start_VGroup[i+1],M.new_VGroup[i]) for i in i_list]
            )
        self.remove(start_VGroup, M.new_VGroup)
        M.reset()
        self.add(M.VGroup)
    
    def full_march(self,M,waittime=0.5):
        self.add(M.VGroup)

        def available_indices(string):
            output = []
            for i in range(len(string)-1):
                if string[i] in A and string[i+1] in L:
                    output.append(i)
            return output

        while len(available_indices(M.string))>0:
            self.multi_letter_swap(M,available_indices(M.string))
            self.wait(waittime)



    






class MagicString(object):
    def __init__(self, string):
        self.string = string
        self.VGroup = self.string_to_VGroup()
        
        for i in range(len(string)):
            if string[i] not in A:
                self.A_string = string[:i]
                break
        for i in range(1,len(string)):
            if string[-i] not in L:
                self.L_string = string[-i+1:]
                break
    
    
    def string_to_VGroup(self, string=None):
        if string == None:
            string = self.string
        return VGroup(*[MathTex(c, color=Colors[c]) for c in string]).arrange_in_grid(rows=1, row_alignments="d", col_widths=[0.3]*len(string))

    def swap_index(self, i):
        self.new_string = self.string[:i] + Swap_dict[self.string[i:i+2]] + self.string[i+2:]
        self.new_VGroup = self.string_to_VGroup(self.new_string)
    
    def reset(self):
        self.string = self.new_string
        self.VGroup = self.string_to_VGroup(self.new_string)
    


X = MagicString("ababia01201")
print(X.A_string)
print(X.L_string)