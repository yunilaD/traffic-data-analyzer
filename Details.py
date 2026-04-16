#Author: Y.M. Dissnayake
#Date:2024/11/27
#Student ID: 20231664
import csv

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
#Asking for the day
    while True:
        try:
            day = int(input('Please enter the day of the survey in the format dd : '))
            if day < 1 or day > 31:
                print('Out of range - values must range from 1 and 31.')
                continue
            else:
                break
        except ValueError:
            print('Integer required')
    if day < 10:
        day = ('0' + str(day))  # if user inputs 1 digit as day converting it to 2 digits

#Asking for the month
    while True:
        try:
            month = int(input('Please enter the day of the survey in the format mm : '))
            if month < 1 or month > 12:
                print('Out of range - values must range from 1 and 12.')
                continue
            else:
                break
        except ValueError:
            print('Integer required ')
    if month < 10:
        month = ('0' + str(month))  # if user inputs 1 digit as month converting it to 2 digits

#Asking for the year
    while True:
        try:
            year = int(input('Please enter the day of the survey in the format yyyy : '))
            if year < 2000 or year > 2024:
                print('Out of range - values must range from 2000 and 2024. ')
                continue

            else:
                break
        except ValueError:
            print("integer required")

    file_path = (f'traffic_data{day}{month}{year}.csv') #creating the file path according to the inputs
    return file_path,day,month,year

    pass  # Validation logic goes here


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        choice = input('Do you want to select another file (Y/N)? ').upper() #converting the user input to uppercase
        if choice == 'Y' or choice == 'N':
            return choice
        else:
            print('Please enter Y or N to continue')

    pass  # Validation logic goes here


# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    - Unique hours with rain
    """
    # Initializing variables
    TotalVehicles = TotalElectricVehicle = TotalTwowheel = trucks = scooters = TotalBicycle = 0
    NorthBus = NoTurn = OverSpeedlimit = TotalElmRabbit = TotalHanleyWest = 0
    rain_hours_set = set()  # Set to track unique hours with rain
    hours = {}

    try:
        with open(file_path, 'r') as file:  # Open the CSV file in reading mode
            reader = csv.DictReader(file)
            for row in reader:
                TotalVehicles += 1
                VehicleType = row['VehicleType'].lower()
                electric = row['elctricHybrid'].lower()
                junction = row['JunctionName'].lower()
                directionIn = row['travel_Direction_in'].lower()
                directionOut = row['travel_Direction_out'].lower()
                speed = int(row['VehicleSpeed'])
                time = row['timeOfDay']
                rain = row['Weather_Conditions'].lower()

                # Calculate metrics
                if 'truck' in VehicleType:
                    trucks += 1
                if electric == 'true':
                    TotalElectricVehicle += 1
                if VehicleType in ['bicycle', 'scooter', 'motorcycle']:
                    TotalTwowheel += 1
                if VehicleType == 'scooter' and junction == 'elm avenue/rabbit road':
                    scooters += 1
                if 'bicycle' in VehicleType:
                    TotalBicycle += 1
                if junction == 'elm avenue/rabbit road' and directionOut == 'n' and VehicleType == 'buss':
                    NorthBus += 1
                if directionIn == directionOut:
                    NoTurn += 1
                if speed > int(row['JunctionSpeedLimit']):
                    OverSpeedlimit += 1
                if junction == 'elm avenue/rabbit road':
                    TotalElmRabbit += 1
                elif junction == 'hanley highway/westway':
                    TotalHanleyWest += 1
                #hours with the highest traffic
                hour = time.split(':')[0]
                if junction == 'hanley highway/westway':
                    hours[hour] = hours.get(hour, 0) + 1
                # Add hour to the rain_hours_set if raining
                if 'rain' in rain:
                    rain_hours_set.add(hour)

        # Doing the calculations
        truck_percentage = round((trucks / TotalVehicles) * 100)
        avg_bicycles_per_hour = round(TotalBicycle / 24)
        scooter_percentage = int((scooters / TotalElmRabbit) * 100) if TotalElmRabbit else 0
        peak_hour_count = max(hours.values(), default=0)
        peak_hours = [hour for hour, count in hours.items() if count == peak_hour_count]
        RainHours = len(rain_hours_set)

        #adding the outcomes into a dictionary
        outcomes = {
            "file_path": file_path,
            "TotalVehicles": TotalVehicles,
            "trucks": trucks,
            "TotalElectricVehicle": TotalElectricVehicle,
            "TotalTwowheel": TotalTwowheel,
            "NorthBus": NorthBus,
            "NoTurn": NoTurn,
            "truck_percentage": truck_percentage,
            "avg_bicycles_per_hour": avg_bicycles_per_hour,
            "OverSpeedlimit": OverSpeedlimit,
            "TotalElmRabbit": TotalElmRabbit,
            "TotalHanleyWest": TotalHanleyWest,
            "scooter_percentage": scooter_percentage,
            "peak_hour_count": peak_hour_count,
            "peak_hours": peak_hours,
            "RainHours": RainHours,
        }
        return outcomes
    except FileNotFoundError:
        print(f"File {file_path} not found. Please check the date entered.")
        return None


    pass  # Logic for processing data goes here


def display_outcomes(outcomes,file_path):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    if outcomes:
        print(f"\nThe name of the csv file: {file_path}."
              f"\nThe total number of vehicles recorded for this date is {outcomes['TotalVehicles']}."
              f"\nThe total number of trucks recorded for this date is {outcomes['trucks']}."
              f"\nThe total number of electric vehicles recorded for this date is {outcomes['TotalElectricVehicle']}."
              f"\nThe total number of two-wheeled vehicles recorded for this date is {outcomes['TotalTwowheel']}."
              f"\nThe total number of buses leaving Elm Avenue/Rabbit Road heading north is {outcomes['NorthBus']}."
              f"\nThe total number of vehicles through both junctions not turning left or right is {outcomes['NoTurn']}."
              f"\nThe percentage of total vehicles recorded that are trucks for this date is {outcomes['truck_percentage']}%."
              f"\nThe average number of bikes per hour for this date is {outcomes['avg_bicycles_per_hour']}."
              f"\nThe total number of vehicles recorded as over the speed limit for this date is {outcomes['OverSpeedlimit']}."
              f"\nThe total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['TotalElmRabbit']}."
              f"\nThe total number of vehicles recorded through Hanley Highway/Westway is {outcomes['TotalHanleyWest']}."
              f"\n{outcomes['scooter_percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters."
              f"\nThe highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_count']}."
              f"\nThe most vehicles through Hanley Highway/Westway were recorded between {', '.join(f'{hour}:00 - {int(hour) + 1}:00' for hour in outcomes['peak_hours'])}."
              f"\nThe number of hours with rain for this date is {outcomes['RainHours']}.\n"
              f"\n"
              f"Saved to results.txt")

    pass  # Printing outcomes to the console


# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    #adding the details to a list
    if outcomes:
        results=[(f"The name of the CSV file: {outcomes['file_path']}.\n"
                       f"The total number of vehicles recorded for this date is {outcomes['TotalVehicles']}.\n"
                       f"The The total number of trucks recorded for this date is {outcomes['trucks']}.\n"
                       f"The total number of electric vehicles recorded for this date is {outcomes['TotalElectricVehicle']}.\n"
                       f"The total number of two-wheeled vehicles recorded for this date is {outcomes['TotalTwowheel']}.\n"
                       f"The total number of buses leaving Elm Avenue/Rabbit Road heading north is {outcomes['NorthBus']}.\n"
                       f"The total number of vehicles through both junctions not turning left or right is {outcomes['NoTurn']}.\n"
                       f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['truck_percentage']}%.\n"
                       f"The average number of bikes per hour for this date is {outcomes['avg_bicycles_per_hour']}.\n"
                       f"The total number of vehicles recorded as over the speed limit for this date is {outcomes['OverSpeedlimit']}.\n"
                       f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['TotalElmRabbit']}.\n"
                       f"The total number of vehicles recorded through Hanley Highway/Westway is {outcomes['TotalHanleyWest']}.\n"
                       f"{outcomes['scooter_percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n"
                       f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_count']}.\n"
                       f"The most vehicles through Hanley Highway/Westway were recorded between {', '.join(f'{hour}:00 - {int(hour) + 1}:00' for hour in outcomes['peak_hours'])}.\n"
                       f"The number of hours with rain for this date is {outcomes['RainHours']}.\n\n"
                       f"**************************************************\n\n")]

        #write to a text file in append mode
        with open(file_name, "a") as resultFile:
            resultFile.write("\n".join(results))
        #Arenberg, J. (2009). Writing a list to a file with Python, with newlines. [online] Stack Overflow. Available at: https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python-with-newlines?newreg=bd10101ac6294a05b78b36c6496b7b36.



    pass  # File writing logic goes here

while True: #till the user enter 'N' program runs
    file_path, day, month, year = validate_date_input()
    outcomes = process_csv_data(file_path)
    if outcomes:
        display_outcomes(outcomes, file_path)
        save_results_to_file(outcomes)
    if validate_continue_input() == 'N':
        print("Exiting the program.")
        break

# if you have been contracted to do this assignment please do not remove this line
