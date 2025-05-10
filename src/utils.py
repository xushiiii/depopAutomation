def clean_hashtags(hashtags_str):
    """
    Clean hashtags by removing # symbols and extra whitespace.
    
    Args:
        hashtags_str (str): String containing hashtags separated by spaces
        
    Returns:
        list: List of cleaned hashtags with # symbols removed and extra whitespace trimmed
    """
    if not hashtags_str:
        return []
        
    # Split by spaces and clean each hashtag
    hashtags = [tag.strip().lstrip('#') for tag in hashtags_str.split()]
    
    # Remove any empty strings
    cleaned_hashtags = [tag for tag in hashtags if tag]
    
    return cleaned_hashtags 