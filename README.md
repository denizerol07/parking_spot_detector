# 🚗 Parking Spot Detection System

> Real-time parking spot detection using OpenCV, Python, and smartphone camera via DroidCam

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Controls](#controls)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements an automated parking spot detection system using computer vision techniques. The system uses your smartphone camera (via DroidCam) to monitor parking spots marked with yellow frames and determines whether each spot is empty or occupied based on brightness analysis.

**Key Concept:** 
- Empty parking spots appear **bright** (high average pixel value)
- Occupied spots appear **dark** due to vehicle shadow (low average pixel value)

## ✨ Features

- 🟡 **Automatic Yellow Frame Detection** - Identifies parking spots by detecting yellow rectangular frames
- 🟢 **Empty Spot Detection** - Marks empty parking spots in green
- 🔴 **Occupied Spot Detection** - Marks occupied spots in red
- 📱 **Smartphone Integration** - Works with DroidCam for wireless camera access
- 🎚️ **Real-time Threshold Adjustment** - Adjust sensitivity on-the-fly with keyboard controls
- 🔍 **Debug Mode** - View grayscale processing for fine-tuning
- 📊 **Live Statistics** - Real-time count of empty vs occupied spots
- 🌐 **Remote Detection** - Works from distance, no need to be close to parking area

## 🎬 Demo

```
╔═══════════════════════════════════════════════════════════╗
║                    PARKING STATUS                         ║
║                                                           ║
║  Empty:  4                                               ║
║  Occupied: 2                                             ║
║                                                           ║
║  [#1] GREEN  - EMPTY                                     ║
║  [#2] RED    - OCCUPIED (car present)                    ║
║  [#3] GREEN  - EMPTY                                     ║
║  [#4] RED    - OCCUPIED (car present)                    ║
║  [#5] GREEN  - EMPTY                                     ║
║  [#6] GREEN  - EMPTY                                     ║
╚═══════════════════════════════════════════════════════════╝
```

## 🔬 How It Works

### Algorithm Overview

```
┌─────────────────┐
│  Camera Feed    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Convert to HSV │  ← Detect yellow color range
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Find Yellow     │  ← Identify parking spot frames
│ Contours        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ For Each Spot:  │
│ - Extract ROI   │  ← Region of Interest
│ - Grayscale     │
│ - Avg Brightness│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Compare with   │  ← Decision making
│  Threshold      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Brightness > T? │
│ YES → EMPTY 🟢  │
│ NO  → OCCUPIED🔴│
└─────────────────┘
```

### Technical Details

1. **Color Detection (HSV)**
   - Converts BGR image to HSV color space
   - Applies color range filter for yellow (Hue: 15-35)
   - Uses morphological operations to clean noise

2. **Contour Detection**
   - Finds external contours of yellow regions
   - Filters by minimum area (2000 pixels)
   - Validates aspect ratio (0.2 - 5.0)

3. **Brightness Analysis**
   - Creates binary mask for each parking spot
   - Extracts pixel values within masked region
   - Calculates mean grayscale value
   - Compares with threshold (default: 120)

4. **Status Determination**
   ```python
   if average_brightness > THRESHOLD:
       status = "EMPTY"   # High brightness = no vehicle
   else:
       status = "OCCUPIED" # Low brightness = vehicle present
   ```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Webcam or smartphone with DroidCam app
- Windows, macOS, or Linux

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/parking-spot-detector.git
cd parking-spot-detector
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
opencv-python>=4.8.0
numpy>=1.24.0
```

### Step 3: Setup DroidCam (for smartphone camera)

1. **Download DroidCam:**
   - PC Client: [https://www.dev47apps.com/](https://www.dev47apps.com/)
   - Mobile App: Available on Google Play Store / Apple App Store

2. **Connect:**
   - Install DroidCam app on your phone
   - Connect phone and PC to the same WiFi network
   - Open DroidCam Client on PC
   - Enter phone's IP address
   - Click "Start"

3. **Find Camera ID:**
   ```bash
   python kamera_bul.py
   ```
   Note the camera ID that works (usually 0 or 1)

## 🚀 Usage

### Basic Usage

```bash
python park_PARLAKLIM.py
```

### Quick Start Guide

1. **Mark Your Parking Spots**
   - Place yellow frames/tape around parking spots
   - Ensure frames are clearly visible

2. **Position Camera**
   - Point smartphone camera at parking area
   - Can be positioned at a distance
   - Ensure good lighting

3. **Run the Program**
   ```bash
   python park_PARLAKLIM.py
   ```

4. **Adjust Threshold** (if needed)
   - Press `+` to increase threshold (if empty spots show as occupied)
   - Press `-` to decrease threshold (if occupied spots show as empty)

5. **Monitor**
   - Green frames = Empty spots
   - Red frames = Occupied spots
   - Live count displayed in top-left panel

## ⚙️ Configuration

Edit these parameters in `park_PARLAKLIM.py`:

```python
# Camera Settings
KAMERA = 1                    # Camera ID (0, 1, 2, ...)

# Yellow Color Detection (HSV)
SARI_ALT = np.array([15, 80, 80])     # Lower bound
SARI_UST = np.array([35, 255, 255])   # Upper bound

# Parking Spot Detection
MIN_ALAN = 2000              # Minimum area in pixels

# Brightness Threshold
PARLAKLIM_ESIK = 120         # 0-255 (default: 120)
                             # Higher = More strict for "empty"
                             # Lower = More lenient for "empty"
```

### Tuning Tips

| Problem | Solution |
|---------|----------|
| Yellow frames not detected | Widen `SARI_ALT` and `SARI_UST` range |
| Small frames ignored | Decrease `MIN_ALAN` |
| Empty spots show as occupied | Increase `PARLAKLIM_ESIK` (+5 at a time) |
| Occupied spots show as empty | Decrease `PARLAKLIM_ESIK` (-5 at a time) |

## 🎮 Controls

| Key | Action |
|-----|--------|
| `q` | Quit program |
| `d` | Toggle debug mode (show grayscale) |
| `+` or `=` | Increase threshold by 5 |
| `-` or `_` | Decrease threshold by 5 |

## 🐛 Troubleshooting

### Camera Not Found

```
❌ Kamera açılamadı!
```

**Solutions:**
- Run `kamera_bul.py` to find correct camera ID
- Ensure DroidCam Client is running
- Check if phone and PC are on same network
- Try different camera IDs (0, 1, 2)

### Yellow Frames Not Detected

**Solutions:**
- Improve lighting conditions
- Adjust `SARI_ALT` and `SARI_UST` values
- Ensure yellow color is pure (not orange/lime)
- Press `d` to see debug mode

### Incorrect Detection

**Empty shows as Occupied:**
- Press `+` to increase threshold
- Improve lighting on parking area
- Check if shadow is covering spot

**Occupied shows as Empty:**
- Press `-` to decrease threshold
- Ensure vehicle creates enough shadow
- Try darker colored toy car for testing

### Performance Issues

**Laggy Video:**
- Reduce DroidCam quality settings
- Ensure strong WiFi connection
- Close other applications

## 📊 Expected Brightness Values

Typical brightness ranges for reference:

```
Empty parking (white floor):    180-220
Empty parking (gray floor):     140-180
Toy car (dark colored):         80-120
Real car (creates shadow):      70-110

Recommended threshold: 120-140
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution

- [ ] Add support for different colored frames
- [ ] Implement machine learning for better detection
- [ ] Add web interface for remote monitoring
- [ ] Support for multiple camera angles
- [ ] Historical data logging
- [ ] Mobile app for viewing status

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**[Your Name]**

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- OpenCV community for excellent computer vision library
- DroidCam developers for smartphone camera integration
- All contributors and testers

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Open an [Issue](https://github.com/YOUR_USERNAME/parking-spot-detector/issues)
3. Contact: your-email@example.com

---

⭐ **Star this repository if you found it helpful!**

Made with ❤️ using OpenCV and Python
