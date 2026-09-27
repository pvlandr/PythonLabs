import calculator
# print(calculator.evaluate(input()))

import converter
s = input().split()
v, f, t = float(s[0]), s[1], s[2]
print(converter.convert(v, f, t))