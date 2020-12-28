from tkinter import *
from tkinter import filedialog
import json


class Gui:
    def __init__(self):
        # Read config and initialize Variables for Gui
        self.config = json.load(open('config.json', 'r'))
        self.window = Tk()
        self.window.title("Progress Sheet Updater - Configurator")
        self.window.geometry("700x120")
        self.path = StringVar()
        self.sheet_id = StringVar()
        self.calculate_averages = IntVar()
        self.run_once = IntVar()
        self.polling_interval = IntVar()
        self.runs_to_average = IntVar()

        # Give startvalue to variables
        self.calculate_averages.set(int(self.config["calculate_averages"]))
        self.sheet_id.set(self.config["sheet_id"])
        self.run_once.set(int(self.config["run_once"]))
        self.polling_interval.set(int(self.config["polling_interval"]))
        self.path.set(self.config["stats_path"])
        self.runs_to_average.set(int(self.config["num_of_runs_to_average"]))

    def browse_path(self):
        self.path.set(filedialog.askdirectory(initialdir=self.path.get(), title="Open Folder"))

    def finished(self):
        self.config["stats_path"] = self.path.get()
        if self.sheet_id.get().find("docs.google.com") != -1:
            full_link = self.sheet_id.get()
            id_temp = full_link[full_link.find("/d/") + 3:]
            id_temp = id_temp[:id_temp.find("/")]
            self.sheet_id.set(id_temp)
        self.config["sheet_id"] = self.sheet_id.get()
        self.config["calculate_averages"] = (self.calculate_averages.get() == 1)
        self.config["run_once"] = (self.run_once.get() == 1)
        self.config["num_of_runs_to_average"] = self.runs_to_average.get()
        self.config["polling_interval"] = self.polling_interval.get()
        with open("config.json", "w") as outfile:
            json.dump(self.config, outfile, indent=4)
        self.window.destroy()

    def main(self):
        # Gui for path
        path_frame = Frame(self.window)
        pre_path_label = Label(path_frame, text="Kovaak's Stats Path: ")
        browse_path_button = Button(path_frame, text="Browse", command=self.browse_path)
        path_label = Label(path_frame, textvariable=self.path)
        pre_path_label.pack(side="left")
        path_label.pack(side="left")
        browse_path_button.pack(side="right")

        # Gui for sheetid
        sheet_id_frame = Frame(self.window)
        sheet_id_entry = Entry(sheet_id_frame, textvariable=self.sheet_id)
        pre_sheet_id_label = Label(sheet_id_frame, text="Progress Sheet ID: ")
        pre_sheet_id_label.pack(side="left")
        sheet_id_entry.pack(fill="x")

        # Gui for advanced options
        advanced_padding = 25
        advanced_frame = Frame(self.window)
        # Calculate Averages
        calculate_averages_box = Checkbutton(advanced_frame, variable=self.calculate_averages,
                                             text="Calculate Averages")
        calculate_averages_box.pack(side="left", padx=advanced_padding)
        # Run once
        run_once_box = Checkbutton(advanced_frame, text="Run Once", variable=self.run_once)
        run_once_box.pack(side="left", padx=advanced_padding)
        # Polling interval
        polling_interval_frame = Frame(advanced_frame)
        polling_interval_label = Label(polling_interval_frame, text="Polling Interval")
        polling_interval_entry = Entry(polling_interval_frame, textvariable=self.polling_interval, width=5)
        polling_interval_entry.pack(side="left")
        polling_interval_label.pack(side="left")
        polling_interval_frame.pack(side="left", padx=advanced_padding)
        # Runs to average
        runs_to_average_frame = Frame(advanced_frame)
        runs_to_average_entry = Entry(runs_to_average_frame, textvariable=self.runs_to_average, width=3)
        runs_to_average_label = Label(runs_to_average_frame, text="Number of runs to average")
        runs_to_average_entry.pack(side="left")
        runs_to_average_label.pack(side="left")
        runs_to_average_frame.pack(side="left", padx=advanced_padding)

        # Finished button
        finished_frame = Frame(self.window)
        finished_button = Button(finished_frame, command=self.finished, text="Finish")
        finished_button.pack()

        # Pack all frames and run mainloop
        path_frame.pack(fill="x")
        sheet_id_frame.pack(fill="x")
        advanced_label = Label(self.window, text="Advanced Settings")
        advanced_label.pack()
        advanced_frame.pack(fill="x")
        finished_frame.pack(fill="x")
        self.window.mainloop()