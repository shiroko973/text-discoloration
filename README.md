# text_discoloration

Colorful terminal output with typewriter effect. Zero dependencies.

## Features

###  Color Output
- 8 colors: Red, Green, Yellow, Blue, Purple, Cyan, White, Black
- Direct color printing: `color_print_red("Hello")`
- Color typewriter effect: `typewriter_blue("Hello", delay=0.05)`

###  Typewriter Effects
- Standard typewriter: `typewriter("text", delay=0.05)`
- Random color typewriter: `random_typewriter("rainbow text")`
- Custom color typewriter: `color_typewriter("text", "green")`

###  Status Prompts
- `info("Loading...")` → Blue [INFO]
- `success("Done!")` → Green [SUCCESS]
- `error("Failed")` → Red [ERROR]
- `warn("Check this")` → Yellow [WARNING]

###  Utilities
- `slow_print("slow text", delay=0.05)` - Print character by character
- `color_print_red("text")` - Print without typewriter effect

## Installation

```bash
pip install text_discoloration