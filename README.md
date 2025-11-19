# Windows Action Recorder & Player Pro v2.2

A comprehensive Python-based automation tool that records your mouse and keyboard actions and replays them with advanced features including workflows, hotkeys, scheduling, image recognition, macro editing, and visual previews.

## 🌟 Features

### Core Features
- **📹 Action Recording**: Captures mouse movements, clicks, scrolls, and keyboard inputs
- **▶ Playback**: Replays recorded actions with adjustable speed
- **💾 Multiple Slots**: Save and manage multiple recordings
- **🎯 Optimized Recording**: Automatically reduces excessive mouse movements

### Advanced Features
- **🔗 Workflow Builder**: Chain multiple recordings into complex automation flows (NEW!)
- **✏ Macro Editor**: Edit recordings without re-recording
- **👁 Recording Preview**: Visualize actions before execution
- **⌨ Global Hotkeys**: Control recording/playback with F9/F10/F11
- **🔁 Interval Repetition**: Repeat actions at specified intervals
- **🎲 Random Delays**: Add human-like delays between actions
- **📅 Scheduling**: Run recordings at specific times
- **🖼 Image Recognition**: Find and click on images on screen
- **🔄 Conditional Logic**: Smart automation with if/then/else logic
- **🖥 GUI Interface**: Full-featured graphical interface
- **📊 Recording Management**: Import, export, rename, and organize recordings

## 📦 Installation

### Prerequisites
- Windows 7 or later
- Python 3.7+

### Setup Steps

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd ai-tester
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Start - GUI Mode
```bash
python gui.py
```
The GUI provides an intuitive interface for all features.

### Quick Start - CLI Mode
```bash
python main_enhanced.py
```
Navigate through menus for full control via command line.

### Basic CLI (Simple)
```bash
python main.py
```
Original simple interface for basic recording/playback.

## 📖 Detailed Usage Guide

### 1. Recording Actions

**GUI**: Click "Start Recording" button or press F9
**CLI**: Select option 1 from main menu

1. Choose a slot name for your recording
2. Press Enter/Click to start
3. Perform your actions
4. Press ESC to stop recording
5. Recording is automatically saved

### 2. Playing Recordings

**GUI**: Select recording and click "Play Once" or press F10
**CLI**: Select option 2 from main menu

Options:
- Normal speed (1.0x)
- Fast playback (2.0x)
- Slow playback (0.5x)
- Custom speed
- With random delays for human-like behavior

### 3. Repeating at Intervals

**GUI**: Click "Repeat at Intervals" button
**CLI**: Select option 3 from main menu

1. Enter interval in seconds (e.g., 30)
2. Choose repeat count or infinite
3. Press Ctrl+C to stop anytime

### 4. Using Hotkeys

**GUI**: Enable in Settings tab
**CLI**: Select option 5 from main menu

Default hotkeys:
- **F9**: Start/Stop Recording
- **F10**: Play Recording
- **F11**: Stop Playback

### 5. Scheduling

**GUI**: Use Scheduler tab
**CLI**: Select option 6 from main menu

Schedule types:
- Run every N minutes
- Daily at specific time (e.g., 9:00 AM)
- Hourly at specific minute (e.g., :30)
- Specific weekdays

Example: Run recording every 30 minutes
```python
# Via CLI menu
Job ID: auto-save
Slot: my-recording
Type: Interval
Value: 30
```

### 6. Image Recognition

**GUI**: Use Image Recognition tools in Settings
**CLI**: Select option 7 from main menu

Capabilities:
- Find image on screen
- Click on image when found
- Wait for image to appear
- Capture screenshots
- Get pixel colors
- Save screen regions as templates

Example workflow:
1. Capture screenshot of button → `button.png`
2. Use "Click on image" feature
3. Bot will find and click the button

### 7. Macro Editor (NEW!)

**GUI**: Macro Editor tab
**CLI**: Select option 8 from main menu

