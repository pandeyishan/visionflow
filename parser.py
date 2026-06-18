
class PipelineNode:
    def __init__(self, name): 
        self.name = name
        self.source = None
        self.blocks = []   # list of BlockNode

class BlockNode:
    def __init__(self, block_type):
        self.type = block_type     # e.g. "ASPECT_RATIO"
        self.props = {}            # e.g. {"mode": "fit", "target": "16:9"}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self): 
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        if self.pos >= len(self.tokens):
            raise SyntaxError(f"Unexpected end of file, expected {expected_type}")
        tok = self.tokens[self.pos]
        if expected_type and tok.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {tok.type} at line {tok.line}")
        self.pos += 1
        return tok

    def parse(self):
        self.consume('KEYWORD')  # PIPELINE
        name = self.consume('IDENT').value
        node = PipelineNode(name)
        self.skip_newlines()  # Skip newlines after pipeline name
        while self.peek() and self.peek().value != 'END':
            self.skip_newlines()
            tok = self.peek()
            if not tok:
                break
            if tok.value == 'SOURCE':
                self.consume(); node.source = self.consume('STRING').value.strip('"')
            elif tok.type == 'KEYWORD':
                node.blocks.append(self.parse_block())
            else:
                # Skip unexpected tokens to prevent infinite loop
                self.consume()
        # Consume END if it exists, otherwise it's okay
        if self.peek() and self.peek().value == 'END':
            self.consume('KEYWORD')  # END
        return node

    def parse_block(self):
        block_type = self.consume('KEYWORD').value
        block = BlockNode(block_type)
        self.skip_newlines()
        while self.peek() and self.peek().type == 'IDENT':
            key = self.consume('IDENT').value
            self.consume('COLON')
            val = self.consume()
            block.props[key] = val.value
            self.skip_newlines()
        return block

    def skip_newlines(self):
        while self.peek() and self.peek().type == 'NEWLINE':
            self.consume()