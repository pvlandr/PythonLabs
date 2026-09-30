import toolkit.calculator
# print(calculator.evaluate(input()))

import toolkit.converter
s = input().split()
v, f, t = float(s[0]), s[1], s[2]
print(toolkit.converter.convert(v, f, t))