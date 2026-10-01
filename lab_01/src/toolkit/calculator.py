import re
from decimal import Decimal

TOKEN_NUMBER = "NUM"
TOKEN_OPERATOR = "OP"

operators = ["+", "-", "*", "/"]
priority = {
    "+": 1,
    "-": 1,

    "*": 2,
    "/": 2
}

def evaluate(expr: str):
    tokens = tokenize(expr)
    # print(tokens)

    return calculate(tokens)

def apply_operator(num1: int | Decimal, num2: int | Decimal, operator: str):
    match(operator):
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            return Decimal(num1) / Decimal(num2)

    raise ValueError(f"Invalid operator: {operator}")

def tokenize(expr: str) -> list[tuple[str, int | Decimal]]:
    STATE_NUMBERS = 0
    STATE_OPERATORS = 1

    expr = expr.replace(" ", "") + " "
    int_pattern = "[\\+-]?[0-9]+(\\.0+)?"
    dec_pattern = "[\\+-]?[0-9]+\\.[0-9]+"

    i = 0
    tokens: list[tuple[str, int | Decimal]] = []

    state = STATE_NUMBERS
    curr_val = ""

    while(i < len(expr)):
        ch = expr[i]

        if(state == STATE_NUMBERS):
            if(ch.isdigit()) or (ch == ".") or (ch in "+-" and len(curr_val) == 0):
                curr_val += ch
                i += 1
            elif(len(curr_val) == 0) and (ch == "("):
                parentheses = 1
                i += 1
                sub_expr = ""

                while(i < len(expr)):
                    ch2 = expr[i]
                    if(ch2 == "("):
                        parentheses += 1
                    elif(ch2 == ")"):
                        parentheses -= 1
                        if(parentheses == 0):
                            break

                    sub_expr += ch2
                    i += 1

                if(parentheses > 0):
                    raise ValueError("Unclosed parentheses.")

                tokens.append((TOKEN_NUMBER, evaluate(sub_expr)))
                state = STATE_OPERATORS
                curr_val = ""
                i += 1
                if(expr[i] == " "):
                    break
            else:
                if(re.fullmatch(pattern=int_pattern, string=curr_val)):
                    curr_val = re.sub(pattern="\\.0+", repl="", string=curr_val)
                    tokens.append((TOKEN_NUMBER, int(curr_val)))
                    curr_val = ""
                    state = STATE_OPERATORS
                elif(re.fullmatch(pattern=dec_pattern, string=curr_val)):
                    tokens.append((TOKEN_NUMBER, Decimal(curr_val)))
                    curr_val = ""
                    state = STATE_OPERATORS
                elif(len(curr_val) == 0):
                    raise Exception(f"Badly formatted expression: {expr}")
                else:
                    raise ValueError(f"Invalid number: {curr_val}")
        elif(state == STATE_OPERATORS):
            if(ch in operators):
                tokens.append((TOKEN_OPERATOR, ch))
                curr_val = ""
                state = STATE_NUMBERS
                i += 1
            else:
                raise ValueError(f"Invalid operator: {ch}")
        else:
            raise Exception(f"Invalid state: {state}")

        if(ch == " "):
            break

    return tokens

def calculate(tokens: list[tuple[str,any]]) -> int | Decimal:
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
        raise Exception("Num stack has leftover values")

    return num_stack[0]