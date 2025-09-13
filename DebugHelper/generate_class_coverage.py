#! /usr/bin/env python3
#
# Generate C++ code with 106B collection classes of various elem type
# Authored by Jeremy Barenholz & Julie Zelenski

import copy
from typing import List, Optional, Any

TYPEDEFS = '''
using namespace std;

#if defined(__APPLE__)
#define BREAKPOINT __builtin_debugtrap(); cout << "BREAK @" << __LINE__ << endl;
#elif defined(_WIN32)
#define BREAKPOINT __debugbreak(); cout << "BREAK @" << __LINE__ << endl;
#endif

struct Thing {
    int num;
    string label;
};
int hashCode(const Thing& t) {
    return t.num;
}
bool operator ==(const Thing& t1, const Thing& t2) {
    return t1.num == t2.num && t1.label == t2.label;
}
bool operator <(const Thing& t1, const Thing& t2) {
    return stanfordcpplib::collections::compareTo(t1.num, t2.num, t1.label, t2.label) < 0;
}

struct Node {
    char letter;
    Node *left, *right;
};

'''

MAIN_PROGRAM = '''
int main() {
    stanford_linear();
    stanford_hash();
    stanford_tree();
    stanford_other();
    fixed_tests();
    return 0;
}
'''

class Type:
    def __init__(
        self,
        inner: 'Type',
        container: Optional['Type'] = None,
        first: Optional['Type'] = None
    ) -> None:
        self.inner = inner
        self.container = container
        self.first = first

    def varname(self) -> str:
        if not self.container and not self.first:
            return f'{self.inner}'
        elif not self.first:
            return f'{self.container}_{self.inner.varname()}'
        else:
            return (f'{self.container}_{self.first.varname()}'
                    f'_{self.inner.varname()}')

    def __str__(self) -> str:
        if not self.container and not self.first:
            return f'{self.inner}'
        elif not self.first:
            return f'{self.container}<{self.inner}>'
        else:
            return f'{self.container}<{self.first}, {self.inner}>'

    def __repr__(self) -> str:
        return f'Type({str(self)})'

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __hash__(self) -> int:
        return hash(str(self))

linear_containers = ['Deque', 'Grid', 'Queue','Stack','Vector', ]
hash_containers = ['HashMap', 'HashSet', ]
tree_containers = ['Map', 'Set', ]
other_containers = [ 'PriorityQueue',]
all_stanford = linear_containers + hash_containers + tree_containers + other_containers

basic_types = [
    'bool',
    'char',
    'double',
    'int',
    'string',
    'GridLocation',
    'Thing'
]

basic_values = {
    'bool': ['false', 'true'],
    'char': [f"'{c}'" for c in 'bB'],
    'double': [str(d) for d in [3.14159, -0.25]],
    'int': [str(i) for i in [106, 1891]],
    'string': [f'"{s}"' for s in ['stanford', 'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']],
    'GridLocation': [f'{{{r}, {c}}}' for r,c in [(3,14)]],
    'Thing': [f'(Thing){{{len(s)}, "{s}"}}' for s in ['purple']]}

def create_init_list_str(type: Type) -> str:
    if type.container == 'Grid':
        n_rows = 3
        inner_parts = ['{' + f"{', '.join(basic_values[type.inner])}" + '}'
                       for i in range(n_rows)]
    elif type.container == 'PriorityQueue' and not type.first:
        new_type = copy.copy(type)
        new_type.first = Type('int')
        return create_init_list_str(new_type)
    elif type.first:
        n = min(len(basic_values[type.inner]), len(basic_values[type.first]))
        inner_parts = [
            '{'
            + f'{basic_values[type.first][i]}, {basic_values[type.inner][i]}'
            + '}'
            for i in range(n)
        ]
    else:
        inner_parts = basic_values[type.inner]

    return '{' + f"{', '.join(inner_parts)}" + '}'

def types_for_container(outer) -> List[Type]:
    types = []
    for inner in [Type(b) for b in basic_types]:
        if outer.endswith('Map'):
            for key in basic_types:
                types.append(Type(inner, outer, Type(key)))
        else:
            types.append(Type(inner, outer))
    return types

def source_for_all(fn_name, containers) -> str:
    lines = [f"void {fn_name}() {{"]
    for outer in containers:
        lines += ['\t{'] + [
        '\t\t'
        + ' '.join([str(t), t.varname().lower(), '=', create_init_list_str(t) + ';'])
        for t in types_for_container(outer)] + ['\t\tBREAKPOINT;\n\t}']
    lines += ["}\n\n"]
    return '\n'.join(lines)

def generate_program() -> str:
    includes = [c.lower() + '.h' for c in all_stanford + ['bits']]
    program = '\n'.join([f'#include "{f}"' for f in includes])
    program += TYPEDEFS
    program += source_for_all("stanford_linear", linear_containers)
    program += source_for_all("stanford_hash", hash_containers)
    program += source_for_all("stanford_tree", tree_containers)
    program += source_for_all("stanford_other", other_containers)
    with open('fixed_tests') as f: fixed = f.read()
    return program + fixed + MAIN_PROGRAM

if __name__ == '__main__':
    print(generate_program())
