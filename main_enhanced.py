"""
Windows Action Recorder & Player Pro
Enhanced CLI with all advanced features
"""

import os
import sys
from recorder import ActionRecorder
from player import ActionPlayer
from recording_manager import RecordingManager
from hotkey_manager import HotkeyRecorderController
from scheduler import AutomationScheduler, ScheduleBuilder
from image_recognition import ImageRecognition


def print_banner():
    """Print program banner"""
    print("\n" + "=" * 70)
    print("  Windows Action Recorder & Player Pro v2.0")
    print("  Advanced automation with hotkeys, scheduling & image recognition")
    print("=" * 70 + "\n")


def print_main_menu():
    """Print main menu"""
    print("\n" + "=" * 70)
    print("MAIN MENU")
    print("=" * 70)
    print("1.  📹 Record Actions (Basic)")
    print("2.  ▶  Play Recording (Once)")
    print("3.  🔁 Repeat Recording (Intervals)")
    print("4.  💾 Manage Recordings (Multiple Slots)")
    print("5.  ⌨  Hotkey Mode (F9/F10/F11)")
    print("6.  📅 Scheduler (Run at specific times)")
    print("7.  🖼  Image Recognition Tools")
    print("8.  ⚙  Settings & Options")
    print("9.  ℹ  View Recording Info")
    print("10. 🖥  Launch GUI")
    print("0.  🚪 Exit")
    print("=" * 70)


def get_user_choice(max_choice=10):
    """Get user menu choice"""
    while True:
        try:
            choice = input(f"\nEnter your choice (0-{max_choice}): ").strip()
            if choice.isdigit() and 0 <= int(choice) <= max_choice:
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 0 and {max_choice}.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def record_actions(recording_manager):
    """Record user actions to a slot"""
    print("\n" + "=" * 70)
    print("RECORDING MODE")
    print("=" * 70)

    slot_name = input("Enter slot name (or press Enter for 'default'): ").strip()
    if not slot_name:
        slot_name = "default"

    print(f"\nRecording to slot: '{slot_name}'")
    print("\nInstructions:")
    print("- Perform the actions you want to record")
    print("- Press ESC when you're done recording")

    input("\nPress ENTER to start recording...")

    recorder = ActionRecorder()
    recorder.start_recording()
    recording_manager.save_recording(slot_name, recorder.actions)

    print(f"\n✓ Recording saved to slot '{slot_name}'!")


def playback_once(recording_manager, player):
    """Playback recording once"""
    slot_name = input("Enter slot name to play (or press Enter for 'default'): ").strip()
    if not slot_name:
        slot_name = "default"

    actions = recording_manager.load_recording(slot_name)
    if not actions:
        return

    print("\nPlayback Options:")
    print("1. Normal speed (1.0x)")
    print("2. Fast (2.0x)")
    print("3. Slow (0.5x)")
    print("4. Custom speed")
    print("5. With random delays (human-like)")

    choice = input("Enter choice (1-5): ").strip()

    speed = 1.0
    if choice == '2':
        speed = 2.0
    elif choice == '3':
        speed = 0.5
    elif choice == '4':
        try:
            speed = float(input("Enter speed multiplier: "))
        except ValueError:
            speed = 1.0

    if choice == '5':
        player.enable_random_delays(0.1, 0.5)
    else:
        player.disable_random_delays()

    player.load_actions(actions)
    player.play(speed_multiplier=speed)
    print("\n✓ Playback complete!")


def repeat_at_intervals(recording_manager, player):
    """Repeat recording at specified intervals"""
    slot_name = input("Enter slot name to repeat (or press Enter for 'default'): ").strip()
    if not slot_name:
        slot_name = "default"

    actions = recording_manager.load_recording(slot_name)
    if not actions:
        return

    while True:
        try:
            interval = float(input("Enter interval between repetitions (seconds): "))
            if interval > 0:
                break
            else:
                print("Interval must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a number.")

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

    # Ask about random delays
    use_random = input("Use random delays? (y/n): ").strip().lower() == 'y'
    if use_random:
        player.enable_random_delays(0.1, 0.5)

    player.load_actions(actions)
    print("\n" + "=" * 70)
    player.play_with_interval(interval_seconds=interval, count=count)
    print("\n✓ Repetition complete!")


