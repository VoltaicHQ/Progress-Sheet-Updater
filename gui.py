import json
from tkinter import *
from tkinter import filedialog


class Gui:
    def __init__(self, **kwargs):
        # Read config and initialize Variables for Gui
        self.config = kwargs
        if self.config["open_config"]:
            self.window = Tk()
            self.window.title("Progress Sheet Updater - Configurator")
            self.window.geometry("890x400")
            self.path = StringVar()
            self.sheet_id = StringVar()
            self.calculate_averages = IntVar()
            self.polling_interval = IntVar()
            self.runs_to_average = IntVar()
            self.open_config = IntVar()
            self.run_mode = StringVar()

            # Initialize Rangelists
            self.name_ranges_entries = []
            self.highscore_ranges_entries = []
            self.average_ranges_entries = []
            self.range_frame_list = []
            self.all_ranges_frame = Frame(self.window)

            # Give startvalue to variables
            self.calculate_averages.set(int(self.config["calculate_averages"]))
            self.sheet_id.set(self.config["sheet_id"])
            self.polling_interval.set(int(self.config["polling_interval"]))
            self.path.set(self.config["stats_path"])
            self.runs_to_average.set(int(self.config["num_of_runs_to_average"]))
            self.open_config.set(int(self.config["open_config"]))
            self.run_mode.set(self.config["run_mode"])
            self.run_mode_options = ["once",
                                     "watchdog",
                                     "interval"]

    def browse_path(self):
        self.path.set(filedialog.askdirectory(initialdir=self.path.get(), title="Open Folder"))

    def new_range(self):
        self.range_frame_list.append(Frame(self.all_ranges_frame, padx=20))
        # Labels
        header_label = Label(self.range_frame_list[-1], text="Range Number: " + str(len(self.range_frame_list)))
        name_label = Label(self.range_frame_list[-1], text="Name Range: ")
        hs_label = Label(self.range_frame_list[-1], text="Highscore Range: ")
        average_label = Label(self.range_frame_list[-1], text="Average Range: ")
        # Add new entries
        self.name_ranges_entries.append(Entry(self.range_frame_list[-1], width=32))
        self.highscore_ranges_entries.append(Entry(self.range_frame_list[-1], width=32))
        self.average_ranges_entries.append(Entry(self.range_frame_list[-1], width=32))
        # Pack new entries
        header_label.grid(row="0", column="0", columnspan="2")
        name_label.grid(row="1", column="0")
        self.name_ranges_entries[-1].grid(row="1", column="1")
        hs_label.grid(row="2", column="0")
        self.highscore_ranges_entries[-1].grid(row="2", column="1")
        average_label.grid(row="3", column="0")
        self.average_ranges_entries[-1].grid(row="3", column="1")
        self.range_frame_list[-1].grid(row=(len(self.range_frame_list)-1) // 3, column=(len(self.range_frame_list)-1) % 3)

    def delete_range(self):
        self.range_frame_list[-1].destroy()
        self.range_frame_list.pop()
        self.name_ranges_entries.pop()
        self.highscore_ranges_entries.pop()
        self.average_ranges_entries.pop()

    def finished(self):
        self.config["stats_path"] = self.path.get()
        if self.sheet_id.get().find("docs.google.com") != -1:
            full_link = self.sheet_id.get()
            id_temp = full_link[full_link.find("/d/") + 3:]
            id_temp = id_temp[:id_temp.find("/")]
            self.sheet_id.set(id_temp)
        self.config["sheet_id"] = self.sheet_id.get()
        self.config["calculate_averages"] = (self.calculate_averages.get() == 1)
        self.config["num_of_runs_to_average"] = self.runs_to_average.get()
        self.config["polling_interval"] = self.polling_interval.get()
        self.config["open_config"] = self.open_config.get() == 1
        self.config["run_mode"] = self.run_mode.get()
        self.config["scenario_name_ranges"] = [entry.get() for entry in self.name_ranges_entries]
        self.config["highscore_ranges"] = [entry.get() for entry in self.highscore_ranges_entries]
        self.config["average_ranges"] = [entry.get() for entry in self.average_ranges_entries]
        with open("config.json", "w") as outfile:
            json.dump(self.config, outfile, indent=4)
        self.window.destroy()

    def main(self):
        if self.config["open_config"]:
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
            # Open config
            open_config_box = Checkbutton(advanced_frame, text="Open config", variable=self.open_config)
            open_config_box.pack(side="left", padx=advanced_padding)
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
            # Run mode
            run_mode_frame = Frame(advanced_frame)
            run_mode_label = Label(advanced_frame, text="Run Mode")
            run_mode_dropdown = OptionMenu(advanced_frame, self.run_mode, *self.run_mode_options)
            run_mode_label.pack(side="left")
            run_mode_dropdown.pack(side="left")
            run_mode_frame.pack(side="left", padx=advanced_padding)

            # Ranges
            i = 0
            while i < len(self.config["scenario_name_ranges"]):
                self.range_frame_list.append(Frame(self.all_ranges_frame, padx=10))
                # Labels
                header_label = Label(self.range_frame_list[i], text="Range Number: "+str(i+1))
                name_label = Label(self.range_frame_list[i], text="Name Range: ")
                hs_label = Label(self.range_frame_list[i], text="Highscore Range: ")
                average_label = Label(self.range_frame_list[i], text="Average Range: ")
                # Add new entries
                self.name_ranges_entries.append(Entry(self.range_frame_list[i], width=32))
                self.highscore_ranges_entries.append(Entry(self.range_frame_list[i], width=32))
                self.average_ranges_entries.append(Entry(self.range_frame_list[i], width=32))
                # Set value of entries
                self.name_ranges_entries[i].insert(0, self.config["scenario_name_ranges"][i])
                self.highscore_ranges_entries[i].insert(0, self.config["highscore_ranges"][i])
                self.average_ranges_entries[i].insert(0, self.config["average_ranges"][i])
                # Pack entries
                header_label.grid(row="0", column="0", columnspan="2")
                name_label.grid(row="1", column="0")
                self.name_ranges_entries[i].grid(row="1", column="1")
                hs_label.grid(row="2", column="0")
                self.highscore_ranges_entries[i].grid(row="2", column="1")
                average_label.grid(row="3", column="0")
                self.average_ranges_entries[i].grid(row="3", column="1")
                self.range_frame_list[i].grid(row=i//3, column=i % 3)
                i += 1

            # Finished/New Range/Delete Range buttons
            finished_frame = Frame(self.window)
            new_range_button = Button(finished_frame, command=self.new_range, text="Add Range")
            new_range_button.grid(row="0", column="0", columnspan="2")
            del_range_button = Button(finished_frame, command=self.delete_range, text="Remove Range")
            del_range_button.grid(row="0", column="2", columnspan="2")
            finished_button = Button(finished_frame, command=self.finished, text="Finish")
            finished_button.grid(row="1", column="1", columnspan="2")

            # Pack all frames and run mainloop
            path_frame.pack(fill="x")
            sheet_id_frame.pack(fill="x")
            advanced_label = Label(self.window, text="Advanced Settings")
            advanced_label.pack()
            advanced_frame.pack(fill="x")
            self.all_ranges_frame.pack(fill="x")
            finished_frame.pack()
            self.window.mainloop()
