import decimal
import re
from decimal import Decimal

from toolkit.errors import *

TOKEN_NUMBER = "NUM"
TOKEN_OPERATOR = "OP"

decimal.getcontext().prec = 10

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
                raise EvaluationError("Деление на 0")
            
            return Decimal(num1) / Decimal(num2)

    raise ValueError(f"Неподдержанный оператор: {operator}")

def tokenize(expr: str) -> list[tuple[str,any]]:
    """Токенизирует выражение"""
    expr = expr.strip()
    i = 0
    tokens: list[tuple[str,any]] = []
    state = 0

    if(len(expr) == 0):
        raise ExpressionError("Пустое выражение")

    while(i < len(expr)):
        ch = expr[i]

        if(ch.isspace()):
            pass
        elif(state == 0):
            try:
                i, number = read_number(expr, i)
                tokens.append((TOKEN_NUMBER, number))

                state = 1
            except EmptyNumberError:
                if(len(tokens) > 0):
                    raise ExpressionError("Два бинарных оператора стоят подряд")
                else:
                    raise ExpressionError("Выражение начинается с бинарного оператора")
        elif(state == 1):
            i, operator = read_operator(expr, i)
            tokens.append((TOKEN_OPERATOR, operator))

            state = 0
            
        i += 1

    if(len(tokens) == 0):
        raise ExpressionError("Пустое выражение")

    if(tokens[-1][0] == TOKEN_OPERATOR):
        raise ExpressionError("Выражение заканчивается на бинарный оператор") 

    return tokens

def read_number(expr: str, i: int) -> tuple[int, int | Decimal]:
    """Читает число или строку из выражения, включая знак"""
    is_negative = False

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
                raise NumberError("Число содержит более чем одну точку")

            num_str = num_str + ch
        elif(ch == ")"):
            raise ExpressionError("Правая скобка не имеет соответствующую левую скобку")
        elif(ch == "("):
            raise ExpressionError("Числа (или скобки) не соединены оператором")
        elif(ch in operator_characters) or (ch.isspace()):
            break
        else:
            raise ExpressionError(f"Недопустимый символ: {ch}")

        i += 1

    i -= 1
    if(len(num_str) == 0):
        raise EmptyNumberError("Пустое число")

    if(num_str.startswith(".")):
        num_str = "0" + num_str

    if(num_str.endswith(".")):
        raise NumberError("Число заканчивается на точку")

    int_pattern = "[\\+-]?[0-9]+(\\.0+)?"
    dec_pattern = "[\\+-]?[0-9]+\\.[0-9]+"

    number: int | Decimal
    if(re.fullmatch(pattern=int_pattern, string=num_str)):
        number = int(num_str)
    elif(re.fullmatch(pattern=dec_pattern, string=num_str)):
        number = Decimal(num_str)
    else:
        raise NumberError(f"Неправильно сформатированное число: {num_str}")

    return i, number

def read_bracket(expr: str, i: int) -> tuple[int, int | Decimal]:
    """Читает и вычесляет скобку из выражения, не включая знак"""
    bracket_expr = ""

    i += 1
    open_brackets = 1

    while(i < len(expr)):
        ch = expr[i]
        if(ch == "("):
            open_brackets += 1
        elif(ch == ")"):
            open_brackets -= 1

            if(open_brackets == 0):
                break

        bracket_expr = bracket_expr + ch
        i += 1

    if(open_brackets > 0):
        raise ExpressionError("Левая скобка не имеет соответствующую правую скобку")

    number = evaluate(bracket_expr)
    return i, number

def read_operator(expr: str, i: int) -> tuple[int, str]:
    """Читает оператор из выражения"""

    ch = expr[i]

    if(ch.isdigit()):
        raise ExpressionError("Числа (или скобки) не соединены оператором")
    elif(ch == "."):
        raise ExpressionError("Неподдержанный оператор: .")
    elif(ch == ")"):
        raise NumberError("Правая скобка не имеет соответствующую левую скобку")
    elif(ch == "("):
        raise NumberError("Числа (или скобки) не соединены оператором")
    elif(ch in operator_characters) or (ch.isspace()):
        pass
    else:
        raise NumberError(f"Недопустимый символ: {ch}")

    for op in operators:
        if((len(op) + i) > len(expr)):
            continue

        test_str = expr[i:i+len(op)]
        if(test_str == op):
            i += len(op) - 1
            return i, op

    raise ExpressionError(f"Неподдержанный оператор: {expr[i]}")

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

    return num_stack[0]