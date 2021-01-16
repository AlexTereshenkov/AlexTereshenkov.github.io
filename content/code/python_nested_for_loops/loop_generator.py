loop = """{for_spaces}for i in range(1):
{print_spaces}print({loop_number})\n"""

code = ""
for i in range(0, 21, 1):
    code += loop.format(
        for_spaces=" " * 2 * i,
        print_spaces=" " * 2 * i + "  ",
        loop_number=i,
    )
print(code)
