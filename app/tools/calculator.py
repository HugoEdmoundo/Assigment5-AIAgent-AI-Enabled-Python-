from typing import Dict, Any
import re

def calculate(expression: str) -> Dict[str, Any]:
    """
    Safely evaluates mathematical expressions.
    Only allows basic arithmetic operations.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Dictionary with expression and result
    """
    # Remove whitespace
    expression = expression.strip()
    
    # Check for empty expression
    if not expression:
        return {"error": "Expression cannot be empty"}
    
    # Only allow numbers, operators, parentheses, and decimal points
    allowed_pattern = r'^[\d\+\-\*\/\(\)\.\s]+$'
    if not re.match(allowed_pattern, expression):
        return {
            "error": "Invalid characters in expression. Only numbers and +, -, *, /, (, ) are allowed"
        }
    
    try:
        # Evaluate the expression
        result = eval(expression)
        
        return {
            "expression": expression,
            "result": result,
            "result_type": type(result).__name__
        }
    except ZeroDivisionError:
        return {
            "error": "Division by zero",
            "expression": expression
        }
    except SyntaxError:
        return {
            "error": "Invalid syntax in expression",
            "expression": expression
        }
    except Exception as e:
        return {
            "error": f"Calculation error: {str(e)}",
            "expression": expression
        }
