"""
Action Player Module
Replays recorded mouse and keyboard actions
"""

import time
from pynput import mouse, keyboard


class ActionPlayer:
    def __init__(self):
        self.actions = []
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def load_actions(self, actions):
        """Load actions to be played"""
        self.actions = actions

    def play(self, speed_multiplier=1.0):
        """
        Play the recorded actions

        Args:
            speed_multiplier: Speed multiplier (1.0 = normal speed, 2.0 = 2x speed, 0.5 = half speed)
        """
        if not self.actions:
            print("No actions to play. Please load a recording first.")
            return

        print(f"Playing {len(self.actions)} actions...")
        print("Starting in 3 seconds...")
        time.sleep(3)

        start_time = time.time()
        last_timestamp = 0

        for i, action in enumerate(self.actions):
            # Calculate delay
            target_timestamp = action['timestamp'] / speed_multiplier
            current_elapsed = time.time() - start_time
            delay = target_timestamp - current_elapsed

            if delay > 0:
                time.sleep(delay)

            # Execute action
            self.execute_action(action)

            # Progress indicator (every 100 actions)
            if (i + 1) % 100 == 0:
                print(f"Progress: {i + 1}/{len(self.actions)} actions")

        print("Playback complete!")

    def execute_action(self, action):
        """Execute a single action"""
        action_type = action['type']

        try:
            if action_type == 'mouse_move':
                self.mouse_controller.position = (action['x'], action['y'])

            elif action_type == 'mouse_click':
                self.mouse_controller.position = (action['x'], action['y'])
                button = self.parse_button(action['button'])

                if action['pressed']:
                    self.mouse_controller.press(button)
                else:
                    self.mouse_controller.release(button)

            elif action_type == 'mouse_scroll':
                self.mouse_controller.position = (action['x'], action['y'])
                self.mouse_controller.scroll(action['dx'], action['dy'])

            elif action_type == 'key_press':
                key = self.parse_key(action['key'])
                self.keyboard_controller.press(key)

            elif action_type == 'key_release':
                key = self.parse_key(action['key'])
                self.keyboard_controller.release(key)

        except Exception as e:
            print(f"Error executing action {action_type}: {e}")

    def parse_button(self, button_str):
        """Parse button string to mouse.Button object"""
        if 'left' in button_str.lower():
            return mouse.Button.left
        elif 'right' in button_str.lower():
            return mouse.Button.right
        elif 'middle' in button_str.lower():
            return mouse.Button.middle
        else:
            return mouse.Button.left

    def parse_key(self, key_str):
        """Parse key string to keyboard key object"""
        # Special keys mapping
        special_keys = {
            'Key.space': keyboard.Key.space,
            'Key.enter': keyboard.Key.enter,
            'Key.tab': keyboard.Key.tab,
            'Key.backspace': keyboard.Key.backspace,
            'Key.delete': keyboard.Key.delete,
            'Key.shift': keyboard.Key.shift,
            'Key.shift_r': keyboard.Key.shift_r,
            'Key.ctrl': keyboard.Key.ctrl,
            'Key.ctrl_r': keyboard.Key.ctrl_r,
            'Key.alt': keyboard.Key.alt,
            'Key.alt_r': keyboard.Key.alt_r,
            'Key.cmd': keyboard.Key.cmd,
            'Key.cmd_r': keyboard.Key.cmd_r,
            'Key.up': keyboard.Key.up,
            'Key.down': keyboard.Key.down,
            'Key.left': keyboard.Key.left,
            'Key.right': keyboard.Key.right,
            'Key.home': keyboard.Key.home,
            'Key.end': keyboard.Key.end,
            'Key.page_up': keyboard.Key.page_up,
            'Key.page_down': keyboard.Key.page_down,
            'Key.caps_lock': keyboard.Key.caps_lock,
            'Key.f1': keyboard.Key.f1,
            'Key.f2': keyboard.Key.f2,
            'Key.f3': keyboard.Key.f3,
            'Key.f4': keyboard.Key.f4,
            'Key.f5': keyboard.Key.f5,
            'Key.f6': keyboard.Key.f6,
            'Key.f7': keyboard.Key.f7,
            'Key.f8': keyboard.Key.f8,
            'Key.f9': keyboard.Key.f9,
            'Key.f10': keyboard.Key.f10,
            'Key.f11': keyboard.Key.f11,
            'Key.f12': keyboard.Key.f12,
        }

        if key_str in special_keys:
            return special_keys[key_str]
        else:
            # Regular character key
            return key_str

    def play_with_interval(self, interval_seconds, count=None):
        """
        Play actions repeatedly with a specified interval

        Args:
            interval_seconds: Interval between repetitions in seconds
            count: Number of times to repeat (None = infinite)
        """
        if not self.actions:
            print("No actions to play. Please load a recording first.")
            return

        print(f"Playing actions every {interval_seconds} seconds...")
        if count:
            print(f"Will repeat {count} times. Press Ctrl+C to stop early.")
        else:
            print("Will repeat indefinitely. Press Ctrl+C to stop.")

        repetition = 0
        try:
            while count is None or repetition < count:
                repetition += 1
                print(f"\n--- Repetition {repetition} ---")
                self.play(speed_multiplier=1.0)

                if count is None or repetition < count:
                    print(f"Waiting {interval_seconds} seconds before next repetition...")
                    time.sleep(interval_seconds)

        except KeyboardInterrupt:
            print(f"\n\nStopped by user after {repetition} repetitions.")
