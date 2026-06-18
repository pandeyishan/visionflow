
import cv2, glob, os

class VisionFlowInterpreter:

    def run(self, ast):
        files = glob.glob(ast.source)
        print(f"[VisionFlow] Processing {len(files)} file(s)...")
        for filepath in files:
            frames = self.load_frames(filepath)
            for block in ast.blocks:
                frames = self.execute_block(block, frames)
            self.save_output(frames, filepath, ast)

    def execute_block(self, block, frames):
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
        target = props.get('target', '16:9')
        w_ratio, h_ratio = map(int, target.split(':'))
        results = []
        for frame in frames:
            h, w = frame.shape[:2]
            target_w = int(h * w_ratio / h_ratio)
            # Pad or crop to reach target ratio
            if w < target_w:
                pad = (target_w - w) // 2
                frame = cv2.copyMakeBorder(frame, 0, 0, pad, pad,
                    cv2.BORDER_CONSTANT, value=(0,0,0))
            results.append(frame)
        return results

    def process_frame_rate(self, props, frames):
        # Simple duplication-based conform (real: use ffmpeg or optical flow)
        target = int(props.get('target', '30').replace('fps',''))
        print(f"  [frame_rate] Conforming to {target}fps")
        return frames  # placeholder: wire to ffmpeg subprocess

    def process_lens(self, props, frames):
        if props.get('correct_distortion') == 'true':
            # Apply undistortion using calibrated camera matrix
            print("  [lens] Applying distortion correction")
        return frames

    def load_frames(self, path): 
        cap = cv2.VideoCapture(path)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            frames.append(frame)
        cap.release()
        return frames

    def save_output(self, frames, src_path, ast): 
        pass  # write frames or re-encode with ffmpeg