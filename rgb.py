import mss
import time
import numpy as np
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor

# --- INITIALIZATION ---
print("Connecting to OpenRGB...")
client = OpenRGBClient()
keyboard = client.devices[0]

# --- CONFIGURATION ---
SMOOTHING_FACTOR = 0.5  # 50% movement per frame. Smooth but fast.
UPDATE_RATE = 0.015     # ~60 FPS update loop
GAMMA = 2.2             # Gamma curve to make LEDs look deep and saturated

# State variables for smoothing
current_r, current_g, current_b = 0.0, 0.0, 0.0

# State variables for HARDWARE SAFETY (Spam Filter)
last_r, last_g, last_b = -1, -1, -1

def apply_gamma(color_value):
    """Curves the brightness to match actual LED light output."""
    return ((color_value / 255.0) ** GAMMA) * 255.0

def get_target_color():
    """Captures the active screen area and calculates a smart average."""
    with mss.mss() as sct:
        # Capture the center 80% to ignore letterboxing and taskbars
        monitor = {"top": 108, "left": 192, "width": 1536, "height": 864}
        img = sct.grab(monitor)
        
        # Convert to numpy and drop the Alpha channel (BGRA -> BGR)
        img_np = np.array(img)[:, :, :3]
        
        # Find the brightness of every pixel and ignore the muddy/dark ones
        pixel_brightness = np.max(img_np, axis=2)
        valid_pixels = img_np[pixel_brightness > 15] 
        
        # If the screen is genuinely pitch black, turn off LEDs naturally
        if len(valid_pixels) == 0:
            return 0.0, 0.0, 0.0 
            
        # Average ONLY the active, colorful pixels
        b, g, r = np.mean(valid_pixels, axis=0)
        
        # Apply Gamma Correction for pure, vibrant colors
        r = apply_gamma(r)
        g = apply_gamma(g)
        b = apply_gamma(b)
        
        return r, g, b

# --- MAIN LOOP ---
print("Safe & Premium Ambient Sync started! Press Ctrl+C to stop.")
try:
    while True:
        # 1. Get the new target color from the screen
        target_r, target_g, target_b = get_target_color()
        
        # 2. Smoothly calculate the transition
        current_r = current_r + (target_r - current_r) * SMOOTHING_FACTOR
        current_g = current_g + (target_g - current_g) * SMOOTHING_FACTOR
        current_b = current_b + (target_b - current_b) * SMOOTHING_FACTOR
        
        # Round the math into final integers for the keyboard
        final_r, final_g, final_b = int(current_r), int(current_g), int(current_b)
        
        # 3. HARDWARE SAFETY CHECK
        # Only send the command if the color has actually changed
        if final_r != last_r or final_g != last_g or final_b != last_b:
            final_color = RGBColor(final_r, final_g, final_b)
            keyboard.set_color(final_color)
            
            # Update the last known color memory
            last_r, last_g, last_b = final_r, final_g, final_b
        
        # 4. Rest to maintain steady FPS
        time.sleep(UPDATE_RATE)

except KeyboardInterrupt:
    print("\nSyncing stopped gracefully.")
    