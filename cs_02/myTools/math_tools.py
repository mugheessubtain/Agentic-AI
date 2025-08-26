from agents import function_tool

@function_tool
def add_numbers(n1: int, n2: int) -> int:
    return n1 + n2


@function_tool
def subtract_numbers(n1: int, n2: int) -> int:
    return n1 - n2

@function_tool
def multiply_numbers(n1: int, n2: int) -> int:
    return n1 * n2

@function_tool
def divide_numbers(n1: int, n2: int) -> float:
    if n2 == 0:
        return 0
    return n1 / n2