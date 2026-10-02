import argparse

import toolkit.calculator
import toolkit.converter

parser = argparse.ArgumentParser(
    prog="python -m toolkit",
    description="TODO",
)
commands = parser.add_subparsers(dest="command", required=True)

calc = commands.add_parser("calc", help="TODO")
calc.add_argument("expression", help="TODO")

convert = commands.add_parser("convert", help="TODO")
convert.add_argument("value", type=int, help="TODO")
convert.add_argument("--from", dest="from_unit", required=True, help="TODO")
convert.add_argument("--to", dest="to_unit", required=True, help="TODO")

args = parser.parse_args()
if args.command == "calc":
    print(toolkit.calculator.evaluate(args.expression))
elif args.command == "convert":
    print(toolkit.converter.convert(args.value, args.from_unit, args.to_unit))