# yt-dlp-gui

A modern and user-friendly graphical interface for yt-dlp, designed to make downloading YouTube videos simple and intuitive.

## Features

- 🎯 Simple and intuitive user interface
- 📂 Customizable download location
- 📊 Real-time download progress with detailed information
  - Download speed
  - File size
  - Time remaining
  - Progress percentage
- 🎨 Modern design with improved readability
- ⚡ Fast downloads powered by yt-dlp

## Installation

### Option 1: Download Executable (Recommended)

1. Go to the [Releases](https://github.com/posky/yt-dlp-gui/releases) page
2. Download the latest `yt-dlp-gui.exe` file
3. Run the executable - no installation required!

### Option 2: From Source

#### Prerequisites

- Python 3.8 or higher
- [Rye](https://rye-up.com/) (Python package manager)

#### Steps

1. Clone the repository:
```bash
git clone https://github.com/posky/yt-dlp-gui.git
cd yt-dlp-gui
```

2. Install dependencies using Rye:
```bash
rye sync
```

## Usage

### Using the Executable
1. Run `yt-dlp-gui.exe`
2. Enter a YouTube URL in the input field
3. (Optional) Change the download location using the folder button
4. Click the download button to start downloading
5. Monitor the progress through the progress bar

### Running from Source
1. Activate the environment and run the application:
```bash
rye run python -m yt_dlp_gui.main
```

2. Follow the same steps as above for downloading videos

## Development

For development:

1. Clone the repository:
```bash
git clone https://github.com/posky/yt-dlp-gui.git
cd yt-dlp-gui
```

2. Set up the development environment:
```bash
rye sync
```

3. Make your changes and test them:
```bash
rye run python -m yt_dlp_gui.main
```

## License

This project is licensed under the Unlicense - see the LICENSE file for details. This follows the same license as yt-dlp to ensure compatibility.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful downloader that powers this GUI
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - The GUI framework used
