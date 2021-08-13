"""
For permutation cycles [[0, 1], [0, 2]]
"""

import matplotlib.pyplot as plt

LEVEL = 4

level_1_lambdas = [-2. + 0.j, 4. + 0.j, 2. + 0.j]

level_2_lambdas = [-2. + 0.j, -0.73205081 + 0.j, 4. + 0.j, 2.73205081 + 0.j,
                   -1.64575131 + 0.j, 3.64575131 + 0.j, 2. + 0.j, 2. + 0.j, 2. + 0.j]

level_3_lambdas = [-2. + 0.j, -1.78065654 + 0.j, -1.06590154 + 0.j, -0.73205081 + 0.j,
                   2.73205081 + 0.j, 3.06590154 + 0.j, 4. + 0.j, 3.78065654 + 0.j,
                   -1.94036585 + 0.j, -0.83146081 + 0.j, 3.94036585 + 0.j, 2.83146081 + 0.j,
                   -1.64575131 + 0.j, -1.64575131 + 0.j, 3.64575131 + 0.j, -1.64575131 + 0.j,
                   3.64575131 + 0.j, 3.64575131 + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j, 2. + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j, 2. + 0.j, 2. + 0.j]

level_4_lambdas = [3.78065654 + 0.j, 3.84005309 + 0.j, 4. + 0.j, 3.96321726 + 0.j,
                   3.06590154 + 0.j, 2.73205081 + 0.j, -1.06590154 + 0.j, -0.98345619 + 0.j,
                   -0.73205081 + 0.j, 3.99004446 + 0.j, 3.94036585 + 0.j, -2. + 0.j,
                   -1.84005309 + 0.j, 2.98345619 + 0.j, 2.7942529 + 0.j, -0.7942529 + 0.j,
                   -1.78065654 + 0.j, -1.96321726 + 0.j, 3.79847473 + 0.j, -1.04170007 + 0.j,
                   3.04170007 + 0.j, 2.749181 + 0.j, -0.749181 + 0.j, -1.99004446 + 0.j,
                   -1.79847473 + 0.j, 2.83146081 + 0.j, 3.64575131 + 0.j, -0.83146081 + 0.j,
                   3.94036585 + 0.j, 2. + 0.j, -0.83146081 + 0.j, 3.64575131 + 0.j,
                   -1.94036585 + 0.j, 2. + 0.j, 2.83146081 + 0.j, -1.64575131 + 0.j,
                   -1.94036585 + 0.j, 3.94036585 + 0.j, 2. + 0.j, -1.64575131 + 0.j,
                   -1.94036585 + 0.j, -1.64575131 + 0.j, -1.64575131 + 0.j, 3.64575131 + 0.j,
                   -0.83146081 + 0.j, 2. + 0.j, 2.83146081 + 0.j, 3.64575131 + 0.j,
                   2. + 0.j, 3.64575131 + 0.j, 3.64575131 + 0.j, 2. + 0.j,
                   2. + 0.j, -1.64575131 + 0.j, -1.64575131 + 0.j, -1.64575131 + 0.j,
                   3.64575131 + 0.j, 3.64575131 + 0.j, 2. + 0.j, 2. + 0.j,
                   -1.64575131 + 0.j, -1.64575131 + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j, 3.64575131 + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j, 2. + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j, 2. + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j, 2. + 0.j, 2. + 0.j, 2. + 0.j,
                   2. + 0.j]


###############################################################################

# For listing out elements in given sets - for testing purposes only
def lister(lis):
    for i in range(len(lis)):
        print(lis[i].real)
    return


# For converting eigenvalue output sets to more usable format (only for undirected graphs)
def list_maker(lis):
    made_list = []
    for i in range(len(lis)):
        made_list.append(lis[i].real)
    return made_list


# Counts eigenvalue multiplicities and labels each element w multiplicity and schreier graph level
def element_counter_and_labeler(lis, level):
    count_list = []
    full_list = []
    total_multiplicity = len(lis)
    for i in range(len(lis)):
        count_list.append(0)
        for j in range(len(lis)):

            if lis[i] == lis[j]:
                count_list[i] += 1
            else:
                continue
    for i in range(len(lis)):
        full_list.append((lis[i], count_list[i]/total_multiplicity, level))
    list_final = list(set(full_list))
    return list_final


###############################################################################

level_1_list = element_counter_and_labeler(list_maker(level_1_lambdas), 1)

level_2_list = element_counter_and_labeler(list_maker(level_2_lambdas), 2)

level_3_list = element_counter_and_labeler(list_maker(level_3_lambdas), 3)

level_4_list = element_counter_and_labeler(list_maker(level_4_lambdas), 4)

super_list = [level_1_list, level_2_list, level_3_list, level_4_list]

###############################################################################


# for picking apart tuple elements from element_counter_and_labeler to use for plotting
def element_label(lis, num):
    x = []
    for i in range(len(lis)):
        x.append(lis[i][num])
    return x

# for ordering eigenvalue lists by their level
def level_sort_key(lst):
    return lst[2]

# for finding which eigenvalues generate at which level of the graph
def eigen_level(lis):
    diff_lvl_same_eigen = []
    for i in range(LEVEL):
        for j in range(LEVEL):
            for k in range(len(lis[i])):
                for l in range(len(lis[j])):
                    if lis[i][k][0] == lis[j][l][0]:
                        a = lis[i][k]
                        b = lis[j][l]
                        diff_lvl_same_eigen.append(a)
                        diff_lvl_same_eigen.append(b)
                    else:
                        continue
    no_dups = list(set(diff_lvl_same_eigen))
    combined_list = []
    for i in range(len(no_dups)):
        eigen = no_dups[i][0]
        same_eigen = []
        for j in range(len(no_dups)):
            if eigen == no_dups[j][0]:
                same_eigen.append(no_dups[j])
        same_eigen.sort(key=level_sort_key)
        combined_list.append(tuple(same_eigen))
    final_list = list(set(combined_list))
    for i in range(len(final_list)):
        final_list[i] = list(final_list[i])
    return final_list

#removes eigenvalues from eigen_level list that appear at the last level of Schreier graph to make plotting better
def shortener(lis):
    shortened_list = []
    for i in range(len(lis)):
        if len(lis[i]) == 1:
            continue
        else:
            shortened_list.append(lis[i])
    return shortened_list

continuity_lines_list = shortener(eigen_level(super_list))

# holdover from v1 - basically here to set axis bounds for now
x_4 = element_label(level_4_list, 0)
y_4 = element_label(level_4_list, 1)

# syntax for 3-D projection
ax = plt.axes(projection='3d')

# axes sizes (adjusted for best viewing experience)
ax.set_xlim3d(min(x_4), max(x_4))
ax.set_ylim3d(1, 4)
ax.set_zlim3d(0, max(y_4))

# listing each set of level eigenvalues
for i in range(len(super_list)):
    x = element_label(super_list[i], 0)
    y = element_label(super_list[i], 1)
    z = element_label(super_list[i], 2)
    ax.scatter(x, y, z, zdir='y')


# plotting lines connecting same eigenvalues throughout levels
for i in range(len(continuity_lines_list)):
    x = element_label(continuity_lines_list[i], 0)
    y = element_label(continuity_lines_list[i], 1)
    z = element_label(continuity_lines_list[i], 2)
    ax.plot(x,y,z, zdir='y')


# graph labeling
ax.set_title('Spectrum Distribution')
ax.set_xlabel('Eigenvalue')
ax.set_ylabel('Level of Schreier Graph')
ax.set_zlabel('Relative Multiplicity')
plt.show()
