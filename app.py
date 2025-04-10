from datetime import date
from database import Base, engine, SessionLocal
from models import User, Expense, Budget
from utils import calculate_total_expenses, group_expenses_by_category, is_over_budget, remaining_budget_percentage

Base.metadata.create_all(bind=engine)

def add_user(session, name):
    user = User(name=name)
    session.add(user)
    session.commit()

def add_expense(session, user_name, category, amount):
    user = session.query(User).filter_by(name=user_name).first()
    exp = Expense(category=category, amount=amount, date=date.today(), user=user)
    session.add(exp)
    session.commit()

def set_budget(session, user_name, category, amount, month):
    user = session.query(User).filter_by(name=user_name).first()
    budget = Budget(category=category, amount=amount, month=month, user=user)
    session.add(budget)
    session.commit()

def report(session, user_name, month):
    user = session.query(User).filter_by(name=user_name).first()
    expenses = [e for e in user.expenses if e.date.strftime('%B') == month]
    grouped = group_expenses_by_category(expenses)
    
    print(f"\nReport for {user_name} - {month}")
    for budget in user.budgets:
        if budget.month == month:
            spent = grouped.get(budget.category, 0)
            print(f"{budget.category}: Spent ₹{spent}, Budget ₹{budget.amount}")
            if is_over_budget(spent, budget.amount):
                print(f"⚠️  You have exceeded your budget in {budget.category}!")
            elif remaining_budget_percentage(spent, budget.amount) <= 10:
                print(f"🔔 Alert: Only {remaining_budget_percentage(spent, budget.amount):.2f}% budget left in {budget.category}")

# Sample Run
if __name__ == '__main__':
    session = SessionLocal()
    add_user(session, "Kishore")
    set_budget(session, "Kishore", "Food", 5000, "April")
    set_budget(session, "Kishore", "Transport", 3000, "April")
    
    add_expense(session, "Kishore", "Food", 2000)
    add_expense(session, "Kishore", "Transport", 2900)
    add_expense(session, "Kishore", "Food", 2800)
    
    report(session, "Kishore", "April")
