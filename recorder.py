"""
Action Recorder Module
Records mouse and keyboard actions with timestamps
"""

import json
import time
from pynput import mouse, keyboard


class ActionRecorder:
    def __init__(self):
        self.actions = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.recording = False

    def start_recording(self):
        """Start recording user actions"""
        self.actions = []
        self.start_time = time.time()
        self.recording = True

        print("Recording started... Press ESC to stop recording.")
        print("Perform your actions now...")

        # Set up mouse listener
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )

        # Set up keyboard listener
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )

        self.mouse_listener.start()
        self.keyboard_listener.start()

        # Wait for ESC key to stop
        self.keyboard_listener.join()

    def stop_recording(self):
        """Stop recording"""
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print(f"\nRecording stopped. Total actions recorded: {len(self.actions)}")

    def on_mouse_move(self, x, y):
        """Record mouse movement"""
        if self.recording:
            timestamp = time.time() - self.start_time
            self.actions.append({
                'type': 'mouse_move',
                'x': x,
                'y': y,
                'timestamp': timestamp
            })

    def on_mouse_click(self, x, y, button, pressed):
        """Record mouse click"""
        if self.recording:
            timestamp = time.time() - self.start_time
            self.actions.append({
                'type': 'mouse_click',
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed,
                'timestamp': timestamp
            })

    def on_mouse_scroll(self, x, y, dx, dy):
        """Record mouse scroll"""
        if self.recording:
            timestamp = time.time() - self.start_time
            self.actions.append({
                'type': 'mouse_scroll',
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'timestamp': timestamp
            })

    def on_key_press(self, key):
        """Record key press"""
        if self.recording:
            # Stop recording on ESC key
            if key == keyboard.Key.esc:
                self.stop_recording()
                return False

            timestamp = time.time() - self.start_time
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)

            self.actions.append({
                'type': 'key_press',
                'key': key_char,
                'timestamp': timestamp
            })

    def on_key_release(self, key):
        """Record key release"""
        if self.recording and key != keyboard.Key.esc:
            timestamp = time.time() - self.start_time
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)

            self.actions.append({
                'type': 'key_release',
                'key': key_char,
                'timestamp': timestamp
            })

    def save_recording(self, filename='recording.json'):
        """Save recorded actions to a JSON file"""
        # Optimize: Remove excessive mouse movements
        optimized_actions = self.optimize_actions(self.actions)

        with open(filename, 'w') as f:
            json.dump(optimized_actions, f, indent=2)

        print(f"Recording saved to {filename}")
        print(f"Optimized from {len(self.actions)} to {len(optimized_actions)} actions")

    def optimize_actions(self, actions):
        """Optimize recorded actions by reducing mouse movements"""
        optimized = []
        last_move_time = 0
        move_threshold = 0.05  # Only record mouse moves every 50ms

        for action in actions:
            if action['type'] == 'mouse_move':
                # Only keep mouse movements with sufficient time gap
                if action['timestamp'] - last_move_time > move_threshold:
                    optimized.append(action)
                    last_move_time = action['timestamp']
            else:
                optimized.append(action)

        return optimized

    def load_recording(self, filename='recording.json'):
        """Load recorded actions from a JSON file"""
        try:
            with open(filename, 'r') as f:
                self.actions = json.load(f)
            print(f"Recording loaded from {filename}")
            print(f"Total actions: {len(self.actions)}")
            return True
        except FileNotFoundError:
            print(f"Error: Recording file '{filename}' not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{filename}'.")
            return False
