from datetime import datetime, timedelta

# -------------------------
# CONFIGURATION
# -------------------------

start_date = datetime.strptime("12/09/2025", "%d/%m/%Y").date()
end_date = datetime.strptime("27/05/2026", "%d/%m/%Y").date()

holidays_str = "22/12/2025:07/01/2026, 30/03/2026:06/04/2026, 8/9/2025, 12/10/2025, 03/11/2025, 05/12/2025, 6/12/2025, 8/12/2025, 16/02/2026, 27/04/2026, 28/4/2026, 28/04/2026, 1/5/2026"

hours_per_day = {
    0: 0,  # Monday
    1: 1,  # Tuesday
    2: 2,  # Wednesday
    3: 0,  # Thursday
    4: 1,  # Friday
    5: 0,  # Saturday
    6: 0   # Sunday
}

# Modules and their Learning Outcomes
modules = {
    "Module 1": {
        "LO1": 15,
        "LO2": 10
    },
    "Module 2": {
        "LO1": 12,
        "LO2": 18,
        "LO3": 10
    },
    "Module 3": {
        "LO1": 20,
        "LO2": 15,
        "LO3": 14
    }
}


# -------------------------
# FUNCTIONS
# -------------------------

def process_holidays(holidays_str):
    holidays = set()
    for item in holidays_str.split(","):
        item = item.strip()
        if ":" in item:
            start_str, end_str = item.split(":")
            start = datetime.strptime(start_str.strip(), "%d/%m/%Y").date()
            end = datetime.strptime(end_str.strip(), "%d/%m/%Y").date()
            day = start
            while day <= end:
                holidays.add(day)
                day += timedelta(days=1)
        else:
            holidays.add(datetime.strptime(item, "%d/%m/%Y").date())
    return holidays


def generate_calendar(start_date, end_date, hours_per_day, holidays):
    calendar = []
    current_day = start_date
    accumulated_hours = 0
    while current_day <= end_date:
        if current_day not in holidays:
            hours = hours_per_day.get(current_day.weekday(), 0)
        else:
            hours = 0
        if hours > 0:
            accumulated_hours += hours
        calendar.append((current_day, hours, accumulated_hours))
        current_day += timedelta(days=1)
    return calendar


def calculate_learning_outcomes(calendar, learning_outcomes):
    results = []
    previous_hours = 0
    total_accumulated = 0

    for lo, lo_hours in learning_outcomes.items():
        target_start = previous_hours + 1
        target_end = previous_hours + lo_hours

        lo_start_date = next(d for d, h, acc in calendar if acc >= target_start)
        lo_end_date = next(d for d, h, acc in calendar if acc >= target_end)

        hours_completed = sum(
            h for d, h, acc in calendar if lo_start_date <= d <= lo_end_date
        )

        teaching_days = sum(
            1 for d, h, acc in calendar if lo_start_date <= d <= lo_end_date and h > 0
        )

        weeks = ((lo_end_date - lo_start_date).days + 1) / 7

        total_accumulated += hours_completed

        teaching_dates = [
            d.strftime("%d/%m/%Y")
            for d, h, acc in calendar
            if lo_start_date <= d <= lo_end_date and h > 0
        ]

        results.append((
            lo, lo_start_date, lo_end_date,
            hours_completed, total_accumulated,
            teaching_days, weeks, teaching_dates
        ))
        previous_hours += lo_hours

    return results


def display_results(module_name, results):
    print(f"\n===== {module_name} =====")
    print(f"{'LO':<5} {'Start':<12} {'End':<12} {'LO Hours':<12} {'Accumulated':<12} {'Days':<6} {'Weeks':<8}")
    print("-" * 90)
    for lo, start, end, hours_completed, accumulated, days, weeks, teaching_dates in results:
        print(f"{lo:<5} {start.strftime('%d/%m/%Y'):<12} {end.strftime('%d/%m/%Y'):<12} "
              f"{hours_completed:<12} {accumulated:<12} {days:<6} {weeks:.1f}")
        # print(f"   Dates: {', '.join(teaching_dates)}")


def save_results_to_txt(filename, modules_results):
    lines = []
    for module_name, results in modules_results.items():
        lines.append(f"===== {module_name} =====")
        for lo, start, end, hours_completed, accumulated, days, weeks, teaching_dates in results:
            lines.append(
                f"{lo} ({start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}): "
                f"{', '.join(teaching_dates)}"
            )
        lines.append("")  # blank line between modules

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✅ Teaching days saved to file: {filename}")


# -------------------------
# MAIN PROGRAM
# -------------------------

holidays = process_holidays(holidays_str)
calendar = generate_calendar(start_date, end_date, hours_per_day, holidays)

modules_results = {}

for module_name, los in modules.items():
    results = calculate_learning_outcomes(calendar, los)
    display_results(module_name, results)
    modules_results[module_name] = results

# Ask if user wants to save results
choice = input("\nDo you want to save teaching days to a TXT file? (Y/N): ").strip().upper()
if choice == "Y":
    save_results_to_txt("teaching_days_per_module.txt", modules_results)
