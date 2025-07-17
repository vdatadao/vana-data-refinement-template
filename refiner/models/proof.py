from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class InstagramProof(BaseModel):
    """
    Instagram verisi için proof modeli.
    Verinin gerçekliğini ve sahipliğini kanıtlar.
    """
    
    # Temel proof bilgileri
    user_id: str
    username_hash: str  # Gizlilik için hash'lenmiş
    proof_type: str = "instagram_data_export"
    
    # Zaman damgaları
    data_export_timestamp: str
    proof_generation_timestamp: str
    
    # Veri bütünlüğü
    total_posts: int
    total_stories: int
    total_comments: int
    total_dms: int
    
    # Hesap doğrulama
    account_creation_estimate: Optional[str] = None
    follower_count: int
    following_count: int
    is_verified: bool
    is_private: bool
    
    # Metadata hash'leri (veri bütünlüğü için)
    profile_hash: str
    posts_hash: str
    stories_hash: str
    comments_hash: str
    dms_hash: str
    
    # Opsiyonel: Instagram API yanıtları
    api_responses: Optional[List[Dict[str, Any]]] = None
    
    # Proof güvenilirliği
    confidence_score: float  # 0.0 - 1.0 arası
    verification_method: str  # "data_export", "api_scraping", "manual_verification"
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }