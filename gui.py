"""
GUI Module
Graphical User Interface for Windows Action Recorder
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import threading
from recorder import ActionRecorder
from player import ActionPlayer
from recording_manager import RecordingManager
from hotkey_manager import HotkeyRecorderController
from scheduler import AutomationScheduler, ScheduleBuilder
from image_recognition import ImageRecognition


class ActionRecorderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows Action Recorder & Player Pro")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Core components
        self.recorder = ActionRecorder()
        self.player = ActionPlayer()
        self.recording_manager = RecordingManager()
        self.image_rec = ImageRecognition()
        self.scheduler = AutomationScheduler(self.player, self.recording_manager)

        # State
        self.current_slot = "default"
        self.is_recording = False
        self.is_playing = False
        self.recording_thread = None

        # Setup hotkeys
        self.hotkey_controller = HotkeyRecorderController(
            self.recorder, self.player, self.recording_manager
        )

        # Setup GUI
        self.setup_ui()

        # Load recordings
        self.refresh_recordings_list()

    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Create tabs
        self.create_recorder_tab()
        self.create_player_tab()
        self.create_recordings_tab()
        self.create_scheduler_tab()
        self.create_settings_tab()

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def create_recorder_tab(self):
        """Create recording tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Record")

        # Slot selection
        frame_slot = ttk.LabelFrame(tab, text="Recording Slot", padding=10)
        frame_slot.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame_slot, text="Slot Name:").pack(side=tk.LEFT, padx=5)
        self.slot_entry = ttk.Entry(frame_slot, width=30)
        self.slot_entry.insert(0, self.current_slot)
        self.slot_entry.pack(side=tk.LEFT, padx=5)

        # Recording controls
        frame_controls = ttk.LabelFrame(tab, text="Recording Controls", padding=10)
        frame_controls.pack(fill=tk.X, padx=10, pady=10)

        self.btn_record = ttk.Button(
            frame_controls,
            text="⏺ Start Recording (F9)",
            command=self.start_recording,
            width=30
        )
        self.btn_record.pack(pady=5)

        self.btn_stop_record = ttk.Button(
            frame_controls,
            text="⏹ Stop Recording (ESC)",
            command=self.stop_recording,
            state=tk.DISABLED,
            width=30
        )
        self.btn_stop_record.pack(pady=5)

        # Recording info
        frame_info = ttk.LabelFrame(tab, text="Recording Status", padding=10)
        frame_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.recording_status = tk.Text(frame_info, height=15, wrap=tk.WORD)
        self.recording_status.pack(fill=tk.BOTH, expand=True)
        self.recording_status.insert("1.0", "No recording in progress.\n\nPress 'Start Recording' or F9 to begin.")

    def create_player_tab(self):
        """Create playback tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Play")

        # Playback controls
        frame_controls = ttk.LabelFrame(tab, text="Playback Controls", padding=10)
        frame_controls.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            frame_controls,
            text="▶ Play Once (F10)",
            command=self.play_once,
            width=30
        ).pack(pady=5)

        ttk.Button(
            frame_controls,
            text="🔁 Repeat at Intervals",
            command=self.play_repeat,
            width=30
        ).pack(pady=5)

        ttk.Button(
            frame_controls,
            text="⏹ Stop Playback (F11)",
            command=self.stop_playback,
            width=30
        ).pack(pady=5)

        # Playback options
        frame_options = ttk.LabelFrame(tab, text="Playback Options", padding=10)
        frame_options.pack(fill=tk.X, padx=10, pady=10)

        # Speed multiplier
        ttk.Label(frame_options, text="Speed Multiplier:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_spinbox = ttk.Spinbox(frame_options, from_=0.1, to=5.0, increment=0.1, textvariable=self.speed_var, width=10)
        speed_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)

        # Random delays
        self.random_delay_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_options,
            text="Enable Random Delays (0.1s - 0.5s)",
            variable=self.random_delay_var,
            command=self.toggle_random_delays
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

    def create_recordings_tab(self):
        """Create recordings management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Recordings")

        # Recordings list
        frame_list = ttk.LabelFrame(tab, text="Saved Recordings", padding=10)
        frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview for recordings
        columns = ('Slot', 'Actions', 'Duration', 'Modified')
        self.recordings_tree = ttk.Treeview(frame_list, columns=columns, show='headings', height=15)

        self.recordings_tree.heading('Slot', text='Slot Name')
        self.recordings_tree.heading('Actions', text='Actions')
        self.recordings_tree.heading('Duration', text='Duration (s)')
        self.recordings_tree.heading('Modified', text='Last Modified')

        self.recordings_tree.column('Slot', width=200)
        self.recordings_tree.column('Actions', width=100)
        self.recordings_tree.column('Duration', width=100)
        self.recordings_tree.column('Modified', width=200)

        self.recordings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=self.recordings_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recordings_tree.configure(yscrollcommand=scrollbar.set)

        # Buttons
        frame_buttons = ttk.Frame(tab)
        frame_buttons.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_buttons, text="🔄 Refresh", command=self.refresh_recordings_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="▶ Load & Play", command=self.load_and_play_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="🗑 Delete", command=self.delete_selected_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="✏ Rename", command=self.rename_selected_recording).pack(side=tk.LEFT, padx=5)

    def create_scheduler_tab(self):
        """Create scheduler tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Scheduler")

        # Scheduler controls
        frame_controls = ttk.LabelFrame(tab, text="Scheduler Controls", padding=10)
        frame_controls.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            frame_controls,
            text="▶ Start Scheduler",
            command=self.start_scheduler,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            frame_controls,
            text="⏹ Stop Scheduler",
            command=self.stop_scheduler,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        # Jobs list
        frame_jobs = ttk.LabelFrame(tab, text="Scheduled Jobs", padding=10)
        frame_jobs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ('ID', 'Slot', 'Type', 'Schedule', 'Enabled', 'Runs')
        self.jobs_tree = ttk.Treeview(frame_jobs, columns=columns, show='headings', height=10)

        for col in columns:
            self.jobs_tree.heading(col, text=col)
            self.jobs_tree.column(col, width=100)

        self.jobs_tree.pack(fill=tk.BOTH, expand=True)

        # Job buttons
        frame_job_buttons = ttk.Frame(tab)
        frame_job_buttons.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_job_buttons, text="➕ Add Job", command=self.add_scheduled_job).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_job_buttons, text="🗑 Remove Job", command=self.remove_scheduled_job).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_job_buttons, text="🔄 Refresh", command=self.refresh_jobs_list).pack(side=tk.LEFT, padx=5)

    def create_settings_tab(self):
        """Create settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings")

        # Hotkeys
        frame_hotkeys = ttk.LabelFrame(tab, text="Global Hotkeys", padding=10)
        frame_hotkeys.pack(fill=tk.X, padx=10, pady=10)

        self.hotkey_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_hotkeys,
            text="Enable Global Hotkeys",
            variable=self.hotkey_enabled_var,
            command=self.toggle_hotkeys
        ).pack(anchor=tk.W)

        hotkey_info = """
        F9  - Start/Stop Recording
        F10 - Play Recording
        F11 - Stop Playback
        """
        ttk.Label(frame_hotkeys, text=hotkey_info, justify=tk.LEFT).pack(anchor=tk.W, padx=20)

        # Image Recognition
        frame_image = ttk.LabelFrame(tab, text="Image Recognition", padding=10)
        frame_image.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame_image, text="Confidence Threshold:").pack(side=tk.LEFT, padx=5)
        confidence_var = tk.DoubleVar(value=0.8)
        ttk.Spinbox(frame_image, from_=0.1, to=1.0, increment=0.05, textvariable=confidence_var, width=10).pack(side=tk.LEFT)

        ttk.Button(frame_image, text="Capture Screenshot", command=self.capture_screenshot).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_image, text="Find Image on Screen", command=self.find_image_gui).pack(side=tk.LEFT, padx=5)

        # About
        frame_about = ttk.LabelFrame(tab, text="About", padding=10)
        frame_about.pack(fill=tk.X, padx=10, pady=10)

        about_text = """
        Windows Action Recorder & Player Pro v2.0

        Advanced automation tool with:
        • Multiple recording slots
        • Random delays for human-like behavior
        • Global hotkey support
        • Image recognition
        • Conditional logic
        • Task scheduling
        """
        ttk.Label(frame_about, text=about_text, justify=tk.LEFT).pack()

    # Recording methods
    def start_recording(self):
        """Start recording"""
        self.current_slot = self.slot_entry.get()
        if not self.current_slot:
            messagebox.showerror("Error", "Please enter a slot name")
            return

        self.is_recording = True
        self.btn_record.config(state=tk.DISABLED)
        self.btn_stop_record.config(state=tk.NORMAL)
        self.recording_status.delete("1.0", tk.END)
        self.recording_status.insert("1.0", f"Recording to slot '{self.current_slot}'...\nPress ESC to stop.\n\n")
        self.update_status("Recording...")

        def record():
            self.recorder.start_recording()
            self.root.after(0, self.on_recording_stopped)

        self.recording_thread = threading.Thread(target=record, daemon=True)
        self.recording_thread.start()

    def stop_recording(self):
        """Stop recording"""
        if self.is_recording:
            self.recorder.stop_recording()

    def on_recording_stopped(self):
        """Called when recording stops"""
        self.is_recording = False
        self.btn_record.config(state=tk.NORMAL)
        self.btn_stop_record.config(state=tk.DISABLED)

        self.recording_manager.save_recording(self.current_slot, self.recorder.actions)

        self.recording_status.insert(tk.END, f"\nRecording saved to slot '{self.current_slot}'\n")
        self.recording_status.insert(tk.END, f"Total actions: {len(self.recorder.actions)}\n")

        self.update_status("Recording saved")
        self.refresh_recordings_list()

    # Playback methods
    def play_once(self):
        """Play recording once"""
        if not self.current_slot:
            messagebox.showerror("Error", "Please select a recording")
            return

        actions = self.recording_manager.load_recording(self.current_slot)
        if not actions:
            messagebox.showerror("Error", f"No recording found in slot '{self.current_slot}'")
            return

        self.update_status("Playing...")

        def play():
            self.player.load_actions(actions)
            self.player.play(speed_multiplier=self.speed_var.get())
            self.root.after(0, lambda: self.update_status("Playback complete"))

        threading.Thread(target=play, daemon=True).start()

    def play_repeat(self):
        """Play recording repeatedly"""
        interval = simpledialog.askfloat("Repeat Interval", "Enter interval in seconds:", minvalue=1.0)
        if not interval:
            return

        count = simpledialog.askinteger("Repeat Count", "Enter number of repetitions (0 for infinite):", minvalue=0)
        if count is None:
            return

        count = None if count == 0 else count

        actions = self.recording_manager.load_recording(self.current_slot)
        if not actions:
            messagebox.showerror("Error", f"No recording found in slot '{self.current_slot}'")
            return

        def play_repeat():
            self.player.load_actions(actions)
            self.player.play_with_interval(interval, count)

        threading.Thread(target=play_repeat, daemon=True).start()
        self.update_status(f"Repeating every {interval}s...")

    def stop_playback(self):
        """Stop playback"""
        self.update_status("Playback stopped")

    def toggle_random_delays(self):
        """Toggle random delays"""
        if self.random_delay_var.get():
            self.player.enable_random_delays()
        else:
            self.player.disable_random_delays()

    # Recording management
    def refresh_recordings_list(self):
        """Refresh recordings list"""
        for item in self.recordings_tree.get_children():
            self.recordings_tree.delete(item)

        recordings = self.recording_manager.list_recordings()
        for rec in recordings:
            self.recordings_tree.insert('', tk.END, values=(
                rec['slot_name'],
                rec['action_count'],
                f"{rec['duration']:.1f}",
                rec['modified'].strftime("%Y-%m-%d %H:%M")
            ))

    def load_and_play_selected(self):
        """Load and play selected recording"""
        selection = self.recordings_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recording")
            return

        item = self.recordings_tree.item(selection[0])
        slot_name = item['values'][0]

        self.current_slot = slot_name
        self.slot_entry.delete(0, tk.END)
        self.slot_entry.insert(0, slot_name)

        self.play_once()

    def delete_selected_recording(self):
        """Delete selected recording"""
        selection = self.recordings_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recording")
            return

        item = self.recordings_tree.item(selection[0])
        slot_name = item['values'][0]

        if messagebox.askyesno("Confirm Delete", f"Delete recording '{slot_name}'?"):
            self.recording_manager.delete_recording(slot_name)
            self.refresh_recordings_list()

    def rename_selected_recording(self):
        """Rename selected recording"""
        selection = self.recordings_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recording")
            return

        item = self.recordings_tree.item(selection[0])
        old_name = item['values'][0]

        new_name = simpledialog.askstring("Rename Recording", f"Enter new name for '{old_name}':")
        if new_name:
            self.recording_manager.rename_recording(old_name, new_name)
            self.refresh_recordings_list()

    # Scheduler methods
    def start_scheduler(self):
        """Start scheduler"""
        self.scheduler.start()
        self.update_status("Scheduler started")

    def stop_scheduler(self):
        """Stop scheduler"""
        self.scheduler.stop()
        self.update_status("Scheduler stopped")

    def add_scheduled_job(self):
        """Add scheduled job"""
        # Simple dialog for adding jobs
        messagebox.showinfo("Add Job", "Use CLI or edit schedule_config.json to add scheduled jobs")

    def remove_scheduled_job(self):
        """Remove scheduled job"""
        selection = self.jobs_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a job")
            return

        item = self.jobs_tree.item(selection[0])
        job_id = item['values'][0]

        if messagebox.askyesno("Confirm Delete", f"Delete job '{job_id}'?"):
            self.scheduler.remove_job(job_id)
            self.refresh_jobs_list()

    def refresh_jobs_list(self):
        """Refresh jobs list"""
        for item in self.jobs_tree.get_children():
            self.jobs_tree.delete(item)

        jobs = self.scheduler.list_jobs()
        for job in jobs:
            self.jobs_tree.insert('', tk.END, values=(
                job['id'],
                job['slot_name'],
                job['schedule_type'],
                job['schedule_value'],
                '✓' if job['enabled'] else '✗',
                job['run_count']
            ))

    # Settings methods
    def toggle_hotkeys(self):
        """Toggle hotkeys"""
        if self.hotkey_enabled_var.get():
            self.hotkey_controller.setup_default_hotkeys()
            self.update_status("Hotkeys enabled")
        else:
            self.hotkey_controller.cleanup()
            self.update_status("Hotkeys disabled")

    def capture_screenshot(self):
        """Capture screenshot"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.image_rec.capture_screenshot(filename)
            messagebox.showinfo("Success", f"Screenshot saved to {filename}")

    def find_image_gui(self):
        """Find image on screen"""
        filename = filedialog.askopenfilename(
            title="Select image to find",
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if filename:
            location = self.image_rec.find_image_on_screen(filename)
            if location:
                messagebox.showinfo("Found", f"Image found at: {location}")
            else:
                messagebox.showwarning("Not Found", "Image not found on screen")

    # Utility methods
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)

    def run(self):
        """Run the GUI"""
        self.root.mainloop()


def main():
    """Main entry point for GUI"""
    app = ActionRecorderGUI()
    app.run()


if __name__ == "__main__":
    main()
