from zipfile import ZipFile

import os

# unzip the file (since .osz files are file archives (zip files))
def unzip(name: str) -> None:

    with ZipFile(name, "r") as f:

        # new path name
        name = "beatmap"
        cwd = os.path.abspath(os.getcwd()) + "\\"
        
        # making new directory
        new_path = os.path.join(cwd, name)

        try:
            os.mkdir(new_path)
        except FileExistsError:
            print("Folder already exists, sorry.")
            raise FileExistsError

        # changing to the directory
        os.chdir(new_path)

        # unzipping
        f.extractall()


def main(name=None):
    if not name:
        # unzipping
        try:
            unzip("test.osz")
        except FileExistsError:
            return

        # getting list of files in current directory (only beatmap difficulties)
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".osu")]

        # printing them nicely
        print("Here are the difficulties found:")
        for i, f in enumerate(files):
            print(f"\t{i+1}: {f}")
        
        # Asking for input
        num = int(input("Select a difficulty: "))
        while num - 1 < 0 or num - len(files) > 0:
            print("Invalid response. ")
            num = int(input("Select a difficulty: "))
        
        print(f"You selected: {files[num - 1]}")
        print(read_file(files[num - 1]))
    else:
        print(read_file(name))


# making this so I don't have to constantly use main (assume main is only for generating the filename)
def read_file(name: str):

    info = []
    curr_section = []

    headers = {"[General]": 0, "[Editor]": 0, "[Metadata]": 0, "[Difficulty]": 0, 
               "[Events]": 0, "[TimingPoints]": 0, "[Colours]": 0, "[HitObjects]": 0}

    with open(name, "r") as file:
        for line in file:
            line = line.strip()
            if line in headers:
                info.append(curr_section)
                curr_section = []
            else:
                curr_section.append(line)

    info.append(curr_section)

    info.pop(0)

    return_dict = {}
    for i, item in enumerate(info):
        return_dict[list(headers.keys())[i].lstrip("[").rstrip("]")] = item
    
    return return_dict


if __name__ == "__main__":
    main("beatmap\\ONE OK ROCK - Start Again (A r M i N) [A r M i Nakis' Hard].osu")
