from ctypes.wintypes import FLOAT
from constants import *

####################### Classes #########################

class AST:
    pass

class NoOp(AST):
    pass

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.type = self.op = op
        self.right = right

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Program(AST):
    def __init__(self, statements):
        self.statements = statements

class Statements(AST):
    def __init__(self, children):
        self.children = children

########################################################

class Parser:
    def __init__(self, lexer):
        '''
        Accepts a string input from the client as text,
        and maintains an index into text and the
        current token instance.
        '''
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        '''
        If the current token matches the passed in
        token type, eat it and update self.current_token
        Otherwise, raise error.
        '''
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def error(self):
        raise Exception('Invalid syntax')

    def parse(self):
        root = self.program()
        if self.current_token.type != EOF:
            self.error()
        return root

    def program(self):
        '''
        program: statements
        '''
        statements = self.statements()
        return Program(statements)


    def statements(self):
        '''
        statements: statement | statement SEMI statements
        '''
        results = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return Statements(results)


    def statement(self):
        '''
        statement: compound_statement | assignment_statement | empty
        '''
        if self.current_token.type == ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def assignment_statement(self):
        '''
        assigment_statement: variable ASSIGN factor SEMI
        '''
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, token, right)

    def variable(self):
        '''
        variable: ID
        '''
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        '''
        empty:
        '''
        return NoOp()

    def expr(self):
        '''
        Parses the text and returns the expression.

        expr: term ((PLUS | MINUS) term)*
        '''
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def term(self):
        '''
        Returns the AST term starting at current_token and eats values as necessary

        term: factor ((MUL | DIV) factor)*
        '''
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        '''
        Returns the factor AST that is current_token and
        eats the current_token

        factor : INTEGER | variable
        '''
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        else:
            node = self.variable()
            return node