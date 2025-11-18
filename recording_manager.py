"""
Recording Manager Module
Manages multiple recording slots
"""

import os
import json
import glob
from datetime import datetime


class RecordingManager:
    def __init__(self, recordings_dir='recordings'):
        self.recordings_dir = recordings_dir
        self._ensure_dir_exists()

    def _ensure_dir_exists(self):
        """Ensure recordings directory exists"""
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)

    def get_recording_path(self, slot_name):
        """Get the full path for a recording slot"""
        return os.path.join(self.recordings_dir, f"{slot_name}.json")

    def list_recordings(self):
        """List all available recordings"""
        pattern = os.path.join(self.recordings_dir, "*.json")
        recordings = []

        for filepath in glob.glob(pattern):
            filename = os.path.basename(filepath)
            slot_name = filename.replace('.json', '')

            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)

                action_count = len(data)
                duration = data[-1]['timestamp'] if data else 0
                file_size = os.path.getsize(filepath)
                modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))

                recordings.append({
                    'slot_name': slot_name,
                    'filepath': filepath,
                    'action_count': action_count,
                    'duration': duration,
                    'file_size': file_size,
                    'modified': modified_time
                })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

        return sorted(recordings, key=lambda x: x['modified'], reverse=True)

    def save_recording(self, slot_name, actions):
        """Save recording to a specific slot"""
        filepath = self.get_recording_path(slot_name)
        with open(filepath, 'w') as f:
            json.dump(actions, f, indent=2)
        print(f"Recording saved to slot '{slot_name}'")

    def load_recording(self, slot_name):
        """Load recording from a specific slot"""
        filepath = self.get_recording_path(slot_name)

        if not os.path.exists(filepath):
            print(f"Error: Recording slot '{slot_name}' not found.")
            return None

        try:
            with open(filepath, 'r') as f:
                actions = json.load(f)
            print(f"Recording loaded from slot '{slot_name}'")
            return actions
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in slot '{slot_name}'.")
            return None

    def delete_recording(self, slot_name):
        """Delete a recording slot"""
        filepath = self.get_recording_path(slot_name)

        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Recording slot '{slot_name}' deleted.")
            return True
        else:
            print(f"Error: Recording slot '{slot_name}' not found.")
            return False

    def rename_recording(self, old_name, new_name):
        """Rename a recording slot"""
        old_path = self.get_recording_path(old_name)
        new_path = self.get_recording_path(new_name)

        if not os.path.exists(old_path):
            print(f"Error: Recording slot '{old_name}' not found.")
            return False

        if os.path.exists(new_path):
            print(f"Error: Recording slot '{new_name}' already exists.")
            return False

        os.rename(old_path, new_path)
        print(f"Recording renamed from '{old_name}' to '{new_name}'.")
        return True

    def export_recording(self, slot_name, export_path):
        """Export recording to a specific location"""
        source = self.get_recording_path(slot_name)

        if not os.path.exists(source):
            print(f"Error: Recording slot '{slot_name}' not found.")
            return False

        with open(source, 'r') as src:
            data = json.load(src)

        with open(export_path, 'w') as dest:
            json.dump(data, dest, indent=2)

        print(f"Recording exported to '{export_path}'")
        return True

    def import_recording(self, import_path, slot_name):
        """Import recording from external file"""
        if not os.path.exists(import_path):
            print(f"Error: File '{import_path}' not found.")
            return False

        try:
            with open(import_path, 'r') as src:
                data = json.load(src)

            self.save_recording(slot_name, data)
            print(f"Recording imported to slot '{slot_name}'")
            return True
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{import_path}'.")
            return False
