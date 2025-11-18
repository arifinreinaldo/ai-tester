"""
Windows Action Recorder & Player
Main program with CLI interface
"""

import os
import sys
from recorder import ActionRecorder
from player import ActionPlayer


def print_banner():
    """Print program banner"""
    print("\n" + "=" * 60)
    print("  Windows Action Recorder & Player")
    print("  Record and replay your mouse and keyboard actions")
    print("=" * 60 + "\n")


def print_menu():
    """Print main menu"""
    print("\nMain Menu:")
    print("1. Record new actions")
    print("2. Playback recording (once)")
    print("3. Repeat recording at intervals")
    print("4. View recording info")
    print("5. Exit")
    print("-" * 60)


def get_user_choice():
    """Get user menu choice"""
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def record_actions():
    """Record user actions"""
    print("\n" + "=" * 60)
    print("RECORDING MODE")
    print("=" * 60)
    print("\nInstructions:")
    print("- Click this window to give it focus")
    print("- Perform the actions you want to record")
    print("- Press ESC when you're done recording")
    print("- Your recording will be saved to 'recording.json'")

    input("\nPress ENTER to start recording...")

    recorder = ActionRecorder()
    recorder.start_recording()
    recorder.save_recording('recording.json')

    print("\n✓ Recording saved successfully!")


def playback_once():
    """Playback recording once"""
    if not os.path.exists('recording.json'):
        print("\n✗ Error: No recording found. Please record actions first.")
        return

    print("\n" + "=" * 60)
    print("PLAYBACK MODE")
    print("=" * 60)

    recorder = ActionRecorder()
    if not recorder.load_recording('recording.json'):
        return

    player = ActionPlayer()
    player.load_actions(recorder.actions)

    print("\nOptions:")
    print("1. Play at normal speed")
    print("2. Play at custom speed")

    choice = input("Enter choice (1-2): ").strip()

    if choice == '2':
        try:
            speed = float(input("Enter speed multiplier (e.g., 1.0=normal, 2.0=2x faster, 0.5=half speed): "))
        except ValueError:
            print("Invalid speed. Using normal speed.")
            speed = 1.0
    else:
        speed = 1.0

    player.play(speed_multiplier=speed)
    print("\n✓ Playback complete!")


def repeat_at_intervals():
    """Repeat recording at specified intervals"""
    if not os.path.exists('recording.json'):
        print("\n✗ Error: No recording found. Please record actions first.")
        return

    print("\n" + "=" * 60)
    print("REPEAT MODE")
    print("=" * 60)

    recorder = ActionRecorder()
    if not recorder.load_recording('recording.json'):
        return

    player = ActionPlayer()
    player.load_actions(recorder.actions)

    print("\nHow would you like to repeat the recording?")

    # Get interval
    while True:
        try:
            interval = float(input("Enter interval between repetitions (seconds): "))
            if interval > 0:
                break
            else:
                print("Interval must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get count
    print("\nRepeat options:")
    print("1. Repeat specific number of times")
    print("2. Repeat indefinitely (until Ctrl+C)")

    choice = input("Enter choice (1-2): ").strip()

    count = None
    if choice == '1':
        while True:
            try:
                count = int(input("Enter number of repetitions: "))
                if count > 0:
                    break
                else:
                    print("Count must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    print("\n" + "=" * 60)
    player.play_with_interval(interval_seconds=interval, count=count)
    print("\n✓ Repetition complete!")


def view_recording_info():
    """Display information about the current recording"""
    if not os.path.exists('recording.json'):
        print("\n✗ Error: No recording found. Please record actions first.")
        return

    print("\n" + "=" * 60)
    print("RECORDING INFORMATION")
    print("=" * 60)

    recorder = ActionRecorder()
    if not recorder.load_recording('recording.json'):
        return

    if not recorder.actions:
        print("\nNo actions in recording.")
        return

    # Calculate statistics
    total_actions = len(recorder.actions)
    duration = recorder.actions[-1]['timestamp'] if recorder.actions else 0

    action_types = {}
    for action in recorder.actions:
        action_type = action['type']
        action_types[action_type] = action_types.get(action_type, 0) + 1

    print(f"\nTotal actions: {total_actions}")
    print(f"Duration: {duration:.2f} seconds")
    print("\nAction breakdown:")
    for action_type, count in sorted(action_types.items()):
        print(f"  - {action_type}: {count}")


def main():
    """Main program loop"""
    print_banner()

    while True:
        print_menu()
        choice = get_user_choice()

        if choice == '1':
            record_actions()
        elif choice == '2':
            playback_once()
        elif choice == '3':
            repeat_at_intervals()
        elif choice == '4':
            view_recording_info()
        elif choice == '5':
            print("\nThank you for using Windows Action Recorder & Player!")
            print("Goodbye!\n")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!\n")
        sys.exit(0)
