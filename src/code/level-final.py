import tkinter as tk
from tkinter import messagebox
import random
import time
import csv
from PIL import Image, ImageDraw, ImageTk
import mysql.connector
import pickle
import subprocess
# Define themes
def get_user_name():
    with open('text.txt','r') as f:
        username=f.read()
        return username
THEMES = {
    "Default": {"frame_color":"#aaa","bg_color": "#bbb", "block_color": "#ddd", "block_hover_color": "#aaa"},
    "Lavender Haze": {"frame_color":"mediumpurple4","bg_color": "white", "block_color": "mediumpurple1", "block_hover_color": "ghostwhite"},
    "Sunflower": {"frame_color":"orange","bg_color": "lightsalmon1", "block_color": "gold", "block_hover_color": "antiquewhite"},
    "Berries": {"frame_color":"goldenrod1","bg_color": "thistle1", "block_color": "plum4", "block_hover_color": "snow"},
    "Aurora": {"frame_color":"CORAL1","bg_color": "white", "block_color": "steelblue", "block_hover_color": "antiquewhite"},
    "Batman": {"frame_color":"gray25","bg_color": "cyan", "block_color": "gray37", "block_hover_color": "violetred1"},
    "Storm": {"frame_color":"deepskyblue4","bg_color": "floralwhite", "block_color": "deepskyblue1", "block_hover_color": "#fce6c9"}
}
levels ={'easy':{'w':12,'h':6,'x':5,'y':5,'m':5},
         'medium':{'w':8,'h':4,'x':7,'y':7,'m':15},
         'hard':{'w':2,'h':1,'x':20,'y':20,'m':99}
         }
def sign_out():
    file_path="src//code//sign_in.py"
    subprocess.Popen(file_path, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    root.destroy()
def show_profile_frame():
    # Create a new window/frame for the profile
    profile_frame = tk.Toplevel(root)
    profile_frame.title("Profile")
    
    # Set the size of the profile frame
    profile_frame.geometry("400x400")  # Adjust size as needed
    profile_frame.config(bg='white')  # Set background to match theme

    # Load and display the profile picture (circular)
    img = Image.open("src\\assets\\7603322.png")  # Load the profile picture
    img = img.resize((80, 80), Image.LANCZOS)  # Resize image as necessary
    profile_picture = ImageTk.PhotoImage(img)
    
    profile_picture_label = tk.Label(profile_frame, image=profile_picture, bg='black')
    profile_picture_label.image = profile_picture  # Keep a reference
    profile_picture_label.place(x=10, y=10)  # Position in the top left corner

    # Create a circular mask for the profile picture
    mask = Image.new("L", (80, 80), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 80, 80), fill=255)

    # Apply the mask to the image
    img.putalpha(mask)
    profile_picture = ImageTk.PhotoImage(img)
    profile_picture_label.config(image=profile_picture)
    profile_picture_label.image = profile_picture

    # Display username under the profile picture
    username_label = tk.Label(profile_frame, text=f"Username: {username}", bg='white')
    username_label.place(x=10, y=100)  # Position under the profile picture

    # Retrieve and display user data
    efficiency, best_time, top_leaders = fetch_user_data()

    # Center the efficiency and best time in the profile frame
    efficiency_label = tk.Label(profile_frame, text=f"Efficiency: {efficiency}", bg='white')
    efficiency_label.place(relx=0.5, rely=0.5, anchor='center')  # Centered

    best_time_label = tk.Label(profile_frame, text=f"Best Time: {best_time}", bg='white')
    best_time_label.place(relx=0.5, rely=0.55, anchor='center')  # Slightly below

    # Create a leaderboard label aligned to the top right corner
    leaderboard_label = tk.Label(profile_frame, text="Top 5 Players:", bg='white')
    leaderboard_label.place(relx=0.85, y=10, anchor='ne')  # Top right corner

    # Display the top 5 players
    leaderboard_start_y = 30  # Starting y position for leaderboard
    for index, player in enumerate(top_leaders):
        player_label = tk.Label(profile_frame, text=f"{index + 1}. {player[0]} - {player[1]} sec", bg='white')
        player_label.place(relx=0.85, y=leaderboard_start_y + (index * 20), anchor='ne')  # Adjust y position for each player

    # Sign Out Button
    sign_out_button = tk.Button(profile_frame, text="Sign Out", command=sign_out, bg='red', fg='white')
    sign_out_button.place(relx=0.5, y=350, anchor='center')  # Centered at the bottom



