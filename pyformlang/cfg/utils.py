""" Internal Usage only """

from typing import Dict, List, Iterable, AbstractSet

from ..objects.cfg_objects import CFGObject, Variable, Epsilon, Production


def remove_nullable_production_sub(body: List[CFGObject],
                                   nullables: AbstractSet[CFGObject]) \
        -> List[List[CFGObject]]:
    """ Recursive sub function to remove nullable objects """
    if not body:
        return [[]]
    all_next = remove_nullable_production_sub(body[1:], nullables)
    res = []
    for body_temp in all_next:
        if body[0] in nullables:
            res.append(body_temp)
        if body[0] != Epsilon():
            res.append([body[0]] + body_temp.copy())
    return res


def remove_nullable_production(production: Production,
                               nullables: AbstractSet[CFGObject]) \
        -> List[Production]:
    """ Get all combinations of productions rules after removing nullable """
    next_prod_l = remove_nullable_production_sub(production.body,
                                                 nullables)
    res = [Production(production.head, prod_l)
           for prod_l in next_prod_l
           if prod_l]
    return res


def get_productions_d(productions: Iterable[Production]) \
        -> Dict[Variable, List[Production]]:
    """ Get productions as a dictionary """
    productions_d: Dict[Variable, List[Production]] = {}
    for production in productions:
        production_head = productions_d.setdefault(production.head, [])
        production_head.append(production)
    return productions_d
