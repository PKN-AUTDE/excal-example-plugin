# EXCAL example plugin
This is an example plugin for the [EXCAL project](https://github.com/PKN-AUTDE/excal). It will check if a source files uses a global variable and raise an error.


## Creating your own Plugins

A very simple Plugin will only need a single class which inherits from excal.NodeVisitor and calls super().__init__(). 



```
class Plugin(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
```
From here the class can implement as many visit functions as wished. EXCAL will walk through the abstract syntax tree (AST)and call the corresponding visit functions of all Plugins. The visit functions follow the naming scheme of their corresponding Nodes in the Clang AST. To see the AST of an file just execute excal with the -p flag and the AST will be printed.


```
excal -f path/to/file.c -i path/to/includes -p
```

Each error found by the visitor functions needs to be yielded.
Feel free to user your own style of error message, at the moment we go with the style of flake8 of providing an id in the form of a 3 letter Code followed by a number.

```
    # visitor function of the Plugin class. gets called when a corresponding node (in this case VAR_DECL) gets visited in the AST
    def visit_var_decl(self, node: AstNode) -> Generator[Offence, None, None]:
    if foundError:
        yield Offence(node.filenamem, node.loaction, "Errormessage", "ERR100")

    # special function, will get called after the AST ends.
    def final_call():
        return
```

EXCAL will need to register the plugin to know how to call it. Therefore add a register function like the following (outside the Plugin class): 

```
def register(pm: PluginManager):
    pm.register(PLUGIN_NAME, Plugin)
```

For EXCAL to find the Plugin you can either place it in the excal/excal/plugins folder and add it to the excal/plugins.json file, or you can build the plugin as its own package and add an entry Point like this:

```
[options.entry_points]
excal_plugins =
    testPlugin = excal_test_plugin:register
```
