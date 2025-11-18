# Windows Action Recorder & Player

A Python-based automation tool that records your mouse and keyboard actions and replays them at specified intervals.

## Features

- Record mouse movements, clicks, and scrolls
- Record keyboard key presses
- Save recordings to JSON files
- Replay recorded actions
- Repeat actions at specified intervals
- Easy-to-use command-line interface

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python main.py
```

### Options:

1. **Record**: Start recording your actions
   - Press `ESC` to stop recording
   - Actions are saved to `recording.json`

2. **Playback**: Replay recorded actions once

3. **Repeat**: Replay actions at intervals
   - Specify the interval in seconds
   - Press `Ctrl+C` to stop repetition

4. **Exit**: Close the program

## File Structure

- `main.py` - Main program with CLI interface
- `recorder.py` - Action recording functionality
- `player.py` - Action playback functionality
- `requirements.txt` - Python dependencies
- `recording.json` - Saved recording (created after first recording)

## Notes

- This tool is designed for Windows
- Run with appropriate permissions
- Be careful when recording sensitive information (passwords, etc.)
