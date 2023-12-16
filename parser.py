#run this line in the terminal, if there is no ply package installed
#pip install ply

import ply.lex as lex
import ply.yacc as yacc

def print_tree(node, indent=0):
    if isinstance(node, list):
        for item in node:
            print_tree(item, indent)
    elif isinstance(node, dict):
        for key, value in node.items():
            print('| ' * indent + f"{key}:")
            print_tree(value, indent + 1)
    else:
        print('| ' * indent + f": {node}")

# List of token names
tokens = ['IDENTIFIER','INTCON','FLOATCON','STRING','PLUS','MINUS','TIMES','DIVIDE','ASSIGN','EQ','NE','LE','LT','GE','GT','AND','OR','NOT','LP','RP','LBK','RBK','LBR','RBR','SC','CM','IF','ELSE','EXIT','FLOAT','INT','READ','RETURN','WHILE','WRITE']

# Dictionary of keywords
keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'exit': 'EXIT',
    'float': 'FLOAT',
    'int': 'INT',
    'read': 'READ',
    'return': 'RETURN',
    'while': 'WHILE',
    'write': 'WRITE',
}

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LP = r'\('
t_RP = r'\)'
t_LBK = r'\['
t_RBK = r'\]'
t_LBR = r'{'
t_RBR = r'}'
t_SC = r';'
t_CM = r','

# Regular expression rules with actions
def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    # Check if the identifier is a keyword
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

