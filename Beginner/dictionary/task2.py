your_expenses = {
    "Hotel": 1200,
    "Food": 800,
    "Transportation": 500,
    "Attractions": 300,
    "Miscellaneous": 200
}

partner_expenses = {
    "Hotel": 1000,
    "Food": 900,
    "Transportation": 600,
    "Attractions": 400,
    "Miscellaneous": 150
}

your_total = sum(your_expenses.values())
partner_total = sum(partner_expenses.values())

print(f"Your total expenses: ${your_total}")
print(f"Your partner's total expenses: ${partner_total}")

if your_total > partner_total:
    print("You spent more money overall.")
elif your_total < partner_total:
    print("Your partner spent more money overall.")
else:
    print("Both spent the same amount.")

significant_difference = 0
category_with_difference = ""

for category in your_expenses:
    difference = abs(your_expenses[category] - partner_expenses[category])
    if difference > significant_difference:
        significant_difference = difference
        category_with_difference = category

print(f"The category with the most significant difference is '{category_with_difference}' with a difference of ${significant_difference}.")
