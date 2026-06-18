
import sys
from lexer import tokenize
from parser import Parser
from interpreter import VisionFlowInterpreter

def run(script_path: str):
    """Execute a VisionFlow pipeline."""
    try:
        with open(script_path) as f:
            source = f.read()
    except FileNotFoundError:
        print(f"[ERROR] Pipeline file not found: {script_path}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        sys.exit(1)
    
    try:
        # Tokenize
        tokens = tokenize(source)
        
        # Parse
        ast = Parser(tokens).parse()
        
        # Execute
        interpreter = VisionFlowInterpreter(output_dir='processed_output')
        interpreter.run(ast)
        
        print(f"\n{'='*60}")
        print(f"[SUCCESS] Pipeline completed!")
        print(f"[INFO] Output saved to: processed_output/")
        print(f"{'='*60}\n")
        
    except SyntaxError as e:
        print(f"[SYNTAX ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.vf>")
        print("\nExample pipeline file (example.vf):")
        print("""
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
        """)
        sys.exit(1)
    run(sys.argv[1])