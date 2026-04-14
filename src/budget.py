"""In-memory per-user token budget tracking."""

import os

DEFAULT_INPUT_BUDGET = int(os.environ.get("BRUSH_UP_INPUT_BUDGET", "250000"))
DEFAULT_OUTPUT_BUDGET = int(os.environ.get("BRUSH_UP_OUTPUT_BUDGET", "60000"))


def check_budget(
    budgets: dict,
    user_id: str,
    max_input_tokens: int = DEFAULT_INPUT_BUDGET,
    max_output_tokens: int = DEFAULT_OUTPUT_BUDGET,
) -> bool:
    usage = get_usage(budgets, user_id)
    return (
        usage["total_input_tokens"] < max_input_tokens
        and usage["total_output_tokens"] < max_output_tokens
    )


def record_usage(
    budgets: dict,
    user_id: str,
    input_tokens: int,
    output_tokens: int,
) -> dict:
    current_input, current_output = budgets.get(user_id, (0, 0))
    budgets[user_id] = (current_input + input_tokens, current_output + output_tokens)
    return get_usage(budgets, user_id)


def get_usage(budgets: dict, user_id: str) -> dict:
    total_input_tokens, total_output_tokens = budgets.get(user_id, (0, 0))
    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
    }
