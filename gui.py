import json
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Notebook


class Gui:
    def __init__(self, **kwargs):
        # Read config and initialize Variables for Gui
        self.config = kwargs
        if self.config["open_config"]:
            self.window = Tk()
            self.window.title("Progress Sheet Updater - Configurator")
            self.window.geometry("890x400")
            self.path = StringVar()
            self.sheet_id_kovaaks = StringVar()
            self.sheet_id_aimlab = StringVar()
            self.calculate_averages = IntVar()
            self.polling_interval = IntVar()
            self.runs_to_average = IntVar()
            self.open_config = IntVar()
            self.run_mode = StringVar()
            self.game = StringVar()
            self.notebook = Notebook(self.window)
            self.kovaaks_frame = Frame(self.notebook)

            # Initialize Rangelists
            self.name_ranges_entries = []
            self.highscore_ranges_entries = []
            self.average_ranges_entries = []
            self.range_frame_list = []
            self.all_ranges_frame = Frame(self.kovaaks_frame)

            # Give startvalue to variables
            self.calculate_averages.set(int(self.config["calculate_averages"]))
            self.sheet_id_kovaaks.set(self.config["sheet_id_kovaaks"])
            self.sheet_id_aimlab.set(self.config["sheet_id_aimlab"])
            self.polling_interval.set(int(self.config["polling_interval"]))
            self.path.set(self.config["stats_path"])
            self.runs_to_average.set(int(self.config["num_of_runs_to_average"]))
            self.open_config.set(int(self.config["open_config"]))
            self.run_mode.set(self.config["run_mode"])
            self.run_mode_options = ["once",
                                     "watchdog",
                                     "interval"]
            self.game.set(self.config["game"])
            self.game_options = ["Aimlab",
                                 "Kovaaks"]

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
        if self.sheet_id_kovaaks.get().find("docs.google.com") != -1:
            full_link = self.sheet_id_kovaaks.get()
            id_temp = full_link[full_link.find("/d/") + 3:]
            id_temp = id_temp[:id_temp.find("/")]
            self.sheet_id_kovaaks.set(id_temp)
        if self.sheet_id_aimlab.get().find("docs.google.com") != -1:
            full_link = self.sheet_id_aimlab.get()
            id_temp = full_link[full_link.find("/d/") + 3:]
            id_temp = id_temp[:id_temp.find("/")]
            self.sheet_id_aimlab.set(id_temp)
        self.config["sheet_id_kovaaks"] = self.sheet_id_kovaaks.get()
        self.config["sheet_id_aimlab"] = self.sheet_id_aimlab.get()
        self.config["calculate_averages"] = (self.calculate_averages.get() == 1)
        self.config["num_of_runs_to_average"] = self.runs_to_average.get()
        self.config["polling_interval"] = self.polling_interval.get()
        self.config["open_config"] = self.open_config.get() == 1
        self.config["run_mode"] = self.run_mode.get()
        self.config["scenario_name_ranges"] = [entry.get() for entry in self.name_ranges_entries]
        self.config["highscore_ranges"] = [entry.get() for entry in self.highscore_ranges_entries]
        self.config["average_ranges"] = [entry.get() for entry in self.average_ranges_entries]
        current_tab = self.notebook.index("current")
        if current_tab:
            self.config["game"] = "Aimlab"
        else:
            self.config["game"] = "Kovaaks"
        with open("config.json", "w") as outfile:
            json.dump(self.config, outfile, indent=4)
        self.window.destroy()

    def main(self):
        if self.config["open_config"]:
            # Kovaaks tab of the notebook
            # Gui for path
            path_frame = Frame(self.kovaaks_frame)
            pre_path_label = Label(path_frame, text="Kovaak's Stats Path: ")
            browse_path_button = Button(path_frame, text="Browse", command=self.browse_path)
            path_label = Label(path_frame, textvariable=self.path)
            pre_path_label.pack(side="left")
            path_label.pack(side="left")
            browse_path_button.pack(side="right")
            path_frame.pack(fill="x")

            # Gui for sheetid of Kovaaks sheet
            sheet_id_frame_kovaaks = Frame(self.kovaaks_frame)
            sheet_id_entry_kovaaks = Entry(sheet_id_frame_kovaaks, textvariable=self.sheet_id_kovaaks)
            pre_sheet_id_label_kovaaks = Label(sheet_id_frame_kovaaks, text="Progress Sheet ID: ")
            pre_sheet_id_label_kovaaks.pack(side="left")
            sheet_id_entry_kovaaks.pack(fill="x")
            sheet_id_frame_kovaaks.pack(fill="x")

            # Runs to average
            runs_to_average_frame = Frame(self.kovaaks_frame)
            runs_to_average_entry = Entry(runs_to_average_frame, textvariable=self.runs_to_average, width=3)
            runs_to_average_label = Label(runs_to_average_frame, text="Number of runs to average")
            runs_to_average_entry.pack(side="left")
            runs_to_average_label.pack(side="left")
            # Calculate Averages (Kovaaks only atm)
            calculate_averages_box = Checkbutton(runs_to_average_frame, variable=self.calculate_averages,
                                                 text="Calculate Averages")
            calculate_averages_box.pack(side="top")
            runs_to_average_frame.pack(side="top")

            # Aimlab tab of the notebook
            aimlab_frame = Frame(self.notebook)

            # Gui for sheetid of Aimlab sheet
            sheet_id_frame_aimlab = Frame(aimlab_frame)
            sheet_id_entry_aimlab = Entry(sheet_id_frame_aimlab, textvariable=self.sheet_id_aimlab)
            pre_sheet_id_label_aimlab = Label(sheet_id_frame_aimlab, text="Progress Sheet ID: ")
            pre_sheet_id_label_aimlab.pack(side="left")
            sheet_id_entry_aimlab.pack(fill="x")
            sheet_id_frame_aimlab.pack(fill="x")

            # Gui for advanced options
            advanced_padding_x = 25
            advanced_padding_y = 10
            advanced_frame = LabelFrame(self.window, text="Advanced Options")
            # Open config
            open_config_box = Checkbutton(advanced_frame, text="Open config", variable=self.open_config)
            open_config_box.grid(row="0", column="2", padx=advanced_padding_x, pady=advanced_padding_y)
            # Polling interval
            polling_interval_frame = Frame(advanced_frame)
            polling_interval_label = Label(polling_interval_frame, text="Polling Interval")
            polling_interval_entry = Entry(polling_interval_frame, textvariable=self.polling_interval, width=5)
            polling_interval_entry.pack(side="left")
            polling_interval_label.pack(side="left")
            polling_interval_frame.grid(row="0", column="3", padx=advanced_padding_x, pady=advanced_padding_y)
            # Run mode
            run_mode_frame = Frame(advanced_frame)
            run_mode_label = Label(run_mode_frame, text="Run Mode")
            run_mode_dropdown = OptionMenu(run_mode_frame, self.run_mode, *self.run_mode_options)
            run_mode_label.pack(side="left")
            run_mode_dropdown.pack(side="left")
            run_mode_frame.grid(row="0", column="4", padx=advanced_padding_x, pady=advanced_padding_y)

            # Ranges
            i = 0
            while i < len(self.config["scenario_name_ranges"]):
                self.range_frame_list.append(Frame(self.all_ranges_frame, padx=10))
                # Labels
                header_label = Label(self.range_frame_list[i], text="Range Number: " + str(i + 1))
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
                self.range_frame_list[i].grid(row=i // 3, column=i % 3)
                i += 1

            self.all_ranges_frame.pack(fill="x")
            # New Range/Delete Range buttons
            range_button_frame = Frame(self.kovaaks_frame)
            new_range_button = Button(range_button_frame, command=self.new_range, text="Add Range")
            new_range_button.grid(row="0", column="0", columnspan="2")
            del_range_button = Button(range_button_frame, command=self.delete_range, text="Remove Range")
            del_range_button.grid(row="0", column="2", columnspan="2")
            range_button_frame.pack()

            # Finished button
            finished_frame = Frame(self.window)
            finished_button = Button(finished_frame, command=self.finished, text="Finish")
            finished_button.grid(row="1", column="1", columnspan="2")

            # Pack all frames
            self.kovaaks_frame.pack(fill="x")
            aimlab_frame.pack(fill="x")
            self.notebook.add(self.kovaaks_frame, text="Kovaaks")
            self.notebook.add(aimlab_frame, text="Aimlab")
            self.notebook.pack()
            advanced_frame.pack(fill="x")
            finished_frame.pack()

            # Choose correct notebook tab
            if self.config["game"] == "Aimlab":
                self.notebook.select(aimlab_frame)
            else:
                self.notebook.select(self.kovaaks_frame)

            # Run mainloop
            self.window.mainloop()
