
import streamlit as st
import calculator_project as calc
import ast
import operator
import math

st.set_page_config(
    page_title="Python Calculator",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Python Calculator")
st.caption("An interactive calculator built with Python and Streamlit")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

if "expression" not in st.session_state:
    st.session_state.expression = ""

# Safe operators supported by the expression parser
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


def calculate_expression(expression):
    """Safely calculate expressions containing numbers and arithmetic operators."""

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not math.isfinite(node.value):
                raise ValueError("Please use finite numbers.")
            return node.value

        if isinstance(node, ast.BinOp):
            operation_type = type(node.op)

            if operation_type not in SAFE_OPERATORS:
                raise ValueError("Unsupported operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if operation_type in (ast.Div, ast.Mod) and right == 0:
                raise ZeroDivisionError(
                    "Division or modulus by zero is undefined."
                )

            if operation_type is ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponent is too large.")
                if abs(left) > 1 and right > 1000:
                    raise ValueError("Result would be too large.")

            result = SAFE_OPERATORS[operation_type](left, right)

            if isinstance(result, (int, float)):
                if isinstance(result, float) and not math.isfinite(result):
                    raise ValueError("Result is too large to display.")
                if abs(result) > 1e100:
                    raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation_type = type(node.op)

            if operation_type not in SAFE_OPERATORS:
                raise ValueError("Unsupported operator.")

            return SAFE_OPERATORS[operation_type](evaluate(node.operand))

        raise ValueError(
            "Invalid expression. Use numbers, operators, and parentheses only."
        )

    try:
        parsed_expression = ast.parse(expression, mode="eval")
        return evaluate(parsed_expression)
    except (SyntaxError, OverflowError) as error:
        raise ValueError(
            "Invalid expression. Example: (10 + 5) * 2"
        ) from error


# Calculator display
st.subheader("Enter your calculation")

expression = st.text_input(
    "Expression",
    value=st.session_state.expression,
    placeholder="Example: 10 + 5 * 3",
    label_visibility="collapsed"
)

st.session_state.expression = expression

# Example expressions
st.caption("Examples: 10 + 5 + 3  |  10 * 5 - 8  |  (10 + 5) * 2")

# Calculate
if st.button("Calculate", type="primary", use_container_width=True):
    if not expression.strip():
        st.warning("Please enter a calculation.")
    else:
        try:
            result = calculate_expression(expression)

            record = f"{expression} = {result}"

            st.session_state.last_result = result
            st.session_state.last_record = record
            st.session_state.last_error = None

            st.session_state.history.append(record)

        except (ValueError, ZeroDivisionError, TypeError) as error:
            st.session_state.last_error = str(error)
            st.session_state.last_result = None

        except ArithmeticError:
            st.session_state.last_error = "This calculation cannot be completed."
            st.session_state.last_result = None

# Result display
if "last_result" in st.session_state:
    if st.session_state.last_result is not None:
        st.success("Calculation completed!")

        st.metric(
            label="Result",
            value=str(st.session_state.last_result)
        )

        st.code(st.session_state.last_record)

    elif st.session_state.get("last_error"):
        st.error(st.session_state.last_error)

# Calculation history
st.divider()
st.subheader("📜 Calculation History")

if st.session_state.history:
    for index, record in enumerate(
        reversed(st.session_state.history), start=1
    ):
        st.write(f"**{index}.** {record}")

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Your calculations will appear here.")
