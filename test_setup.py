#!/usr/bin/env python3
"""Test script to validate VisionFlow installation and functionality."""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules are available."""
    print("Testing imports...")
    try:
        import cv2
        print(f"  ✓ OpenCV {cv2.__version__}")
    except ImportError:
        print("  ✗ OpenCV not found. Install with: pip install opencv-python")
        return False
    
    try:
        import numpy
        print(f"  ✓ NumPy {numpy.__version__}")
    except ImportError:
        print("  ✗ NumPy not found. Install with: pip install numpy")
        return False
    
    print("  ✓ All imports successful\n")
    return True

def test_lexer():
    """Test lexer functionality."""
    print("Testing Lexer...")
    try:
        from lexer import tokenize
        
        code = """PIPELINE test
    SOURCE "test.mp4"
    ASPECT_RATIO
        target: 16:9
END"""
        
        tokens = tokenize(code)
        print(f"  ✓ Tokenized {len(tokens)} tokens")
        return True
    except Exception as e:
        print(f"  ✗ Lexer error: {e}")
        return False

def test_parser():
    """Test parser functionality."""
    print("Testing Parser...")
    try:
        from lexer import tokenize
        from parser import Parser
        
        code = """PIPELINE test
    SOURCE "test.mp4"
    ASPECT_RATIO
        target: 16:9
        mode: fit
END"""
        
        tokens = tokenize(code)
        ast = Parser(tokens).parse()
        print(f"  ✓ Parsed pipeline: {ast.name}")
        print(f"  ✓ Blocks: {[b.type for b in ast.blocks]}")
        return True
    except Exception as e:
        print(f"  ✗ Parser error: {e}")
        return False

def test_interpreter():
    """Test interpreter initialization."""
    print("Testing Interpreter...")
    try:
        from interpreter import VisionFlowInterpreter
        
        interp = VisionFlowInterpreter()
        print(f"  ✓ Interpreter initialized")
        print(f"  ✓ Output directory: {interp.output_dir}")
        return True
    except Exception as e:
        print(f"  ✗ Interpreter error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("VisionFlow Installation Test")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_lexer,
        test_parser,
        test_interpreter,
    ]
    
    results = [test() for test in tests]
    
    print("="*60)
    if all(results):
        print("✓ All tests passed! VisionFlow is ready to use.")
        print("\nQuick start:")
        print("  1. Create a .vf file with your pipeline")
        print("  2. Run: python main.py your_pipeline.vf")
        print("="*60 + "\n")
        return 0
    else:
        print("✗ Some tests failed. See errors above.")
        print("="*60 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
