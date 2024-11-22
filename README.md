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

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yt-dlp-gui.git
cd yt-dlp-gui
```

2. Install the required dependencies:
```bash
pip install -r requirements.lock
```

## Usage

1. Run the application:
```bash
python -m yt_dlp_gui.main
```

2. Enter a YouTube URL in the input field
3. (Optional) Change the download location using the folder button
4. Click the download button to start downloading
5. Monitor the progress through the progress bar

## Development

For development, install additional dependencies:

```bash
pip install -r requirements-dev.lock
```

## License

This project is licensed under the Unlicense - see the LICENSE file for details. This follows the same license as yt-dlp to ensure compatibility.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful downloader that powers this GUI
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - The GUI framework used
