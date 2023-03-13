import datetime
import lzma

import time

import pygame


class Replay:

    gamemode: str                               # byte
    game_version: int                           # int
    beatmap_md5: str                            # string
    username: str                               # string
    score_md5: str                              # string

    hit_judgments: dict[str, int]

    score: int                                  # int
    combo: int                                  # short
    is_fc: bool                                 # byte
    mods_used: list[str]                        # int
                     
    bar_graph: list[str]                        # string
    time_stamp: datetime                        # long
    data: list[tuple[int, float, float, int]]   # int length

    score_id: int                               # long

    def __init__(self, filename: str):
        try:
            with open(filename, "rb") as file:
                gm = self.read_byte(file)[0]
                self.gamemode = self.get_gamemode(gm)

                self.game_version = self.read_int(file)

                self.beatmap_md5 = self.read_string(file)

                self.username = self.read_string(file)

                self.score_md5 = self.read_string(file)

                self.hit_judgments = self.get_judgments(file)

                self.score = self.read_int(file)
                
                self.combo  = self.read_short(file)

                fc = self.read_byte(file)[0]
                self.is_fc = self.get_fc(fc)

                mod = self.read_int(file)
                self.mods_used = self.get_mods(mod)

                bar = self.read_string(file)
                self.bar_graph = self.get_bar(bar)

                ts = self.read_long(file)
                self.time_stamp = self.get_date(ts)

                length = self.read_int(file)
                d = file.read(length)
                self.data = self.get_data(d)

                self.score_id = self.read_long(file)

        except FileNotFoundError:
            raise FileNotFoundError("File not found.")
    
    def __str__(self):
        s = ""
        s += f"Gamemode: {self.gamemode}\n"
        s += f"Version: {self.game_version}\n"
        s += f"Beatmap MD5 hash: {self.beatmap_md5}\n"
        s += f"Username: {self.username}\n"
        s += f"Replay MD5 hash: {self.score_md5}\n"
        for key in self.hit_judgments:
            s += f"{key}: {self.hit_judgments[key]}\n"
        s += f"Score: {self.score}\n"
        s += f"Max combo: {self.combo}\n"
        s += f"FC? {self.is_fc}\n"
        s += f"Mods used: {', '.join(self.mods_used)}\n"
        s += f"Time: {str(self.time_stamp)}\n"
        s += f"Score ID: {self.score_id}"
        return s
    
    def read_byte(self, file) -> bytes:
        return file.read(1)
    
    def read_short(self, file) -> int:
        return int.from_bytes(file.read(2), "little")
    
    def read_int(self, file) -> int:
        return int.from_bytes(file.read(4), "little")
    
    def read_long(self, file) -> int:
        return int.from_bytes(file.read(8), "little")
    
    def read_uleb128(self, file) -> int:
        result, shift = 0, 0
        while True:
            byte = self.read_byte(file)[0]
            result |= ((byte & 0x7f) >> shift)
            if ((byte & 0x80) == 0):
                break
            shift += 7
        return result

    def read_string(self, file) -> str:
        byte = self.read_byte(file)[0]

        if byte == 0x00:
            return ""
        elif byte != 0x0b:
            return ""
    
        length = self.read_uleb128(file)

        return_str = b""
        for _ in range(length):
            return_str += self.read_byte(file)
        
        return return_str.decode()

    def get_gamemode(self, num: int) -> str:
        gamemodes = ["osu!Standard", "Taiko", "CTB", "osu!mania"]
        return gamemodes[num]

    def get_mods(self, num: int) -> list[str]:
        mods = [
            "NoFail", "Easy", "TouchDevice", "Hidden", "HardRock",
            "SuddenDeath", "DoubleTime", "Relax", "Halftime",
            "Nightcore", "Flashlight", "Autopilot", "Perfect",
            "Key4", "Key5", "Key6", "Key7", "Key8", "FadeIn",
            "Random" "Cinema", "TargetPractice", "Key9",
            "Coop", "Key1", "Key3", "Key2", "ScoreV2", "Mirror"
        ]

        if num == 0:
            return ["None"]

        your_mods = []

        for i in range(len(mods)):
            if ((num >> i) & 1) == 1:
                your_mods.append(mods[i])
        
        if "Nightcore" in your_mods:
            your_mods.remove("DoubleTime")
        
        if "Key4" in your_mods and "Key5" in your_mods \
            and "Key6" in your_mods and "Key7" in your_mods and "Key8" in your_mods:
            your_mods.remove("Key4")
            your_mods.remove("Key5")
            your_mods.remove("Key6")
            your_mods.remove("Key7")
            your_mods.remove("Key8")
            your_mods.append("KeyMod")
        
        return your_mods

    def get_fc(self, num: int) -> bool:
        return True if num == 1 else False

    def get_bar(self, s: str) -> list[str]:
        return s.split(",")

    def get_date(self, ticks: int) -> datetime:
        return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=ticks/10)

    def get_data(self, data: bytes) -> list[tuple[int, float, float, int]]:

        # decompressing data
        data = lzma.decompress(data, format=lzma.FORMAT_AUTO)
        data = data.decode("ascii")

        # parsing data
        data = data.rstrip(",")
        data = data.split(",")

        # return lst of events
        events = []

        for event in data:
            # splitting it based on "|" delim
            event = event.split("|")

            event_time = int(event[0])
            x = float(event[1])
            y = float(event[2])
            keys = int(event[3])

            events.append((event_time, x, y, keys))

        return events

    def get_judgments(self, reader) -> dict[str, int]:
        judgments = {}

        if self.gamemode == "osu!Standard":
            judgments["300s"] = self.read_short(reader)
            judgments["100s"] = self.read_short(reader)
            judgments["50s"] = self.read_short(reader)
            judgments["Gekis"] = self.read_short(reader)
            judgments["Katus"] = self.read_short(reader)
            judgments["Misses"] = self.read_short(reader)
        elif self.gamemode == "Taiko":
            judgments["300s"] = self.read_short(reader)
            judgments["150s"] = self.read_short(reader)
            self.read_short(reader)
            self.read_short(reader)
            self.read_short(reader)
            judgments["Misses"] = self.read_short(reader)
        elif self.gamemode == "CTB":
            judgments["300s"] = self.read_short(reader)
            judgments["100s"] = self.read_short(reader)
            judgments["small fruit"] = self.read_short(reader)
            self.read_short(reader)
            self.read_short(reader)
            judgments["Misses"] = self.read_short(reader)
        else:
            judgments["300s"] = self.read_short(reader)
            judgments["100s"] = self.read_short(reader)
            judgments["50s"] = self.read_short(reader)
            judgments["Max 300s"] = self.read_short(reader)
            judgments["200s"] = self.read_short(reader)
            judgments["Misses"] = self.read_short(reader)

        return judgments

            
    def draw_cursor(self) -> None:

        if self.gamemode != "osu!Standard":
            return
        
        # frames
        frames = []

        # trail
        circle_trail = []

        # initialize pygame
        screen = pygame.display.set_mode((512, 384))

        for event in self.data:
            x = event[1]
            y = event[2]
            keys = event[3]

            # draw the frame
            buffer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            buffer.fill((0, 0, 0))

            # adding to the trail (making it length 5)
            circle_trail.insert(0, (x, y))
            if len(circle_trail) > 5:
                circle_trail.pop()
            
            # drawing the circles
            opacity = 255
            for circle in circle_trail:
                col = (255, 255, 255, opacity)
                pygame.draw.circle(buffer, col, (circle[0], circle[1]), 5)
                opacity -= (255//5)

            # adding to the list of frames
            frames.append(buffer.copy())

        # drawing the frames now
        for i in range(len(frames)):
            # display the frame, time it
            start = time.time()
            screen.blit(frames[i], (0, 0))
            pygame.display.flip()
            end = time.time()

            delta = (end - start) * 0.001
            actual_time = int(self.data[i][0])

            if actual_time - delta >= 0:
                pygame.event.pump()  # add this to clear the event queue
                pygame.time.delay(actual_time)
            else:
                print("Delay.")
