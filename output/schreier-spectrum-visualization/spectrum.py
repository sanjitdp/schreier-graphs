'''
For permutation cycle [0,1][0,2]
'''

level_1_lambdas = [-2.+0.j,  4.+0.j,  2.+0.j]

level_2_lambdas = [-2.        +0.j, -0.73205081+0.j,  4.        +0.j,  2.73205081+0.j,
       -1.64575131+0.j,  3.64575131+0.j,  2.        +0.j,  2.        +0.j,2.+0.j]

level_3_lambdas = [-2.        +0.j, -1.78065654+0.j, -1.06590154+0.j, -0.73205081+0.j,
        2.73205081+0.j,  3.06590154+0.j,  4.        +0.j,  3.78065654+0.j,
       -1.94036585+0.j, -0.83146081+0.j,  3.94036585+0.j,  2.83146081+0.j,
       -1.64575131+0.j, -1.64575131+0.j,  3.64575131+0.j, -1.64575131+0.j,
        3.64575131+0.j,  3.64575131+0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j,  2.        +0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j,  2.        +0.j,  2.        +0.j]

level_4_lambdas = [ 3.78065654+0.j,  3.84005309+0.j,  4.        +0.j,  3.96321726+0.j,
        3.06590154+0.j,  2.73205081+0.j, -1.06590154+0.j, -0.98345619+0.j,
       -0.73205081+0.j,  3.99004446+0.j,  3.94036585+0.j, -2.        +0.j,
       -1.84005309+0.j,  2.98345619+0.j,  2.7942529 +0.j, -0.7942529 +0.j,
       -1.78065654+0.j, -1.96321726+0.j,  3.79847473+0.j, -1.04170007+0.j,
        3.04170007+0.j,  2.749181  +0.j, -0.749181  +0.j, -1.99004446+0.j,
       -1.79847473+0.j,  2.83146081+0.j,  3.64575131+0.j, -0.83146081+0.j,
        3.94036585+0.j,  2.        +0.j, -0.83146081+0.j,  3.64575131+0.j,
       -1.94036585+0.j,  2.        +0.j,  2.83146081+0.j, -1.64575131+0.j,
       -1.94036585+0.j,  3.94036585+0.j,  2.        +0.j, -1.64575131+0.j,
       -1.94036585+0.j, -1.64575131+0.j, -1.64575131+0.j,  3.64575131+0.j,
       -0.83146081+0.j,  2.        +0.j,  2.83146081+0.j,  3.64575131+0.j,
        2.        +0.j,  3.64575131+0.j,  3.64575131+0.j,  2.        +0.j,
        2.        +0.j, -1.64575131+0.j, -1.64575131+0.j, -1.64575131+0.j,
        3.64575131+0.j,  3.64575131+0.j,  2.        +0.j,  2.        +0.j,
       -1.64575131+0.j, -1.64575131+0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j,  3.64575131+0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j,  2.        +0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j,  2.        +0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j,  2.        +0.j,  2.        +0.j,  2.        +0.j,
        2.        +0.j]

###############################################################################

# For listing out elements in given sets - for testing purposes only
def lister(lis):
  for i in range(len(lis)):
    print(lis[i].real)
  return

# For converting eigenvalue output sets to more usable format (only for undirected graphs)
def list_maker(lis):
  list = []
  for i in range(len(lis)):
    list.append(lis[i].real)
  return list

# Counts eigenvalue multiplicities and labels each element w multiplicity and schreier graph level
def element_counter_and_labeler(lis,level):
  count_list = []
  full_list = []
  for i in range(len(lis)):
    count_list.append(0)
    for j in range(len(lis)):
      
      if lis[i]==lis[j]:
        count_list[i] += 1
      else:
        continue
  for i in range(len(lis)):
    full_list.append((lis[i],count_list[i],level))
  list_final = list(set(full_list))
  return list_final

###############################################################################

level_1_list = element_counter_and_labeler(list_maker(level_1_lambdas),1)

level_2_list = element_counter_and_labeler(list_maker(level_2_lambdas),2)

level_3_list = element_counter_and_labeler(list_maker(level_3_lambdas),3)

level_4_list = element_counter_and_labeler(list_maker(level_4_lambdas),4)

###############################################################################
  
# for picking apart tuple elements from element_counter_and_labeler to use for plotting
def element_label(lis,num):
    x = []
    for i in range(len(lis)):
        x.append(lis[i][num])
    return x

#list values partitioned for plotting
x_1 = element_label(level_1_list,0)
y_1 = element_label(level_1_list,1)
z_1 = element_label(level_1_list,2)

x_2 = element_label(level_2_list,0)
y_2 = element_label(level_2_list,1)
z_2 = element_label(level_2_list,2)

x_3 = element_label(level_3_list,0)
y_3 = element_label(level_3_list,1)
z_3 = element_label(level_3_list,2)

x_4 = element_label(level_4_list,0)
y_4 = element_label(level_4_list,1)
z_4 = element_label(level_4_list,2)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# syntax for 3-D projection
ax = plt.axes(projection ='3d')

# axes sizes (adjusted for best viewing experience)
ax.set_xlim3d(min(x_4), max(x_4))
ax.set_ylim3d(1, 4)
ax.set_zlim3d(0, max(y_4))

# listing each set of level eigenvalues
ax.scatter(x_4, y_4, z_4, zdir='y')
ax.scatter(x_3, y_3, z_3, zdir='y')
ax.scatter(x_2, y_2, z_2, zdir='y')
ax.scatter(x_1, y_1, z_1, zdir='y')

# graph labeling
ax.set_title('Spectrum Distribution')
ax.set_xlabel('Eigenvalue')
ax.set_zlabel('Multiplicity')
ax.set_ylabel('Level of Schreier Graph')
plt.show()