def fetch_user_data():
    # Establish database connection
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='MySQL1234',
        database='userdata'
    )
    
    cursor = connection.cursor()
    
    # Retrieve the current user's ID based on the username
    cursor.execute("SELECT userid FROM data WHERE username = %s", (username,))
    result = cursor.fetchone()
    current_user_id = result[0] if result else None  # Ensure we handle cases where no user is found

    if current_user_id is not None:
        # Query to get efficiency and best time for the current user
        cursor.execute("SELECT efficiency, best_time FROM game_stats WHERE userid = %s", (current_user_id,))
        user_stats = cursor.fetchone()  # Fetch once

        if user_stats:
            efficiency, best_time = user_stats
        else:
            efficiency, best_time = 0, 0  # Default values if no stats are found

        # Query to get the leaderboard (top 5 players with usernames)
        cursor.execute("""
            SELECT d.username, g.best_time 
            FROM game_stats g
            JOIN data d ON g.userid = d.userid
            ORDER BY g.best_time ASC 
            LIMIT 5
        """)
        top_leaders = cursor.fetchall()
    else:
        efficiency, best_time = 0, 0
        top_leaders = []

    # Close the database connection
    cursor.close()
    connection.close()

    return efficiency, best_time, top_leaders



# Example usage: Show profile frame when the profile button is clicked
##profile_button = tk.Button(root, text="Profile", command=show_profile_frame)
##profile_button.pack()

help_count = 0
help_button = None
current_theme = None  # Declare current_theme globally
win_label = None
lose_label = None
restart_button = None
quit_button = None
timer = None  # Initialize timer globally
username = get_user_name()  # Placeholder for the actual username
profile_picture_path = "src\\assets\\7603322.png"  # Update this to the actual path



