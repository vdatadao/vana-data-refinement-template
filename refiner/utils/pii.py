import hashlib

def mask_email(email: str) -> str:
    """
    Mask email addresses by hashing the local part (before @).
    
    Args:
        email: The email address to mask
        
    Returns:
        Masked email address with hashed local part
    """
    if not email or '@' not in email:
        return email
        
    local_part, domain = email.split('@', 1)
    hashed_local = hashlib.md5(local_part.encode()).hexdigest()
    
    return f"{hashed_local}@{domain}"

def hash_text(text: str) -> str:
    """
    Hash any text using SHA-256 for privacy protection.
    
    Args:
        text: The text to hash
        
    Returns:
        SHA-256 hash of the text
    """
    if not text:
        return ""
    
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def hash_username(username: str) -> str:
    """
    Hash username for privacy while maintaining uniqueness.
    
    Args:
        username: The username to hash
        
    Returns:
        Hashed username
    """
    return hash_text(username.lower())

def anonymize_bio(bio: str) -> dict:
    """
    Anonymize bio by returning only analytical data.
    
    Args:
        bio: The bio text
        
    Returns:
        Dictionary with bio analytics (length, word count, etc.)
    """
    if not bio:
        return {
            'length': 0,
            'word_count': 0,
            'has_url': False,
            'has_email': False,
            'has_hashtags': False
        }
    
    words = bio.split()
    
    return {
        'length': len(bio),
        'word_count': len(words),
        'has_url': any('http' in word or 'www.' in word for word in words),
        'has_email': '@' in bio and '.' in bio,
        'has_hashtags': '#' in bio
    }