from constants import *

class Token:
    def __init__(self, type, value):
        '''
        Accepts and saves the type and value of the token.
        '''
        self.type = type
        self.value = value

    def __repr__(self):
        '''
        String representation of an object.
        '''
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, text):
        '''
        Accepts a string input from the client as text,
        and maintains an index into text, the current char and the
        current token instance.
        '''
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        '''
        Raises parsing error.
        '''
        raise Exception('Invalid character')

    def advance(self):
        '''
        Advance the self.pos pointer, and
        update self.current_char
        '''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # EOF
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        '''
        Advances through the string over
        all whitespace starting at current_char
        '''
        # while we see a space and we haven't reached
        # the end of the file
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self):
        '''
        Returns the next element of the input buffer,
        or None if EOF.
        '''
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def _id(self):
        '''
        Handles identifiers and reserved keywords.
        '''
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token(ID, result)


    def number(self):
        '''
        Return the number consumed from the input — multi-digit integer or float.
        The pointer and current_char is updated
        '''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token(INTEGER, int(result))

    def get_next_token(self):
        '''
        Tokenizer (AKA scanner or lexical analyzer).
        Breaks the text input into tokens and returns
        them one at a time.
        '''
        # while we haven't reached end of file
        while self.current_char is not None:

            current_char = self.current_char

            # whitespace
            if current_char.isspace():
                self.skip_whitespace()
                continue

            # keyword
            elif self.current_char.isalpha():
                return self._id()

            # assignment operator
            elif self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            else:
                self.error()

        return Token(EOF, None)
