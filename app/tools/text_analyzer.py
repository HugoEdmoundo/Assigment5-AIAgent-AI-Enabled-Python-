from typing import Dict, Any

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyzes text and returns various statistics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing text statistics
    """
    if not text:
        return {
            "error": "Text cannot be empty",
            "character_count": 0,
            "word_count": 0
        }
    
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    # Calculate average word length
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / len(words) if words else 0
    
    return {
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", "")),
        "word_count": len(words),
        "sentence_count": sentences if sentences > 0 else 1,
        "average_word_length": round(avg_word_length, 2),
        "longest_word": max(words, key=len) if words else "",
        "shortest_word": min(words, key=len) if words else ""
    }