def manage_recordings(recording_manager):
    """Manage multiple recording slots"""
    while True:
        print("\n" + "=" * 70)
        print("RECORDING MANAGEMENT")
        print("=" * 70)
        print("1. List all recordings")
        print("2. Delete recording")
        print("3. Rename recording")
        print("4. Export recording")
        print("5. Import recording")
        print("0. Back to main menu")
        print("=" * 70)

        choice = get_user_choice(5)

        if choice == '0':
            break
        elif choice == '1':
            list_recordings(recording_manager)
        elif choice == '2':
            delete_recording(recording_manager)
        elif choice == '3':
            rename_recording(recording_manager)
        elif choice == '4':
            export_recording(recording_manager)
        elif choice == '5':
            import_recording(recording_manager)


def list_recordings(recording_manager):
    """List all recordings"""
    recordings = recording_manager.list_recordings()

    if not recordings:
        print("\nNo recordings found.")
        return

    print("\n" + "=" * 70)
    print("SAVED RECORDINGS")
    print("=" * 70)
    print(f"{'Slot Name':<20} {'Actions':<10} {'Duration':<12} {'Modified'}")
    print("-" * 70)

    for rec in recordings:
        print(f"{rec['slot_name']:<20} {rec['action_count']:<10} {rec['duration']:.1f}s{'':<8} {rec['modified'].strftime('%Y-%m-%d %H:%M')}")


