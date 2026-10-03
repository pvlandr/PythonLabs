import re
from decimal import Decimal

from toolkit.errors import *

TOKEN_NUMBER = "NUM"
TOKEN_OPERATOR = "OP"

operator_characters = ["+", "-", "*", "/"]
operators = ["+", "-", "*", "/"]
operators.sort(key=len, reverse=True)

priority = {
    "+": 1,
    "-": 1,

    "*": 2,
    "/": 2
}

def evaluate(expr: str):
    """Вычесляет выражение"""
    tokens = tokenize(expr)
    # print(tokens)

    return calculate(tokens)

def apply_operator(num1: int | Decimal, num2: int | Decimal, operator: str):
    """Применяет бинарный оператор к двум числам"""
    match(operator):
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            if(num2 == 0):
                raise EvaluationError("Division by zero")
            
            return Decimal(num1) / Decimal(num2)

    raise ValueError(f"Invalid operator: {operator}")

def tokenize(expr: str) -> list[tuple[str,any]]:
    """Токенизирует выражение"""
    expr = expr.strip()
    i = 0
    tokens: list[tuple[str,any]] = []
    state = 0

    if(len(expr) == 0):
        raise ExpressionError("Expression is empty")

    while(i < len(expr)):
        ch = expr[i]

        if(ch.isspace()):
            pass
        elif(state == 0):
            i, number = read_number(expr, i)
            tokens.append((TOKEN_NUMBER, number))

            # switch to operators
            state = 1
        elif(state == 1):
            i, operator = read_operator(expr, i)
            tokens.append((TOKEN_OPERATOR, operator))

            # switch to numbers
            state = 0
            
        i += 1

    return tokens

def read_number(expr: str, i: int) -> tuple[int, int | Decimal]:
    """Читает число или строку из выражения, включая знак"""
    is_negative = False

    # read sign
    while(i < len(expr)):
        ch = expr[i]

        if(ch == "-"):
            is_negative = not is_negative
        elif(ch == "+"):
            pass
        else:
            break

        i += 1

    number: int | Decimal
    if(expr[i] == "("):
        i, number = read_bracket(expr, i)
    else:
        i, number = read_number_literal(expr, i)

    if(is_negative):
        number *= -1
    
    return i, number

def read_number_literal(expr: str, i: int) -> tuple[int, int | Decimal]:
    """Читает число из выражения, не включая знак"""
    num_str = ""

    while(i < len(expr)):
        ch = expr[i]

        if(ch.isdigit()):
            num_str = num_str + ch
        elif(ch == "."):
            if("." in num_str):
                raise NumberError("Number contains more than one decimal point")

            num_str = num_str + ch
        elif(ch == ")"):
            raise NumberError("Closing bracket does not have a matching opening bracket")
        elif(ch == "("):
            raise NumberError("Number is followed by an opening bracket without an operator")
        elif(ch in operator_characters) or (ch.isspace()):
            break
        else:
            raise NumberError(f"Invalid character: {ch}")

        i += 1

    i -= 1
    if(len(num_str) == 0):
        raise NumberError("Empty number")

    if(num_str.startswith(".")):
        num_str = "0" + num_str

    if(num_str.endswith(".")):
        raise NumberError("Number ends with a decimal point")

    int_pattern = "[\\+-]?[0-9]+(\\.0+)?"
    dec_pattern = "[\\+-]?[0-9]+\\.[0-9]+"

    number: int | Decimal
    if(re.fullmatch(pattern=int_pattern, string=num_str)):
        number = int(num_str)
    elif(re.fullmatch(pattern=dec_pattern, string=num_str)):
        number = Decimal(num_str)
    else:
        raise NumberError(f"Badly formatted number: {num_str}")

    return i, number

def read_bracket(expr: str, i: int) -> tuple[int, int | Decimal]:
    """Читает и вычесляет скобку из выражения, не включая знак"""
    bracket_expr = ""

    # skip first bracket
    i += 1
    open_brackets = 1

    while(i < len(expr)):
        ch = expr[i]
        if(ch == "("):
            open_brackets += 1
        elif(ch == ")"):
            open_brackets -= 1

            # break before adding to bracket_expr to skip last bracket
            if(open_brackets == 0):
                break

        bracket_expr = bracket_expr + ch
        i += 1

    if(open_brackets > 0):
        raise ExpressionError("Unclosed bracket")

    number = evaluate(bracket_expr)
    return i, number

def read_operator(expr: str, i: int) -> tuple[int, str]:
    """Читает оператор из выражения"""
    for op in operators:
        if((len(op) + i) > len(expr)):
            continue

        test_str = expr[i:i+len(op)]
        if(test_str == op):
            i += len(op) - 1
            return i, op

    raise ExpressionError("A number/bracket is followed by an invalid operator")

def calculate(tokens: list[tuple[str,any]]) -> int | Decimal:
    """Вычесляет токенизированное выражение"""
    num_stack: list[int | Decimal] = []
    op_stack: list[str] = []

    for (ttype, tvalue) in tokens:
        if(ttype == TOKEN_NUMBER):
            num_stack.append(tvalue)
        elif(ttype == TOKEN_OPERATOR):
            while(len(op_stack) > 0 and priority[op_stack[-1]] >= priority[tvalue]):
                op = op_stack.pop()
                num2, num1 = num_stack.pop(), num_stack.pop()
                num_stack.append(apply_operator(num1, num2, op))
            op_stack.append(tvalue)

    while(len(op_stack) > 0):
        op = op_stack.pop()
        num2, num1 = num_stack.pop(), num_stack.pop()
        num_stack.append(apply_operator(num1, num2, op))

    if(len(num_stack) != 1):
        raise EvaluationError("Num stack has leftover values")

    return num_stack[0]