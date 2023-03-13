import datetime
import lzma

import time

import pygame


def read_byte(file):
    return file.read(1)

def read_short(file):
    val = file.read(2)
    return int.from_bytes(val, "little")

def read_int(file):
    val = file.read(4)
    return int.from_bytes(val, "little")

def read_long(file):
    val = file.read(8)
    return int.from_bytes(val, "little")


def read_uleb128(file):
    result, shift = 0,0
    while True:
        byte = read_byte(file)[0]    # 01111111
        result |= ((byte & 0b01111111) >> shift)
        if ((byte & 0b10000000) == 0):
            break
        shift += 7
    return result

def read_string(file):
    first_byte = read_byte(file)[0]

    if first_byte == 0x00:
        return ""
    elif first_byte != 0x0b:
        return ""  # this really shouldn't ever happen; if it does, something went wrong

    length = read_uleb128(file)

    return_str = b''
    for _ in range(length):    
        return_str += read_byte(file)
    
    return return_str.decode()


def get_mods(num):
    mods = ["Mirror", "ScoreV2", "Key2", "Key3", "Key1", "Coop", "Key9",
            "TargetPractice", "Cinema", "Random", "FadeIn",
            "Key8", "Key7", "Key6", "Key5", "Key4", "Perfect", "Autopilot",
            "Flashlight", "Nightcore", "Halftime", "Relax", "DoubleTime",
            "SuddenDeath", "HardRock", "Hidden", "TouchDevice", "Easy",
            "NoFail"]

    mods = mods[::-1]
    
    if num == 0:
        return ["None"]
    
    your_mods = []
    for i in range(30, -1, -1):
        if (num >> i) & 1 == 1:
            your_mods.append(mods[i])
    
    if "Nightcore" in your_mods:
        your_mods.remove("DoubleTime")
    
    if "Key4" in your_mods and "Key5" in your_mods and "Key6" in your_mods and "Key7" in your_mods and "Key8" in your_mods:
        your_mods.remove("Key4")
        your_mods.remove("Key5")
        your_mods.remove("Key6")
        your_mods.remove("Key7")
        your_mods.remove("Key8")
        your_mods.append("KeyMod")
    
    return your_mods


def get_gamemode(num):
    modes = ["osu!Standard", "Taiko", "CTB", "osu!mania"]
    return modes[num]

def get_date(ticks):
    return str(datetime.datetime(1, 1, 1) \
        + datetime.timedelta(microseconds=ticks/10))
    

def get_data(data):
    data = lzma.decompress(data, format=lzma.FORMAT_AUTO)
    data = data.decode("ascii")
    
    data = data.rstrip(",")
    data = data.split(",")

    count = 0
    events = []


    # Initialize Pygame

    # Set up the display
    screen = pygame.display.set_mode((512, 384))


    # draw all frames and store them in an array
    frames = []
    circle_trail = []  # list of (x, y) tuples

    for event in data:
        event = event.split("|")

        event_time = event[0]
        x = event[1]
        y = event[2]
        keys = event[3]

        # draw the frame
        buffer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        buffer.fill((0, 0, 0))

        # if (int(keys) & 0b0111) > 0:
        #     col = [255, 0, 0]
        # else:
        #     col = [255, 255, 255]
        col = [255, 255, 255]

        circle_trail.insert(0, (int(float(x) // 1), int(float(y) // 1)))
        if len(circle_trail) > 5:
            circle_trail.pop()
        
        opacity = 255  # subtract by (255/10) each time
        for circle in circle_trail:
            col = [255, 255, 255]
            col.append(opacity)
            col = tuple(col)
            pygame.draw.circle(buffer, col, (circle[0], circle[1]), 5)
            opacity -= (255//5)


        # pygame.draw.circle(buffer, col, (int(float(x) // 1), int(float(y) // 1)), 5)
        frames.append(buffer.copy())
        events.append([event_time, x, y, keys])
    

    for i in range(len(frames)):
        # display the frame, time it
        start = time.time()
        screen.blit(frames[i], (0, 0))
        pygame.display.flip()
        end = time.time()

        delta = (end - start) * 0.001
        actual_time = int(events[i][0])

        if actual_time - delta >= 0:
            pygame.event.pump()  # add this to clear the event queue
            pygame.time.delay(actual_time)
        else:
            print("Delay.")

    return events


def parse_data(file):
    gamemode = get_gamemode(read_byte(file)[0])
    game_version = read_int(file)
    beatmap_md5 = read_string(file)
    username = read_string(file)
    score_md5 = read_string(file)

    # assume that all scores are osu! standard
    hit_300 = read_short(file)
    hit_100 = read_short(file)
    hit_50 = read_short(file)
    hit_geki = read_short(file)
    hit_katu = read_short(file)
    hit_miss = read_short(file)

    score = read_int(file)
    combo = read_short(file)
    is_fc = True if read_byte(file)[0] == 1 else False
    mods_used = get_mods(read_int(file))
    bar_graph = read_string(file)  # might not always contain things, from experience.
    time_stamp = get_date(read_long(file))
    data_length = read_int(file)

    # replay data is tricky. it's not a certain amount of bytes, like int, long, or short
    # the number of bytes is given by data_length
    # so we can do this
    data = file.read(data_length)

    score_id = read_long(file)
    
    return [gamemode, game_version, beatmap_md5, username, score_md5,
            hit_300, hit_100, hit_50, hit_geki, hit_katu, hit_miss,
            score, combo, is_fc, mods_used, bar_graph, time_stamp,
            data_length, data, score_id]


if __name__ == "__main__":

    filename = "test.osr"
    data = []
    with open(filename, "rb") as file:
        data = parse_data(file)
    
    gameplay_data = data[18]

    get_data(gameplay_data)

