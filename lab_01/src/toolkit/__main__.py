import argparse
from decimal import Decimal

import toolkit.calculator
import toolkit.converter

parser = argparse.ArgumentParser(
    prog="python -m toolkit",
    description="Калькулятор и конвертер величин",
)
commands = parser.add_subparsers(dest="command", required=True)

calc = commands.add_parser("calc", help="Вычисляет выражение")
calc.add_argument("expression", help="Математическое выражение")

convert = commands.add_parser("convert", help="Переводит число в другую единицу измерения")
convert.add_argument("value", type=Decimal, help="Начальное число")
convert.add_argument("--from", dest="from_unit", required=True, help="Начальная единица измерения")
convert.add_argument("--to", dest="to_unit", required=True, help="Новая единица измерения")

args = parser.parse_args()
if args.command == "calc":
    print(toolkit.calculator.evaluate(args.expression))
elif args.command == "convert":
    print(toolkit.converter.convert(args.value, args.from_unit, args.to_unit))