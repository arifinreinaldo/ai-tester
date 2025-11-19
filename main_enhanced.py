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
from macro_editor import MacroEditor
from recording_preview import RecordingPreview
from workflow_builder import (
    Workflow, WorkflowManager, PlayRecordingStep, DelayStep,
    ConditionalStep, LoopStep, TryCatchStep
)


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
    print("8.  ✏  Macro Editor (Edit Recordings)")
    print("9.  👁  Preview Recording (Visualize)")
    print("10. 🔗 Workflow Builder (Chain Recordings)")
    print("11. ⚙  Settings & Options")
    print("12. ℹ  View Recording Info")
    print("13. 🖥  Launch GUI")
    print("0.  🚪 Exit")
    print("=" * 70)


def get_user_choice(max_choice=13):
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


def macro_editor_menu(recording_manager):
    """Macro editor menu"""
    slot_name = input("Enter slot name to edit (or press Enter for 'default'): ").strip()
    if not slot_name:
        slot_name = "default"

    actions = recording_manager.load_recording(slot_name)
    if not actions:
        return

    editor = MacroEditor()
    editor.load_recording(actions)

    while True:
        print("\n" + "=" * 70)
        print(f"MACRO EDITOR - Editing: {slot_name}")
        print("=" * 70)
        print("1.  List actions")
        print("2.  Delete action")
        print("3.  Delete range")
        print("4.  Insert delay")
        print("5.  Remove mouse movements")
        print("6.  Simplify recording")
        print("7.  Scale speed")
        print("8.  View statistics")
        print("9.  Undo last edit")
        print("10. Save changes")
        print("11. Save as new slot")
        print("0.  Back (discard changes)")
        print("=" * 70)

        choice = get_user_choice(11)

        if choice == '0':
            if editor.has_changes():
                confirm = input("You have unsaved changes. Discard? (y/n): ").strip().lower()
                if confirm == 'y':
                    break
            else:
                break
        elif choice == '1':
            start = int(input("Start index (default 0): ").strip() or "0")
            count = int(input("How many to show (default 20): ").strip() or "20")
            editor.list_actions(start, count)
        elif choice == '2':
            index = int(input("Enter action index to delete: ").strip())
            editor.delete_action(index)
        elif choice == '3':
            start = int(input("Enter start index: ").strip())
            end = int(input("Enter end index: ").strip())
            editor.delete_range(start, end)
        elif choice == '4':
            index = int(input("Insert delay after which action index: ").strip())
            delay = float(input("Enter delay in seconds: ").strip())
            editor.insert_delay(index, delay)
        elif choice == '5':
            editor.remove_mouse_movements()
        elif choice == '6':
            editor.simplify_recording()
        elif choice == '7':
            multiplier = float(input("Enter speed multiplier (0.5=slower, 2.0=faster): ").strip())
            editor.scale_speed(multiplier)
        elif choice == '8':
            stats = editor.get_statistics()
            print("\n" + "=" * 70)
            print("RECORDING STATISTICS")
            print("=" * 70)
            print(f"Total actions: {stats['total_actions']}")
            print(f"Duration: {stats['duration']:.2f}s")
            print("\nAction types:")
            for action_type, count in stats['action_types'].items():
                print(f"  {action_type}: {count}")
        elif choice == '9':
            editor.undo()
        elif choice == '10':
            recording_manager.save_recording(slot_name, editor.get_actions())
            print(f"✓ Changes saved to '{slot_name}'")
        elif choice == '11':
            new_slot = input("Enter new slot name: ").strip()
            if new_slot:
                recording_manager.save_recording(new_slot, editor.get_actions())
                print(f"✓ Saved as '{new_slot}'")


