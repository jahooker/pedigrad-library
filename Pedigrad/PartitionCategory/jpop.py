from Pedigrad.utils import nub


def join_partitions(
  parts1: list[list[int]],
  parts2: list[list[int]],
) -> list[list[int]]:
  '''
  Given two lists, each of disjoint sets of indices in some range,
  return the list of the maximal unions of internal lists
  that intersect within the concatenation of the two input lists (see below).
  '''
  assert {x for xs in parts1 for x in xs} == {x for xs in parts2 for x in xs}
  # Make copies so as not to modify the inputs
  # and eliminate repeats in each part:
  tmp1 = [nub(xs) for xs in parts1]
  tmp2 = [nub(xs) for xs in parts2]
  for xs1 in tmp1:
    # Get the union of xs1 with every part in tmp2 that intersects it
    for x1 in xs1:
      for i, xs2 in enumerate(tmp2):
        if any(x1 == x2 for x2 in xs2):
          xs1 = nub(xs1 + tmp2.pop(i))  # The union of xs1 and xs2
          # Assume x1 occurs nowhere else in tmp2
          assert x1 not in (x for xs in tmp2 for x in xs)
          break
    # Append the union to tmp2
    tmp2.append(xs1)
  return tmp2


def overlap(xs, ys):
  return any(x in ys for x in xs)


def overlap_trans(A, C, S):
  ''' Do `A` and `C` overlap transitively
      (possibly via a chain of overlapping lists in `S`)?
      `A` and `C` needn't be in `S`.
  '''
  return overlap(A, C) or \
  any(overlap_trans(B, C, [D for D in S if D not in (A, B, C)])
  for B in S if B != A and overlap(A, B))


def check(f):
  def f2(A, S):
    result = f(A, S)
    assert     all(overlap_trans(A, C, S) for C in result)
    assert not any(overlap_trans(A, C, S) for C in [X for X in S if X not in result])
    return result
  return f2


@check
def all_that_overlap_trans(A: list, parts: list[list]) -> list[list]:
  ''' Return the lists in `parts` that intersect `A`,
      whether directly or through a chain of other lists.
  '''
  pos, neg = [], []
  for B in parts:
    # if B != A:
      (pos if overlap(A, B) else neg).append(B)
  return sum((all_that_overlap_trans(B, neg) for B in pos), pos)


# Equivalent to (earlier implementation of) join_partitions(S, S)
def join_trans(*parts: list[list]) -> list[list]:
  ''' Join `parts` transitively.
  '''
  # return nub(tuple(nub(sum(sorted(all_that_overlap_trans(A, S)), []))) for A in S)
  J = []
  for part in parts:
    x = nub(sum(sorted(all_that_overlap_trans(part, parts)), []))
    if x not in J:
      J.append(x)
  return J


def __test():
  p1 = [[0, 3], [1, 4], [2]]    # e.g. partition_from_list('abcab')
  p2 = [[0, 1], [2], [3], [4]]  # e.g. partition_from_list('aabcd')
  assert join_partitions(p1, p2) == [[1, 4, 0, 3], [2]]
  assert join_trans(*p1, *p2) == [[0, 1, 3, 4], [2]]
  S = [[1, 2], [3, 4], [5, 6], [4, 5], [2, 3]]
  assert (x := sorted(map(sorted, join_trans(*S)))) == [[1, 2, 3, 4, 5, 6]], x
  # assert (x := sorted(map(sorted, join_partitions(S, S)))) == [[1, 2, 3, 4, 5, 6]], x
  assert (x := all_that_overlap_trans([1, 2], S)) == [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]], x
  assert (x := sorted([A for A in S if overlap_trans(A, [1], S)])) == [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]], x


__test()
