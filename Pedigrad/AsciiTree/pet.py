#------------------------------------------------------------------------------
#print_evolutionary_tree(partitions): standard output
#------------------------------------------------------------------------------
from .top import tree_of_partitions
from .ctta import convert_tree_to_atpf
from .cata import convert_atpf_to_atf
from .patf import print_atf


def print_evolutionary_tree(partitions):
  '''
  This function takes a list of partitions between which a sequence of composable morphisms exists and returns the tree encoded by this sequence of morphisms.

  '''
  #Returns a sequence of morphisms of partitions.
  tree = tree_of_partitions(partitions)
  #Returns an ascii tree pre-format and its depth.
  atpf = convert_tree_to_atpf(tree)
  #Returns the ascii tree format of the atpf.
  atf = convert_atpf_to_atf(*atpf)
  #Prints the atf on the standard output.
  print_atf(atf, atpf[1])