def delete_recording(recording_manager):
    """Delete a recording"""
    slot_name = input("Enter slot name to delete: ").strip()
    if slot_name:
        confirm = input(f"Are you sure you want to delete '{slot_name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            recording_manager.delete_recording(slot_name)


def rename_recording(recording_manager):
    """Rename a recording"""
    old_name = input("Enter current slot name: ").strip()
    new_name = input("Enter new slot name: ").strip()
    if old_name and new_name:
        recording_manager.rename_recording(old_name, new_name)


def export_recording(recording_manager):
    """Export a recording"""
    slot_name = input("Enter slot name to export: ").strip()
    export_path = input("Enter export file path: ").strip()
    if slot_name and export_path:
        recording_manager.export_recording(slot_name, export_path)


def import_recording(recording_manager):
    """Import a recording"""
    import_path = input("Enter file path to import: ").strip()
    slot_name = input("Enter slot name for imported recording: ").strip()
    if import_path and slot_name:
        recording_manager.import_recording(import_path, slot_name)


def hotkey_mode(recorder, player, recording_manager):
    """Run with hotkey support"""
    print("\n" + "=" * 70)
    print("HOTKEY MODE")
    print("=" * 70)
    print("\nSetting up global hotkeys...")

    controller = HotkeyRecorderController(recorder, player, recording_manager)

    slot_name = input("Enter slot name to use (or press Enter for 'default'): ").strip()
    if slot_name:
        controller.set_current_slot(slot_name)

    controller.setup_default_hotkeys()

    print("\nHotkey mode active!")
    print("Press Ctrl+C to exit hotkey mode.\n")

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nExiting hotkey mode...")
        controller.cleanup()


def scheduler_menu(player, recording_manager):
    """Scheduler menu"""
    scheduler = AutomationScheduler(player, recording_manager)
    scheduler.load_schedule()

    while True:
        print("\n" + "=" * 70)
        print("SCHEDULER")
        print("=" * 70)
        print("1. Start scheduler")
        print("2. Stop scheduler")
        print("3. Add scheduled job")
        print("4. List scheduled jobs")
        print("5. Remove scheduled job")
        print("6. Enable/Disable job")
        print("0. Back to main menu")
        print("=" * 70)

        choice = get_user_choice(6)

        if choice == '0':
            scheduler.stop()
            break
        elif choice == '1':
            scheduler.start()
            print("Scheduler started! (Running in background)")
        elif choice == '2':
            scheduler.stop()
        elif choice == '3':
            add_scheduled_job(scheduler)
        elif choice == '4':
            list_scheduled_jobs(scheduler)
        elif choice == '5':
            remove_scheduled_job(scheduler)
        elif choice == '6':
            toggle_job(scheduler)


def add_scheduled_job(scheduler):
    """Add a scheduled job"""
    job_id = input("Enter job ID: ").strip()
    slot_name = input("Enter recording slot name: ").strip()

    print("\nSchedule Type:")
    print("1. Every N minutes")
    print("2. Daily at specific time")
    print("3. Hourly at specific minute")

    choice = input("Enter choice (1-3): ").strip()

    if choice == '1':
        minutes = input("Enter interval in minutes: ").strip()
        schedule_type, schedule_value = ScheduleBuilder.every_n_minutes(int(minutes))
    elif choice == '2':
        time_str = input("Enter time (HH:MM): ").strip()
        schedule_type, schedule_value = ScheduleBuilder.daily_at(time_str)
    elif choice == '3':
        minute = input("Enter minute (0-59): ").strip()
        schedule_type, schedule_value = ScheduleBuilder.hourly_at(int(minute))
    else:
        print("Invalid choice")
        return

    scheduler.add_job(job_id, slot_name, schedule_type, schedule_value)


def list_scheduled_jobs(scheduler):
    """List all scheduled jobs"""
    jobs = scheduler.list_jobs()

    if not jobs:
        print("\nNo scheduled jobs.")
        return

    print("\n" + "=" * 70)
    print("SCHEDULED JOBS")
    print("=" * 70)

    for job in jobs:
        status = "✓ Enabled" if job['enabled'] else "✗ Disabled"
        print(f"\nJob ID: {job['id']}")
        print(f"  Slot: {job['slot_name']}")
        print(f"  Schedule: {job['schedule_type']} - {job['schedule_value']}")
        print(f"  Status: {status}")
        print(f"  Run Count: {job['run_count']}")
        if job['last_run']:
            print(f"  Last Run: {job['last_run']}")


def remove_scheduled_job(scheduler):
    """Remove a scheduled job"""
    job_id = input("Enter job ID to remove: ").strip()
    if job_id:
        scheduler.remove_job(job_id)


def toggle_job(scheduler):
    """Enable or disable a job"""
    job_id = input("Enter job ID: ").strip()
    action = input("Enable or disable? (e/d): ").strip().lower()

    if action == 'e':
        scheduler.enable_job(job_id)
    elif action == 'd':
        scheduler.disable_job(job_id)


def image_recognition_menu():
    """Image recognition tools"""
    image_rec = ImageRecognition()

    while True:
        print("\n" + "=" * 70)
        print("IMAGE RECOGNITION TOOLS")
        print("=" * 70)
        print("1. Capture screenshot")
        print("2. Find image on screen")
        print("3. Click on image")
        print("4. Wait for image to appear")
        print("5. Get pixel color")
        print("6. Save screen region as template")
        print("0. Back to main menu")
        print("=" * 70)

        choice = get_user_choice(6)

        if choice == '0':
            break
        elif choice == '1':
            filename = input("Enter filename to save (e.g., screenshot.png): ").strip()
            image_rec.capture_screenshot(filename)
        elif choice == '2':
            image_path = input("Enter image file path to find: ").strip()
            image_rec.find_image_on_screen(image_path)
        elif choice == '3':
            image_path = input("Enter image file path to click: ").strip()
            image_rec.click_image(image_path)
        elif choice == '4':
            image_path = input("Enter image file path to wait for: ").strip()
            timeout = int(input("Enter timeout in seconds: ").strip())
            image_rec.wait_for_image(image_path, timeout)
        elif choice == '5':
            x = int(input("Enter X coordinate: ").strip())
            y = int(input("Enter Y coordinate: ").strip())
            color = image_rec.get_pixel_color(x, y)
            print(f"Pixel color at ({x}, {y}): RGB{color}")
        elif choice == '6':
            x = int(input("Enter X coordinate: ").strip())
            y = int(input("Enter Y coordinate: ").strip())
            width = int(input("Enter width: ").strip())
            height = int(input("Enter height: ").strip())
            filename = input("Enter template filename: ").strip()
            image_rec.save_region_as_template(x, y, width, height, filename)


def settings_menu(player):
    """Settings menu"""
    while True:
        print("\n" + "=" * 70)
        print("SETTINGS & OPTIONS")
        print("=" * 70)
        print("1. Configure random delays")
        print("2. Set playback speed")
        print("3. Image recognition confidence")
        print("4. View screen size")
        print("0. Back to main menu")
        print("=" * 70)

        choice = get_user_choice(4)

        if choice == '0':
            break
        elif choice == '1':
            enable = input("Enable random delays? (y/n): ").strip().lower() == 'y'
            if enable:
                min_delay = float(input("Enter min delay (seconds): ").strip())
                max_delay = float(input("Enter max delay (seconds): ").strip())
                player.enable_random_delays(min_delay, max_delay)
            else:
                player.disable_random_delays()
        elif choice == '2':
            speed = float(input("Enter playback speed multiplier: ").strip())
            print(f"Speed set to {speed}x")
        elif choice == '3':
            confidence = float(input("Enter confidence threshold (0.0-1.0): ").strip())
            image_rec = ImageRecognition()
            image_rec.set_confidence(confidence)
        elif choice == '4':
            image_rec = ImageRecognition()
            width, height = image_rec.get_screen_size()
            print(f"Screen size: {width}x{height}")


def view_recording_info(recording_manager):
    """Display information about a recording"""
    slot_name = input("Enter slot name (or press Enter for 'default'): ").strip()
    if not slot_name:
        slot_name = "default"

    actions = recording_manager.load_recording(slot_name)
    if not actions:
        return

    print("\n" + "=" * 70)
    print(f"RECORDING INFO: {slot_name}")
    print("=" * 70)

    total_actions = len(actions)
    duration = actions[-1]['timestamp'] if actions else 0

    action_types = {}
    for action in actions:
        action_type = action['type']
        action_types[action_type] = action_types.get(action_type, 0) + 1

    print(f"\nTotal actions: {total_actions}")
    print(f"Duration: {duration:.2f} seconds")
    print("\nAction breakdown:")
    for action_type, count in sorted(action_types.items()):
        print(f"  - {action_type}: {count}")


def launch_gui():
    """Launch the GUI"""
    print("\nLaunching GUI...")
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error: Could not import GUI module: {e}")
    except Exception as e:
        print(f"Error launching GUI: {e}")


def main():
    """Main program loop"""
    print_banner()

    # Initialize components
    recorder = ActionRecorder()
    player = ActionPlayer()
    recording_manager = RecordingManager()

    while True:
        print_main_menu()
        choice = get_user_choice(10)

        if choice == '0':
            print("\nThank you for using Windows Action Recorder & Player Pro!")
            print("Goodbye!\n")
            sys.exit(0)
        elif choice == '1':
            record_actions(recording_manager)
        elif choice == '2':
            playback_once(recording_manager, player)
        elif choice == '3':
            repeat_at_intervals(recording_manager, player)
        elif choice == '4':
            manage_recordings(recording_manager)
        elif choice == '5':
            hotkey_mode(recorder, player, recording_manager)
        elif choice == '6':
            scheduler_menu(player, recording_manager)
        elif choice == '7':
            image_recognition_menu()
        elif choice == '8':
            settings_menu(player)
        elif choice == '9':
            view_recording_info(recording_manager)
        elif choice == '10':
            launch_gui()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!\n")
        sys.exit(0)
