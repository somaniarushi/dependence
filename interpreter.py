from constants import *

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}
        self.running_var = None
        self.mapping = {}

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_Program(self, node):
        self.visit(node.statements)

    def visit_Statements(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.running_var = var_name
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        self.running_var = None

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            # graph generator
            if self.running_var != None: self.add_mapping(var_name)
            return val

    # for graph generation
    def add_mapping(self, var):
        if self.running_var in self.mapping:
            self.mapping[self.running_var].append(var)
        else:
            self.mapping[self.running_var] = [var]

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self, node):
        return node.value