def update_wingame_stats():
    username = get_user_name()
    time = timer.get_elapsed_time()
    gameplayed = 1
    gamewon = 1
    data = [username, gameplayed, gamewon, time]

    # Write data to a binary file using pickle
    with open('w.dat', 'wb') as f:
        pickle.dump(data, f)

    # Read data from the binary file and update the database
    with open('w.dat', 'rb') as f:
        data = pickle.load(f)

        username = data[0]
        games_played = data[1]
        games_won = data[2]
        time = data[3]

        try:
            # Establish the connection to the database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='MySQL1234',
                database='userdata'
            )
            cursor = connection.cursor()

            # Get the userid based on the username
            cursor.execute("SELECT userid FROM data WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                userid = result[0]

                # Update the game_stats table
                cursor.execute("""
                    INSERT INTO game_stats (userid, games_played, games_won, best_time)
                    VALUES (%s, 1, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    games_played = games_played + 1,
                    games_won = games_won + %s,
                    best_time = LEAST(best_time, %s);
                """, (userid, games_won, time, games_won, time))

                # Commit the changes to the database
                connection.commit()

        except Error as e:
            print(f"Error occurred: {e}")
        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()


def update_losegame_stats():
    username = get_user_name()
    
    gameplayed = 1
    gamewon = 0
    data = [username, gameplayed, gamewon]

    # Write data to a binary file using pickle
    with open('w.dat', 'wb') as f:
        pickle.dump(data, f)

    # Read data from the binary file and update the database
    with open('w.dat', 'rb') as f:
        data = pickle.load(f)

        username = data[0]
        games_played = data[1]
        games_won = data[2]
        

        # Establish the connection to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MySQL1234',
            database='userdata'
        )
        cursor = connection.cursor()

        # Get the userid based on the username
        cursor.execute("SELECT userid FROM data WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            userid = result[0]

            # Update the game_stats table by incrementing games_played and games_won
            cursor.execute("""
                INSERT INTO game_stats (userid, games_played, games_won)
                VALUES (%s, 1, %s)
                ON DUPLICATE KEY UPDATE
                games_played = games_played + 1,
                games_won = games_won + %s;
            """, (userid, games_won,games_won))

            # Commit the changes to the database
            connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

class Block:
    all = []
    particles = []
    number_of_mines_left = None
    number_of_mines = 5
    number_of_flags = 0
    number_of_blocks=64

    def __init__(self, x, y, root, mine=False):
        self.mine = mine
        self.opened = False
        self.flagged = False
        self.x = x
        self.y = y
        self.block = None
        self.root = root  # Store root reference
        Block.all.append(self)

    def create_block(self, location):
        try:
            self.block = tk.Button(location, width=var['w'], height=var['h'], relief='raised', bg=THEMES["Default"]["block_color"], font=('Arial', 10, 'bold'))
            self.block.bind('<Button-1>', self.left_click)
            self.block.bind('<Button-3>', self.right_click)
            self.block.bind("<Enter>", self.on_enter)
            self.block.bind("<Leave>", self.on_leave)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating block: {e}")

    def place_block(self):
        try:
            self.block.grid(column=self.x, row=self.y, padx=1, pady=1)  # Adjust padx and pady as needed
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while placing block: {e}")

    def ran_mines(first_click):
        all_blocks_except_first = [block for block in Block.all if block != first_click]
        picked_blocks = random.sample(all_blocks_except_first, Block.number_of_mines)
        for picked_block in picked_blocks:
            picked_block.mine = True
            


    # Modify the `left_click` method in the `Block` class to ensure `ran_mines()` is called correctly
    
    # other class methods and properties...
    def left_click(self, event):
        if not timer.running:
            timer.start()

        if not any(block.mine for block in Block.all):
            Block.ran_mines(self)

        if self.mine:
            self.show_mine()
            Block.reveal_all_mines()
            Block.disable_all_blocks()
            update_losegame_stats()
            show_lose_screen()
        else:
            if self.surrounded_mines == 0:
                for block in self.surrounded_blocks:
                    if not block.opened:
                        block.show_block()
            self.show_block()

            unopened_blocks = [block for block in Block.all if not block.opened and not block.mine]
            #print(f"Unopened blocks: {len(unopened_blocks)}, Expected to win if this equals {Block.number_of_mines}")

            if len(unopened_blocks) == Block.number_of_mines:  # All non-mine blocks are opened
                Block.reveal_all_mines()
                Block.disable_all_blocks()
                update_wingame_stats()                
                show_win_screen()

    # other class methods...

    def right_click(self, event):
        if not self.opened:
            if not self.flagged and Block.number_of_mines > 0:
                self.block.configure(text='🚩', bg=THEMES["Default"]["block_color"], fg="red", font=('Arial', 10, 'bold'))  # Flag icon
                self.flagged = True
                Block.number_of_mines -= 1
                Block.number_of_flags += 1
                Block.number_of_blocks -=1
               
                if Block.number_of_mines_left:
                    Block.number_of_mines_left.configure(text=f'Mines Left: {Block.number_of_mines}')
##                if flags_count_label:
##                    flags_count_label.configure(text=f'Flags: {Block.number_of_flags}')
            elif self.flagged:
                self.block.configure(text='', bg=THEMES["Default"]["block_color"])  # Remove flag icon
                self.flagged = False
                Block.number_of_mines += 1
                Block.number_of_flags -= 1
                if Block.number_of_mines_left:
                    Block.number_of_mines_left.configure(text=f'Mines Left: {Block.number_of_mines}')
                if flags_count_label:
                    flags_count_label.configure(text=f'Flags: {Block.number_of_flags}')

    def on_enter(self, event):
        if not self.opened:
            theme = THEMES[current_theme.get()]
            self.block.configure(bg=theme["block_hover_color"])  # Change color when hovered

    def on_leave(self, event):
        if not self.opened:
            theme = THEMES[current_theme.get()]
            self.block.configure(bg=theme["block_color"])  # Change back to default color when not hovered

    def show_block(self):
        if not self.opened and not self.flagged:
            self.opened = True
            if self.mine:
                self.block.configure(bg='red', relief='sunken', text='💣')
                Block.number_of_mines -= 1
                if Block.number_of_mines_left:
                    Block.number_of_mines_left.configure(text=f'Mines Left: {Block.number_of_mines}')
            else:
                # Choose color based on the number of surrounded mines
                colors = {1: 'blue', 2: 'green', 3: 'red', 4: 'navy', 5: 'maroon', 6: 'teal', 7: 'black', 8: 'gray'}
                number_of_mines = self.surrounded_mines
                if number_of_mines == 0:
                    theme = THEMES[current_theme.get()]
                    self.block.configure(text='', bg=theme["bg_color"], relief='sunken')  # Use theme bg color
                else:
                    theme = THEMES[current_theme.get()]
                    color = colors.get(number_of_mines, 'black')
                    self.block.configure(text=number_of_mines, bg=theme["bg_color"], fg=color, relief='sunken')  # Use theme bg color

    def show_mine(self):
        self.block.configure(bg='red', relief='sunken', text='💣')

    @property
    def surrounded_blocks(self):
        blocks = [self.get_block(self.x - 1, self.y - 1), self.get_block(self.x - 1, self.y),
                  self.get_block(self.x - 1, self.y + 1), self.get_block(self.x, self.y - 1),
                  self.get_block(self.x + 1, self.y - 1), self.get_block(self.x + 1, self.y),
                  self.get_block(self.x + 1, self.y + 1), self.get_block(self.x, self.y + 1)]
        blocks = [block for block in blocks if block is not None]
        return blocks

    @property
    def surrounded_mines(self):
        count = 0
        for block in self.surrounded_blocks:
            if block.mine:
                count += 1
        return count

    def get_block(self, x, y):
        for block in Block.all:
            if block.x == x and block.y == y:
                return block


            


    @staticmethod
    def reveal_all_mines():
        for block in Block.all:
            if block.mine:
                block.show_mine()

    @staticmethod
    def disable_all_blocks():
        for block in Block.all:
            if block.block:
                block.block.configure(state='disabled')


# Modify the Timer class to include a time limit for Time Trial mode
class Timer:
    def __init__(self, label):
        self.label = label
        self.running = False
        self.start_time = None
        self.time_limit = 90  # Time limit in seconds (1.5 minutes)

    def start(self):
        self.start_time = time.time()
        self.running = True
        self.update()

    def stop(self):
        self.running = False

    def reset(self):
        self.stop()
        self.start_time = None
        self.label.config(text="Time: 00:00:00")

    def update(self):
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            if elapsed_time >= self.time_limit:  # Check if time limit exceeded
                self.stop()
                show_lose_screen()  # Force a loss if time limit exceeded
            else:
                hours = elapsed_time // 3600
                minutes = (elapsed_time % 3600) // 60
                seconds = elapsed_time % 60
                self.label.config(text=f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
                self.label.after(1000, self.update)  # Update every second
    def get_elapsed_time(self):
        return int(time.time() - self.start_time)
        

def restart_game():
    global help_count, help_button,current_theme, win_label, lose_label, restart_button, quit_button
    stored_theme = current_theme.get()  # Store the current theme
    help_count = 0
    def apply_level():
            stored_theme = current_theme.get()  # Store the current theme
            current_theme.set(stored_theme)  # Reapply the stored theme
                
            global var
            level = level_var.get()
            # Get the current level from StringVar
            var = levels[level]  # Access the level dictionary

            for widget in main_frame.winfo_children():
                widget.destroy()

            Block.all = []
            Block.particles = []
            Block.number_of_mines = levels[level]['m']
            Block.number_of_blocks = var['x'] * var['y']

            for x in range(var['x']):
                for y in range(var['y']):
                    block = Block(x, y, main_frame)
                    block.create_block(main_frame)
                    block.place_block()
            change_theme()  # Update the theme
    def change_theme():
            theme = THEMES[current_theme.get()]
##            root.configure(bg=theme["frame_color"])  # Change root background color
##            main_frame.configure(bg=theme["bg_color"])  # Change main_frame background color
##            top_frame.config(bg=theme["frame_color"])
##            left_frame.config(bg=theme["frame_color"])
##            middle_frame.config(bg=theme["frame_color"])
##            right_frame.config(bg=theme["frame_color"])
##                   
##
            for block in Block.all:
                if block.block:
                    block.block.configure(bg=theme["block_color"])  # Change block background color
                    if not block.opened:
                        block.block.configure(bg=theme["block_color"])  # Change block background color when not opened
        
        


    try:
        # Remove win or lose message if they exist
        if win_label:
            win_label.destroy()
            win_label = None
        if lose_label:
            lose_label.destroy()
            lose_label = None

        # Remove restart and quit buttons if they exist
        if restart_button:
            restart_button.destroy()
            restart_button = None
        if quit_button:
            quit_button.destroy()
            quit_button = None
        
        for block in Block.all:
            if block.block:
                block.block.destroy()
        Block.all.clear()
        Block.number_of_mines = levels[level_var.get()]['m']
        Block.number_of_blocks = levels[level_var.get()]['x'] * levels[level_var.get()]['y'] - Block.number_of_mines

        for x in range(levels[level_var.get()]['x']):
            for y in range(levels[level_var.get()]['y']):
                block = Block(x, y, main_frame)
                block.create_block(main_frame)
                block.place_block()

        first_click = Block(0, 0, main_frame)
        Block.ran_mines(first_click)
        Block.number_of_mines_left.configure(text=f'Mines Left: {Block.number_of_mines}')
##        flags_count_label.configure(text=f'Flags: {Block.number_of_flags}')
        timer.reset()
        #current_theme.set(stored_theme)
        apply_level()# Reapply the stored theme
##        change_theme()  # Update the theme
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while restarting game: {e}")

def use_help():
    global help_count, help_button
    if help_count < 2:
        for block in Block.all:
            if block.mine and not block.flagged:
                block.right_click(None)
                help_count += 1
                break
        if help_count == 2:
            help_button.place_forget()  # Hide the help button
            messagebox.showinfo('Help Limit','Help Limit Exceeded')
        elif help_count == 1:
            messagebox.showinfo('Help Limit','You only use it once more!')
    else:
        messagebox.showinfo('Help Limit','Help Limit Exceeded')
        help_button.place_forget()  # Hide the help button if the limit is exceeded


def show_help():
    help_text = """
    Welcome to Minesweeper!

    The objective of Minesweeper is to clear the board without detonating any mines.
   
    How to Play:
    1. Left-click on a block to reveal what's underneath it.
    2. If you reveal a mine, you lose the game.
    3. If you reveal an empty space, it will show a number indicating how many mines are adjacent to that block.
    4. Use the numbers to deduce where the mines are located.
    5. Right-click on a block to flag it as a potential mine.
    6. Once you've flagged all the mines, you win the game!

    Advanced Strategies:
    - Pay attention to the numbers. They indicate how many mines are adjacent to a block.
    - Use logical deduction to determine the locations of mines.
    - Don't rush. Take your time to carefully consider each move.

    Good luck and have fun playing Minesweeper!
    """
    messagebox.showinfo("Minesweeper Help", help_text)


def show_win_screen():
    destroy_blocks()  # Destroy blocks first
    root.after(1000, lambda: display_win_message())  # Delay displaying win message by 1 second

def show_lose_screen():
    destroy_blocks()  # Destroy blocks first
    root.after(1000, lambda: display_lose_message())  # Delay displaying lose message by 1 second

def destroy_blocks():
    for block in Block.all:
        if block.block:
            fade_out_block(block.block)

def fade_out_block(widget, duration=1000):
    current_background = widget.cget("background")
    current_alpha = 255  # Default alpha value
    if current_background.startswith("#"):
        current_alpha = int(current_background[1:3], 16)  # Extract alpha value from hexadecimal color code
    delay = duration / 10  # Delay between steps
    step = current_alpha / 10  # Number of steps for fading
    fade_out_step(widget, current_alpha, step, delay)

def fade_out_step(widget, current_alpha, step, delay):
    if current_alpha <= 0:
        widget.destroy()
    else:
        new_alpha = max(current_alpha - step, 0)  # Ensure alpha value doesn't go below 0
        new_color = "#%02x%02x%02x" % (int(widget.winfo_rgb(widget.cget("background"))[0] / 256),
                                        int(widget.winfo_rgb(widget.cget("background"))[1] / 256),
                                        int(new_alpha))
        widget.configure(bg=new_color)  # Update background color with new alpha value
        widget.after(int(delay), fade_out_step, widget, new_alpha, step, delay)

def end_game():
            root.destroy()

def display_win_message():
    global win_frame, win_label, restart_button, quit_button, win_timer_label,main_frame
    Timer.stop(timer)
    e= timer.get_elapsed_time()
##    print(e)
    main_frame.configure(bg="#3498db")
    win_frame = tk.Frame(root, bg=THEMES[current_theme.get()]["bg_color"], highlightbackground=THEMES[current_theme.get()]["frame_color"], highlightthickness=3)
    win_frame.place(relx=0.5, rely=0.5, anchor="center")
    win_label = tk.Label(win_frame, text="Congratulations! You Have Won", font=('Arial', 18, 'bold'), pady=20, bg=THEMES[current_theme.get()]["bg_color"], fg="black")
    win_label.pack(expand=True)
    restart_button = tk.Button(win_frame, text="Exit", command=end_game)
    restart_button.pack(pady=10)
    win_timer_label = tk.Label(win_frame, text="Restarting in 3 seconds", font=('Arial', 12), pady=10, bg=THEMES[current_theme.get()]["bg_color"], fg="black")
    win_timer_label.pack()
    root.after(1000, update_win_timer)
def add_to_leaderboard():
    with open('leaderboard.csv','a') as f:
        time=timer.label.cget('text')
        a=[name,time]
        writer=csv.writer(f)
        writer.writerow(a)
       
       

def display_lose_message():
    global lose_frame, lose_label, restart_button, quit_button, lose_timer_label,main_frame
    Timer.stop(timer)
    e= timer.get_elapsed_time()
##    print(e)
    main_frame.configure(bg="#3498db")
   
    lose_frame = tk.Frame(root, bg=THEMES[current_theme.get()]["bg_color"], highlightbackground=THEMES[current_theme.get()]["frame_color"], highlightthickness=3)
    lose_frame.place(relx=0.5, rely=0.5, anchor="center")
    lose_label = tk.Label(lose_frame, text="Game Over. You Clicked on a mine.", font=('Arial', 18, 'bold'), pady=20, bg=THEMES[current_theme.get()]["bg_color"], fg="black")
    lose_label.pack()
    restart_button = tk.Button(lose_frame, text="Exit", command=end_game)
    restart_button.pack(pady=10)
    lose_timer_label = tk.Label(lose_frame, text="Restarting in 3 seconds", font=('Arial', 12), pady=10, bg=THEMES[current_theme.get()]["bg_color"], fg="black")
    lose_timer_label.pack()
    root.after(1000, update_lose_timer)

def update_win_timer():
    global win_timer_label
    count = int(win_timer_label.cget("text").split(" ")[-2])
    if count > 1:
        win_timer_label.config(text=f"Restarting in {count - 1} seconds")
        root.after(1000, update_win_timer)
    else:
        destroy_win_message()

def update_lose_timer():
    global lose_timer_label
    count = int(lose_timer_label.cget("text").split(" ")[-2])
    if count > 1:
        lose_timer_label.config(text=f"Restarting  in {count - 1} seconds")
        root.after(1000, update_lose_timer)
    else:
        destroy_lose_message()

def destroy_win_message():
    win_frame.destroy()
    restart_game()
def open_user_profile():
    # Logic to open the user profile
    messagebox.showinfo("User Profile", f"Welcome, {username}!")

def destroy_lose_message():
    lose_frame.destroy()
    restart_game()
##def change_theme():
##            theme = THEMES[current_theme.get()]
##            root.configure(bg=theme["frame_color"])  # Change root background color
##            main_frame.configure(bg=theme["bg_color"])  # Change main_frame background color
##            top_frame.config(bg=theme["frame_color"])
##            left_frame.config(bg=theme["frame_color"])
##            middle_frame.config(bg=theme["frame_color"])
##            right_frame.config(bg=theme["frame_color"])
##                   
##
##            for block in Block.all:
##                if block.block:
##                    block.block.configure(bg=theme["block_color"])  # Change block background color
##                    if not block.opened:
##                        block.block.configure(bg=theme["block_color"])
def main():
    try:
        
        def change_theme():
            theme = THEMES[current_theme.get()]
            root.configure(bg=theme["frame_color"])  # Change root background color
            main_frame.configure(bg=theme["bg_color"])  # Change main_frame background color
            top_frame.config(bg=theme["frame_color"])
            left_frame.config(bg=theme["frame_color"])
            middle_frame.config(bg=theme["frame_color"])
            right_frame.config(bg=theme["frame_color"])
                   

            for block in Block.all:
                if block.block:
                    block.block.configure(bg=theme["block_color"])  # Change block background color
                    if not block.opened:
                        block.block.configure(bg=theme["block_color"])  # Change block background color when not opened
        
        

     
        global root, level_var, current_theme, help_button, timer, game_mode_var, current_level
        root = tk.Tk()
        current_theme = tk.StringVar(value="Default")  # Set default theme
        level_var = tk.StringVar(value='easy')  # Set default level

        
        
        root.state('zoomed')
        root.resizable(False, False)
        root.title('Minesweeper Game')

        top_frame = tk.Frame(root, bg="#3498db")
        top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        
        left_frame = tk.Frame(root, bg="#3498db")
        left_frame.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.9)

        middle_frame = tk.Frame(root, bg="#3498db")
        middle_frame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.9)

        right_frame = tk.Frame(root, bg="#3498db")
        right_frame.place(relx=0.8, rely=0.1, relwidth=0.2, relheight=0.9)

        game_title = tk.Label(top_frame, text='Minesweeper Game', font=('Arial', 24, 'bold'), bg="#1abc9c", fg="white")
        game_title.pack(expand=True)
        
        def create_circle_image(image_path, size=(50, 50)):
            img = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)  # Use the updated attribute
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            img.putalpha(mask)

            return ImageTk.PhotoImage(img)

        # Example usage
         # Set the correct path to the profile picture
        circular_profile_image = create_circle_image(profile_picture_path)
        profile_button = tk.Button(top_frame, text=username, image=circular_profile_image, compound='left', command=show_profile_frame)
        profile_button.image = circular_profile_image  # Keep a reference to avoid garbage collection
        profile_button.pack(side='right', padx=10)


        global main_frame
        theme = THEMES[current_theme.get()]
        main_frame = tk.Frame(middle_frame, bg=THEMES[current_theme.get()]["bg_color"])
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        def apply_level():
            stored_theme = current_theme.get()  # Store the current theme
            current_theme.set(stored_theme)  # Reapply the stored theme
                
            global var
            level = level_var.get()
            # Get the current level from StringVar
            var = levels[level]  # Access the level dictionary

            for widget in main_frame.winfo_children():
                widget.destroy()

            Block.all = []
            Block.particles = []
            Block.number_of_mines = levels[level]['m']
            Block.number_of_blocks = var['x'] * var['y']

            for x in range(var['x']):
                for y in range(var['y']):
                    block = Block(x, y, main_frame)
                    block.create_block(main_frame)
                    block.place_block()
            change_theme()  # Update the theme

        
        

        menu = tk.Menu(root, tearoff=False)
        submenu = tk.Menu(menu, tearoff=False)
        submenu2 = tk.Menu(menu, tearoff=False)
        for theme_name in THEMES:
            submenu.add_radiobutton(label=theme_name, variable=current_theme, value=theme_name, command=change_theme)
        menu.add_cascade(label="Theme", menu=submenu)
        menu.add_command(label="Exit", command=root.destroy)
        for level_name in levels:
            submenu2.add_radiobutton(label=level_name, variable=level_var, value=level_name, command=apply_level)
        menu.add_cascade(label="Levels", menu=submenu2)
        root.config(menu=menu)
        

        settings_button = tk.Button(left_frame, text='\u2699', font=('Arial', 14), bg="#9b59b6", fg="white", command=lambda: menu.post(settings_button.winfo_rootx(), settings_button.winfo_rooty() - menu.winfo_height()))
        settings_button.pack(side="bottom", pady=10)
        help_button = tk.Button(left_frame, text='Help', font=('Arial', 14), bg="#9b59b6", fg="white", command=use_help)
        help_button.pack(side="bottom", pady=10)

        global timer
        timer_label = tk.Label(right_frame, text="Time: 00:00:00", font=('Arial', 14), bg="#1abc9c", fg="white")
        timer_label.place(relx=0.5, rely=0.2, anchor='n')
        timer = Timer(timer_label)

##        global flags_count_label
##        flags_count_label = tk.Label(right_frame, text=f'Flags: {Block.number_of_flags}', font=('Arial', 14), bg=theme["frame_color"], fg="white")
##        flags_count_label.place(relx=0.5, rely=0.3, anchor='n')

        Block.number_of_mines_left = tk.Label(left_frame, text=f'Mines Left: {Block.number_of_mines}', font=('Arial', 14), bg="#1abc9c", fg="white")
        Block.number_of_mines_left.pack(pady=20)

        apply_level()  # Apply the default level

        def change_label_color():
            theme = THEMES[current_theme.get()]
            stored_theme = current_theme.get()  # Store the current theme
            current_theme.set(stored_theme)  # Reapply the stored theme
            timer_label.config(bg=theme["frame_color"])
        
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")




if __name__ == '__main__':
    main()
