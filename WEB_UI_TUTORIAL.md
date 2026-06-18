# VisionFlow Web UI - Tutorial

## Overview

The VisionFlow web UI is a **visual pipeline builder** that helps you create VisionFlow DSL files without writing code. It's like a drag-and-drop interface for building computer vision preprocessing pipelines.

## ⚠️ Important Note

**The UI does NOT execute the pipelines.** It only generates the code. You must:
1. Build your pipeline in the UI
2. Download it as a `.vf` file
3. Run it from the command line with `python main.py`

## Step-by-Step Guide

### Step 1: Open the UI

Open `index.html` in your web browser:
```
file:///C:/Users/Ishan/Desktop/4th%20semester/DSL/index.html
```

### Step 2: Set the SOURCE Path

In the **SOURCE** field, enter the path to your files:

```
"sample_images/*.jpg"
"videos/*.mp4"
"photos/**/*.jpg"
"single_file.jpg"
```

**Glob patterns:**
- `*.jpg` - All .jpg files in that folder
- `**/*.jpg` - All .jpg files recursively
- `*.{mp4,avi}` - Multiple formats

### Step 3: Drag Blocks to Build Your Pipeline

From the left sidebar under "Available Blocks", drag:

- **ASPECT_RATIO** - Fix frame dimensions to target ratio
- **FRAME_RATE** - Conform video to target fps
- **LENS** - Remove lens distortion

The blocks appear on the canvas as you drag them.

### Step 4: Configure Block Properties

Click on each block to edit its properties:

**ASPECT_RATIO:**
- `target`: The target ratio (16:9, 4:3, 1:1, etc.)
- `mode`: How to adjust (fit, pad, crop)

**FRAME_RATE:**
- `target`: Target fps (24fps, 30fps, 60fps)

**LENS:**
- `correct_distortion`: true or false

### Step 5: Download Your Pipeline

Click the blue **"📥 Download Code"** button:
- Your `.vf` file is downloaded
- Browser will save it with your pipeline name (e.g., `my_pipeline.vf`)

### Step 6: Run the Pipeline

Open your terminal and run:

```bash
cd "C:\Users\Ishan\Desktop\4th semester\DSL"
python main.py my_pipeline.vf
```

### Step 7: Check Results

Your processed files are in the `processed_output/` folder:
- Filenames end with `_processed` (e.g., `image_processed.jpg`)
- Same format as input (video→video, image→image)

## Example Workflow

### Example 1: Convert 4:3 images to 16:9

**In the UI:**
1. Set SOURCE: `"sample_images/*.jpg"`
2. Drag ASPECT_RATIO block
3. Set `target: 16:9`
4. Set `mode: pad` (add black bars)
5. Download as `convert_to_16_9.vf`

**In terminal:**
```bash
python main.py convert_to_16_9.vf
```

**Result:** All images converted to 16:9 aspect ratio in `processed_output/`

---

### Example 2: Fix phone video + standardize

**In the UI:**
1. Set SOURCE: `"phone_videos/*.mp4"`
2. Drag ASPECT_RATIO → target: 16:9, mode: fit
3. Drag LENS → correct_distortion: true
4. Drag FRAME_RATE → target: 30fps
5. Download as `phone_video_fix.vf`

**In terminal:**
```bash
python main.py phone_video_fix.vf
```

**Result:** Videos fixed, standardized, and ready for ML training

---

## Real-Time Code Preview

The right panel shows your generated `.vf` code in **real-time**:

```
PIPELINE my_pipeline
    SOURCE "sample_images/*.jpg"
    ASPECT_RATIO
        target: 16:9
        mode: pad
    LENS
        correct_distortion: true
END
```

This is exactly what gets saved when you download.

## Load Examples

Click **"Examples"** to load pre-built pipelines:
- **Video Preprocessing** - Full 3-block pipeline
- **Image Sequence** - Simple aspect ratio adjustment

These help you understand what's possible.

## Validation Feedback

The UI validates your SOURCE path:

- ✓ Green checkmark = Valid path pattern
- ⚠️ Warning = Check your path syntax

Valid patterns:
- `"videos/*.mp4"`
- `"photos/**/*.jpg"`
- `"image.jpg"`
- `"C:\Users\Ishan\Desktop\4th semester\DSL\images\*.jpg"`

## Tips & Tricks

### Tip 1: Use Relative Paths
It's easier to use relative paths from your project folder:
```
Instead of: "C:\Users\Ishan\Desktop\videos\*.mp4"
Use: "videos/*.mp4"
```

### Tip 2: Test with Sample Files
Before processing your real data, test with the sample files:
```
"sample_images/*.jpg"
```

### Tip 3: Copy Code Directly
You can copy the code from the preview and paste it into a text editor, then save as `.vf`

### Tip 4: Quick Start
Click **"Quick Start"** button in header for step-by-step walkthrough

### Tip 5: Remove Blocks
Click the ✕ button on any block to remove it

## Troubleshooting

### "No files found matching: ..."
- Check the SOURCE path is correct
- Make sure files exist in that location
- Try using absolute path instead of relative

### Missing output files
- Files are saved to `processed_output/` folder
- Check that folder exists and is writable
- Look for `_processed` suffix in filenames

### UI doesn't respond
- Reload the page (Ctrl+R)
- Check browser console for errors (F12)
- Try with a different browser

## What Happens Behind the Scenes

```
1. UI (index.html)
   └─ Collects configuration
       └─ Generates .vf code
           └─ Download as file

2. You download and run
   └─ python main.py file.vf
       └─ Lexer tokenizes
           └─ Parser builds AST
               └─ Interpreter executes
                   └─ Results in processed_output/
```

The UI is the **visual layer** for building the code. The **actual processing** happens when you run `python main.py` in the terminal.

## Next Steps

1. ✅ Open `index.html` in browser
2. ✅ Build your first pipeline
3. ✅ Download the `.vf` file
4. ✅ Run with `python main.py`
5. ✅ Check `processed_output/`

**You're ready to process your computer vision datasets!** 🎬
