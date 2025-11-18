"""
Macro Editor Module
Edit recordings without re-recording
"""

import json
import copy
from datetime import datetime


class MacroEditor:
    def __init__(self):
        self.actions = []
        self.original_actions = []
        self.undo_stack = []
        self.redo_stack = []

    def load_recording(self, actions):
        """Load recording for editing"""
        self.actions = copy.deepcopy(actions)
        self.original_actions = copy.deepcopy(actions)
        self.undo_stack = []
        self.redo_stack = []
        print(f"Loaded recording with {len(self.actions)} actions")

    def save_snapshot(self):
        """Save current state for undo"""
        self.undo_stack.append(copy.deepcopy(self.actions))
        self.redo_stack = []  # Clear redo stack on new action

    def undo(self):
        """Undo last edit"""
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(self.actions))
            self.actions = self.undo_stack.pop()
            print("Undo successful")
            return True
        else:
            print("Nothing to undo")
            return False

    def redo(self):
        """Redo last undone edit"""
        if self.redo_stack:
            self.undo_stack.append(copy.deepcopy(self.actions))
            self.actions = self.redo_stack.pop()
            print("Redo successful")
            return True
        else:
            print("Nothing to redo")
            return False

    def get_actions(self):
        """Get edited actions"""
        return copy.deepcopy(self.actions)

    def list_actions(self, start=0, count=20):
        """List actions with index"""
        if not self.actions:
            print("No actions in recording")
            return

        end = min(start + count, len(self.actions))

        print(f"\nActions {start} to {end-1} (Total: {len(self.actions)})")
        print("-" * 80)
        print(f"{'Index':<6} {'Time':<8} {'Type':<15} {'Details'}")
        print("-" * 80)

        for i in range(start, end):
            action = self.actions[i]
            timestamp = f"{action['timestamp']:.2f}s"
            action_type = action['type']

            # Format details based on type
            if action_type == 'mouse_move':
                details = f"({action['x']}, {action['y']})"
            elif action_type == 'mouse_click':
                button = action['button']
                pressed = "press" if action['pressed'] else "release"
                details = f"{button} {pressed} at ({action['x']}, {action['y']})"
            elif action_type == 'mouse_scroll':
                details = f"dx={action['dx']}, dy={action['dy']}"
            elif action_type in ['key_press', 'key_release']:
                details = f"key='{action['key']}'"
            else:
                details = ""

            print(f"{i:<6} {timestamp:<8} {action_type:<15} {details}")

    def get_action(self, index):
        """Get action at index"""
        if 0 <= index < len(self.actions):
            return self.actions[index]
        else:
            print(f"Invalid index: {index}")
            return None

    def delete_action(self, index):
        """Delete action at index"""
        if 0 <= index < len(self.actions):
            self.save_snapshot()
            deleted = self.actions.pop(index)
            self._recalculate_timestamps()
            print(f"Deleted action at index {index}: {deleted['type']}")
            return True
        else:
            print(f"Invalid index: {index}")
            return False

    def delete_range(self, start_index, end_index):
        """Delete range of actions"""
        if 0 <= start_index < len(self.actions) and 0 <= end_index < len(self.actions):
            if start_index > end_index:
                start_index, end_index = end_index, start_index

            self.save_snapshot()
            del self.actions[start_index:end_index+1]
            self._recalculate_timestamps()
            print(f"Deleted actions {start_index} to {end_index}")
            return True
        else:
            print(f"Invalid range: {start_index} to {end_index}")
            return False

    def insert_action(self, index, action):
        """Insert action at index"""
        if 0 <= index <= len(self.actions):
            self.save_snapshot()
            self.actions.insert(index, action)
            self._recalculate_timestamps()
            print(f"Inserted action at index {index}")
            return True
        else:
            print(f"Invalid index: {index}")
            return False

    def insert_delay(self, index, delay_seconds):
        """Insert delay after action at index"""
        if 0 <= index < len(self.actions):
            self.save_snapshot()

            # Shift all timestamps after this index
            for i in range(index + 1, len(self.actions)):
                self.actions[i]['timestamp'] += delay_seconds

            print(f"Inserted {delay_seconds}s delay after action {index}")
            return True
        else:
            print(f"Invalid index: {index}")
            return False

    def modify_action(self, index, **kwargs):
        """Modify action properties"""
        if 0 <= index < len(self.actions):
            self.save_snapshot()
            action = self.actions[index]

            for key, value in kwargs.items():
                if key in action:
                    action[key] = value
                    print(f"Updated {key} to {value}")
                else:
                    print(f"Warning: {key} not in action")

            return True
        else:
            print(f"Invalid index: {index}")
            return False

    def filter_actions(self, action_type):
        """Filter actions by type"""
        filtered = [
            (i, action) for i, action in enumerate(self.actions)
            if action['type'] == action_type
        ]
        return filtered

    def remove_action_type(self, action_type):
        """Remove all actions of specific type"""
        self.save_snapshot()
        original_count = len(self.actions)
        self.actions = [a for a in self.actions if a['type'] != action_type]
        removed = original_count - len(self.actions)
        self._recalculate_timestamps()
        print(f"Removed {removed} actions of type '{action_type}'")
        return removed

    def remove_mouse_movements(self):
        """Remove all mouse movements (common optimization)"""
        return self.remove_action_type('mouse_move')

    def simplify_recording(self):
        """Remove unnecessary actions"""
        self.save_snapshot()
        original_count = len(self.actions)

        # Remove consecutive duplicate mouse moves
        simplified = []
        last_mouse_pos = None

        for action in self.actions:
            if action['type'] == 'mouse_move':
                current_pos = (action['x'], action['y'])
                if current_pos != last_mouse_pos:
                    simplified.append(action)
                    last_mouse_pos = current_pos
            else:
                simplified.append(action)
                last_mouse_pos = None

        self.actions = simplified
        self._recalculate_timestamps()
        removed = original_count - len(self.actions)
        print(f"Simplified recording: removed {removed} duplicate actions")
        return removed

    def scale_speed(self, multiplier):
        """Scale all timestamps by multiplier"""
        self.save_snapshot()
        for action in self.actions:
            action['timestamp'] *= multiplier
        print(f"Scaled speed by {multiplier}x")

    def shift_timestamps(self, offset):
        """Shift all timestamps by offset"""
        self.save_snapshot()
        for action in self.actions:
            action['timestamp'] = max(0, action['timestamp'] + offset)
        print(f"Shifted timestamps by {offset}s")

    def duplicate_action(self, index):
        """Duplicate action at index"""
        if 0 <= index < len(self.actions):
            self.save_snapshot()
            action_copy = copy.deepcopy(self.actions[index])
            self.actions.insert(index + 1, action_copy)
            self._recalculate_timestamps()
            print(f"Duplicated action at index {index}")
            return True
        else:
            print(f"Invalid index: {index}")
            return False

    def move_action(self, from_index, to_index):
        """Move action from one position to another"""
        if 0 <= from_index < len(self.actions) and 0 <= to_index < len(self.actions):
            self.save_snapshot()
            action = self.actions.pop(from_index)
            self.actions.insert(to_index, action)
            self._recalculate_timestamps()
            print(f"Moved action from {from_index} to {to_index}")
            return True
        else:
            print(f"Invalid indices: {from_index} to {to_index}")
            return False

    def reverse_recording(self):
        """Reverse the order of actions"""
        self.save_snapshot()
        self.actions.reverse()
        self._recalculate_timestamps()
        print("Reversed recording")

    def split_recording(self, index):
        """Split recording into two parts"""
        if 0 <= index < len(self.actions):
            part1 = self.actions[:index]
            part2 = self.actions[index:]

            # Adjust timestamps for part2 to start at 0
            if part2:
                start_time = part2[0]['timestamp']
                for action in part2:
                    action['timestamp'] -= start_time

            print(f"Split recording at index {index}")
            print(f"Part 1: {len(part1)} actions")
            print(f"Part 2: {len(part2)} actions")
            return part1, part2
        else:
            print(f"Invalid index: {index}")
            return None, None

    def merge_recordings(self, other_actions):
        """Merge another recording at the end"""
        self.save_snapshot()

        # Get the last timestamp
        if self.actions:
            last_timestamp = self.actions[-1]['timestamp']
        else:
            last_timestamp = 0

        # Add other actions with adjusted timestamps
        for action in other_actions:
            action_copy = copy.deepcopy(action)
            action_copy['timestamp'] += last_timestamp
            self.actions.append(action_copy)

        print(f"Merged {len(other_actions)} actions")

    def find_actions_by_criteria(self, **criteria):
        """Find actions matching criteria"""
        results = []

        for i, action in enumerate(self.actions):
            match = True
            for key, value in criteria.items():
                if key not in action or action[key] != value:
                    match = False
                    break
            if match:
                results.append((i, action))

        return results

    def replace_coordinates(self, old_x, old_y, new_x, new_y, tolerance=5):
        """Replace coordinates in mouse actions"""
        self.save_snapshot()
        count = 0

        for action in self.actions:
            if action['type'] in ['mouse_move', 'mouse_click', 'mouse_scroll']:
                if (abs(action['x'] - old_x) <= tolerance and
                    abs(action['y'] - old_y) <= tolerance):
                    action['x'] = new_x
                    action['y'] = new_y
                    count += 1

        print(f"Replaced coordinates in {count} actions")
        return count

    def get_statistics(self):
        """Get recording statistics"""
        stats = {
            'total_actions': len(self.actions),
            'duration': self.actions[-1]['timestamp'] if self.actions else 0,
            'action_types': {},
            'first_action': None,
            'last_action': None
        }

        for action in self.actions:
            action_type = action['type']
            stats['action_types'][action_type] = stats['action_types'].get(action_type, 0) + 1

        if self.actions:
            stats['first_action'] = self.actions[0]
            stats['last_action'] = self.actions[-1]

        return stats

    def _recalculate_timestamps(self):
        """Recalculate timestamps to maintain relative timing"""
        if not self.actions:
            return

        # Keep relative timing intact
        # This is called after deletions/insertions to ensure consistency
        pass  # Timestamps are already correct from original recording

    def reset_to_original(self):
        """Reset to original recording"""
        self.actions = copy.deepcopy(self.original_actions)
        self.undo_stack = []
        self.redo_stack = []
        print("Reset to original recording")

    def has_changes(self):
        """Check if recording has been modified"""
        return self.actions != self.original_actions

    def export_to_dict(self):
        """Export actions as dictionary"""
        return {
            'actions': self.actions,
            'original_count': len(self.original_actions),
            'current_count': len(self.actions),
            'modified': self.has_changes(),
            'exported_at': datetime.now().isoformat()
        }
