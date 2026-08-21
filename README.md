File-Organizer

A Python tool that automatically sorts files in a folder into subfolders based on their type (Images, Documents, Music, Videos, etc.), so you don't have to move them by hand.

What does it do exactly?

Imagine you have a Downloads folder full of mixed files: photos, PDFs, songs, videos... This program checks every file and moves it into the right subfolder automatically:

Before:
Downloads/
├── photo.jpg
├── invoice.pdf
├── song.mp3
└── video.mp4

After:
Downloads/
├── Images/
│   └── photo.jpg
├── Documents/
│   └── invoice.pdf
├── Music/
│   └── song.mp3
└── Videos/
    └── video.mp4
Key features
Automatic classification by file type (extension).
Fully customizable rules: decide which extension goes to which folder by editing a simple text file — no code changes needed.
Dry-run mode (--dry-run): shows you exactly what the program would do BEFORE moving anything for real. Great for testing safely the first time.
Overwrite protection: if a file with the same name already exists at the destination, the new one is automatically renamed instead of overwriting it.
Activity log: keeps a record of everything the program does, so you can review what was moved and when.
Requirements
Python installed (version 3.8 or higher). You can check this by running:
  python --version
Installation
Download or clone this project folder to your computer.
Open a terminal inside the project folder.
Install the only dependency needed:
   pip install -r requirements.txt

That's it — no additional setup required.

How to use it
Step 1: Try it safely first (recommended)

Before moving any files for real, you can simulate the result:

python main.py "C:\Users\YourUser\Downloads" --dry-run

(On Mac or Linux the path format is different, e.g. /Users/YourUser/Downloads)

This will show you something like this on screen, without moving anything at all:

2026-08-21 10:15:32 - INFO - === DRY-RUN MODE: no files will be moved ===
2026-08-21 10:15:32 - INFO - photo.jpg            → Images/photo.jpg
2026-08-21 10:15:32 - INFO - invoice.pdf          → Documents/invoice.pdf
2026-08-21 10:15:32 - INFO - song.mp3             → Music/song.mp3
Step 2: Organize for real

If the simulation result looks correct, run the same command without --dry-run:

python main.py "C:\Users\YourUser\Downloads"

This time the files will actually be moved into their corresponding folders.

Customizing what goes where

The first time you run the program, a file called rules.json is automatically created inside the config/ folder. Open it with any text editor (even Notepad) and edit it as you like:

json
{
    ".jpg": "Images",
    ".png": "Images",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".mp3": "Music",
    ".mp4": "Videos",
    ".zip": "Compressed"
}

Each line means "this extension goes to this folder". You can freely add, remove, or change lines. Any file type not listed here will be placed in a folder called Others, so nothing ever gets left unorganized.

Frequently asked questions

Can it lose or delete my files? No. The program never deletes files. At worst, a file ends up in a different folder than expected, and you can always move it back manually. On top of that, if it detects a file with the same name already at the destination, it won't overwrite it — it saves the new one under a different name instead (e.g. photo (1).jpg).

What happens if I run the program twice in a row? No problem. The second run will simply find no new files to move (they're already organized), or it will organize only the new files you've added since the last run.

Where can I see exactly what the program did? Inside the logs/ folder, a file called organizer.log is automatically generated with the full record of every run, including date and time.

Do I need to know how to code to use it? No. You just need to run the command shown in the terminal. To customize the rules, you only need to edit a simple text file.

Running the automated tests (for developers)

If you want to verify that all the code works correctly:

pytest
Project structure
File-Organizer/
│
├── file_organizer/          Main source code
│   ├── scanner.py            Finds the files in the target folder
│   ├── classifier.py         Decides the category of each file
│   ├── organizer.py          Moves (or simulates moving) each file
│   ├── config.py             Loads and validates the classification rules
│   └── logger.py             Logs the program's activity
│
├── config/
│   └── rules.json             Classification rules (editable)
│
├── logs/
│   └── organizer.log          Run history (generated automatically)
│
├── tests/                     Automated tests
│
├── main.py                     Program entry point
├── requirements.txt
└── README.md
Safety note

It's always recommended to run with --dry-run first before organizing an important folder, to confirm the result matches what you expect.

License

This project is licensed under the MIT License — see the LICENSE file for details.