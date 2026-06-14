# RGB Ambient Display Sync (OpenRGB)

This Python script syncs your RGB keyboard color with your screen in real-time

It captures the active display area, calculates a smart average color,
applies gamma correction for deep saturation, and smoothly transitions
your keyboard lighting using OpenRGB SDK.

---

## Requirements

- Python 3.9+
- OpenRGB installed
- Keyboard supported by OpenRGB
- OpenRGB SDK Server enabled

---

## Install Dependencies

```
pip install openrgb-python mss numpy
```

---

## Setup Instructions

1. Install OpenRGB  
2. Open OpenRGB  
3. Make sure your keyboard appears in Devices  
4. Go to SDK Server → Start Server  
5. Run:

```
python rgb.py
```

---

## Features

- Smart screen color detection
- Gamma correction for accurate LED color output
- Smooth transitions (no flicker)
- Hardware safety check (prevents spamming commands)
- ~60 FPS update loop

---

## Stop

Press Ctrl + C to stop syncing.

---

## Notes

- Script assumes keyboard is the first detected device.
- Modify monitor capture region if using different resolution.
- Make sure OpenRGB SDK server is running before executing

---

## License

Private project. Modify and use as needed.
