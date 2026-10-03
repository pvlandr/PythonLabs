# калькулятор
class NumberError(Exception):
    """Ошибка при чтении числа"""

class EmptyNumberError(Exception):
    """Ошибка при отсутствии ожидаемого числа"""

class ExpressionError(Exception):
    """Ошибка при чтении выражения"""

class EvaluationError(Exception):
    """Ошибка при вычислении выражения"""

# конвертер
class UnitError(Exception):
    """Ошибка с выбранными единицами измерений"""

class ConversionError(Exception):
    """Ошибка при переводе числа"""

class ConversionTableError(Exception):
    """Ошибка при чтении таблицы конвертаций"""