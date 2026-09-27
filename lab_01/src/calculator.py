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

def applyOperator(num1: int | Decimal, num2: int | Decimal, operator: str):
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
    intPattern = "[\\+-]?[0-9]+(\\.0+)?"
    decPattern = "[\\+-]?[0-9]+\\.[0-9]+"

    i = 0
    tokens: list[tuple[str, int | Decimal]] = []

    state = STATE_NUMBERS
    currVal = ""

    while(i < len(expr)):
        ch = expr[i]

        if(state == STATE_NUMBERS):
            if(ch.isdigit()) or (ch == ".") or (ch in "+-" and len(currVal) == 0):
                currVal += ch
                i += 1
            elif(len(currVal) == 0) and (ch == "("):
                parentheses = 1
                i += 1
                subExpr = ""

                while(i < len(expr)):
                    ch2 = expr[i]
                    if(ch2 == "("):
                        parentheses += 1
                    elif(ch2 == ")"):
                        parentheses -= 1
                        if(parentheses == 0):
                            break

                    subExpr += ch2
                    i += 1

                if(parentheses > 0):
                    raise ValueError("Unclosed parentheses.")

                tokens.append((TOKEN_NUMBER, evaluate(subExpr)))
                state = STATE_OPERATORS
                currVal = ""
                i += 1
                if(expr[i] == " "):
                    break
            else:
                if(re.fullmatch(pattern=intPattern, string=currVal)):
                    currVal = re.sub(pattern="\\.0+", repl="", string=currVal)
                    tokens.append((TOKEN_NUMBER, int(currVal)))
                    currVal = ""
                    state = STATE_OPERATORS
                elif(re.fullmatch(pattern=decPattern, string=currVal)):
                    tokens.append((TOKEN_NUMBER, Decimal(currVal)))
                    currVal = ""
                    state = STATE_OPERATORS
                elif(len(currVal) == 0):
                    raise Exception(f"Badly formatted expression: {expr}")
                else:
                    raise ValueError(f"Invalid number: {currVal}")
        elif(state == STATE_OPERATORS):
            if(ch in operators):
                tokens.append((TOKEN_OPERATOR, ch))
                currVal = ""
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
    numStack: list[int | Decimal] = []
    opStack: list[str] = []

    for (ttype, tvalue) in tokens:
        if(ttype == TOKEN_NUMBER):
            numStack.append(tvalue)
        elif(ttype == TOKEN_OPERATOR):
            while(len(opStack) > 0 and priority[opStack[-1]] >= priority[tvalue]):
                op = opStack.pop()
                num2, num1 = numStack.pop(), numStack.pop()
                numStack.append(applyOperator(num1, num2, op))
            opStack.append(tvalue)

    while(len(opStack) > 0):
        op = opStack.pop()
        num2, num1 = numStack.pop(), numStack.pop()
        numStack.append(applyOperator(num1, num2, op))

    if(len(numStack) != 1):
        raise Exception("Num stack has leftover values")

    return numStack[0]