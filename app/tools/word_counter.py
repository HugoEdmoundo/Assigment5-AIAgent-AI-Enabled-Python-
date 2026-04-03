from typing import Dict, Any
import re

def count_words(text: str, word: str) -> Dict[str, Any]:
    """
    Counts occurrences of a specific word in text.
    Case-insensitive by default.
    
    Args:
        text: The text to search in
        word: The word to count
        
    Returns:
        Dictionary with count and additional info
    """
    if not text or not word:
        return {
            "error": "Both text and word parameters are required",
            "count": 0
        }
    
    # Case-insensitive counting
    text_lower = text.lower()
    word_lower = word.lower()
    
    # Count exact word matches (not substrings)
    # Using word boundaries
    pattern = r'\b' + re.escape(word_lower) + r'\b'
    matches = re.findall(pattern, text_lower)
    exact_count = len(matches)
    
    # Also count substring occurrences
    substring_count = text_lower.count(word_lower)
    
    # Find positions of matches
    positions = [m.start() for m in re.finditer(pattern, text_lower)]
    
    return {
        "word": word,
        "exact_word_count": exact_count,
        "substring_count": substring_count,
        "text_length": len(text),
        "word_length": len(word),
        "positions": positions[:10],  # Limit to first 10 positions
        "percentage": round((exact_count / len(text.split())) * 100, 2) if text.split() else 0
    }
