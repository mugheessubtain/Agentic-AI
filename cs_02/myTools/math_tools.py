from agents import function_tool

@function_tool
def add_numbers(n1: int, n2: int) -> int:
    print("Add tool fired ---------->")
    return n1 + n2


@function_tool
def subtract_numbers(n1: int, n2: int) -> int:
    print("Subtract tool fired ---------->")
    
    return n1 - n2

@function_tool
def multiply_numbers(n1: int, n2: int) -> int:
    print("multiply tool fired ---------->")

    return n1 * n2

@function_tool
def divide_numbers(n1: int, n2: int) -> float:
    print("Divide tool fired ---------->")

    if n2 == 0:
        return 0
    return n1 / n2