def preview_recording_menu(recording_manager):
    """Preview recording menu"""
    slot_name = input("Enter slot name to preview (or press Enter for 'default'): ").strip()
    if not slot_name:
        slot_name = "default"

    actions = recording_manager.load_recording(slot_name)
    if not actions:
        return

    preview = RecordingPreview()
    preview.load_recording(actions)

    while True:
        print("\n" + "=" * 70)
        print(f"RECORDING PREVIEW - Viewing: {slot_name}")
        print("=" * 70)
        print("1. Show summary")
        print("2. Show timeline")
        print("3. Show detailed view")
        print("4. Show mouse path")
        print("5. Show keyboard sequence")
        print("6. Show action frequency")
        print("7. Show delays analysis")
        print("8. Show click hotspots")
        print("9. Export text report")
        print("0. Back to main menu")
        print("=" * 70)

        choice = get_user_choice(9)

        if choice == '0':
            break
        elif choice == '1':
            preview.show_summary()
        elif choice == '2':
            segments = int(input("Enter number of segments (default 20): ").strip() or "20")
            preview.show_timeline(segments)
        elif choice == '3':
            start = float(input("Start time in seconds (default 0): ").strip() or "0")
            end = float(input("End time in seconds (press Enter for end): ").strip() or str(actions[-1]['timestamp']))
            max_actions = int(input("Max actions to show (default 50): ").strip() or "50")
            preview.show_detailed_view(float(start), float(end), max_actions)
        elif choice == '4':
            sample = int(input("Sample rate (default 10): ").strip() or "10")
            preview.show_mouse_path(sample)
        elif choice == '5':
            preview.show_keyboard_sequence()
        elif choice == '6':
            preview.show_action_frequency()
        elif choice == '7':
            preview.show_delays_analysis()
        elif choice == '8':
            preview.show_hotspots()
        elif choice == '9':
            filename = input("Enter filename (e.g., report.txt): ").strip()
            if filename:
                preview.export_text_report(filename)


def workflow_builder_menu(recording_manager, player):
    """Workflow builder menu"""
    workflow_manager = WorkflowManager()

    while True:
        print("\n" + "=" * 70)
        print("WORKFLOW BUILDER")
        print("=" * 70)
        print("1. Create new workflow")
        print("2. Edit existing workflow")
        print("3. Execute workflow")
        print("4. List workflows")
        print("5. Delete workflow")
        print("0. Back to main menu")
        print("=" * 70)

        choice = get_user_choice(5)

        if choice == '0':
            break
        elif choice == '1':
            create_workflow(workflow_manager, recording_manager, player)
        elif choice == '2':
            edit_workflow(workflow_manager, recording_manager, player)
        elif choice == '3':
            execute_workflow(workflow_manager, recording_manager, player)
        elif choice == '4':
            list_workflows(workflow_manager)
        elif choice == '5':
            delete_workflow_func(workflow_manager)


