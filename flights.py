
"""
Flight Departure Data Analysis
Coursework Project – Python
"""

# ------------------ IMPORTS ------------------
import csv
from collections import Counter
from graphics import *

# ------------------ GLOBAL DATA ------------------
data_list = []

airport_name = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Barajas",
    "CDG": "Paris Charles de Gaulle",
    "IST": "Istanbul Airport",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Humberto Delgado Airport",
    "FRA": "Frankfurt Airport",
    "FCO": "Rome Fiumicino Airport",
    "MUC": "Munich International Airport",
    "BCN": "Barcelona El Prat Airport"
}

airline_codes = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

# ------------------ FUNCTIONS ------------------

def load_csv(filename):
    """Load CSV data into data_list."""
    data_list.clear()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data_list.append(row)


def airport_code():
    """Prompt user for valid airport code."""
    while True:
        code = input("Enter a 3-letter airport code: ").upper()
        if len(code) != 3:
            print("Code must be exactly 3 letters.")
        elif code not in airport_name:
            print("Invalid airport code.")
        else:
            return code


def year_input(airport):
    """Prompt user for valid year."""
    while True:
        year = input(f"Enter year of travel from {airport}: ")
        if year.isdigit() and len(year) == 4:
            year = int(year)
            if 2000 <= year <= 2025:
                return year
        print("Year must be between 2000 and 2025.")


def draw_box(win, x, y, width, height, colour):
    bar = Rectangle(Point(x, y), Point(x + width, y + height))
    bar.setFill(colour)
    bar.draw(win)

# ------------------ MAIN PROGRAM ------------------

if __name__ == "__main__":

    print("--------------------------------------------------")
    airport = airport_code()
    selected_airport_name = airport_name[airport]
    print(f"Selected Airport: {airport} - {selected_airport_name}")

    year_of_departure = year_input(airport)
    print(f"Year Selected: {year_of_departure}")

    selected_data_file = f"{airport}{year_of_departure}.csv"
    print(f"Loading file: {selected_data_file}")
    print("--------------------------------------------------")

    load_csv(selected_data_file)

    total_flights = len(data_list)
    terminal_2_flights = sum(1 for r in data_list if r[8] == '2')
    under_600_miles = sum(1 for r in data_list if int(r[5]) < 600)
    air_france_flights = sum(1 for r in data_list if r[1].startswith("AF"))

    flights_below_15C = 0
    for r in data_list:
        try:
            temp = int(r[10].split("°")[0])
            if temp < 15:
                flights_below_15C += 1
        except:
            pass

    ba_flights = [r for r in data_list if r[1].startswith("BA")]
    avg_ba_per_hour = round(len(ba_flights) / 12, 2)
    percent_ba = round((len(ba_flights) / total_flights) * 100, 2)

    af_flights = [r for r in data_list if r[1].startswith("AF")]
    af_delayed = sum(1 for r in af_flights if r[2] != r[3])
    percent_af_delayed = round((af_delayed / len(af_flights)) * 100, 2) if af_flights else 0

    rain_hours = len(set(
        r[2].split(":")[0] for r in data_list if "rain" in r[10].lower()
    ))

    dest_counts = Counter(r[4] for r in data_list)
    least_common_dest = [d for d, c in dest_counts.items() if c == min(dest_counts.values())]

    print("--------------------------------------------------")
    print(f"Total flights: {total_flights}")
    print(f"Terminal 2 flights: {terminal_2_flights}")
    print(f"Flights under 600 miles: {under_600_miles}")
    print(f"Air France flights: {air_france_flights}")
    print(f"Flights below 15°C: {flights_below_15C}")
    print(f"Average BA flights/hour: {avg_ba_per_hour}")
    print(f"BA percentage: {percent_ba}%")
    print(f"AF delayed flights: {percent_af_delayed}%")
    print(f"Rain hours: {rain_hours}")
    print(f"Least common destination(s): {', '.join(least_common_dest)}")
    print("--------------------------------------------------")

    # Save results
    with open("results.txt", "a") as f:
        f.write(f"{airport} {year_of_departure} Results\n")
        f.write(f"Total flights: {total_flights}\n")
        f.write("-" * 40 + "\n")

    # ------------------ HISTOGRAM ------------------

    while True:
        code = input("Enter airline code for histogram: ").upper()
        if code in airline_codes:
            break
        print("Invalid airline code.")

    flights_per_hour = [0] * 12
    for r in data_list:
        if r[1][:2].upper() == code:
            hour = int(r[2].split(":")[0])
            if 0 <= hour < 12:
                flights_per_hour[hour] += 1

    win = GraphWin("Flights per Hour Histogram", 900, 600)

    title = Text(Point(450, 30),
        f"{airline_codes[code]} Departures from {selected_airport_name} ({year_of_departure})")
    title.setSize(18)
    title.setStyle("bold")
    title.draw(win)

    y = 100
    for hour in range(12):
        width = flights_per_hour[hour] * 20
        draw_box(win, 150, y, width, 40, "purple")
        Text(Point(120, y + 20), f"{hour:02d}:00").draw(win)
        Text(Point(150 + width + 15, y + 20), str(flights_per_hour[hour])).draw(win)
        y += 60
