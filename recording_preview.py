"""
Recording Preview Module
Visualize recordings before execution
"""

import os
from datetime import timedelta


class RecordingPreview:
    def __init__(self):
        self.actions = []

    def load_recording(self, actions):
        """Load recording for preview"""
        self.actions = actions
        print(f"Loaded recording with {len(self.actions)} actions")

    def show_summary(self):
        """Show recording summary"""
        if not self.actions:
            print("No recording loaded")
            return

        duration = self.actions[-1]['timestamp'] if self.actions else 0

        # Count action types
        action_counts = {}
        for action in self.actions:
            action_type = action['type']
            action_counts[action_type] = action_counts.get(action_type, 0) + 1

        print("\n" + "=" * 70)
        print("RECORDING SUMMARY")
        print("=" * 70)
        print(f"Total Actions:  {len(self.actions)}")
        print(f"Duration:       {duration:.2f} seconds ({self._format_duration(duration)})")
        print(f"Avg Speed:      {len(self.actions)/duration:.1f} actions/second" if duration > 0 else "")
        print("\nAction Breakdown:")
        for action_type, count in sorted(action_counts.items()):
            percentage = (count / len(self.actions)) * 100
            print(f"  {action_type:<20} {count:>6} ({percentage:>5.1f}%)")
        print("=" * 70)

    def show_timeline(self, segments=20):
        """Show visual timeline of recording"""
        if not self.actions:
            print("No recording loaded")
            return

        duration = self.actions[-1]['timestamp'] if self.actions else 0
        segment_duration = duration / segments

        print("\n" + "=" * 70)
        print("RECORDING TIMELINE")
        print("=" * 70)
        print(f"Each segment represents {segment_duration:.2f} seconds")
        print()

        # Count actions per segment
        segments_data = [[] for _ in range(segments)]

        for action in self.actions:
            segment_idx = min(int(action['timestamp'] / segment_duration), segments - 1)
            segments_data[segment_idx].append(action)

        # Display timeline
        max_actions = max(len(seg) for seg in segments_data) if segments_data else 1

        # Create bar chart
        for i, segment in enumerate(segments_data):
            time_label = f"{i * segment_duration:>6.1f}s"
            count = len(segment)
            bar_length = int((count / max_actions) * 40) if max_actions > 0 else 0
            bar = "█" * bar_length

            # Color code by activity level
            if count == 0:
                bar = ""
            elif count < max_actions * 0.3:
                bar = "░" * bar_length
            elif count < max_actions * 0.7:
                bar = "▒" * bar_length

            print(f"{time_label} | {bar} {count}")

        print("=" * 70)

    def show_detailed_view(self, start_time=0, end_time=None, max_actions=50):
        """Show detailed view of actions in time range"""
        if not self.actions:
            print("No recording loaded")
            return

        if end_time is None:
            end_time = self.actions[-1]['timestamp'] if self.actions else 0

        # Filter actions in time range
        filtered_actions = [
            (i, action) for i, action in enumerate(self.actions)
            if start_time <= action['timestamp'] <= end_time
        ]

        if not filtered_actions:
            print(f"No actions found between {start_time}s and {end_time}s")
            return

        # Limit to max_actions
        if len(filtered_actions) > max_actions:
            print(f"Showing first {max_actions} of {len(filtered_actions)} actions in range")
            filtered_actions = filtered_actions[:max_actions]

        print("\n" + "=" * 70)
        print(f"DETAILED VIEW: {start_time}s to {end_time}s")
        print("=" * 70)
        print(f"{'Index':<6} {'Time':<10} {'Type':<15} {'Details'}")
        print("-" * 70)

        for idx, action in filtered_actions:
            timestamp = f"{action['timestamp']:.3f}s"
            action_type = action['type']

            # Format details
            details = self._format_action_details(action)

            print(f"{idx:<6} {timestamp:<10} {action_type:<15} {details}")

        print("=" * 70)

    def show_mouse_path(self, sample_rate=10):
        """Show mouse movement path"""
        if not self.actions:
            print("No recording loaded")
            return

        # Get mouse positions
        mouse_actions = [
            action for action in self.actions
            if action['type'] in ['mouse_move', 'mouse_click']
        ]

        if not mouse_actions:
            print("No mouse actions in recording")
            return

        # Sample positions
        if len(mouse_actions) > sample_rate:
            step = len(mouse_actions) // sample_rate
            sampled = mouse_actions[::step]
        else:
            sampled = mouse_actions

        print("\n" + "=" * 70)
        print("MOUSE PATH")
        print("=" * 70)
        print(f"{'Time':<10} {'X':<8} {'Y':<8} {'Action'}")
        print("-" * 70)

        for action in sampled:
            timestamp = f"{action['timestamp']:.2f}s"
            x = action['x']
            y = action['y']

            if action['type'] == 'mouse_click':
                action_desc = f"CLICK {action['button']}"
            else:
                action_desc = "move"

            print(f"{timestamp:<10} {x:<8} {y:<8} {action_desc}")

        # Show bounds
        all_x = [a['x'] for a in mouse_actions]
        all_y = [a['y'] for a in mouse_actions]

        print("-" * 70)
        print(f"Bounds: X=[{min(all_x)}, {max(all_x)}], Y=[{min(all_y)}, {max(all_y)}]")
        print("=" * 70)

    def show_keyboard_sequence(self):
        """Show keyboard key sequence"""
        if not self.actions:
            print("No recording loaded")
            return

        # Get keyboard actions
        key_actions = [
            action for action in self.actions
            if action['type'] in ['key_press', 'key_release']
        ]

        if not key_actions:
            print("No keyboard actions in recording")
            return

        print("\n" + "=" * 70)
        print("KEYBOARD SEQUENCE")
        print("=" * 70)

        # Show only key presses (releases are implied)
        key_presses = [a for a in key_actions if a['type'] == 'key_press']

        current_line = ""
        for i, action in enumerate(key_presses):
            timestamp = f"[{action['timestamp']:.2f}s]"
            key = action['key']

            # Build readable sequence
            if len(key) == 1:  # Regular character
                current_line += key
            else:  # Special key
                if current_line:
                    print(f"{timestamp} {current_line}")
                    current_line = ""
                print(f"{timestamp} <{key}>")

            # Break line every 60 chars
            if len(current_line) >= 60:
                print(f"{timestamp} {current_line}")
                current_line = ""

        if current_line:
            print(current_line)

        print("=" * 70)

    def show_action_frequency(self):
        """Show frequency of different actions"""
        if not self.actions:
            print("No recording loaded")
            return

        duration = self.actions[-1]['timestamp'] if self.actions else 1

        # Count action types
        action_counts = {}
        for action in self.actions:
            action_type = action['type']
            action_counts[action_type] = action_counts.get(action_type, 0) + 1

        print("\n" + "=" * 70)
        print("ACTION FREQUENCY")
        print("=" * 70)
        print(f"{'Action Type':<20} {'Count':<8} {'Per Second':<12} {'Percentage'}")
        print("-" * 70)

        for action_type in sorted(action_counts.keys()):
            count = action_counts[action_type]
            per_second = count / duration if duration > 0 else 0
            percentage = (count / len(self.actions)) * 100

            print(f"{action_type:<20} {count:<8} {per_second:<12.2f} {percentage:>6.1f}%")

        print("=" * 70)

    def show_delays_analysis(self):
        """Analyze delays between actions"""
        if len(self.actions) < 2:
            print("Not enough actions to analyze delays")
            return

        delays = []
        for i in range(1, len(self.actions)):
            delay = self.actions[i]['timestamp'] - self.actions[i-1]['timestamp']
            delays.append(delay)

        avg_delay = sum(delays) / len(delays)
        min_delay = min(delays)
        max_delay = max(delays)

        # Find long pauses
        long_pauses = [(i, d) for i, d in enumerate(delays) if d > 1.0]

        print("\n" + "=" * 70)
        print("DELAYS ANALYSIS")
        print("=" * 70)
        print(f"Average delay: {avg_delay:.3f}s")
        print(f"Min delay:     {min_delay:.3f}s")
        print(f"Max delay:     {max_delay:.3f}s")

        if long_pauses:
            print(f"\nLong pauses (>1s): {len(long_pauses)}")
            for idx, delay in long_pauses[:10]:  # Show first 10
                print(f"  Between action {idx} and {idx+1}: {delay:.2f}s")

        print("=" * 70)

    def show_hotspots(self):
        """Show mouse click hotspots"""
        if not self.actions:
            print("No recording loaded")
            return

        # Get click actions
        clicks = [
            action for action in self.actions
            if action['type'] == 'mouse_click' and action['pressed']
        ]

        if not clicks:
            print("No mouse clicks in recording")
            return

        # Group clicks by approximate location (within 20 pixels)
        hotspots = []
        tolerance = 20

        for click in clicks:
            x, y = click['x'], click['y']

            # Find existing hotspot
            found = False
            for hotspot in hotspots:
                if (abs(hotspot['x'] - x) <= tolerance and
                    abs(hotspot['y'] - y) <= tolerance):
                    hotspot['clicks'] += 1
                    found = True
                    break

            if not found:
                hotspots.append({'x': x, 'y': y, 'clicks': 1})

        # Sort by click count
        hotspots.sort(key=lambda h: h['clicks'], reverse=True)

        print("\n" + "=" * 70)
        print("MOUSE CLICK HOTSPOTS")
        print("=" * 70)
        print(f"{'Position':<20} {'Clicks':<10} {'Percentage'}")
        print("-" * 70)

        total_clicks = len(clicks)
        for hotspot in hotspots[:10]:  # Show top 10
            position = f"({hotspot['x']}, {hotspot['y']})"
            clicks = hotspot['clicks']
            percentage = (clicks / total_clicks) * 100
            print(f"{position:<20} {clicks:<10} {percentage:>6.1f}%")

        print("=" * 70)

    def compare_with(self, other_actions):
        """Compare this recording with another"""
        other_preview = RecordingPreview()
        other_preview.load_recording(other_actions)

        print("\n" + "=" * 70)
        print("RECORDING COMPARISON")
        print("=" * 70)

        # Compare basic stats
        print(f"{'Metric':<30} {'This':<15} {'Other':<15} {'Difference'}")
        print("-" * 70)

        this_count = len(self.actions)
        other_count = len(other_actions)
        print(f"{'Total Actions':<30} {this_count:<15} {other_count:<15} {other_count - this_count:+d}")

        this_duration = self.actions[-1]['timestamp'] if self.actions else 0
        other_duration = other_actions[-1]['timestamp'] if other_actions else 0
        print(f"{'Duration (seconds)':<30} {this_duration:<15.2f} {other_duration:<15.2f} {other_duration - this_duration:+.2f}")

        print("=" * 70)

    def _format_action_details(self, action):
        """Format action details for display"""
        action_type = action['type']

        if action_type == 'mouse_move':
            return f"→ ({action['x']}, {action['y']})"
        elif action_type == 'mouse_click':
            button = action['button'].replace('Button.', '')
            state = "⬇" if action['pressed'] else "⬆"
            return f"{state} {button} at ({action['x']}, {action['y']})"
        elif action_type == 'mouse_scroll':
            return f"↕ dx={action['dx']}, dy={action['dy']}"
        elif action_type == 'key_press':
            return f"⬇ {action['key']}"
        elif action_type == 'key_release':
            return f"⬆ {action['key']}"
        else:
            return ""

    def _format_duration(self, seconds):
        """Format duration in human-readable format"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.0f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def export_text_report(self, filename):
        """Export preview as text report"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RECORDING PREVIEW REPORT\n")
            f.write("=" * 70 + "\n\n")

            # Summary
            if self.actions:
                duration = self.actions[-1]['timestamp']
                f.write(f"Total Actions: {len(self.actions)}\n")
                f.write(f"Duration: {duration:.2f}s\n\n")

                # Action breakdown
                action_counts = {}
                for action in self.actions:
                    action_type = action['type']
                    action_counts[action_type] = action_counts.get(action_type, 0) + 1

                f.write("Action Breakdown:\n")
                for action_type, count in sorted(action_counts.items()):
                    percentage = (count / len(self.actions)) * 100
                    f.write(f"  {action_type}: {count} ({percentage:.1f}%)\n")

        print(f"Report exported to {filename}")