Edit recordings without re-recording:

**Editing Operations:**
- **Delete Actions**: Remove specific actions by index
- **Delete Range**: Remove multiple actions at once
- **Insert Delays**: Add pauses between actions
- **Remove Mouse Moves**: Strip all mouse movements
- **Simplify**: Remove duplicate/redundant actions
- **Scale Speed**: Speed up or slow down entire recording
- **Undo/Redo**: Undo mistakes while editing
- **Statistics**: View action breakdown

**Use Cases:**
- Fix mistakes in recording without re-doing everything
- Remove unwanted mouse movements
- Add strategic delays
- Optimize recording size
- Combine multiple recordings

**Example Workflow:**
```
1. Record your actions (accidentally move mouse around)
2. Open Macro Editor → Load recording
3. Remove all mouse movements
4. Insert 2s delay after action #10
5. Delete actions 50-60 (typo correction)
6. Save changes
```

### 8. Recording Preview (NEW!)

**GUI**: Preview tab
**CLI**: Select option 9 from main menu

Visualize recordings before execution:

**Preview Options:**
- **Summary**: Total actions, duration, action breakdown
- **Timeline**: Visual bar chart of activity over time
- **Detailed View**: Action-by-action breakdown with timestamps
- **Mouse Path**: See where mouse moved and clicked
- **Keyboard Sequence**: View all keystrokes in order
- **Action Frequency**: How often each action type occurs
- **Delays Analysis**: Find long pauses in recording
- **Click Hotspots**: See where you clicked most

**Benefits:**
- Review what will happen before running
- Identify mistakes before automation runs
- Understand recording structure
- Find optimization opportunities
- Debug problematic recordings

**Example Preview Output:**
```
RECORDING SUMMARY
====================================
Total Actions:  247
Duration:       45.3 seconds
Avg Speed:      5.4 actions/second

Action Breakdown:
  mouse_move          180 (72.9%)
  mouse_click          45 (18.2%)
  key_press            15 ( 6.1%)
  key_release          15 ( 6.1%)
```

### 9. Multiple Recording Slots

**GUI**: Recordings tab shows all slots
**CLI**: Select option 4 from main menu

Features:
- Create unlimited recording slots
- List all recordings with details
- Rename recordings
- Delete recordings
- Import/Export recordings
- View recording statistics

## 🎯 Use Cases

### Gaming Automation
- Farm resources automatically
- Auto-click at intervals
- Complete repetitive quests

### Office Automation
- Auto-fill forms
- Repetitive data entry
- Regular file backups
- Scheduled report generation

### Web Automation
- Monitor websites for changes
- Auto-refresh pages
- Fill forms repeatedly
- Click buttons at intervals

### Testing
- Automated UI testing
- Regression testing
- Load testing

## 📁 File Structure

```
ai-tester/
├── main.py                    # Simple CLI interface
├── main_enhanced.py           # Advanced CLI interface with all features
├── gui.py                     # Full-featured GUI interface
├── recorder.py                # Recording functionality
├── player.py                  # Playback functionality
├── recording_manager.py       # Multiple slots management
├── macro_editor.py            # Edit recordings (NEW!)
├── recording_preview.py       # Visualize recordings (NEW!)
├── hotkey_manager.py          # Global hotkeys
├── scheduler.py               # Task scheduling
├── image_recognition.py       # Image-based automation
├── conditional_logic.py       # Smart automation logic
├── requirements.txt           # Python dependencies
├── recordings/                # Saved recordings (auto-created)
└── README.md                  # This file
```

## ⚙ Configuration

### Random Delays
Add human-like behavior to avoid detection:
```python
# Enable in player
player.enable_random_delays(min_delay=0.1, max_delay=0.5)
```

### Image Recognition Confidence
Adjust matching threshold (0.0 to 1.0):
```python
image_rec.set_confidence(0.8)  # 80% confidence
```