def create_workflow(workflow_manager, recording_manager, player):
    """Create a new workflow"""
    name = input("Enter workflow name: ").strip()
    if not name:
        print("Workflow name cannot be empty")
        return

    workflow = Workflow(name)
    print(f"\nCreated workflow: {name}")

    # Add steps
    step_id = 0
    while True:
        print("\n" + "=" * 70)
        print(f"WORKFLOW: {name} (Current steps: {len(workflow.steps)})")
        print("=" * 70)
        print("Add step:")
        print("1. Play recording")
        print("2. Add delay")
        print("3. Conditional (if/then/else)")
        print("4. Loop")
        print("5. Try/Catch (error handling)")
        print("6. Save and exit")
        print("0. Cancel")
        print("=" * 70)

        choice = input("Enter choice: ").strip()

        if choice == '0':
            return
        elif choice == '6':
            workflow_manager.save_workflow(workflow)
            print(f"✓ Workflow '{name}' saved!")
            return
        elif choice == '1':
            slot = input("Enter recording slot name: ").strip()
            speed = float(input("Enter playback speed (default 1.0): ").strip() or "1.0")
            step_name = input("Step name (optional): ").strip()
            step = PlayRecordingStep(step_id, slot, speed, step_name or f"Play {slot}")
            workflow.add_step(step)
            step_id += 1
            print(f"✓ Added step: Play '{slot}'")
        elif choice == '2':
            seconds = float(input("Enter delay in seconds: ").strip())
            step_name = input("Step name (optional): ").strip()
            step = DelayStep(step_id, seconds, step_name or f"Delay {seconds}s")
            workflow.add_step(step)
            step_id += 1
            print(f"✓ Added step: Delay {seconds}s")
        elif choice == '3':
            print("\nCondition type:")
            print("1. Image exists")
            print("2. Pixel color")
            cond_choice = input("Enter choice: ").strip()

            if cond_choice == '1':
                image_path = input("Enter image path: ").strip()
                confidence = float(input("Confidence (0.0-1.0, default 0.8): ").strip() or "0.8")
                condition_type = 'image_exists'
                condition_params = {'image_path': image_path, 'confidence': confidence}
            elif cond_choice == '2':
                x = int(input("Enter X coordinate: ").strip())
                y = int(input("Enter Y coordinate: ").strip())
                print("Enter expected RGB color (e.g., 255,0,0 for red):")
                color_input = input().strip()
                r, g, b = map(int, color_input.split(','))
                tolerance = int(input("Tolerance (default 10): ").strip() or "10")
                condition_type = 'pixel_color'
                condition_params = {'x': x, 'y': y, 'expected_color': (r, g, b), 'tolerance': tolerance}
            else:
                print("Invalid choice")
                continue

            step_name = input("Step name (optional): ").strip()
            step = ConditionalStep(step_id, condition_type, condition_params, [], [], step_name or "Conditional")
            workflow.add_step(step)
            step_id += 1
            print("✓ Added conditional step (you can add then/else steps later)")
        elif choice == '4':
            print("\nLoop type:")
            print("1. Loop N times")
            loop_choice = input("Enter choice: ").strip()

            if loop_choice == '1':
                count = int(input("Enter loop count: ").strip())
                loop_type = 'count'
                loop_params = {'count': count}
            else:
                print("Invalid choice")
                continue

            step_name = input("Step name (optional): ").strip()
            step = LoopStep(step_id, loop_type, loop_params, [], step_name or f"Loop {count}x")
            workflow.add_step(step)
            step_id += 1
            print(f"✓ Added loop step (you can add steps to loop later)")
        elif choice == '5':
            retry_count = int(input("Enter retry count (0 for no retry): ").strip() or "0")
            step_name = input("Step name (optional): ").strip()
            step = TryCatchStep(step_id, [], [], retry_count, step_name or "Try/Catch")
            workflow.add_step(step)
            step_id += 1
            print("✓ Added try/catch step")


def edit_workflow(workflow_manager, recording_manager, player):
    """Edit existing workflow"""
    name = input("Enter workflow name to edit: ").strip()
    workflow = workflow_manager.load_workflow(name)

    if not workflow:
        return

    print(f"\nEditing workflow: {name}")
    print(f"Current steps: {len(workflow.steps)}")

    # Simple edit - just show steps
    for i, step in enumerate(workflow.steps):
        print(f"{i}. {step.name} ({step.step_type})")

    print("\nEdit options not fully implemented in CLI. Use GUI for advanced editing.")
    input("Press Enter to continue...")


def execute_workflow(workflow_manager, recording_manager, player):
    """Execute a workflow"""
    name = input("Enter workflow name to execute: ").strip()
    workflow = workflow_manager.load_workflow(name)

    if not workflow:
        return

    print(f"\nAbout to execute workflow: {name}")
    print(f"Steps: {len(workflow.steps)}")

    confirm = input("Execute? (y/n): ").strip().lower()
    if confirm == 'y':
        workflow.execute(recording_manager, player)


def list_workflows(workflow_manager):
    """List all workflows"""
    workflows = workflow_manager.list_workflows()

    if not workflows:
        print("\nNo workflows found.")
        return

    print("\n" + "=" * 70)
    print("SAVED WORKFLOWS")
    print("=" * 70)
    print(f"{'Name':<30} {'Steps':<10} {'Modified'}")
    print("-" * 70)

    for wf in workflows:
        print(f"{wf['name']:<30} {wf['steps']:<10} {wf['modified'][:19]}")

    print("=" * 70)


def delete_workflow_func(workflow_manager):
    """Delete a workflow"""
    name = input("Enter workflow name to delete: ").strip()
    if name:
        confirm = input(f"Delete workflow '{name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            workflow_manager.delete_workflow(name)


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
        choice = get_user_choice(13)

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
            macro_editor_menu(recording_manager)
        elif choice == '9':
            preview_recording_menu(recording_manager)
        elif choice == '10':
            workflow_builder_menu(recording_manager, player)
        elif choice == '11':
            settings_menu(player)
        elif choice == '12':
            view_recording_info(recording_manager)
        elif choice == '13':
            launch_gui()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!\n")
        sys.exit(0)
