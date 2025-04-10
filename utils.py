from datetime import datetime
from models import Expense

def calculate_total_expenses(expenses):
    return sum(exp.amount for exp in expenses)

def group_expenses_by_category(expenses):
    grouped = {}
    for exp in expenses:
        grouped.setdefault(exp.category, 0)
        grouped[exp.category] += exp.amount
    return grouped

def is_over_budget(total_spent, budget_limit):
    return total_spent > budget_limit

def remaining_budget_percentage(total_spent, budget_limit):
    return 100 - ((total_spent / budget_limit) * 100)