### Playback Speed
Adjust playback speed:
- 0.5 = Half speed (slower)
- 1.0 = Normal speed
- 2.0 = Double speed (faster)

## 🔧 Advanced Features

### Conditional Logic

Create smart automation that responds to screen conditions:

```python
from conditional_logic import SmartPlayer, ImageExistsCondition
from player import ActionPlayer
from image_recognition import ImageRecognition

player = ActionPlayer()
image_rec = ImageRecognition()
smart_player = SmartPlayer(player, image_rec)

# Wait for button, then click
smart_player.wait_for_image_then_click('button.png', timeout=30)

# Conditional clicking
smart_player.conditional_click(
    if_image='condition.png',
    then_click_image='button_a.png',
    else_click_image='button_b.png'
)

# Loop until target appears
smart_player.loop_until_image_appears(
    check_image='target.png',
    actions=my_actions,
    max_iterations=100
)
```

### Programmatic Usage

```python
from recorder import ActionRecorder
from player import ActionPlayer
from recording_manager import RecordingManager

# Setup
recorder = ActionRecorder()
player = ActionPlayer()
manager = RecordingManager()

# Record
recorder.start_recording()  # Press ESC to stop
manager.save_recording('my-task', recorder.actions)

# Play
actions = manager.load_recording('my-task')
player.load_actions(actions)
player.enable_random_delays(0.1, 0.3)
player.play(speed_multiplier=1.5)  # 1.5x speed

# Repeat
player.play_with_interval(interval_seconds=60, count=10)
```

## 🐛 Troubleshooting

### pip not recognized
```bash
python -m pip install -r requirements.txt
```

### Permission errors
Run Command Prompt as Administrator

### Hotkeys not working
- Check if another app is using the same hotkeys
- Try disabling and re-enabling hotkeys
- Restart the application

### Image recognition not finding images
- Increase screenshot/template size
- Lower confidence threshold
- Ensure image appears exactly as in template
- Check screen resolution matches

### Recording not capturing actions
- Run as Administrator
- Check antivirus isn't blocking
- Ensure pynput is properly installed

## 📝 Tips & Best Practices

1. **Test First**: Always test recordings in a safe environment
2. **Use Descriptive Names**: Name slots clearly (e.g., "email-automation" not "rec1")
3. **Start Simple**: Begin with simple recordings before complex automation
4. **Failsafe**: Keep mouse in corner to emergency stop (PyAutoGUI failsafe)
5. **Random Delays**: Use random delays to avoid bot detection
6. **Backup Important Recordings**: Export important recordings to safe location
7. **Screen Resolution**: Record and play on same resolution for accuracy
8. **Image Templates**: Capture larger templates for better recognition

## 🔒 Security Notes

- **Never record passwords** or sensitive information
- Review recordings before scheduling
- Be careful with automated clicks (e.g., delete buttons)
- Test in safe environment first
- Keep recordings private (may contain personal info)

## 📄 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions welcome! Feel free to submit issues and pull requests.

## 🆘 Support

For issues and questions:
1. Check troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Check Python version compatibility

## 🔮 Future Features

Potential additions:
- OCR text recognition
- Mouse gesture recognition
- Cloud sync for recordings
- Mobile device control
- Macro scripting language
- Recording editor
- Performance analytics

## ⚡ Quick Reference

### CLI Commands
```
python gui.py              # Launch GUI
python main_enhanced.py    # Launch enhanced CLI
python main.py             # Launch simple CLI
```

### Default Hotkeys
```
F9  - Start/Stop Recording
F10 - Play Recording
F11 - Stop Playback
ESC - Stop Recording (while recording)
```

### File Locations
```
recordings/        # Your saved recordings
schedule_config.json  # Scheduled jobs
```

---

**Windows Action Recorder & Player Pro v2.1** - Powerful automation made simple! 🚀
✨ **New in v2.1**: Macro Editor & Recording Preview!
