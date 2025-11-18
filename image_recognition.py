"""
Image Recognition Module
Provides image-based automation capabilities
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image
import os


class ImageRecognition:
    def __init__(self):
        self.confidence = 0.8
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort

    def set_confidence(self, confidence):
        """Set matching confidence threshold (0.0 to 1.0)"""
        self.confidence = max(0.0, min(1.0, confidence))
        print(f"Confidence set to: {self.confidence}")

    def capture_screenshot(self, filename=None, region=None):
        """
        Capture screenshot

        Args:
            filename: Path to save screenshot (optional)
            region: Tuple (x, y, width, height) to capture specific region

        Returns:
            PIL Image object
        """
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        if filename:
            screenshot.save(filename)
            print(f"Screenshot saved to: {filename}")

        return screenshot

    def find_image_on_screen(self, image_path, confidence=None):
        """
        Find image on screen

        Args:
            image_path: Path to image file to find
            confidence: Confidence threshold (uses default if None)

        Returns:
            Tuple (x, y, width, height) or None if not found
        """
        if confidence is None:
            confidence = self.confidence

        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            return None

        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                print(f"Image found at: {location}")
                return location
            else:
                print(f"Image not found on screen.")
                return None
        except Exception as e:
            print(f"Error finding image: {e}")
            return None

    def find_all_images_on_screen(self, image_path, confidence=None):
        """
        Find all instances of image on screen

        Args:
            image_path: Path to image file to find
            confidence: Confidence threshold (uses default if None)

        Returns:
            List of tuples [(x, y, width, height), ...]
        """
        if confidence is None:
            confidence = self.confidence

        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            return []

        try:
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            print(f"Found {len(locations)} instances of image.")
            return locations
        except Exception as e:
            print(f"Error finding images: {e}")
            return []

    def click_image(self, image_path, confidence=None, button='left', clicks=1):
        """
        Find and click on image

        Args:
            image_path: Path to image file to click
            confidence: Confidence threshold (uses default if None)
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks

        Returns:
            True if clicked, False otherwise
        """
        location = self.find_image_on_screen(image_path, confidence)

        if location:
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2

            pyautogui.click(center_x, center_y, clicks=clicks, button=button)
            print(f"Clicked at ({center_x}, {center_y})")
            return True
        else:
            print(f"Could not click - image not found.")
            return False

    def wait_for_image(self, image_path, timeout=10, check_interval=0.5, confidence=None):
        """
        Wait for image to appear on screen

        Args:
            image_path: Path to image file to wait for
            timeout: Maximum wait time in seconds
            check_interval: How often to check in seconds
            confidence: Confidence threshold (uses default if None)

        Returns:
            Tuple (x, y, width, height) or None if timeout
        """
        import time

        print(f"Waiting for image (timeout: {timeout}s)...")
        elapsed = 0

        while elapsed < timeout:
            location = self.find_image_on_screen(image_path, confidence)
            if location:
                print(f"Image appeared after {elapsed:.1f}s")
                return location

            time.sleep(check_interval)
            elapsed += check_interval

        print(f"Timeout: Image did not appear within {timeout}s")
        return None

    def get_pixel_color(self, x, y):
        """
        Get color of pixel at coordinates

        Args:
            x, y: Screen coordinates

        Returns:
            Tuple (r, g, b)
        """
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        return color

    def match_pixel_color(self, x, y, expected_color, tolerance=10):
        """
        Check if pixel color matches expected color

        Args:
            x, y: Screen coordinates
            expected_color: Tuple (r, g, b)
            tolerance: Allowed difference per channel

        Returns:
            True if match, False otherwise
        """
        actual_color = self.get_pixel_color(x, y)

        match = all(
            abs(actual_color[i] - expected_color[i]) <= tolerance
            for i in range(3)
        )

        return match

    def save_region_as_template(self, x, y, width, height, filename):
        """
        Capture screen region and save as template image

        Args:
            x, y: Top-left coordinates
            width, height: Region size
            filename: Path to save template

        Returns:
            True if successful
        """
        try:
            region = (x, y, width, height)
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(filename)
            print(f"Template saved to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

    def get_screen_size(self):
        """Get screen resolution"""
        size = pyautogui.size()
        return size.width, size.height

    def locate_center(self, location):
        """
        Get center coordinates of location

        Args:
            location: Tuple (x, y, width, height)

        Returns:
            Tuple (center_x, center_y)
        """
        if location:
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2
            return (center_x, center_y)
        return None
