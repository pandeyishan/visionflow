# VisionFlow: Complete Implementation Guide

## ✅ Current Status: FULLY FUNCTIONAL

VisionFlow is now a **complete, production-ready DSL** for computer vision preprocessing. Here's what works:

### What You Can Do Right Now

#### 1. **Aspect Ratio Management**
- Adjust video/image dimensions to match target aspect ratios
- Three modes: **fit** (scale + pad), **pad** (letterbox), **crop**
- Supports all standard ratios: 16:9, 4:3, 1:1, 21:9, etc.

```
ASPECT_RATIO
    target: 16:9
    mode: fit
```

#### 2. **Frame Rate Conforming**
- Conform video frame rates to target fps
- Uses frame duplication for upsampling
- Frame dropping for downsampling

```
FRAME_RATE
    target: 30fps
```

#### 3. **Lens Distortion Correction**
- Removes optical distortion from camera footage
- Uses default camera calibration matrix
- Can be tuned per camera

```
LENS
    correct_distortion: true
```

---

## Getting Started

### Prerequisites

```bash
pip install opencv-python numpy
```

### Test Your Setup

```bash
python test_setup.py
```

This will verify:
- ✓ OpenCV installation
- ✓ Lexer working
- ✓ Parser working
- ✓ Interpreter ready

### Create Your First Pipeline

1. **Create a `.vf` file** (e.g., `my_pipeline.vf`):

```
PIPELINE video_preprocessing
    SOURCE "videos/*.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: fit
    FRAME_RATE
        target: 30fps
    LENS
        correct_distortion: true
END
```

2. **Create the source directory** with your videos:

```bash
mkdir videos
# Copy your .mp4 files to videos/
```

3. **Run the pipeline**:

```bash
python main.py my_pipeline.vf
```

4. **Get your results**:

All processed files appear in `processed_output/`

---

## Complete Examples

### Example 1: Simple Aspect Ratio Fix
**File: `examples/simple.vf`**

Use this if you only need to fix aspect ratio:

```
PIPELINE simple_video_prep
    SOURCE "sample_videos/*.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: fit
END
```

### Example 2: Full Preprocessing Pipeline
**File: `examples/complete.vf`**

Complete preprocessing for ML training:

```
PIPELINE full_video_pipeline
    SOURCE "videos/*.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: pad
    FRAME_RATE
        target: 30fps
    LENS
        correct_distortion: true
END
```

### Example 3: Image Sequence Processing
```
PIPELINE image_pipeline
    SOURCE "photos/*.jpg"
    ASPECT_RATIO
        target: 4:3
        mode: pad
END
```

---

## How It Works (Architecture)

### Pipeline Execution Flow

```
.vf File (VisionFlow DSL)
    ↓
LEXER (tokenizes syntax)
    ↓
PARSER (builds AST - Abstract Syntax Tree)
    ↓
INTERPRETER (executes pipeline)
    ├─ Load frames (video or image)
    ├─ Apply ASPECT_RATIO block
    ├─ Apply FRAME_RATE block
    ├─ Apply LENS block
    ├─ Process batch of files (glob pattern)
    └─ Save output as .mp4 or .jpg
    ↓
processed_output/ (Results)
```

### Core Features

**Batch Processing**
- Handles multiple files with glob patterns
- `"videos/*.mp4"` processes all .mp4 files in videos/
- `"images/**/*.jpg"` processes all .jpg recursively
- Progress tracking for each file

**Flexible Output**
- Video → Video (maintains format)
- Image → Image
- Auto-saved with `_processed` suffix

**Real Computer Vision**
- OpenCV undistort() for lens correction
- Proper padding/cropping for aspect ratios
- Frame rate conforming with duplication

---

## Syntax Reference

### Pipeline Structure

```
PIPELINE <name>
    SOURCE "<glob_pattern>"
    <BLOCK_1>
        <prop>: <value>
    <BLOCK_2>
        <prop>: <value>
END
```

### Block Reference

#### ASPECT_RATIO
```
ASPECT_RATIO
    target: 16:9        # Target aspect ratio
    mode: fit           # fit | pad | crop
```

**Modes:**
- `fit`: Scale to fit, then pad (letterbox)
- `pad`: Add black borders (pillarbox/letterbox)
- `crop`: Remove content (destructive)

#### FRAME_RATE
```
FRAME_RATE
    target: 30fps       # Target frames per second
```

**Common values:**
- `24fps` (film)
- `30fps` (NTSC, most common)
- `60fps` (high-speed)

#### LENS
```
LENS
    correct_distortion: true    # true | false
```

---

## Advanced Usage

### Custom Source Patterns

```bash
# Single video
SOURCE "video.mp4"

# All .mp4 files in a directory
SOURCE "videos/*.mp4"

# All .mp4 files recursively
SOURCE "videos/**/*.mp4"

# Mix of formats
SOURCE "footage/*.{mp4,avi}"

# Wildcards anywhere
SOURCE "*/raw_footage/*.mp4"
```

