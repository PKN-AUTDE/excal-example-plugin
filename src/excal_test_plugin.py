from visitor import NodeVisitor
from pluginManager import PluginManager
from astNode import AstNode

from typing import Generator
from typing import Tuple
from clang.cindex import CursorKind


PLUGIN_NAME = "testPluginPackage"

class customVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()

    def visit_var_decl(self, node: AstNode) -> Generator[Tuple[str, int, int, str], None, None]:
        if node.parent.kind == CursorKind.TRANSLATION_UNIT:
            yield node.location.filename, node.location.line, node.location.col, \
                "ERR100 No global Variables."


def register(pm: PluginManager):
    pm.register(PLUGIN_NAME, customVisitor)
