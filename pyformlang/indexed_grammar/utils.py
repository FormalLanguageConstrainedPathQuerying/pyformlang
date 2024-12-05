""" Utility for indexed grammars """

# pylint: disable=cell-var-from-loop

from typing import Callable, List, Set, Iterable, Any


def exists(list_elements: List[Any],
           check_function: Callable[[Any], bool]) -> bool:
    """exists
    Check whether at least an element x of l is True for f(x)
    :param list_elements: A list of elements to test
    :param check_function: The checking function (takes one parameter and  \
    return a boolean)
    """
    for element in list_elements:
        if check_function(element):
            return True
    return False


def addrec_bis(l_sets: Iterable[Any],
               marked_left: Set[Any],
               marked_right: Set[Any]) -> bool:
    """addrec_bis
    Optimized version of addrec
    :param l_sets: a list containing tuples (C, M) where:
        * C is a non-terminal on the left of a consumption rule
        * M is the set of the marked set for the right non-terminal in the
        production rule
    :param marked_left: Sets which are marked for the non-terminal on the
    left of the production rule
    :param marked_right: Sets which are marked for the non-terminal on the
    right of the production rule
    """
    was_modified = False
    for marked in list(marked_right):
        l_temp = [x for x in l_sets if x[0] in marked]
        s_temp = [x[0] for x in l_temp]
        # At least one symbol to consider
        if frozenset(s_temp) == marked and len(marked) > 0:
            was_modified |= addrec_ter(l_temp, marked_left)
    return was_modified


def addrec_ter(l_sets: List[Any], marked_left: Set[Any]) -> bool:
    """addrec
    Explores all possible combination of consumption rules to mark a
    production rule.
    :param l_sets: a list containing tuples (C, M) where:
        * C is a non-terminal on the left of a consumption rule
        * M is the set of the marked set for the right non-terminal in the
        production rule
    :param marked_left: Sets which are marked for the non-terminal on the
    left of the production rule
    :return Whether an element was actually marked
    """
    # End condition, nothing left to process
    temp_in = [x[0] for x in l_sets]
    exists_after = [
        exists(l_sets[index + 1:], lambda x: x[0] == l_sets[index][0])
        for index in range(len(l_sets))]
    exists_before = [l_sets[index][0] in temp_in[:index]
                     for index in range(len(l_sets))]
    marked_sets = [l_sets[index][1] for index in range(len(l_sets))]
    marked_sets = [sorted(x, key=lambda x: -len(x)) for x in marked_sets]
    # Try to optimize by having an order of the sets
    sorted_zip = sorted(zip(exists_after, exists_before, marked_sets),
                        key=lambda x: -len(x[2]))
    exists_after, exists_before, marked_sets = \
        zip(*sorted_zip)
    res = False
    # contains tuples of index, temp_set
    to_process = [(0, frozenset())]
    done = set()
    while to_process:
        index, new_temp = to_process.pop()
        if index >= len(l_sets):
            # Check if at least one non-terminal was considered, then if the
            # set of non-terminals considered is marked of the right
            # non-terminal in the production rule, then if a new set is
            # marked or not
            if new_temp not in marked_left:
                marked_left.add(new_temp)
                res = True
            continue
        if exists_before[index] or exists_after[index]:
            to_append = (index + 1, new_temp)
            to_process.append(to_append)
        if not exists_before[index]:
            # For all sets which were marked for the current consumption rule
            for marked_set in marked_sets[index]:
                if marked_set <= new_temp:
                    to_append = (index + 1, new_temp)
                elif new_temp <= marked_set:
                    to_append = (index + 1, marked_set)
                else:
                    to_append = (index + 1, new_temp.union(marked_set))
                if to_append not in done:
                    done.add(to_append)
                    to_process.append(to_append)
    return res