### Chaining Multiple Blocks

```
PIPELINE multi_stage
    SOURCE "raw/*.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: fit
    LENS
        correct_distortion: true
    FRAME_RATE
        target: 30fps
END
```

Blocks execute in order:
1. Load video
2. Fix aspect ratio
3. Correct lens distortion
4. Conform frame rate
5. Save output

---

## Troubleshooting

### No files matched

```
[ERROR] No files found matching: videos/*.mp4
```

**Fix:** Check that:
1. Directory exists
2. File extension matches exactly
3. Glob pattern is correct

### Import errors

```
ModuleNotFoundError: No module named 'cv2'
```

**Fix:**
```bash
pip install opencv-python
```

### Video codec errors

Some systems need additional codecs:
```bash
pip install opencv-contrib-python
```

### Permission denied

Make sure the `processed_output/` directory is writable.

---

## Performance Tips

### For Large Videos
- Process one file at a time using separate `.vf` files
- Use `mode: crop` instead of `mode: pad` to avoid upscaling

### For Batch Processing
- Use glob patterns to process multiple files in one run
- VisionFlow automatically parallelizes frame loading

### Memory Usage
- VisionFlow loads entire videos into memory
- For very large videos (>5GB), process in segments

---

## Web UI Usage

Open `index.html` in your browser to:
- **Drag-and-drop** blocks to design pipelines
- **Real-time preview** of generated `.vf` code
- **Load examples** to get started quickly
- **Export `.vf` files** to run from command line

Then execute:
```bash
python main.py exported_pipeline.vf
```

---

## What's Inside

### File Structure
```
DSL/
├── main.py              # Entry point - run pipelines
├── lexer.py             # Tokenize .vf syntax
├── parser.py            # Build AST from tokens
├── interpreter.py       # Execute AST (FULLY IMPLEMENTED)
├── index.html           # Web UI for pipeline design
├── test_setup.py        # Verify installation
├── README.md            # Full documentation
└── examples/
    ├── simple.vf        # Aspect ratio only
    ├── complete.vf      # Full preprocessing
    └── example1.vf      # Video preprocessing
```

### Key Implementation Details

**Interpreter (`interpreter.py`)** now includes:
- ✅ Full `process_aspect_ratio()` with fit/pad/crop
- ✅ Full `process_frame_rate()` with frame duplication
- ✅ Full `process_lens()` with cv2.undistort()
- ✅ Video loading (VideoCapture)
- ✅ Image loading (imread)
- ✅ Video saving (VideoWriter)
- ✅ Batch processing with glob
- ✅ Error handling and reporting

---

## Extending VisionFlow

### Adding a New Block Type

Edit `lexer.py` to add keyword:
```python
TOKEN_PATTERNS = [
    ('KEYWORD',  r'\b(PIPELINE|SOURCE|ASPECT_RATIO|FRAME_RATE|LENS|MY_BLOCK|OUTPUT|END)\b'),
    ...
]
```

Edit `interpreter.py` to implement:
```python
def process_my_block(self, props, frames):
    """Process custom block."""
    # Your CV code here
    return frames
```

Register in dispatch:
```python
dispatch = {
    'ASPECT_RATIO': self.process_aspect_ratio,
    'FRAME_RATE': self.process_frame_rate,
    'LENS': self.process_lens,
    'MY_BLOCK': self.process_my_block,  # Add here
}
```

---

## Real-World Use Cases

### 1. **Prepare Data for Object Detection**
```
PIPELINE yolo_prep
    SOURCE "raw_footage/*.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: pad
    FRAME_RATE
        target: 30fps
END
```

### 2. **Standardize Mobile Phone Videos**
```
PIPELINE mobile_video_fix
    SOURCE "phone_videos/*.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: crop
    LENS
        correct_distortion: true
END
```

### 3. **Create Training Dataset from Photos**
```
PIPELINE photo_dataset
    SOURCE "raw_photos/*.jpg"
    ASPECT_RATIO
        target: 1:1
        mode: pad
END
```

---

## FAQ

**Q: Can I process images and videos in the same pipeline?**
A: Yes! Mix them in your source glob pattern.

**Q: What's the maximum file size?**
A: Limited by available RAM. VisionFlow loads entire videos into memory.

**Q: Can I customize the camera calibration matrix?**
A: Yes! Edit the default matrix in `interpreter.py` under `process_lens()`.

**Q: Does it support GPU acceleration?**
A: Future enhancement. Currently uses CPU (OpenCV on CPU).

**Q: Can I chain multiple processing operations?**
A: Yes! Add as many blocks as needed - they execute in order.

---

## Next Steps

1. ✅ Test installation: `python test_setup.py`
2. ✅ Try examples: `python main.py examples/simple.vf`
3. ✅ Create your own pipeline
4. ✅ Use the web UI to design visually
5. ✅ Export and run from CLI

---

**VisionFlow is ready to process your computer vision datasets!** 🎬

For issues or improvements, visit: https://github.com/pandeyishan/visionflow
