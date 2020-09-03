
import math
import sys

def is_digit(char):
    if char in '0123456789':
        return True
    return False

def is_letter(char):
    if char.lower() in 'qwertyuiopasdfghjklzxcvbnm_':
        return True
    return False

class Lexer:

    def __init__(self):
        '''
            Get the file name and read it
        '''
        if len(sys.argv) != 1:
            try:
                with open(sys.argv[1]) as f:
                    self.text = f.read()
            except:
                print(f'File {sys.argv[1]} not found!')
                exit()
        self.EOF = len(self.text)-1 # End of file
        self.pos = 0 # Position
        self.tokens = [] # All tokens
    
    def parse(self):
        comment = False
        while True:
            #print(self.pos)
            if self.pos == self.EOF:
                if not comment:
                    if is_letter(self.text[self.pos]):
                        self.tokens.append((self.get_word()))
                    elif is_digit(self.text[self.pos]):
                        self.tokens.append((self.get_number()))
                break
            if self.pos >= self.EOF:
                break
            if is_letter(self.text[self.pos]):
                if not comment:
                    self.tokens.append(self.get_word())
                    self.pos += 1
            elif is_digit(self.text[self.pos]):
                if not comment:
                    self.tokens.append(self.get_number())
            elif self.text[self.pos] == '+':
                if not comment:
                    self.tokens.append(('ADD','+'))
                    self.pos += 1
            elif self.text[self.pos] == '-':
                if not comment:
                    self.tokens.append(('SUB','-'))
            elif self.text[self.pos] == '*':
                if not comment:
                    self.tokens.append(('MUL','*'))
            elif self.text[self.pos] == '/':
                if not comment:
                    self.tokens.append(('DIV','/'))
            elif self.text[self.pos] == '=':
                if not comment:
                    self.tokens.append(('CREATE_VAR',''))
            elif self.text[self.pos] == '"':
                if not comment:
                    self.tokens.append(self.get_string())
                    self.pos += 1
            elif self.text[self.pos] == '#':
                comment = True
            elif self.text[self.pos] == '\n':
                comment = False
            else:
                self.pos += 1

    def get_word(self):
        start = self.pos
        if self.pos != self.EOF:
            self.pos += 1
        while True:
            if self.pos == self.EOF or not is_letter(self.text[self.pos]):
                if self.pos == self.EOF:
                    if is_letter(self.text):
                        return ('WORD',self.text[start:])
                    return ('WORD',self.text[start:self.pos])
                else:
                    return ('WORD',self.text[start:self.pos])
            self.pos += 1

    def get_number(self):
        start = self.pos
        self.pos += 1
        while True:
            if self.pos >= self.EOF or not is_digit(self.text[self.pos]):
                if self.pos == self.EOF:
                    if is_digit(self.text[self.pos]):
                        return ('NUMBER',self.text[start:])
                    else:
                        return ('NUMBER',self.text[start:self.pos])
                else:
                    return ('NUMBER',self.text[start:self.pos])
            self.pos += 1

    def get_string(self):
        self.pos += 1
        t = ''
        s = self.pos
        while True:
            if self.pos == self.EOF or self.text[self.pos] == '"':
                if self.pos == self.EOF:
                    break
                elif self.text[self.pos] == '"':
                    if self.text[self.pos-1] == '\\':
                        t += '"'
                    else:
                        break
            t += self.text[self.pos]
            self.pos += 1
        return ('STRING',t)

class Parser:

    def __init__(self,tokens):
        self.tokens = tokens

    def parse(self):
        i = 0
        eof = len(self.tokens)
        vars = {}
        functions = ['print','println']
        #print(self.tokens)
        while True:
            t = ''
            if i >= eof:
                break
            if self.tokens[i][0] == 'WORD':
                #print(self.tokens[i][1])
                if self.tokens[i][1] == 'print':
                    i += 1 # Ignore ('WORD','print')
                    while True:
                        if i >= eof:
                            break
                        if self.tokens[i][0] == 'STRING':
                            print(self.tokens[i][1],end='')
                        elif self.tokens[i][0] == 'NUMBER':
                            while self.tokens[i][0] in ['NUMBER','ADD']:
                                t += self.tokens[i][1]
                                i += 1
                                if i >= eof:
                                    break
                            print(eval(t),end='')
                        elif self.tokens[i][0] == 'WORD':
                            try:
                                _ = vars[self.tokens[i][1]]
                            except:
                                print('Syntax error: \n  Word not reserved:',self.tokens[i])
                                exit()
                            print(vars[self.tokens[i][1]],end='')
                        i += 1
                elif self.tokens[i][1] == 'println':
                    i += 1 # Ignore ('WORD','println')
                    eval_ = False
                    while True:
                        if i >= eof:
                            break
                        if self.tokens[i][0] == 'STRING':
                            print(self.tokens[i][1],end='')
                        elif self.tokens[i][0] == 'NUMBER':
                            while self.tokens[i][0] in ['NUMBER','ADD']:
                                t += self.tokens[i][1]
                                i += 1
                                if i >= eof:
                                    break
                            print(eval(t),end='')
                        elif self.tokens[i][0] == 'WORD':
                            try:
                                _ = vars[self.tokens[i][1]]
                            except:
                                print('Syntax error: \n  Word not reserved:',self.tokens[i])
                                exit()
                            print(vars[self.tokens[i][1]],end='')
                        i += 1
                    print() # Because 'println'
            elif self.tokens[i][0] == 'CREATE_VAR':
                vars.update({self.tokens[i-1][1]:self.tokens[i+1][1]})
                i += 1
            i += 1
        print('==========')
        print('vars:\n',vars)
        print('tokens:\n',self.tokens)
        print('==========')

Lexer = Lexer()
Lexer.parse()

Parser = Parser(Lexer.tokens).parse()