def t_FLOATCON(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTCON(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    t.value = t.value[1:-1]  # remove the quotes
    return t

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define a rule to ignore whitespace and tabs
t_ignore = ' \t'

# Define a rule to handle comments
def t_COMMENT(t):
    r'\/\*[\s\S]*?\*\/|\/\*[\s\S]*$'
    pass

# Error handling rule
def t_error(t):
    print(f"Lexical error: Unexpected character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Grammar rules
def p_Program(p):
    '''Program : DeclList Procedures
               | Procedures'''
    if len(p) == 3:
        p[0] = {'Program': {p[1], p[2]}} # If DeclList is present
    else:
        p[0] = {'Program': p[1]}

def p_Procedures(p):
    '''Procedures : ProcedureDecl Procedures
                  | ProcedureDecl'''
    if len(p) == 3:
        p[0] = {'Procedures':{p[1], p[2]}}  # Concatenate ProcedureDecl with the rest of Procedures
    else:
        p[0] = {'Procedures': p[1]}

def p_ProcedureDecl(p):
    '''ProcedureDecl : ProcedureHead ProcedureBody'''
    p[0] = {'ProcedureDecl': {**p[1], **p[2]}}

def p_ProcedureHead(p):
    '''ProcedureHead : FunctionDecl DeclList
                     | FunctionDecl'''
    if len(p) == 3:
        p[0] = {'ProcedureHead':{**p[1], **p[2]}}
    else:
        p[0] = {'ProcedureHead':p[1]}

def p_FunctionDecl(p):
    '''FunctionDecl : Type IDENTIFIER LP RP LBR'''
    p[0] = {'FunctionDecl': {**p[1], 'Name': p[2], 'LP': p[3], 'RP':p[4], 'LBR':p[5]}}

def p_ProcedureBody(p):
    '''ProcedureBody : StatementList RBR'''
    p[0] = {'ProcedureBody': p[1], 'Right Braces':p[2]}

def p_DeclList(p):
    '''DeclList : Type IdentifierList SC
                | DeclList Type IdentifierList SC'''
    if len(p) == 4:
        p[0] = {'DeclList':{**p[1], **p[2]}, 'Semicolon':p[3]} # Single declaration
    else:
        p[0] = {'DeclList': {p[1], {**p[2], **p[3]}}, 'Semicolon':p[4]}

def p_IdentifierList(p):
    '''IdentifierList : VarDecl
                     | IdentifierList CM VarDecl '''
    if len(p) == 2:
        p[0] = {'IdentifierList': p[1]}  # Single variable declaration
    else:
        p[0] = {**p[1] , **p[3]}


def p_VarDecl(p):
    '''VarDecl : IDENTIFIER
               | IDENTIFIER LBK INTCON RBK'''
    if len(p) == 2:
        p[0] = {'Variable Declaration': p[1]}  # Simple variable declaration
    else:
        p[0] = {'Variable Declaration': p[1], 'Array_size': p[3]}

def p_Type(p):
    '''Type : INT
            | FLOAT'''
    p[0] = {'Type': p[1]}


def p_StatementList(p):
    '''StatementList : Statement
                    | StatementList Statement'''
    if len(p) == 2:
        p[0] = {'StatementList': p[1]}  # Single statement
    else:
        p[0] = {'StatementList': {**p[1], **p[2]}}

def p_Statement(p):
    '''Statement : Assignment
                 | IfStatement
                 | WhileStatement
                 | IOStatement
                 | ReturnStatement
                 | ExitStatement
                 | CompoundStatement'''
    p[0] = {'Statement': p[1]}

def p_Assignment(p):
    '''Assignment : Variable ASSIGN Expr SC'''
    p[0] = {'Assignment':{'variable': p[1], 'ASSIGN': p[2], 'expression': p[3], 'semicolon':p[4]}}

def p_IfStatement(p):
    '''IfStatement : IF Test CompoundStatement
                   | IF Test CompoundStatement ELSE CompoundStatement'''
    if len(p) == 4:
        p[0] = {'IfStatement':{'Condition': p[2], 'Then_body': p[3]}}
    else:
        p[0] = {'If_Else_Statement':{'Condition': p[2], 'Then_body': p[3]}, 'Else_body': p[5]}

def p_Test(p):
    '''Test : LP Expr RP'''
    p[0] = {'Test':{'LP':p[1], 'Expression':p[2], 'RP':p[3]}}

def p_WhileStatement(p):
    '''WhileStatement : WHILE WhileExpr Statement'''
    p[0] = {'WhileStatement': {'While Expression': p[2], 'Statement': p[3]}}

def p_WhileExpr(p):
    '''WhileExpr : LP Expr RP'''
    p[0] = {'WhileExpr': p[2]}

def p_IOStatement(p):
    '''IOStatement : READ LP Variable RP SC
                   | WRITE LP Expr RP SC
                   | WRITE LP StringConstant RP SC'''
    if p[1] == 'read':
        p[0] = {'IOStatement':{'type': 'read_statement', 'LP':p[2], 'variable': p[3], 'RP':p[4], 'Semicolon':p[5]}}
    elif p[1] == 'write' and isinstance(p[3], str):
        p[0] = {'IOStatement':{'type': 'write_statement', 'LP':p[2], 'StringConstant': p[3], 'RP':p[4], 'Semicolon':p[5]}}
    else:
        p[0] = {'IOStatement':{'type': 'write_statement', 'LP':p[2], 'Expression': p[3], 'RP':p[4], 'Semicolon':p[5]}}

def p_ReturnStatement(p):
    '''ReturnStatement : RETURN Expr SC'''
    p[0] = {'ReturnStatement':{'expression': p[2]}}

def p_ExitStatement(p):
    '''ExitStatement : EXIT SC'''
    p[0] = {'ExitStatement': p[1]}


def p_CompoundStatement(p):
    '''CompoundStatement : LBR StatementList RBR'''
    p[0] = {'CompoundStatement': p[2]}

def p_Expr(p):
    '''Expr : Expr AND SimpleExpr
            | Expr OR SimpleExpr
            | SimpleExpr
            | NOT SimpleExpr'''
    if len(p) == 4:
        p[0] = {'Expr':{'operator': p[2], 'left': p[1], 'right': p[3]}}
    elif len(p) == 3:
        p[0] = {'Expr':{'operator': 'NOT', 'expression': p[2]}}
    else:
        p[0] = {'Expr':p[1]}


def p_SimpleExpr(p):
    '''SimpleExpr : SimpleExpr EQ AddExpr
                  | SimpleExpr NE AddExpr
                  | SimpleExpr LE AddExpr
                  | SimpleExpr LT AddExpr
                  | SimpleExpr GE AddExpr
                  | SimpleExpr GT AddExpr
                  | AddExpr'''
    if len(p) == 4:
        p[0] = {'SimpleExpr':{'operator': p[2], 'left': p[1], 'right': p[3]}}
    else:
        p[0] = {'SimpleExpr':p[1]}


def p_AddExpr(p):
    '''AddExpr : AddExpr PLUS MulExpr
               | AddExpr MINUS MulExpr
               | MulExpr'''
    if len(p) == 4:
        p[0] = {'AddExpr':{'operator': p[2], 'left': p[1], 'right': p[3]}}
    else:
        p[0] = {'AddExpr':p[1]}

def p_MulExpr(p):
    '''MulExpr : MulExpr TIMES Factor
               | MulExpr DIVIDE Factor
               | Factor'''
    if len(p) == 4:
        p[0] = {'MulExpr':{'operator': p[2], 'left': p[1], 'right': p[3]}}
    else:
        p[0] = {'MulExpr':p[1]}

def p_Factor(p):
    '''Factor : Variable
              | Constant
              | IDENTIFIER LP RP
              | LP Expr RP'''
    if len(p) == 2:
        p[0] = {'Factor': p[1]}
    elif len(p) == 4:
        p[0] = {'Factor': p[2]}
    else:
        p[0] = {'Factor': p[2]}

def p_Variable(p):
    '''Variable : IDENTIFIER
                | IDENTIFIER LBK Expr RBK'''
    if len(p) == 2:
        p[0] = {'Variable': p[1]}
    else:
        p[0] = {{'Array Variable': p[1], 'Array size': p[3]}}

def p_StringConstant(p):
    '''StringConstant : STRING'''
    p[0] = {'StringConstant': p[1]}

def p_Constant(p):
    '''Constant : INTCON
                | FLOATCON'''
    p[0] = {'Constant': p[1]}

# Error rule for syntax errors
def p_error(p):
    print(f"Syntax error at line {p.lineno}: Unexpected token '{p.value}'")

# Build the parser
parser = yacc.yacc()

def parse_source_code(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            source_code = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    lexer.input(source_code)

    # List to store tokens
    tokens = []

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        tokens.append((tok.type, tok.value))
    print('\n-------------------------------------------------------------')
    print("Lexical Output")
    print('-------------------------------------------------------------\n')
    print(tokens)

    result = parser.parse(source_code, lexer=lexer)

    return result

# Example usage
file_path = r"/workspaces/pa4-parser-vrohan10/source_code_1.cminus"

result_parse=parse_source_code(file_path)

print('\n-------------------------------------------------------------')
print("YACC output")
print('-------------------------------------------------------------\n')
print(result_parse)
print('\n-------------------------------------------------------------')
print("Abstract Syntax Tree")
print('-------------------------------------------------------------\n')
print_tree(result_parse)