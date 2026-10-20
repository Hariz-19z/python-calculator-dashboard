
import ast
import operator
import math

history = []

# Operators allowed by our calculator
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


# Calculate a complete mathematical expression
def calculate_expression(expression):

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):

        # Handle the complete expression
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        # Handle numbers
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not math.isfinite(node.value):
                raise ValueError("Please use finite numbers.")
            return node.value

        # Handle operations with two sides
        if isinstance(node, ast.BinOp):

            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = SAFE_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            # Prevent division or modulus by zero
            if type(node.op) in (ast.Div, ast.Mod) and right == 0:
                raise ZeroDivisionError("Cannot divide or take modulus by zero.")

            # Prevent excessively large exponents
            if type(node.op) is ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponent is too large.")

            result = operation(left, right)

            # Prevent excessively large or infinite results
            if isinstance(result, float) and not math.isfinite(result):
                raise ValueError("Result is too large to display.")

            if abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        # Handle positive and negative numbers
        if isinstance(node, ast.UnaryOp):

            operation = SAFE_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            return operation(evaluate(node.operand))

        # Reject unsupported expressions
        raise ValueError(
            "Invalid expression. Use numbers and arithmetic operators only."
        )

    return evaluate(tree)


# Display calculator menu
def display_menu():

    print("\n" + "=" * 40)
    print("          PYTHON CALCULATOR")
    print("=" * 40)

    print("Enter a complete mathematical expression.")
    print("Examples: 10 + 20 + 30")
    print("          (10 + 20) * 3")
    print("          100 / 5 + 8 * 2")

    print("\n[H] View History")
    print("[C] Clear History")
    print("[Q] Quit")

    print("=" * 40)


# Display calculation history
def show_history():

    if not history:
        print("\nNo calculations in history yet.")
        return

    print("\n--- Calculation History ---")

    for index, entry in enumerate(history, start=1):
        print(f"{index}. {entry}")

    print("---------------------------")


# Main calculator program
def main():

    while True:

        display_menu()

        expression = input("\nEnter calculation or choose H/C/Q: ").strip()

        # Quit calculator
        if expression.lower() == "q":
            print("\nExiting calculator. Goodbye!")
            break

        # View history
        if expression.lower() == "h":
            show_history()
            continue

        # Clear history
        if expression.lower() == "c":
            history.clear()
            print("\nCalculation history cleared.")
            continue

        # Calculate expression
        try:
            result = calculate_expression(expression)

            record = f"{expression} = {result}"

            history.append(record)

            print(f"\nResult: {result}")

        except (ValueError, ZeroDivisionError, SyntaxError, TypeError) as error:
            print(f"\nError: {error}")

        except (ArithmeticError, RecursionError):
            print("\nError: This calculation cannot be completed safely.")


if __name__ == "__main__":
    main()

        

    
    
        