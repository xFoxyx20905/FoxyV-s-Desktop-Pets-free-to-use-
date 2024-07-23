import tkinter as tk
import random
import time
import os


class Desktop_Pet_Func:
    def __init__(self, monitor_index, 
                 screen_areas, screen_heights, screen_widths, 
                 work_areas, work_heights, work_widths,
                 pet_selected_folder, pet_name, mode):
        self.monitor_index = monitor_index
        self.screen_areas = screen_areas
        self.screen_heights = screen_heights
        self.screen_widths = screen_widths
        self.work_areas = work_areas
        self.work_heights = work_heights
        self.work_widths = work_widths
        self.mode = mode
        self.pet_selected_folder = pet_selected_folder
        self.pet_name = pet_name
        self.window = tk.Tk()

        self.is_falling = False
        self.is_landing = False

        # Path to the gif files
        project_root = os.path.dirname(os.path.abspath(__file__))
        print(f"Project Root: {project_root}")
        
        # Use os.path.join to ensure correct path construction
        impath = os.path.join(project_root, self.pet_selected_folder.lstrip('/'))
        print(f"Constructed Image Path: {impath}")

        # Helper function to load gif frames and check file existence
        def load_gif_frames(gif_name, frame_count):
            gif_path = os.path.join(impath, f'{gif_name}.gif')
            print(f"Loading GIF: {gif_path}")
            if not os.path.exists(gif_path):
                print(f"File not found: {gif_path}")
            return [tk.PhotoImage(file=gif_path, format=f'gif -index {i}') for i in range(frame_count)]

        # Call buddy's action gif
        self.idle = load_gif_frames(f'{self.pet_name}_idle', 5) # 5 = 5 frames
        self.idle_to_sleep = load_gif_frames(f'{self.pet_name}_idle_to_sleep', 8) # 8 = 8 frames
        self.sleep = load_gif_frames(f'{self.pet_name}_sleep', 3) # 3 = 3 frames
        self.sleep_to_idle = load_gif_frames(f'{self.pet_name}_sleep_to_idle', 8) # 8 = 8 frames
        self.walk_left = load_gif_frames(f'{self.pet_name}_walking_left', 8) # 8 = 8 frames
        self.walk_right = load_gif_frames(f'{self.pet_name}_walking_right', 8) # 8 = 8 frames
        self.idle_to_eating = load_gif_frames(f'{self.pet_name}_idle_to_eating', 8) # 8 = 8 frames
        self.eating = load_gif_frames(f'{self.pet_name}_eating', 4) # 4 = 4 frames
        self.eating_to_idle = load_gif_frames(f'{self.pet_name}_eating_to_idle', 8) # 8 = 8 frames
        self.idle_to_playing = load_gif_frames(f'{self.pet_name}_idle_to_playing', 8) # 8 = 8 frames
        self.playing = load_gif_frames(f'{self.pet_name}_playing', 8) # 8 = 8 frames
        self.playing_to_idle = load_gif_frames(f'{self.pet_name}_playing_to_idle', 8) # 8 = 8 frames
        self.falling = load_gif_frames(f'{self.pet_name}_falling', 8) # 8 = 8 frames
        self.land = load_gif_frames(f'{self.pet_name}_land', 8) # 8 = 8 frame

        if self.mode:
            self.walk_up = load_gif_frames(f'{self.pet_name}_walking_left', 8)
            self.walk_down = load_gif_frames(f'{self.pet_name}_walking_right', 8)

        # Print debug information
        print(f"Monitor Index: {monitor_index}")
        print(f"Screen Areas: {screen_areas}")
        print(f"Work Areas: {work_areas}")
        print(f"Selected Pet Folder: {pet_selected_folder}")
        print(f"Selected Pet Name: {pet_name}")

        # Ensure monitor_index is within the bounds of screen_areas
        monitor_origin_screen = (screen_areas[monitor_index][0], screen_areas[monitor_index][1])    
        monitor_origin_work = (work_areas[monitor_index][0], work_areas[monitor_index][1])    
        need_adjustment = monitor_origin_screen, monitor_origin_work != (0, 0)
        print("Monitor Origin (Screen):", screen_areas[monitor_index][0], screen_areas[monitor_index][1])

        if need_adjustment:
            adjusted_coordinates_screen = [(area[0] - monitor_origin_screen[0], area[1] - monitor_origin_screen[1], 
                                            area[2] - monitor_origin_screen[0], area[3] - monitor_origin_screen[1])
                                            for area in self.screen_areas]
            print("Adjusted Coords (Screen):", adjusted_coordinates_screen)
            adjusted_coordinates_work = [(area[0] - monitor_origin_work[0], area[1] - monitor_origin_work[1],
                                          area[2] - monitor_origin_work[0], area[3] - monitor_origin_work[1])
                                          for area in self.work_areas]
            print("Adjusted Coords (Work):", adjusted_coordinates_work)

            self.x = int(adjusted_coordinates_screen[self.monitor_index][0] + (adjusted_coordinates_screen[self.monitor_index][2] - adjusted_coordinates_screen[self.monitor_index][0]) * 0.5)
            if self.mode:
                self.y = int(adjusted_coordinates_screen[self.monitor_index][1] + (adjusted_coordinates_screen[self.monitor_index][3] - adjusted_coordinates_screen[self.monitor_index][1]) * 0.5)
            else:
                if adjusted_coordinates_work == adjusted_coordinates_screen:
                    self.y = int(adjusted_coordinates_screen[self.monitor_index][1] + (adjusted_coordinates_screen[self.monitor_index][3] - adjusted_coordinates_screen[self.monitor_index][1])-100) # add  when needed
                else:
                    self.y = int(adjusted_coordinates_work[self.monitor_index][1] + (adjusted_coordinates_work[self.monitor_index][3] - adjusted_coordinates_work[self.monitor_index][1])-100) # add  when needed
        else:
            self.x = int(self.screen_widths[self.monitor_index] * 0.5)
            if self.mode:
                self.y = int(self.screen_heights[self.monitor_index] * 0.5)
            else:
                if self.work_areas == self.screen_areas:
                    self.y = int(self.screen_heights[self.monitor_index]-100) # add  when needed
                else:
                    self.y = int(self.work_heights[self.monitor_index] -100) # add when needed

        print("Cat placed at:", self.x, "on x-Axis")
        print("Cat placed at:", self.y, "on y-Axis")

        # Set up dragging functionality
        self.lastClickX = 0
        self.lastClickY = 0
        self.window.bind('<Button-1>', self.save_last_click_pos)
        self.window.bind('<B1-Motion>', self.dragging)
        self.window.bind('<ButtonRelease-1>', self.stop_dragging)

        self.cycle = 0
        self.check = 1
        self.event_number = random.randint(2, 3)

        self.frame = self.idle[0]
        
        #window configuration
        self.window.config(highlightbackground = 'black')
        self.label = tk.Label(self.window, bd = 0, bg = 'black')
        self.window.overrideredirect(True)
        self.window.wm_attributes('-topmost', True)
        self.window.attributes('-transparentcolor', 'black')
        
        self.label.pack()
        
        #loop the program
        self.window.after(1, self.update, self.cycle, self.check, self.event_number, self.x, self.y)
        self.window.mainloop()

    def save_last_click_pos(self, event):
        self.lastClickX = event.x
        self.lastClickY = event.y

    def dragging(self, event):
        monitor_origin = (self.screen_areas[self.monitor_index][0], self.screen_areas[self.monitor_index][1])
        x, y = event.x_root - self.lastClickX, event.y_root - self.lastClickY
        self.x = x - monitor_origin[0]
        self.y = y - monitor_origin[1]
        # Update window position
        self.window.geometry("+%s+%s" % (x, y))

    def stop_dragging(self, event):
        pass

    #transfer random no. to event
    def event(self, cycle, check, event_number, x, y):
        #print("Entering event method with event_number:", event_number)
        idle_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] #12 (idle to eating) #13 (idle to playing) #14 (idle to sleep)
        walk_left = [15, 16, 17]
        walk_right = [18, 19, 20]
        walk_up = [21, 22, 23]
        walk_down = [24, 25, 26]
        eating_num = [27, 28, 29, 30, 31, 32] #33 (eating to idle)
        playing_num = [34, 35, 36, 37, 38, 39] #40 (playing to idle)
        sleep_num = [41, 42, 43, 44, 45, 46] #47 (sleep to idle)

        if self.event_number in idle_num:
            #print("Condition idle")
            self.check = 0
            self.window.after(400, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 = idle
            #print("idle", event_number)
        elif self.event_number == 12:
            #print("Condition idle_to_eating")
            self.check = 1
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 12 = idle to eating
            #print("idle to eating", event_number)
        elif self.event_number == 13:
            #print("Condition idle_to_playing")
            self.check = 4
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 13 = idle to playing
            #print("idle to playing", event_number)
        elif self.event_number == 14:
            #print("Condition idle_to_eating")
            self.check = 7
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 14 = idle to eating
            #print("idle to eating", event_number)
        elif self.event_number in walk_left:
            #print("Condition walking left")
            self.check = 10
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 15, 16, 17 = walk towards left
            #print("walking left", event_number)
        elif self.event_number in walk_right:
            #print("Condition walking right")
            self.check = 11
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no 18, 19, 20 = walk towards right
            #print("walking right", event_number)
        elif self.event_number in eating_num:
            #print("Condition eating")
            self.check = 2
            self.window.after(200, self.update, self.cycle, self.check, self.event_number, self.x, self.y) # no 21, 22, 23, 24, 25, 26 = eating
            #print("eating", event_number)
        elif self.event_number in playing_num:
            #print("Condition playing")
            self.check = 5
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y) # no 28, 29, 30, 31, 32, 33 = playing
            #print("playing", event_number)
        elif self.event_number in sleep_num:
            #print("Condition sleep")
            self.check = 8
            self.window.after(400, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 35, 36, 37, 38, 39, 40 = sleep
            #print("sleeping", event_number)
        elif self.event_number == 33:
            #print("Condition eating_to_idle")
            self.check = 3
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 33 = eating to idle
            #print("eating to idle", event_number)
        elif self.event_number == 40:
            #print("Condition playing_to_idle")
            self.check = 6
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 40 = playing to idle
            #print("playing to idle", event_number)
        elif self.event_number == 47:
            #print("Condition sleep_to_idle")
            self.check = 9
            self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 47 = sleep to idle
            #print("sleep to idle", event_number)
        elif self.mode:
            if self.event_number in walk_up:
                #print("Condition walking up")
                self.check = 12
                self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no. 42, 43, 44 = walk up
                #print("walking up", event_number)
            elif self.event_number in walk_down:
                #print("Condition walking down")
                self.check = 13
                self.window.after(100, self.update, self.cycle, self.check, self.event_number, self.x, self.y)  # no 45, 46, 47 = walk down
                #print("walking down", event_number)

    #making gif work 
    def gif_work(self, cycle, frames, event_number, a, b):
        if self.cycle < len(frames) - 1:
            self.cycle += 1
        else:
            self.cycle = 0
            if not self.mode:
                exclude_numbers = [21, 22, 23, 24, 25, 26]
                event_number = random.randint(a, b)
                while event_number in exclude_numbers:
                    event_number = random.randint(a, b)
            else:
                event_number = random.randint(a, b)
        return self.cycle, event_number
    
    def update_falling(self):
        # Check if the pet is falling
        target_y = int(self.screen_heights[self.monitor_index] - 100) if self.work_areas == self.screen_areas else int(self.work_heights[self.monitor_index] - 100)
        if not self.mode and self.y < target_y:
            self.is_falling = True
            # Update falling animation frame using gif_work
            self.cycle, self.event_number = self.gif_work(self.cycle, self.falling, self.event_number, 1, 1)
            self.frame = self.falling[self.cycle]
            # Adjust falling speed and limit the falling distance
            self.y += 1  # Adjust falling speed as needed
            if self.y >= target_y:
                self.y = target_y  # Limit the falling distance
                self.cycle = 0  # Reset cycle for landing animation
                  # Stop falling animation when reaching the bottom

                # Start the landing animation
                self.is_landing = True
                self.update_landing()
        else:
            self.is_falling = False

        if not self.is_landing:  # Only schedule next falling update if not landing
            self.window.geometry('100x100+' + str(self.x + self.screen_areas[self.monitor_index][0]) + '+' + str(self.y + self.screen_areas[self.monitor_index][1]))
            self.window.after(50, self.update_falling)

    def update_landing(self):
        if self.is_landing:
            # Update landing animation frame using gif_work
            self.cycle, self.event_number = self.gif_work(self.cycle, self.land, self.event_number, 1, 1)
            self.frame = self.land[self.cycle]
            # Check if the landing animation has completed
            if self.cycle == len(self.land) - 1:
                self.is_falling = False
                self.is_landing = False  # Stop landing animation when completed
                self.cycle = 0  # Reset cycle for the next animation
        else:
            self.is_landing = False
        
        self.window.geometry('100x100+' + str(self.x + self.screen_areas[self.monitor_index][0]) + '+' + str(self.y + self.screen_areas[self.monitor_index][1]))
        
        if self.is_landing:  # Schedule the next update for landing
            
            self.window.after(100, self.update_landing)
        else:  # Continue with normal updates
            self.window.after(100, self.update_falling)

    # update gif frame
    def update(self, cycle, check, event_number, x, y):
        #print("Entering update method with event_number:", event_number)
        #print("Current Animation State:", self.check)
        x -= self.x
        y -= self.y
        self.update_falling()
        if 0 <= self.x <= (self.screen_widths[self.monitor_index] - 72) and 0 <= self.y <= (self.screen_heights[self.monitor_index] - 72):
            #print("Coordinates within bounds")
            if not self.is_falling and not self.is_landing:
                # idle
                if self.check == 0:
                    self.frame = self.idle[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.idle, self.event_number, 1, 26)
                    #print("Idle frame updated, new event_number:", event_number)
                # idle to sleep
                elif self.check == 1:
                    self.frame = self.idle_to_eating[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.idle_to_eating, self.event_number, 27, 27)
                    #print("Idle to eating frame updated, new event_number:", event_number)
                # sleep
                elif self.check == 2:
                    self.frame = self.eating[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.eating, self.event_number, 27, 33)
                    #print("Eating frame updated, new event_number:", event_number)
                # sleep to idle
                elif self.check == 3:
                    self.frame = self.eating_to_idle[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.eating_to_idle, self.event_number, 1, 1)
                    #print("Eating to idle frame updated, new event_number:", event_number)
                # idle to sleep
                elif self.check == 4:
                    self.frame = self.idle_to_playing[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.idle_to_playing, self.event_number, 34, 34)
                    #print("Idle to playing frame updated, new event_number:", event_number)
                # sleep
                elif self.check == 5:
                    self.frame = self.playing[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.playing, self.event_number, 34, 40)
                    #print("Playing frame updated, new event_number:", event_number)
                # sleep to idle
                elif self.check == 6:
                    self.frame = self.playing_to_idle[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.playing_to_idle, self.event_number, 1, 1)
                    #print("Playing to idle frame updated, new event_number:", event_number)
                # idle to sleep
                elif self.check == 7:
                    self.frame = self.idle_to_sleep[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.idle_to_sleep, self.event_number, 41, 41)
                    #print("Idle to sleep frame updated, new event_number:", event_number)
                # sleep
                elif self.check == 8:
                    self.frame = self.sleep[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.sleep, self.event_number, 41, 47)
                    #print("Sleep frame updated, new event_number:", event_number)
                # sleep to idle
                elif self.check == 9:
                    self.frame = self.sleep_to_idle[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.sleep_to_idle, self.event_number, 1, 1)
                    #print("Sleep to idle frame updated, new event_number:", event_number)
                # walk towards left
                elif self.check == 10:
                    self.frame = self.walk_left[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.walk_left, self.event_number, 1, 26)
                    self.x -= 5
                    #print("Walking left frame updated, new event_number:", event_number)
                # walk toward right
                elif self.check == 11:
                    self.frame = self.walk_right[self.cycle]
                    self.cycle, self.event_number = self.gif_work(self.cycle, self.walk_right, self.event_number, 1, 26)
                    self.x += 5
                    #print("Walking right frame updated, new event_number:", event_number)

                # Additional logic for mode-specific animations
                if self.mode:
                    # walk up
                    if self.check == 12:
                        self.frame = self.walk_up[self.cycle]
                        self.cycle, self.event_number = self.gif_work(self.cycle, self.walk_up, self.event_number, 1, 26)
                        self.y -= 5
                        #print("Walking up frame updated, new event_number:", event_number)
                    # walk down
                    elif self.check == 13:
                        self.frame = self.walk_down[self.cycle]
                        self.cycle, self.event_number = self.gif_work(self.cycle, self.walk_down, self.event_number, 1, 26)
                        self.y += 5
                        #print("Walking down frame updated, new event_number:", event_number)

        # If the cat hits the screen border, reverse its direction
        if self.x < 0:
            self.x = 0
        elif self.x > (self.screen_widths[self.monitor_index] - 72):
            self.x = self.screen_widths[self.monitor_index] - 72

        # Reverse direction if hitting top or bottom border
        if self.y < 0:
            self.y = 0
        elif self.y > (self.screen_heights[self.monitor_index] - 72):
            self.y = self.screen_heights[self.monitor_index] - 72

        # Update pet's position after dragging
        self.window.geometry('100x100+' + str(self.x + self.screen_areas[self.monitor_index][0]) + '+' + str(self.y + self.screen_areas[self.monitor_index][1]))

        # Update pet's position within the window
        self.label.config(image=self.frame)
        self.window.after(100, self.event, self.cycle, self.check, self.event_number, self.x, self.y)