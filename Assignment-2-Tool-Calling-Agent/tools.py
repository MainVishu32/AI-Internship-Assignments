import ast
import operator
from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool


# Allowed mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def safe_calculate(node):
    """Safely evaluate a mathematical expression."""

    if isinstance(node, ast.Expression):
        return safe_calculate(node.body)

    if isinstance(node, ast.Constant) and isinstance(
        node.value, (int, float)
    ):
        return node.value

    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        value = safe_calculate(node.operand)

        if isinstance(node.op, ast.UAdd):
            return +value

        return -value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = safe_calculate(node.left)
        right = safe_calculate(node.right)

        return OPERATORS[type(node.op)](left, right)

    raise ValueError("Only basic mathematical expressions are allowed.")


@tool
def calculator(expression: str) -> str:
    """
    Perform safe basic mathematical calculations.

    Supports addition, subtraction, multiplication,
    division, modulo, powers, and parentheses.
    """

    try:
        tree = ast.parse(expression, mode="eval")
        result = safe_calculate(tree)

        return str(result)

    except ZeroDivisionError:
        return "Calculation failed: division by zero."

    except Exception:
        return (
            "Calculation failed. "
            "Please provide a valid mathematical expression."
        )


@tool
def get_time(timezone: str) -> str:
    """
    Get the current date and time for a specified timezone.

    Examples:
    Asia/Kolkata
    Asia/Tokyo
    America/New_York
    Europe/London
    """

    try:
        current_time = datetime.now(ZoneInfo(timezone))

        return current_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except Exception:
        return (
            f"Unable to get the time. "
            f"'{timezone}' is not a valid timezone."
        )