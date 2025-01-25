This is an advanced Minesweeper game developed using Python and Tkinter. It includes multiple themes, difficulty levels, user profiles, and a database to track performance. The game supports efficient user management, customization, and competitive leaderboards, making it engaging and personalized.

Features

1. User Profiles

Users can create profiles by signing in through the Sign-In Screen.

Profiles include the username and a profile picture, which can be updated or displayed in the profile window.

User data such as:

Best Time

Efficiency

Number of Games Played

Number of Games Won
is tracked using an SQL database.

2. Multiple Difficulty Levels

The game supports three levels of difficulty:

Easy: Smaller board with fewer mines.

Medium: Medium-sized board with more mines.

Hard: Large board with the highest number of mines.

3. Themes

Users can switch between multiple themes, including:

Default

Lavender Haze

Sunflower

Aurora

Batman

Storm

Themes dynamically change the colors of the blocks, background, and hover effects.

4. Game Mechanics

Left-Click: Reveals the block. If it's a mine, the game is lost.

Right-Click: Flags the block as a potential mine.

Win Condition: Open all non-mine blocks.

Lose Condition: Click on a mine or run out of time.

5. Timer and Time Limit

A real-time timer tracks how long you take to complete a level.

In Time Trial mode, a time limit is enforced, adding an extra challenge.

6. Help System

A Help Button explains the rules and strategies for playing Minesweeper.

7. Leaderboard

Displays the top 5 players with the best times from the SQL database.

How It Works

1. Sign-In and Profiles

Users sign in using their username (stored in a local file).

Profiles include efficiency and best times retrieved from the SQL database.

A "Profile" button displays the user’s stats and top leaderboard players.

2. SQL Database Integration

The game uses a MySQL database (userdata) to store user information.

Tables:

data: Stores user IDs and usernames.

game_stats: Tracks games played, games won, and the best time for each user.

 
3. Gameplay

After signing in, select a difficulty level and start playing.By default the 
difficulty is set to medium.

Mines are placed randomly, ensuring the first click is never a mine.

Use logical deduction and flag blocks you suspect to contain mines.

4. Restart and Customization

You can restart the game while retaining the selected difficulty and theme.

The timer resets on every restart.

5. Efficiency Calculation

Efficiency is calculated using the ratio of games won to total games played.

How to Use

Prerequisites

Python 3.x installed on your system.

Required Python libraries:

tkinter

mysql-connector-python

Pillow

pickle

subprocess

A MySQL database set up with the required tables.

Setup Instructions

Clone or download the project files.

Install the required Python libraries:

pip install mysql-connector-python Pillow

Set up the MySQL database using the provided schema.

Run the game:

python minesweeper.py

Playing the Game

Sign in or create a new profile.

Choose a difficulty level.

Start playing by left-clicking to reveal blocks and right-clicking to flag mines.

Monitor your time and use the leaderboard to track progress.

File Structure
minesweeper.py:a basic game menu where u get to sign in
sign_in.py:Helps user sign into his exsisting profile
sign_up.py:Helps user create a profile
level-final.py: Main game logic and UI.
text.txt: Stores the currently signed-in username.
userdata (MySQL database): Stores user and game statistics.
w.dat: Temporary binary file to save and load gameplay stats using pickle.

leaderboard.csv: Local file for tracking scores.

Future Enhancements

Adding support for multiplayer gameplay.

Enhanced themes with animations and sound effects.

Online leaderboard integration to compete globally.

Enjoy the game! If you encounter any issues or have feature suggestions, feel free to contribute or provide feedback.

