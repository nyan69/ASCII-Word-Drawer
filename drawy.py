import sys
import string
import pyfiglet
import random
import shutil
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# === Setup ===
fig = pyfiglet.Figlet(font="standard")

# Available colors
color_options = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE
}
color_list = list(color_options.values())


def build_blocks_for(
    text: str,
    mode: str,
    fig: pyfiglet.Figlet,
    color_list: list,
    single_color: str | None
) -> list[tuple[str, list[str]]]:
    """
    Given a single line of `text`, build and return a list of
    (color_code, ascii_art_lines) tuples for each character/space.
    `single_color` is used in mode "1"; otherwise ignored.
    """
    # Precompute exact space block from font
    space_block = fig.renderText(" ").splitlines()

    letter_blocks: list[tuple[str, list[str]]] = []
    available_colors = color_list.copy()

    prev_space = True
    current_word_color = None

    for char in text:
        # handle spaces
        if char == " ":
            letter_blocks.append((Style.RESET_ALL, space_block))
            prev_space = True
            continue

        # pick color
        if mode == "1":
            # single color for all letters
            char_color = single_color or Fore.WHITE
        elif mode == "2":
            # random color per letter (no repeats until exhausted)
            if not available_colors:
                available_colors = color_list.copy()
                random.shuffle(available_colors)
            char_color = available_colors.pop()
        else:  # mode == "3"
            # one color per word (no repeats until exhausted)
            if prev_space:
                if not available_colors:
                    available_colors = color_list.copy()
                    random.shuffle(available_colors)
                current_word_color = available_colors.pop()
            char_color = current_word_color

        # render character
        art_lines = fig.renderText(char).splitlines()
        letter_blocks.append((char_color, art_lines))
        prev_space = False

    return letter_blocks


def render_blocks(letter_blocks: list[tuple[str, list[str]]]) -> None:
    """Print the list of (color, art_lines) blocks to the terminal."""
    max_height = max(len(lines) for _, lines in letter_blocks)
    for row in range(max_height):
        for color_code, lines in letter_blocks:
            segment = lines[row] if row < len(lines) else " " * len(lines[0])
            print(color_code + segment + Style.RESET_ALL, end='')
        print()


def main():
    # === MENU ===
    print("=== Word Drawer ===")
    print("0. Exit")
    print("1. One color for all letters")
    print("2. Random color per letter (no repeats until all used)")
    print("3. One color per word (no repeats until all used)")

    # Mode selection
    while True:
        mode = input("Choose mode (0, 1, 2 or 3): ").strip()
        if mode in ("0", "1", "2", "3"):
            break
        print("❌ Invalid input. Please enter 0, 1, 2, or 3.")

    if mode == "0":
        print("👋 Exiting. Goodbye!")
        sys.exit(0)

    # If mode 1, ask for the color name
    chosen_color: str | None = None
    if mode == "1":
        print(
            "Type the name of a color (red, green, yellow, blue, "
            "magenta, cyan, white). Leave blank or enter anything else to default to white."
        )
        choice = input("Color: ").strip().lower()
        if choice in color_options:
            chosen_color = color_options[choice]
        else:
            if choice:
                print(f'❌ "{choice}" not recognized. Defaulting to white.')
            chosen_color = Fore.WHITE

    # Terminal info & capacity estimates
    term_width = shutil.get_terminal_size().columns
    print(f"\n📏 Terminal width: {term_width} columns")

    max_char_width = max(len(line) for line in fig.renderText("W").splitlines())
    worst_case_cols = term_width // max_char_width
    print(f"📦 Estimated capacity (worst-case): {worst_case_cols} chars")

    total_pool_width = sum(
        max(len(line) for line in fig.renderText(ch).splitlines())
        for ch in string.ascii_letters + string.digits
    )
    avg_width = total_pool_width / len(string.ascii_letters + string.digits)
    typical_cols = int(term_width // avg_width)
    print(f"🧮 Estimated capacity (typical):    {typical_cols} chars\n")

    # === MULTI-LINE INPUT ===
    print("📋 Paste your text (finish with Ctrl+D on Linux/macOS or Ctrl+Z on Windows):")
    raw = sys.stdin.read()
    if not raw.strip():
        print("⚠️ No text entered; nothing to draw.")
        sys.exit(1)

    lines = raw.rstrip("\n").splitlines()
    print(f"✏️ Got {len(lines)} line(s). Rendering...\n")

    # Build & render each line
    for text in lines:
        blocks = build_blocks_for(
            text,
            mode,
            fig,
            color_list.copy(),
            single_color=chosen_color
        )
        render_blocks(blocks)
        print()  # blank line between ASCII-art lines

if __name__ == "__main__":
    main()
