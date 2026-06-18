#!/usr/bin/env python3
"""Create test images for VisionFlow demo."""

import cv2
import numpy as np
import os

os.makedirs('sample_images', exist_ok=True)

# Create test images with different aspect ratios
print("[*] Creating test images...")

# Image 1: 640x480 (4:3 ratio)
img1 = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.rectangle(img1, (50, 50), (590, 430), (100, 150, 200), -1)
cv2.putText(img1, 'Test Image 1', (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
cv2.imwrite('sample_images/test_image1.jpg', img1)
print("  ✓ Created: sample_images/test_image1.jpg (640x480, 4:3)")

# Image 2: 800x600 (4:3 ratio)
img2 = np.zeros((600, 800, 3), dtype=np.uint8)
cv2.rectangle(img2, (50, 50), (750, 550), (200, 100, 150), -1)
cv2.putText(img2, 'Test Image 2', (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
cv2.imwrite('sample_images/test_image2.jpg', img2)
print("  ✓ Created: sample_images/test_image2.jpg (800x600, 4:3)")

print("\n[SUCCESS] All test images created!")
