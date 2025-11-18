"""
Conditional Logic Module
Provides conditional execution and smart automation
"""

import time
from image_recognition import ImageRecognition
from player import ActionPlayer


class Condition:
    """Base condition class"""

    def __init__(self, name=""):
        self.name = name

    def evaluate(self):
        """Evaluate condition - returns True/False"""
        raise NotImplementedError("Subclass must implement evaluate()")


class ImageExistsCondition(Condition):
    """Condition: Check if image exists on screen"""

    def __init__(self, image_path, confidence=0.8, name=""):
        super().__init__(name or f"Image exists: {image_path}")
        self.image_path = image_path
        self.confidence = confidence
        self.image_rec = ImageRecognition()

    def evaluate(self):
        location = self.image_rec.find_image_on_screen(self.image_path, self.confidence)
        return location is not None


class PixelColorCondition(Condition):
    """Condition: Check if pixel has specific color"""

    def __init__(self, x, y, expected_color, tolerance=10, name=""):
        super().__init__(name or f"Pixel ({x},{y}) color check")
        self.x = x
        self.y = y
        self.expected_color = expected_color
        self.tolerance = tolerance
        self.image_rec = ImageRecognition()

    def evaluate(self):
        return self.image_rec.match_pixel_color(
            self.x, self.y, self.expected_color, self.tolerance
        )


class TimeCondition(Condition):
    """Condition: Check current time"""

    def __init__(self, start_time=None, end_time=None, name=""):
        super().__init__(name or "Time check")
        self.start_time = start_time  # Format: "HH:MM"
        self.end_time = end_time

    def evaluate(self):
        from datetime import datetime

        now = datetime.now().strftime("%H:%M")

        if self.start_time and self.end_time:
            return self.start_time <= now <= self.end_time
        elif self.start_time:
            return now >= self.start_time
        elif self.end_time:
            return now <= self.end_time

        return True


class CounterCondition(Condition):
    """Condition: Check counter value"""

    def __init__(self, counter_name, operator, value, name=""):
        super().__init__(name or f"Counter {counter_name} {operator} {value}")
        self.counter_name = counter_name
        self.operator = operator  # '==', '!=', '<', '>', '<=', '>='
        self.value = value
        self.counters = {}

    def set_counter(self, counter_name, value):
        """Set counter value"""
        self.counters[counter_name] = value

    def increment_counter(self, counter_name):
        """Increment counter"""
        if counter_name not in self.counters:
            self.counters[counter_name] = 0
        self.counters[counter_name] += 1

    def evaluate(self):
        counter_value = self.counters.get(self.counter_name, 0)

        if self.operator == '==':
            return counter_value == self.value
        elif self.operator == '!=':
            return counter_value != self.value
        elif self.operator == '<':
            return counter_value < self.value
        elif self.operator == '>':
            return counter_value > self.value
        elif self.operator == '<=':
            return counter_value <= self.value
        elif self.operator == '>=':
            return counter_value >= self.value

        return False


class ConditionalAction:
    """Action that executes based on conditions"""

    def __init__(self, name=""):
        self.name = name
        self.conditions = []
        self.actions = []
        self.else_actions = []
        self.logic = "AND"  # "AND" or "OR"

    def add_condition(self, condition):
        """Add a condition"""
        self.conditions.append(condition)

    def add_action(self, action):
        """Add action to execute if conditions pass"""
        self.actions.append(action)

    def add_else_action(self, action):
        """Add action to execute if conditions fail"""
        self.else_actions.append(action)

    def set_logic(self, logic):
        """Set condition logic (AND/OR)"""
        self.logic = logic.upper()

    def evaluate_conditions(self):
        """Evaluate all conditions based on logic"""
        if not self.conditions:
            return True

        results = [cond.evaluate() for cond in self.conditions]

        if self.logic == "AND":
            return all(results)
        elif self.logic == "OR":
            return any(results)

        return False

    def execute(self):
        """Execute conditional action"""
        if self.evaluate_conditions():
            print(f"[{self.name}] Conditions passed - executing actions")
            for action in self.actions:
                action()
        else:
            print(f"[{self.name}] Conditions failed - executing else actions")
            for action in self.else_actions:
                action()


class SmartPlayer:
    """Enhanced player with conditional logic"""

    def __init__(self, player, image_rec):
        self.player = player
        self.image_rec = image_rec
        self.conditions = []

    def wait_for_image_then_click(self, image_path, timeout=30, confidence=0.8):
        """Wait for image to appear, then click it"""
        print(f"Waiting for image: {image_path}")
        location = self.image_rec.wait_for_image(image_path, timeout, confidence=confidence)

        if location:
            self.image_rec.click_image(image_path, confidence)
            return True
        else:
            print(f"Image did not appear - skipping click")
            return False

    def loop_until_image_appears(self, check_image, actions, max_iterations=100):
        """
        Loop actions until specific image appears

        Args:
            check_image: Image to check for
            actions: List of actions to perform
            max_iterations: Maximum loop iterations
        """
        iteration = 0

        while iteration < max_iterations:
            # Check if target image exists
            if self.image_rec.find_image_on_screen(check_image):
                print(f"Target image found after {iteration} iterations")
                break

            # Perform actions
            self.player.load_actions(actions)
            self.player.play()

            iteration += 1
            time.sleep(1)  # Small delay between iterations

        if iteration >= max_iterations:
            print(f"Max iterations reached without finding image")

    def conditional_click(self, if_image, then_click_image, else_click_image=None):
        """
        If image exists, click one thing, else click another

        Args:
            if_image: Image to check for
            then_click_image: Image to click if condition is true
            else_click_image: Image to click if condition is false (optional)
        """
        if self.image_rec.find_image_on_screen(if_image):
            print(f"Condition true - clicking {then_click_image}")
            self.image_rec.click_image(then_click_image)
        elif else_click_image:
            print(f"Condition false - clicking {else_click_image}")
            self.image_rec.click_image(else_click_image)

    def repeat_until_success(self, action_func, check_func, max_attempts=10, delay=2):
        """
        Repeat action until check function returns True

        Args:
            action_func: Function to execute
            check_func: Function that returns True when successful
            max_attempts: Maximum attempts
            delay: Delay between attempts in seconds
        """
        for attempt in range(1, max_attempts + 1):
            print(f"Attempt {attempt}/{max_attempts}")

            action_func()
            time.sleep(delay)

            if check_func():
                print(f"Success after {attempt} attempts!")
                return True

        print(f"Failed after {max_attempts} attempts")
        return False
