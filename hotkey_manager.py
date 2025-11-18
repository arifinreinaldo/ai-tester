"""
Hotkey Manager Module
Manages global hotkeys for recording and playback
"""

import keyboard
import threading


class HotkeyManager:
    def __init__(self):
        self.hotkeys = {}
        self.enabled = False

    def register_hotkey(self, key_combination, callback, description=""):
        """
        Register a global hotkey

        Args:
            key_combination: Hotkey combination (e.g., 'f9', 'ctrl+shift+r')
            callback: Function to call when hotkey is pressed
            description: Description of what the hotkey does
        """
        try:
            keyboard.add_hotkey(key_combination, callback, suppress=False)
            self.hotkeys[key_combination] = {
                'callback': callback,
                'description': description
            }
            print(f"Hotkey registered: {key_combination} - {description}")
            return True
        except Exception as e:
            print(f"Error registering hotkey {key_combination}: {e}")
            return False

    def unregister_hotkey(self, key_combination):
        """Unregister a hotkey"""
        try:
            keyboard.remove_hotkey(key_combination)
            if key_combination in self.hotkeys:
                del self.hotkeys[key_combination]
            print(f"Hotkey unregistered: {key_combination}")
            return True
        except Exception as e:
            print(f"Error unregistering hotkey {key_combination}: {e}")
            return False

    def unregister_all(self):
        """Unregister all hotkeys"""
        for key_combo in list(self.hotkeys.keys()):
            self.unregister_hotkey(key_combo)

    def list_hotkeys(self):
        """List all registered hotkeys"""
        return self.hotkeys.copy()

    def enable(self):
        """Enable hotkey listening"""
        self.enabled = True
        print("Hotkey manager enabled")

    def disable(self):
        """Disable hotkey listening"""
        self.enabled = False
        self.unregister_all()
        print("Hotkey manager disabled")


class HotkeyRecorderController:
    """
    Controller for managing recording and playback with hotkeys
    """

    def __init__(self, recorder, player, recording_manager):
        self.recorder = recorder
        self.player = player
        self.recording_manager = recording_manager
        self.hotkey_manager = HotkeyManager()
        self.is_recording = False
        self.is_playing = False
        self.current_slot = "default"
        self.recording_thread = None
        self.playback_thread = None

    def setup_default_hotkeys(self):
        """Setup default hotkey bindings"""
        self.hotkey_manager.register_hotkey(
            'f9',
            self.toggle_recording,
            'Toggle Recording (Start/Stop)'
        )
        self.hotkey_manager.register_hotkey(
            'f10',
            self.play_recording,
            'Play Recording Once'
        )
        self.hotkey_manager.register_hotkey(
            'f11',
            self.stop_playback,
            'Stop Current Playback'
        )

        self.hotkey_manager.enable()
        print("\n=== Default Hotkeys ===")
        print("F9  - Start/Stop Recording")
        print("F10 - Play Recording")
        print("F11 - Stop Playback")
        print("=======================\n")

    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start recording in background thread"""
        if self.is_recording:
            print("Already recording!")
            return

        self.is_recording = True
        print(f"\n[F9] Recording started to slot '{self.current_slot}'...")
        print("Press F9 again to stop recording.\n")

        def record_thread():
            self.recorder.start_recording()
            # Recording stopped by ESC or hotkey
            self.is_recording = False

        self.recording_thread = threading.Thread(target=record_thread, daemon=True)
        self.recording_thread.start()

    def stop_recording(self):
        """Stop current recording"""
        if not self.is_recording:
            print("Not currently recording!")
            return

        print(f"\n[F9] Stopping recording...")
        self.recorder.stop_recording()
        self.recording_manager.save_recording(self.current_slot, self.recorder.actions)
        self.is_recording = False

    def play_recording(self):
        """Play recording in background thread"""
        if self.is_playing:
            print("Already playing!")
            return

        if self.is_recording:
            print("Cannot play while recording!")
            return

        actions = self.recording_manager.load_recording(self.current_slot)
        if not actions:
            print(f"No recording found in slot '{self.current_slot}'")
            return

        self.is_playing = True
        print(f"\n[F10] Playing recording from slot '{self.current_slot}'...")

        def play_thread():
            self.player.load_actions(actions)
            self.player.play()
            self.is_playing = False
            print(f"\n[F10] Playback complete!")

        self.playback_thread = threading.Thread(target=play_thread, daemon=True)
        self.playback_thread.start()

    def stop_playback(self):
        """Stop current playback"""
        if not self.is_playing:
            print("Not currently playing!")
            return

        print(f"\n[F11] Stopping playback...")
        self.is_playing = False
        # Note: Actual stopping would require interrupt mechanism in player

    def set_current_slot(self, slot_name):
        """Set the current recording slot"""
        self.current_slot = slot_name
        print(f"Current slot set to: {slot_name}")

    def cleanup(self):
        """Clean up hotkey manager"""
        self.hotkey_manager.disable()
