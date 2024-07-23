from win32api import GetMonitorInfo, EnumDisplayMonitors
import customtkinter as ctk
import json
import os

# Import only necessary functions from Pet_Module.PetModule
from Pet_Module.PetModule import Desktop_Pet_Func

# Get the Monitor Infos
monitors = EnumDisplayMonitors()

# Extract screen areas from monitor info
screen_areas = [GetMonitorInfo(monitor[0]).get("Monitor") for monitor in monitors]
screen_widths = [area[2] - area[0] for area in screen_areas]
screen_heights = [area[3] - area[1] for area in screen_areas]

# Extract work areas from monitor info
work_areas = [GetMonitorInfo(monitor[0]).get("Work") for monitor in monitors]
work_widths = [area[2] - area[0] for area in work_areas]
work_heights = [area[3] - area[1] for area in work_areas]

# Debug print screen areas
print("Screen Areas:", screen_areas)
print("Work Areas:", work_areas)

# Get the directory of the project's root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the path to config.json relative to the project's root directory
config_file_path = os.path.join(project_root, "config.json")

# Function to load the configuration file
def load_config():
    with open(config_file_path, 'r') as file:
        config = json.load(file)
    return config

# Function to save the configuration file
def save_config(config):
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

# Function to handle pet selection
def select_pet(pet):
    config = load_config()
    config['selected_pet'] = pet
    save_config(config)

# Placeholder for the cat instance
cat_instance = None

def on_submit():
    monitor_index = monitor_var.get()
    mode_value = mode_var.get()
    pet_selected = pet_var.get()

    # Load the updated configuration
    config = load_config()
    config['selected_pet'] = pet_selected
    save_config(config)
    pet_selected_folder = config['pet_folder'].get(pet_selected)

    # Debug prints to check the values
    print(f"Monitor Index: {monitor_index}")
    print(f"Screen Areas: {screen_areas}")
    print(f"Selected Pet Folder: {pet_selected_folder}")
    print(f"Selected Pet Name: {pet_selected}")

    # Check if both monitor and pet are selected
    if monitor_index != -1 and pet_selected: 
        options_window.destroy()
        Desktop_Pet_Func(monitor_index, 
                         screen_areas, screen_heights, screen_widths, 
                         work_areas, work_heights, work_widths,
                         pet_selected_folder, pet_selected, mode_value)
    else:
        error_label.configure(text="Please select both a monitor and a Pet.")

# Create main window
options_window = ctk.CTk()
options_window.title("Choose Monitor, Mode and Pet")
options_window.geometry('400x500')
options_window.resizable(False, False)
options_window.wm_attributes('-topmost', True)

# Variables to hold the selected values
monitor_var = ctk.IntVar(value=-1)
mode_var = ctk.BooleanVar()
pet_var = ctk.StringVar(value='')

# Create custom Font size
font_label = ctk.CTkFont(size=20)
font_credit = ctk.CTkFont(size=12)

# Main header
Main_Header = ctk.CTkLabel(options_window, text="Desktop Pet", font=font_label)
Main_Header.pack()

# Create a frame for center alignment
frame = ctk.CTkFrame(options_window, width=300)
frame.pack(expand=True)

# Create a frame for the bottom right alignment
bottom_frame = ctk.CTkFrame(options_window, fg_color="transparent")
bottom_frame.pack(side="bottom", anchor="se", padx=10, pady=10)

# Text at the bottom right
author_label = ctk.CTkLabel(bottom_frame, text="by FoxyVolpino", font=font_credit)
author_label.pack()

# Create monitor selection checkboxes
ctk.CTkLabel(frame, text="Select Monitor:", font=font_label).grid(row=0, column=0, columnspan=2, pady=10, padx=20)
for index_monitor, monitor in enumerate(monitors):
    row = (index_monitor // 2) + 1
    column = (index_monitor % 2)
    ctk.CTkRadioButton(frame, radiobutton_width=20, radiobutton_height=20, text=f"Monitor {index_monitor + 1}", variable=monitor_var, value=index_monitor).grid(row=row, column=column, pady=5, padx= (20,0))

# Create mode selection checkbox
ctk.CTkLabel(frame, text="Select Mode:", font=font_label).grid(row=len(monitors) + 1, column=0, columnspan=2, pady=10, padx=20)
ctk.CTkCheckBox(frame, checkbox_width=20, checkbox_height=20, border_width=2, text="Free-roam (unchecked for Task bar)", variable=mode_var).grid(row=len(monitors) + 2, column=0, columnspan=2, pady=5)

# Create Pet selection checkboxes 
config = load_config()
available_pets = list(config['pet_folder'].keys())
selected_pet = config['selected_pet']
pet_var.set(selected_pet)

# Create Pet selection radio buttons
ctk.CTkLabel(frame, text="Select Pet:", font=font_label).grid(row=len(monitors) + 3, column=0, columnspan=2, pady=10, padx=20)
for index_pet, pet in enumerate(available_pets):
    row = (index_pet // 2) + len(monitors) + 4
    column = (index_pet % 2)
    ctk.CTkRadioButton(frame, radiobutton_width=20, radiobutton_height=20, text=pet.capitalize(), variable=pet_var, value=pet).grid(row=row, column=column, pady=5, padx=(20, 0))

# Submit button
ctk.CTkButton(frame, text="Submit", command=on_submit,
              hover=True, hover_color="Dark Green",
              fg_color="Green").grid(row=len(monitors) + 5 + len(available_pets), column=0, columnspan=2, pady=10)

# Error message label
error_label = ctk.CTkLabel(frame, text="", fg_color="transparent", text_color="red")
error_label.grid(row=len(monitors) + 6 + len(available_pets), column=0, columnspan=2)

# Start the Tkinter event loop
options_window.mainloop()