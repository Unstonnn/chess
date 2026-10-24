# Chess

A two-player chess game built in Python with Pygame. Play on a graphical board, choose your promotion and clock settings, and review previous positions during a game.

## Features

- Local two-player chess with a graphical board.
- Optional game clock with configurable starting time and per-move increment.
- Automatic queen promotion or manual promotion to a queen, rook, bishop, or knight.
- In-game move history browsing.
- Sound effects for moves, captures, castling, promotion, check, and game end.
- Chess end conditions including checkmate, stalemate, repetition, the 50-move rule, and insufficient material.

## Requirements and platform support

- Python 3.9 or newer
- The packages listed in [requirements.txt](requirements.txt)

The interactive menu is Windows-specific. The board-only game can also be used on macOS and Linux. The chess game in `echec.py` depends on `guiEchec.py` for its graphical interface. Keep `guiEchec.py`, the `Images` and `audio` folders, and `led.ttf` alongside `echec.py`.

## Install and run

On Windows, open PowerShell in the project directory and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python echec.py
```

On macOS or Linux, create and activate a virtual environment, install the requirements, then run `echec.py`. For example:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 echec.py
```

## Game modes

`Game()` starts with the menu and options on Windows. If the menu imports are unavailable on another operating system, it starts directly at the board instead.

```python
game = Game()
```

Pass `True` to skip the menu and start directly at the board on any operating system:

```python
game = Game(True)
```

From the Windows menu, you can start a game, change options, or quit. The options include automatic or manual promotion and an optional clock with configurable starting time and increment.

## Controls

- **Mouse:** Select a piece and then its destination.
- **Q**, **R**, **B**, or **N:** Choose a promotion piece when automatic promotion is disabled.
- **Left / Right arrow:** Browse previous positions after pressing **Left** during a game.
- **Close the game window:** Return to the menu.
- **Escape:** Exit the application.

## Use from Python

Import `Game` from `echec.py` to use it in another Python file:

```python
from echec import Game
```

## Build Windows executables

The release executables can be built on Windows with PyInstaller. From the project directory, create and activate a Python 3.13 environment, then install the build dependencies:

```powershell
py -3.13 -m venv venv
.\venv\Scripts\activate
pip install pyinstaller pygame-ce inquirer==3.4.1 blessed readchar
```

The executable's game mode is determined by the `Game(...)` call in the `if __name__ == "__main__":` block of `echec.py` when you build it.

For the menu version, make sure that block calls `Game()`, then run:

```powershell
pyinstaller --clean --onefile --name "chess" --add-data "Images;Images" --add-data "audio;audio" --add-data "led.ttf;." --hidden-import inquirer --hidden-import ctypes --hidden-import blessed --hidden-import readchar --copy-metadata readchar --copy-metadata inquirer echec.py
```

For the board-only version, temporarily change the call to `Game(True)` and add `--noconsole`:

```powershell
pyinstaller --clean --noconsole --onefile --name "chessNoMenu" --add-data "Images;Images" --add-data "audio;audio" --add-data "led.ttf;." --hidden-import inquirer --hidden-import ctypes --hidden-import blessed --hidden-import readchar --copy-metadata readchar --copy-metadata inquirer echec.py
```

## Background and credits

I created the chess game in `echec.py` for a computer science class. The graphical interface in `guiEchec.py`, the piece images in `Images`, and the `led.ttf` font were provided as pre-made resources; I did not create them.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
