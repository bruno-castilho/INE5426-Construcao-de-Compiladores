"""
Bruno da Silva Castilho;
Leonardo Seishi Yamazaki;
Rafael Francisco Réus;
Rafael Begnini de Castilhos.
"""
import uuid
from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Tuple, Any, Deque
from enum import Enum, auto


class DataType(Enum):
    FUNC = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    NULL = auto()


@dataclass
class TreeNode:
    def __init__(
        self,
        left: Optional["TreeNode"],
        right: Optional["TreeNode"],
        value: Optional[Union[str, int, float]],
        res_type: str,
    ):
        self.id = uuid.uuid4()

        self.value = value
        self.left = left
        self.right = right
        self.res_type = res_type

    def as_dict(self):
        left = None if self.left is None else self.left.as_dict()
        right = None if self.right is None else self.right.as_dict()

        return {
            "value": self.value,
            "right": right,
            "left": left,
        }

    def __str_(self):
        return f"TreeNode id= {self.id} with value {self.value};"


@dataclass
class EntryTable:
    IDENT: str
    datatype: str
    values: List[int]
    lineno: int

    def as_dict(self):
        return {
            "IDENT": self.IDENT,
            "datatype": self.datatype,
            "values": self.values,
            "lineno": self.lineno,
        }


class Scope:
    def __init__(self, outer_scope=None, loop=False):
        self.entry_table: List[EntryTable] = []
        self.outer_scope: Optional[Scope] = outer_scope
        self.inner_scopes: List = []
        self.loop: bool = loop

    def __str__(self):
        return str(entry for entry in self.entry_table)

    def add_entry(self, entry: EntryTable):
        has_var, lineno = self.contains_var(entry.IDENT)

        if has_var:
            raise VariableInScopeError(f"Variável {entry.IDENT} na linha {entry.lineno} já foi declarada na linha {lineno}")
        self.entry_table.append(entry)

    def add_inner_scope(self, scope: Any):
        self.inner_scopes.append(scope)

    def contains_var(self, var_IDENT: str) -> Tuple[bool, Union[int, None]]:
        for entry in self.entry_table:
            if entry.IDENT == var_IDENT:
                return True, entry.lineno
        return False, None

    def as_dict(self):
        return {
            "table": [entry.as_dict() for entry in self.entry_table],
            "inner_scopes": [scope.as_dict() for scope in self.inner_scopes],
        }


class ScopeStack:
    def __init__(self):
        self.stack: Deque[Scope] = deque()

    def __len__(self):
        return len(self.stack)

    def is_epsilon(self):
        return True if len(self.stack) == 0 else False

    def length(self):
        return len(self.stack)

    def push(self, x: Scope):
        self.stack.append(x)

    def pop(self) -> Scope:
        return self.stack.pop()

    def seek(self) -> Optional[Scope]:
        if self.is_epsilon():
            return None
        else:
            return self.stack[-1]
