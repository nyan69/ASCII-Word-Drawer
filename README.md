# ASCII Word Drawer

ASCII Word Drawer is a simple Python-based project used to explore what’s possible with ASCII art in Python. It generates colorful ASCII art words directly in your terminal using pyfiglet and colorama, serving as a fun experiment in terminal-based rendering and color customization. This repo is also a way to figure out how things are supposed to work here on GitHub.

## Features

- **Color Modes**
  1.  Single color for all letters
  2.  Random color per letter (no repeats until all colors are used)
  3.  Random color per word (no repeats until all colors are used)
- **Capacity Estimates**: Automatically calculates how many characters fit in your terminal based on font metrics.
- **Multi-line Support**: Paste or pipe text of any length.
- **ASCII Art**: Utilizes the `pyfiglet` library for stylized text.

## Prerequisites

- Python
- pip (typically included with Python 3; if missing, install via your OS package manager)
- pyfiglet library (`pip install pyfiglet`)
- colorama library (`pip install colorama`)
- A Unix-like terminal (macOS/Linux) or Windows Command Prompt / PowerShell

## Installation
 **Install dependencies**

```bash
pip install pyfiglet colorama
```

## Usage

Run the script and follow the prompts:

1. Select a color mode (0 to exit, 1–3 to choose color behavior).
2. (Mode 1 only) Enter a color name (red, green, yellow, blue, magenta, cyan, white).
3. Paste your text and finish with `Ctrl+D` (macOS/Linux) or `Ctrl+Z` (Windows).
4. View your colorful ASCII-art output.

## Edge Cases Handled
Empty input: The program exits gracefully with a warning if no text is entered.

Invalid mode selection: The user is repeatedly prompted until a valid mode (0, 1, 2, or 3) is entered.

Invalid color choice (mode 1): If an unrecognized color is entered, the program defaults to white and issues a warning.

Color cycling resets: For modes with random colors (per letter or per word), once all colors are used, the color list is reset and reshuffled to avoid repeats until all colors are exhausted.

Spaces in input: Spaces are handled explicitly by inserting a blank ASCII art block and managing color changes between words.

