# replay-parser-testing

wip replay parser for osu!

![](https://cdn.discordapp.com/attachments/599688004654596108/1084671585614565386/ezgif.com-crop.gif)

### What does it do?

This replay parser allows you to get information about an osu! replay (.osr file) without actually needing osu!. This information includes:

- Player username
- Score information (score, max combo, 300s, etc.)
- Exact time the score was set (in UTC)
- Exact cursor positions and keypresses (including smoke)

And more.

(EDIT 12am March 13th): Replay viewer now creates a `Replay` object, allowing you to access a replay's attributes easier. You can also print the replay object, telling you all the information about the play. 

Also, the cursor visualization is now a method (`draw_cursor()`),

~~As of right now, this program is not very user-friendly, but I'll be working to change that soon.~~

~~The main functionality of this program right now is a real-time visualization of the user's cursor in a pygame window. Your mileage of this visualization may vary; the code is rendering frames to the screen up to every 60th of a second.~~

### Requirements

- Python (version 3.7+)
- pygame, datetime, time, lzma modules

### Usage

Create a new `Replay` object with the following code:

```python
r = Replay("filename.osr")
```

You can print out the basics of the replay by printing the object:

```python
print(r)
```

And you can draw the cursor visualization with the following command:

```python
r.draw_cursor()
```

### TODO

Unfortunately, the functionality of this replay parser isn't the most useful yet. Eventually, I want to be able to:

- Get map data via. the Beatmap MD5 hash
- Visualize hitcircles underneath the cursor
- Optimize the cursor drawing, so that it plays a video rather than rendering the replay in real-time

But for the time being, I think it's okay. I hope you get some use out of it :3 