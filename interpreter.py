
import cv2
import glob
import os
import numpy as np
from pathlib import Path

class VisionFlowInterpreter:
    """Execute VisionFlow AST with real computer vision processing."""

    def __init__(self, output_dir='processed_output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def run(self, ast):
        """Main execution: load, process, and save files."""
        files = sorted(glob.glob(ast.source))
        
        if not files:
            print(f"[ERROR] No files found matching: {ast.source}")
            return
        
        print(f"\n{'='*60}")
        print(f"[VisionFlow] Pipeline: {ast.name}")
        print(f"[VisionFlow] Processing {len(files)} file(s)...")
        print(f"{'='*60}\n")
        
        for idx, filepath in enumerate(files, 1):
            try:
                print(f"[{idx}/{len(files)}] Processing: {Path(filepath).name}")
                
                # Load frames (video or image)
                frames = self.load_frames(filepath)
                if not frames:
                    print(f"  [WARN] Could not load frames from {filepath}")
                    continue
                
                print(f"  Loaded {len(frames)} frame(s)")
                
                # Apply each block in pipeline
                for block in ast.blocks:
                    frames = self.execute_block(block, frames)
                
                # Save output
                self.save_output(frames, filepath, ast.name)
                print(f"  ✓ Saved to: {self.output_dir}\n")
                
            except Exception as e:
                print(f"  [ERROR] {str(e)}\n")

    def execute_block(self, block, frames):
        """Execute a single processing block."""
        dispatch = {
            'ASPECT_RATIO': self.process_aspect_ratio,
            'FRAME_RATE':   self.process_frame_rate,
            'LENS':         self.process_lens,
        }
        handler = dispatch.get(block.type)
        if handler:
            return handler(block.props, frames)
        return frames

    def process_aspect_ratio(self, props, frames):
        """Adjust frames to target aspect ratio."""
        target = props.get('target', '16:9')
        mode = props.get('mode', 'fit').lower()
        
        # Parse target ratio
        if ':' in target:
            w_ratio, h_ratio = map(int, target.split(':'))
        else:
            print(f"  [WARN] Invalid aspect ratio format: {target}")
            return frames
        
        target_ratio = w_ratio / h_ratio
        results = []
        
        for frame in frames:
            h, w = frame.shape[:2]
            current_ratio = w / h
            
            if abs(current_ratio - target_ratio) < 0.001:
                # Already correct ratio
                results.append(frame)
                continue
            
            if mode == 'pad':
                # Pad to reach target ratio
                if current_ratio < target_ratio:
                    # Too tall, pad sides
                    new_w = int(h * target_ratio)
                    pad_left = (new_w - w) // 2
                    pad_right = new_w - w - pad_left
                    frame = cv2.copyMakeBorder(frame, 0, 0, pad_left, pad_right,
                                               cv2.BORDER_CONSTANT, value=(0, 0, 0))
                else:
                    # Too wide, pad top/bottom
                    new_h = int(w / target_ratio)
                    pad_top = (new_h - h) // 2
                    pad_bottom = new_h - h - pad_top
                    frame = cv2.copyMakeBorder(frame, pad_top, pad_bottom, 0, 0,
                                               cv2.BORDER_CONSTANT, value=(0, 0, 0))
            
            elif mode == 'crop':
                # Crop to reach target ratio
                if current_ratio > target_ratio:
                    # Too wide, crop sides
                    new_w = int(h * target_ratio)
                    crop_left = (w - new_w) // 2
                    frame = frame[:, crop_left:crop_left + new_w]
                else:
                    # Too tall, crop top/bottom
                    new_h = int(w / target_ratio)
                    crop_top = (h - new_h) // 2
                    frame = frame[crop_top:crop_top + new_h, :]
            
            else:  # mode == 'fit' (default)
                # Scale and pad to fit
                if current_ratio > target_ratio:
                    # Too wide, scale down
                    new_w = int(h * target_ratio)
                    frame = cv2.resize(frame, (new_w, h))
                    pad_left = (w - new_w) // 2
                    pad_right = w - new_w - pad_left
                    frame = cv2.copyMakeBorder(frame, 0, 0, pad_left, pad_right,
                                               cv2.BORDER_CONSTANT, value=(0, 0, 0))
                else:
                    # Too tall, scale down
                    new_h = int(w / target_ratio)
                    frame = cv2.resize(frame, (w, new_h))
                    pad_top = (h - new_h) // 2
                    pad_bottom = h - new_h - pad_top
                    frame = cv2.copyMakeBorder(frame, pad_top, pad_bottom, 0, 0,
                                               cv2.BORDER_CONSTANT, value=(0, 0, 0))
            
            results.append(frame)
        
        print(f"  [ASPECT_RATIO] Applied {target} ({mode})")
        return results

    def process_frame_rate(self, props, frames):
        """Conform frame rate by duplicating frames."""
        target_fps = int(props.get('target', '30').replace('fps', '').strip())
        
        if len(frames) < 2:
            print(f"  [FRAME_RATE] Skipped (need at least 2 frames)")
            return frames
        
        # Simple frame duplication approach
        # For 24fps->30fps: duplicate some frames
        # For 30fps->24fps: drop some frames
        
        current_fps = 30  # Assume source is 30fps (can be extracted from video)
        ratio = target_fps / current_fps
        
        if ratio > 1:
            # Need more frames - duplicate
            results = []
            dup_factor = round(ratio)
            for frame in frames:
                for _ in range(dup_factor):
                    results.append(frame)
        else:
            # Need fewer frames - drop
            step = round(1 / ratio)
            results = frames[::step]
        
        print(f"  [FRAME_RATE] Conformed to {target_fps}fps ({len(frames)} -> {len(results)} frames)")
        return results

    def process_lens(self, props, frames):
        """Apply lens distortion correction."""
        if props.get('correct_distortion', 'false').lower() != 'true':
            return frames
        
        # Default camera matrix (can be calibrated per camera)
        # These are reasonable defaults for typical cameras
        h, w = frames[0].shape[:2]
        focal_length = w
        center = (w / 2, h / 2)
        
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float32)
        
        # Mild distortion coefficients (can be tuned)
        dist_coeffs = np.array([0.1, -0.1, 0, 0, 0], dtype=np.float32)
        
        results = []
        for frame in frames:
            corrected = cv2.undistort(frame, camera_matrix, dist_coeffs)
            results.append(corrected)
        
        print(f"  [LENS] Applied distortion correction to {len(frames)} frame(s)")
        return results

    def load_frames(self, path):
        """Load frames from video or image file."""
        path = str(path).strip('"')  # Remove quotes if present
        
        # Check if video or image
        video_ext = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
        image_ext = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        ext = os.path.splitext(path)[1].lower()
        
        if ext in video_ext:
            return self.load_video_frames(path)
        elif ext in image_ext:
            return self.load_image_frames(path)
        else:
            print(f"  [ERROR] Unsupported format: {ext}")
            return []

    def load_video_frames(self, path):
        """Load all frames from a video file."""
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"  [ERROR] Cannot open video: {path}")
            return []
        
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return frames

    def load_image_frames(self, path):
        """Load a single image as a frame."""
        frame = cv2.imread(path)
        if frame is None:
            print(f"  [ERROR] Cannot read image: {path}")
            return []
        return [frame]

    def save_output(self, frames, src_path, pipeline_name):
        """Save processed frames as video or image sequence."""
        if not frames:
            return
        
        filename = Path(src_path).stem
        src_ext = Path(src_path).suffix.lower()
        
        # Save as video if original was video
        video_ext = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
        
        if src_ext in video_ext:
            self.save_video(frames, filename, pipeline_name)
        else:
            self.save_image(frames[0], filename, pipeline_name)

    def save_video(self, frames, filename, pipeline_name):
        """Save frames as a video file."""
        if not frames:
            return
        
        h, w = frames[0].shape[:2]
        output_path = os.path.join(self.output_dir, f"{filename}_processed.mp4")
        
        # Use MP4 codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30
        
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        
        for frame in frames:
            out.write(frame)
        
        out.release()

    def save_image(self, frame, filename, pipeline_name):
        """Save frame as an image file."""
        output_path = os.path.join(self.output_dir, f"{filename}_processed.jpg")
        cv2.imwrite(output_path, frame)
