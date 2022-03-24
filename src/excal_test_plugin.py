from excal.visitor import NodeVisitor
from excal.pluginManager import PluginManager
from excal.astNode import AstNode
from excal.offence import Offence

from typing import Generator
from typing import Tuple
from clang.cindex import CursorKind


PLUGIN_NAME = "testPluginPackage"


class customVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()

    def visit_var_decl(self, node: AstNode) -> Generator[Offence, None, None]:
        if node.parent.kind == CursorKind.TRANSLATION_UNIT:
            yield Offence(node.filename, node.location, "No global Variables.", "ERR100")

    def visit_decl_stmt(self, node: AstNode) -> Generator[Offence, None, None]:
        for sib in node.get_older_Siblings():
            if sib.kind != CursorKind.DECL_STMT:
                yield Offence(node.filename, node.location, "Declare all variables at top of scope.", "ERR101")
        return


def register(pm: PluginManager):
    pm.register(PLUGIN_NAME, customVisitor)
