from excal.visitor import NodeVisitor
from excal.pluginManager import PluginManager
from excal.astNode import AstNode

from typing import Generator
from typing import Tuple
from clang.cindex import CursorKind


PLUGIN_NAME = "testPluginPackage"


class customVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()

    def visit_var_decl(self, node: AstNode) -> Generator[Tuple[str, int, int, str], None, None]:
        if node.parent.kind == CursorKind.TRANSLATION_UNIT:
            yield node.filename, node.location.line, node.location.col, \
                "ERR100 No global Variables."

    def visit_decl_stmt(self, node: AstNode) -> Generator[Tuple[str, int, int, str], None, None]:
        for sib in node.get_older_Siblings():
            if sib.kind != CursorKind.DECL_STMT:
                yield node.filename, node.location.line, node.location.col, \
                    "ERR101 Declare all variables at top of scope."
        return


def register(pm: PluginManager):
    pm.register(PLUGIN_NAME, customVisitor)
