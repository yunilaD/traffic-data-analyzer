#Author: Y.M. Dissnayake
#Date:2024/12/22
#Student ID: 20231664


# Task D: Histogram Display
import tkinter as tk
import csv

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title('Histogram') #set the title
        self.canvas=tk.Canvas(self.root, width=1400,height=700,bg='light cyan')
        self.canvas.pack() #add the canvas to window

        #make sure the histogram window popup and be in top
        self.root.update_idletasks()
        self.root.focus_force()
        self.root.attributes('-topmost',True)
        self.root.attributes('-topmost',False)
        pass  # Setup logic for the window and canvas

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        #Create a dictionary to store traffic counts
        junction_counts={
            'Elm Avenue/Rabbit Road':[0]*24,
            'Hanley Highway/Westway':[0]*24
        }

        for row in self.traffic_data:
            hour=int(row['timeOfDay'].split(':')[0])#extract the hour from hh:mm
            junction=row['JunctionName']
            if junction in junction_counts:
                junction_counts[junction][hour]+=1

        max_count = max(
            max(junction_counts[j]) for j in junction_counts)  # Get the maximum count across all hours for scaling
        bar_width = 20
        spacing = 10
        x_start = 100
        y_base = 600
        scale = (y_base - 100) / max_count if max_count > 0 else 1
        colors = ["medium spring green", "light salmon"]

        # Create bars
        for hour in range(24):
            x = x_start + hour * (2 * bar_width + spacing)
            for i, (junction, counts) in enumerate(junction_counts.items()):
                y = y_base - counts[hour] * scale
                self.canvas.create_rectangle(
                    x + i * bar_width, y, x + (i + 1) * bar_width, y_base,
                    fill=colors[i], outline="black"
                )
                self.canvas.create_text(
                    x + (i + 0.5) * bar_width, y - 10,
                    text=str(counts[hour]), font=("Arial", 8), fill="black"
                )
                # Draw x-axis and y-axis
                self.canvas.create_line(x_start - 10, y_base, x_start + 24 * (bar_width * 2 + spacing), y_base, width=2)

            # Main title and lables
            self.canvas.create_text(280, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})",font=("Arial", 16))
            self.canvas.create_text(700, 650, text="Hours 00:00 to 24:00", font=("Arial", 12))

            for hour in range(24):
                x = x_start + hour * (2 * bar_width + spacing) + bar_width
                self.canvas.create_text(x, y_base + 20, text=str(hour), font=("Arial", 10))

        pass  # Drawing logic goes here

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        legendX=50
        legendY=60
        labels=["Elm Avenue/Rabbithh Road", "Hanley Highway/Westway"]
        colors = ["medium spring green", "light salmon"]

        for i, label in enumerate(labels):
            self.canvas.create_rectangle(legendX, legendY + i * 20, legendX + 20, legendY + i * 20 + 10,fill=colors[i])
            self.canvas.create_text(legendX + 30, legendY + i * 20 + 5, text=label, font=("Arial", 10),anchor="w")

        pass  # Logic for adding a legend

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()
        pass  # Tkinter main loop logic


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            with open(file_path,'r') as file: #open CSV in r mode
                reader=csv.DictReader(file)
                self.current_data=list(reader) #store the read data from rows
            print(f'Loaded data from {file_path}.')
        except FileNotFoundError:
            return False
        except Exception as exception:
            print(f'Error loading file : {exception}')
            return False
        return True

        pass  # File loading and data extraction logic

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data=[] #reset the list

        pass  # Logic for clearing data

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        # Asking for the day
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

        # Asking for the month
        while True:
            try:
                month = int(input('Please enter the month of the survey in the format mm : '))
                if month < 1 or month > 12:
                    print('Out of range - values must range from 1 and 12.')
                    continue
                else:
                    break
            except ValueError:
                print('Integer required ')
        if month < 10:
            month = ('0' + str(month))  # if user inputs 1 digit as month converting it to 2 digits

        # Asking for the year
        while True:
            try:
                year = int(input('Please enter the year of the survey in the format yyyy : '))
                if year < 2000 or year > 2024:
                    print('Out of range - values must range from 2000 and 2024. ')
                    continue

                else:
                    break
            except ValueError:
                print("integer required")

        file_path = f"traffic_data{day}{month}{year}.csv"

        # Load the CSV file and return the file path if successful
        if self.load_csv_file(file_path):
            return file_path
        else:
            print("File not found. Please try again.")

        pass  # Logic for user interaction

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            self.clear_previous_data()
            file_path=self.handle_user_interaction() #get the file path according to inputs

            #if data loaded successfully
            if self.current_data:
                date=file_path[-12:-4] #extract date from file name
                app=HistogramApp(self.current_data,date)
                app.run()

            while True:
                choice = input('\nDo you want to select another file? (y/n): ').lower()
                if choice == 'y':
                    break
                elif choice == 'n':
                    print('\nExiting Program...')
                    return
                else:
                    print('Invalid input. Please enter "y" or "n".')

        pass  # Loop logic for handling multiple files

#Main program
processor=MultiCSVProcessor()
processor.process_files()
