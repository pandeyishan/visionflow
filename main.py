
import sys
from lexer import tokenize
from parser import Parser
from interpreter import VisionFlowInterpreter

def run(script_path: str):
    with open(script_path) as f:
        source = f.read()
    tokens   = tokenize(source)
    ast      = Parser(tokens).parse()
    VisionFlowInterpreter().run(ast)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.vf>")
        sys.exit(1)
    run(sys.argv[1])