''' Products and coproducts in the category of partitions
'''
from .efp import _epi_factorize_partition


def product_of_partitions(xs: list, ys: list) -> list[int]:
  ''' Given two lists of the same length,
      return a canonical factorization of their zip.

      ```
      (x1, y1) == (x2, y2) iff x1 == x2 and y1 == y2
      ```
  ```
  product_of_partitions('111123', 'abcccc')
  >>> [0, 1, 2, 2, 3, 4]
  ```

  '''
  assert len(xs) == len(ys), "Lengths must match"
  return _epi_factorize_partition(list(zip(xs, ys)))


def coproduct_of_partitions(xs: list, ys: list) -> list[int]:
  ''' Given two lists of the same length,
      return their coproduct (or join) as partitions,
      specifically the quotient of the join of their preimages.

      ```
      (x1, y1) == (x2, y2) iff x1 == x2 or y1 == y2
      ```
  '''
  from . import Partition, partition_from_list, join_partitions, FAST
  assert len(xs) == len(ys), "Lengths must match"
  # Return the coproduct of two partitions as the quotient of the
  # equivalence relation induced by the join of two partitions' preimages.
  join = Partition(join_partitions(
    partition_from_list(xs),
    partition_from_list(ys),
    FAST
  ))
  return join.quotient()


def __product_impl2(xs: list, ys: list) -> list[int]:
  classes = []
  idxs = []
  for x1, y1 in zip(xs, ys):
    for i, cls in enumerate(classes):
      if any(x1 == x2 and y1 == y2 for (x2, y2) in cls):
        cls.append((x1, y1))
        idxs.append(i)
        break
    else:
      idxs.append(len(classes))
      classes.append([(x1, y1)])
  return idxs


def __coproduct_impl2(xs: list, ys: list) -> list[int]:
  classes = []
  idxs = []
  for x1, y1 in zip(xs, ys):
    for i, cls in enumerate(classes):
      if any(x1 == x2 or y1 == y2 for (x2, y2) in cls):
        cls.append((x1, y1))
        idxs.append(i)
        break
    else:
      idxs.append(len(classes))
      classes.append([(x1, y1)])
  return idxs


def __test():
  assert   product_of_partitions('111123', 'abcccc') == [0, 1, 2, 2, 3, 4]
  assert coproduct_of_partitions('111123', 'abcccc') == [0, 0, 0, 0, 0, 0]
  assert         __product_impl2('111123', 'abcccc') == [0, 1, 2, 2, 3, 4]
  assert       __coproduct_impl2('111123', 'abcccc') == [0, 0, 0, 0, 0, 0]  


__test()