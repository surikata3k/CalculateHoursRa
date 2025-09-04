from datetime import datetime, date, timedelta

# -------------------------
# CONFIGURATION
# -------------------------

# Start and end dates (Spanish format dd/mm/yyyy)
start_date = datetime.strptime("12/09/2025", "%d/%m/%Y").date()
end_date = datetime.strptime("27/05/2026", "%d/%m/%Y").date()

# Holidays in string format (dd/mm/yyyy or ranges dd/mm/yyyy:dd/mm/yyyy)
#holidays_str = "02/10/2025, 12/10/2025, 06/12/2025:08/12/2025, 01/11/2025:02/11/2025"
holidays_str = "22/12/2025:07/01/2026, 30/03/2026:06/04/2026, 8/9/2025, 12/10/2025, 03/11/2025, 05/12/2025, 6/12/2025, 8/12/2025, 16/02/2026, 27/04/2026, 28/4/2026, 28/04/2026, 1/5/2026"

# Class hours per day (0 = no class)
# Monday=0 ... Sunday=6
hours_per_day = {
    0: 0,  # Monday
    1: 1,  # Tuesday
    2: 2,  # Wednesday
    3: 0,  # Thursday
    4: 1,  # Friday
    5: 0,  # Saturday
    6: 0   # Sunday
}

# Learning Outcomes (RA) and their planned hours
learning_outcomes = {
    "LO1": 20,
    "LO2": 20,
    "LO3": 20,
    "LO4": 20,
    "LO5": 19
}

# -------------------------
# PROCESS HOLIDAYS
# -------------------------

holidays = set()

for item in holidays_str.split(","):
    item = item.strip()
    if ":" in item:
        # range of dates
        start_str, end_str = item.split(":")
        start = datetime.strptime(start_str.strip(), "%d/%m/%Y").date()
        end = datetime.strptime(end_str.strip(), "%d/%m/%Y").date()
        day = start
        while day <= end:
            holidays.add(day)
            day += timedelta(days=1)
    else:
        # single date
        holidays.add(datetime.strptime(item, "%d/%m/%Y").date())

# -------------------------
# GENERATE CALENDAR
# -------------------------

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

# -------------------------
# CALCULATE START AND END DATE FOR EACH LEARNING OUTCOME
# -------------------------

results = []
previous_hours = 0
total_accumulated = 0

for lo, lo_hours in learning_outcomes.items():
    target_start = previous_hours + 1
    target_end = previous_hours + lo_hours

    lo_start_date = next(d for d, h, acc in calendar if acc >= target_start)
    lo_end_date = next(d for d, h, acc in calendar if acc >= target_end)

    hours_completed = sum(
        h for d, h, acc in calendar
        if lo_start_date <= d <= lo_end_date
    )

    teaching_days = sum(
        1 for d, h, acc in calendar
        if lo_start_date <= d <= lo_end_date and h > 0
    )

    weeks = ((lo_end_date - lo_start_date).days + 1) / 7

    total_accumulated += hours_completed
    results.append((
        lo, lo_start_date, lo_end_date,
        hours_completed, total_accumulated,
        teaching_days, weeks
    ))
    previous_hours += lo_hours

# -------------------------
# SHOW RESULT
# -------------------------

print(f"{'LO':<5} {'Start':<12} {'End':<12} {'LO Hours':<12} {'Accumulated':<12} {'Days':<6} {'Weeks':<8}")
print("-" * 90)
for lo, start, end, hours_completed, accumulated, days, weeks in results:
    print(f"{lo:<5} {start.strftime('%d/%m/%Y'):<12} {end.strftime('%d/%m/%Y'):<12} "
          f"{hours_completed:<12} {accumulated:<12} {days:<6} {weeks:.1f}")


# -------------------------
# ASK HOW TO DISPLAY TEACHING DAYS PER LEARNING OUTCOME
# -------------------------

print("\nHow do you want to display the teaching days of each LO?")
print("A - On screen")
print("B - To file")
print("C - Do not display")
option = input("Option (A/B/C): ").strip().upper()

while option not in ["A", "B", "C"]:
    option = input("Invalid option. Enter A, B or C: ").strip().upper()

# Prepare content if we want to display or save
teaching_days_content = []

# -------------------------
# SHOW RESULT AND TEACHING DAYS (depending on option)
# -------------------------

print(f"\n{'LO':<5} {'Start':<12} {'End':<12} {'LO Hours':<12} {'Accumulated':<12} {'Days':<6} {'Weeks':<8}")
print("-" * 90)

for lo, start, end, hours_completed, accumulated, days, weeks in results:
    print(f"{lo:<5} {start.strftime('%d/%m/%Y'):<12} {end.strftime('%d/%m/%Y'):<12} "
          f"{hours_completed:<12} {accumulated:<12} {days:<6} {weeks:.1f}")

    lo_teaching_days = [
        d.strftime("%d/%m/%Y")
        for d, h, acc in calendar
        if start <= d <= end and h > 0
    ]

    if option == "A":
        print("  Teaching days:")
        for day in lo_teaching_days:
            print(f"    - {day}")
        print()

    elif option == "B":
        # Add to content to save later
        teaching_days_content.append(f"{lo} ({start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}):")
        teaching_days_content.extend([f"  - {day}" for day in lo_teaching_days])
        teaching_days_content.append("")  # blank line between LOs

# If saving to file was chosen
if option == "B":
    filename = "teaching_days_per_LO.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(teaching_days_content))
    print(f"\n✅ Teaching days saved to file: {filename}")
