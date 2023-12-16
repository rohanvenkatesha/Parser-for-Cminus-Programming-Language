# Parser-for-Cminus-Programming-Language

Language Specification:
Language Specification: The self-designed language is called cminus and it has the following features:
• It is a case-sensitive language that uses ASCII characters.
• It supports only two data types: basic type int and a standard data type float.
• It supports arithmetic, logical, relational, and assignment operators.
• It supports if-else, while, and compound statements for control flow.
• It supports single-line and multi-line comments that start with /* and end with */
• It supports identifiers that start with a letter and can contain alphanumeric characters.
• It supports literals that are enclosed in single quotes for strings, and supports only decimal notation for 
floating point numbers.
• It supports keywords that are reserved for the language and cannot be used as identifiers. The keywords
are: int, float, if, else, exit, while, read, write, and return.
Ply is a Python library that provides a set of tools to write lexical and syntactic analyzers. You will now add the 
parsing code to generate parse tree (abstract syntax tree - AST) of the given cminus code snippet.
You can use the following hints to write the parser rules:
• Use the p_<name> function syntax to define a rule. The <name> part should match the 
corresponding non-terminal in the grammar.
• Use the p[0], p[1], …, p[n] syntax to access the symbols on the right-hand side of the rule. The p[0] symbol 
is the result of the rule.
• Use the p.slice[n] syntax to access the token object of the n-th symbol. The token object has attributes 
such as type, value, lineno, and lexpos.
• Use the p_error function to handle syntax errors. The function takes a single argument which is the token 
object where the error occurred. You can print an error message and skip the rest of the input.
• Use the yacc function to create the parser object. You can pass the lexer object and the start symbol as 
arguments.
