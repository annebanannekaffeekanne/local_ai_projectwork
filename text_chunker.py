import re

class TextChunker:
    """
    Class for splitting text into chunks of a specified maximum length.
    Tries to preserve sentence boundaries when possible.
    """
    
    def __init__(self, maxlen=1000):
        """
        Initialize the TextChunker with a maximum length for chunks.
        
        Args:
            maxlen (int): Maximum length of each chunk in characters
        """
        self.maxlen = maxlen
        # Regular expression for splitting text into sentences
        self.sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
    
    def chunk(self, text):
        """
        Split text into chunks of maximum length while preserving sentence boundaries when possible.
        
        Args:
            text (str): The text to be chunked
            
        Yields:
            str: Chunks of text with maximum length of self.maxlen
        """
        if not text or not isinstance(text, str):
            # Handle empty or invalid input
            return
            
        # Split text into sentences
        sentences = self.sentence_pattern.split(text)
        
        current_chunk = ""
        
        for sentence in sentences:
            # If a single sentence is longer than maxlen, we need to split it by characters
            if len(sentence) > self.maxlen:
                # First yield any accumulated chunk
                if current_chunk:
                    yield current_chunk
                    current_chunk = ""
                
                # Then split the long sentence into chunks of maxlen characters
                for i in range(0, len(sentence), self.maxlen):
                    yield sentence[i:i + self.maxlen]
            
            # If adding this sentence would make the chunk too long, yield the current chunk
            elif len(current_chunk) + len(sentence) > self.maxlen:
                yield current_chunk
                current_chunk = sentence
            
            # Otherwise, add the sentence to the current chunk
            else:
                if current_chunk:
                    current_chunk += " " + sentence.strip()
                else:
                    current_chunk = sentence.strip()
        
        # Yield any remaining text
        if current_chunk:
            yield current_chunk

