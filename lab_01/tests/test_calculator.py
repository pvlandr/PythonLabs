import pytest
from toolkit.calculator import evaluate
from toolkit.errors import *


def test_arithmetic():
    assert evaluate("1 + 1") == 2
    assert evaluate("5 - 4") == 1
    assert evaluate("5 * 2") == 10
    assert evaluate("125 / 4") == 31.25
    assert evaluate("1 + 2 + 3") == 6
    assert evaluate("3 - 2 + 1") == 2
    assert evaluate("2 * 3 * 4") == 24
    assert evaluate("10 / 2 / 5") == 1

def test_order_of_operations():
    assert evaluate("2 * 2 + 3 * 3") == 13
    assert evaluate("3 - 18 / 9 * 2 + 2 * 1") == 1
    assert evaluate("(1 + 2) * (3 + 4)") == 21

def test_unary_operator():
    assert evaluate("+1") == 1
    assert evaluate("-1") == -1
    assert evaluate("+++---1") == -1
    assert evaluate("+-+-+------+++++----1") == 1

def test_mixed_unary_binary_operators():
    assert evaluate("-1+-1") == -2
    assert evaluate("+1++1") == 2
    assert evaluate("-1--1") == 0

def test_expression_errors():
    with pytest.raises(ExpressionError, match="Пустое выражение"):
        evaluate("")
    
    with pytest.raises(ExpressionError):
        evaluate("2 3")
    
    with pytest.raises(ExpressionError):
        evaluate("* 2")
    
    with pytest.raises(ExpressionError):
        evaluate("2 *")
        
    with pytest.raises(ExpressionError):
        evaluate("2 * / 2")

    with pytest.raises(ExpressionError):
        evaluate("2(2)")

    with pytest.raises(ExpressionError):
        evaluate("2 + (2")

    with pytest.raises(ExpressionError):
        evaluate("2) + 2")

    with pytest.raises(ExpressionError):
        evaluate("a")

def test_number_errors():
    with pytest.raises(NumberError):
        evaluate("2..0")

    with pytest.raises(NumberError):
        evaluate("2.")

def test_divide_by_zero():
    with pytest.raises(EvaluationError):
        evaluate("1 / 0")
    
    with pytest.raises(EvaluationError):
        evaluate("(1.5 + 2.3) / (1.3 - 1.3)")