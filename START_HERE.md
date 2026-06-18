# VisionFlow - Complete In-UI Execution

You now have a **complete integrated system** - build, configure, and execute pipelines all in the same web interface!

## 🚀 Quick Start (30 seconds)

### 1. Start the Server
```bash
python run_server.py
```

This will:
- ✓ Install Flask automatically
- ✓ Start the server on `localhost:5000`
- ✓ Open your browser automatically

### 2. Use the Web UI
1. **Set SOURCE** - Enter your file path (e.g., `"sample_images/*.jpg"`)
2. **Drag Blocks** - Add ASPECT_RATIO, FRAME_RATE, LENS blocks
3. **Configure** - Set target ratio, mode, fps, etc.
4. **Click "▶ Run Pipeline"** - Execute directly in the UI!

### 3. View Results
- **Live Output** - See execution logs in real-time
- **Output Files** - List of processed files appears instantly
- **No Download Needed** - Everything happens in one place

---

## 📋 Architecture

```
Web Browser (index.html)
    ↓
    [Build pipeline visually]
    ↓ Click "▶ Run Pipeline"
    ↓
Flask Server (server.py)
    ↓
    [Execute VisionFlow]
    ├─ Lexer → Parser → Interpreter
    ├─ Process files
    └─ Return results
    ↓
Web UI
    ↓
    [Display output + file list]
```

---

## 💻 Detailed Setup

### Prerequisites
```bash
python --version  # Should be 3.8+
```

### Installation
No manual installation needed! `run_server.py` installs everything:
- Flask (web framework)
- Flask-CORS (cross-origin requests)
- OpenCV (computer vision)
- NumPy (numerical computing)

### Start Server
```bash
cd "C:\Users\Ishan\Desktop\4th semester\DSL"
python run_server.py
```

Expected output:
```
[*] Checking dependencies...
  ✓ Flask
  ✓ flask-cors
  ✓ opencv-python
  ✓ numpy

======================================================================
                   VISIONFLOW WEB SERVER
======================================================================

[*] Server starting on http://localhost:5000

[===================================]
  Web UI:     http://localhost:5000
  Browser:    Opening automatically...
[===================================]

[*] VisionFlow server is running!
[*] Press Ctrl+C to stop
```

Then your browser opens automatically!

---

## 🎯 Workflow Example

### Example: Convert Images to 16:9

1. **Start Server**
   ```bash
   python run_server.py
   ```

2. **In the UI:**
   - Pipeline Name: `image_converter`
   - SOURCE: `"sample_images/*.jpg"`
   - Drag ASPECT_RATIO block
   - Set target: `16:9`
   - Set mode: `pad`

3. **Execute**
   - Click **"▶ Run Pipeline"** button
   - Watch output in real-time
   - See processed files listed

4. **Check Results**
   - Files shown in "Output Files" section
   - Actual files in: `processed_output/`

**Total time: < 1 minute!** ⚡

---

## 📊 Features

| Feature | Status |
|---------|--------|
| Build pipeline visually | ✅ Drag-drop UI |
| Execute in browser | ✅ Click "▶ Run" |
| Live output | ✅ Real-time logs |
| Results display | ✅ Files listed |
| Auto server start | ✅ `run_server.py` |
| Auto browser open | ✅ Automatic |
| Download option | ✅ Still available |

---

## 🔧 Technical Details

### Server Files
- `server.py` - Flask backend (executes pipelines)
- `run_server.py` - Auto-installer + launcher
- `index.html` - Web UI (builds pipelines + shows results)

### Ports
- Web UI: `http://localhost:5000`
- API: `http://localhost:5000/api/`

### API Endpoints
- `POST /api/execute` - Execute a pipeline
- `GET /api/files` - List output files
- `GET /health` - Server health check

---

## ⚙️ Configuration

### Change Server Port
Edit `server.py` or `run_server.py`:
```python
app.run(host='127.0.0.1', port=5000)  # Change 5000 to desired port
```

### Change Output Directory
Edit `server.py`:
```python
interpreter = VisionFlowInterpreter(output_dir='your_output_folder')
```

### Disable Auto-Browser
Edit `run_server.py`:
```python
# Comment this line:
webbrowser.open('http://localhost:5000')
```

---

## 🐛 Troubleshooting

### "Cannot connect to server"
- Make sure `python run_server.py` is running
- Check that port 5000 is not in use
- Try a different port in the code

### "ModuleNotFoundError: No module named 'flask'"
- Run `python run_server.py` again (it auto-installs)
- Or manually: `pip install flask flask-cors`

### Browser doesn't open automatically
- Manually go to: `http://localhost:5000`
- Or click "Quick Start" button for help

### Processing takes too long
- Large files take time
- Check terminal to see progress
- Don't close the terminal window

### Output files not showing
- Check `processed_output/` folder directly
- Make sure SOURCE path is correct
- Try the example: `"sample_images/*.jpg"`

---

## 🎬 Next Steps

1. ✅ Run `python run_server.py`
2. ✅ Build your first pipeline
3. ✅ Click **"▶ Run Pipeline"**
4. ✅ See results instantly!

---

## 📚 Additional Resources

- **Full Guide:** See `GUIDE.md`
- **Web UI Tutorial:** See `WEB_UI_TUTORIAL.md`
- **Examples:** Click "Examples" in the UI
- **Quick Start:** Click "Quick Start" in the UI

---

## 🎯 You're All Set!

Everything is integrated. Build, execute, and see results in one place!

```bash
python run_server.py
# That's it! 🎉
```

---

**VisionFlow - Simple. Complete. Powerful.** 🚀
