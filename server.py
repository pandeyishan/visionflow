#!/usr/bin/env python3
"""Simple Flask server to execute VisionFlow pipelines from the web UI."""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import tempfile
import traceback
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from lexer import tokenize
from parser import Parser
from interpreter import VisionFlowInterpreter

# Determine the directory where server.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

class PipelineExecutor:
    """Execute VisionFlow pipelines and capture output."""
    
    def __init__(self):
        self.output_lines = []
    
    def log(self, message):
        """Capture log messages."""
        self.output_lines.append(message)
        print(message)
    
    def execute(self, pipeline_code, source_path):
        """Execute a pipeline and return results."""
        self.output_lines = []
        
        try:
            # Validate source path exists
            if not source_path or source_path == '""':
                self.log("[ERROR] No SOURCE path provided")
                return False
            
            # Log start
            self.log(f"\n{'='*60}")
            self.log(f"[VisionFlow] Executing pipeline...")
            self.log(f"{'='*60}\n")
            
            # Tokenize
            self.log("[*] Tokenizing VisionFlow code...")
            tokens = tokenize(pipeline_code)
            self.log(f"[✓] Tokenized {len(tokens)} tokens\n")
            
            # Parse
            self.log("[*] Parsing AST...")
            ast = Parser(tokens).parse()
            self.log(f"[✓] Parsed pipeline: {ast.name}\n")
            
            # Override source
            ast.source = source_path.strip('"')
            
            # Execute
            self.log("[*] Executing pipeline...\n")
            interpreter = VisionFlowInterpreter(output_dir='processed_output')
            
            # Monkey-patch print to capture output
            original_print = print
            def captured_print(*args, **kwargs):
                msg = ' '.join(str(arg) for arg in args)
                self.output_lines.append(msg)
                original_print(msg, **kwargs)
            
            # Temporarily replace print
            import builtins
            builtins.print = captured_print
            
            try:
                interpreter.run(ast)
            finally:
                builtins.print = original_print
            
            self.log(f"\n{'='*60}")
            self.log("[SUCCESS] Pipeline execution complete!")
            self.log(f"{'='*60}")
            
            # Get output files
            output_files = []
            if os.path.exists('processed_output'):
                output_files = sorted(os.listdir('processed_output'))
            
            return True, output_files
            
        except Exception as e:
            self.log(f"\n[ERROR] {str(e)}")
            self.log(traceback.format_exc())
            return False, []
    
    def get_output(self):
        """Get captured output."""
        return '\n'.join(self.output_lines)


executor = PipelineExecutor()


@app.route('/api/execute', methods=['POST'])
def execute_pipeline():
    """Execute a pipeline from the UI."""
    try:
        data = request.json
        pipeline_code = data.get('code', '')
        source_path = data.get('source', '')
        
        # Execute
        success, output_files = executor.execute(pipeline_code, source_path)
        
        return jsonify({
            'success': success,
            'output': executor.get_output(),
            'files': output_files,
            'output_dir': os.path.abspath('processed_output')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'output': f"[ERROR] {str(e)}\n{traceback.format_exc()}"
        }), 400


@app.route('/api/files', methods=['GET'])
def list_files():
    """List output files."""
    try:
        files = []
        if os.path.exists('processed_output'):
            for f in sorted(os.listdir('processed_output')):
                path = os.path.join('processed_output', f)
                size = os.path.getsize(path)
                files.append({
                    'name': f,
                    'size': size,
                    'path': path
                })
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({'status': 'ok', 'version': '1.0'})


@app.route('/', methods=['GET'])
def serve_ui():
    """Serve the web UI."""
    return send_file(os.path.join(BASE_DIR, 'index.html'))


@app.route('/index.html', methods=['GET'])
def serve_index():
    """Serve index.html directly."""
    return send_file(os.path.join(BASE_DIR, 'index.html'))


if __name__ == '__main__':
    print("\n" + "="*60)
    print("VisionFlow Web Server")
    print("="*60)
    print("\n[*] Starting server on http://localhost:5000")
    print("[*] Open index.html in your browser")
    print("[*] Pipelines will execute on this server\n")
    print("="*60 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
