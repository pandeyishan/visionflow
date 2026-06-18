
import re
from dataclasses import dataclass

TOKEN_PATTERNS = [
    ('KEYWORD',  r'\b(PIPELINE|SOURCE|ASPECT_RATIO|FRAME_RATE|LENS|OUTPUT|END)\b'),
    ('STRING',   r'"[^"]*"'),
    ('RATIO',    r'\d+:\d+'),
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('UNIT',     r'fps|px|ms'),
    ('BOOL',     r'\b(true|false)\b'),
    ('IDENT',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('COLON',    r':'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('COMMENT',  r'#.*'),
]

@dataclass
class Token:
    type: str
    value: str
    line: int

def tokenize(source: str) -> list[Token]:
    tokens = []
    line = 1
    pos = 0
    while pos < len(source):
        for tok_type, pattern in TOKEN_PATTERNS:
            match = re.match(pattern, source[pos:])
            if match:
                if tok_type not in ('SKIP', 'COMMENT'):
                    tokens.append(Token(tok_type, match.group(), line))
                if tok_type == 'NEWLINE':
                    line += 1
                pos += len(match.group())
                break
        else:
            raise SyntaxError(f"Unknown character '{source[pos]}' at line {line}")
    return tokens