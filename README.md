# replay-parser-testing

wip replay parser for osu!

![](https://cdn.discordapp.com/attachments/599688004654596108/1084671585614565386/ezgif.com-crop.gif)

### What does it do?

This replay parser allows you to get information about an osu! replay (.osr file) without actually needing osu!. This information includes:

- Player username
- Score information (score, max combo, 300s, etc.)
- Exact time it was set (in UTC)
- Exact cursor positions and keypresses (including smoke)

And more.

As of right now, this program is not very user-friendly, but I'll be working to change that soon.

The main functionality of this program right now is a real-time visualization of the user's cursor in a pygame window. Your mileage of this visualization may vary; the code is rendering frames to the screen up to every 60th of a second.

### Requirements

- Python (version 3.7+)
- pygame, datetime, time, lzma modules

### Usage

Clone the repository:

`git clone https://github.com/clarks03/replay-parser-testing.git`

Download a replay you would like to get details for. Copy it, then cd into the repo:

`cd replay-parser-testing`

Then copy the replay file into this directory.

Edit the file titled `replay_parser.py` in your text editor of choice. Then go to line 207:

```python
if __name__ == "__main__":

    filename = "test.osr"  # this line
    data = []
    with open(filename, "rb") as file:
        data = parse_data(file)
    
    gameplay_data = data[18]

    get_data(gameplay_data)
```

And replace the string `filename` with the name of your replay. Then run the file, and a window should pop up showing your replay cursor! The window will be black for a bit while the program calculates the frames, but it should begin playing after ~10 seconds (again, your mileage may vary.)

### Problems

This is a very WIP project that I worked on over a weekend for fun, so it's not perfect. Please be patient while I make it useable.
