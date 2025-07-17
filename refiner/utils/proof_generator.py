import hashlib
import json
from datetime import datetime
from typing import Dict, Any, List

from refiner.models.proof import InstagramProof
from refiner.models.unrefined import InstagramData
from refiner.utils.pii import hash_text

class InstagramProofGenerator:
    """
    Instagram verisi için proof oluşturucu.
    Verinin gerçekliğini ve sahipliğini kanıtlayan proof dosyası üretir.
    """
    
    def __init__(self, data: InstagramData):
        self.data = data
    
    def generate_proof(self) -> InstagramProof:
        """
        Instagram verisi için comprehensive proof oluşturur.
        """
        
        # Veri hash'lerini hesapla
        profile_hash = self._hash_profile_data()
        posts_hash = self._hash_posts_data()
        stories_hash = self._hash_stories_data()
        comments_hash = self._hash_comments_data()
        dms_hash = self._hash_dms_data()
        
        # Güvenilirlik skorunu hesapla
        confidence_score = self._calculate_confidence_score()
        
        # Doğrulama metodunu belirle
        verification_method = self._determine_verification_method()
        
        proof = InstagramProof(
            user_id=self.data.user_id,
            username_hash=hash_text(self.data.profile.username),
            data_export_timestamp=self.data.data_export_timestamp,
            proof_generation_timestamp=datetime.now().isoformat(),
            
            # Veri sayıları
            total_posts=len(self.data.posts),
            total_stories=len(self.data.stories),
            total_comments=len(self.data.comments),
            total_dms=len(self.data.direct_messages),
            
            # Hesap bilgileri
            follower_count=self.data.profile.follower_count,
            following_count=self.data.profile.following_count,
            is_verified=self.data.profile.is_verified,
            is_private=self.data.profile.is_private,
            
            # Hash'ler
            profile_hash=profile_hash,
            posts_hash=posts_hash,
            stories_hash=stories_hash,
            comments_hash=comments_hash,
            dms_hash=dms_hash,
            
            # Güvenilirlik
            confidence_score=confidence_score,
            verification_method=verification_method
        )
        
        return proof
    
    def _hash_profile_data(self) -> str:
        """Profil verisi için hash oluştur."""
        profile_data = {
            "username": self.data.profile.username,
            "full_name": self.data.profile.full_name,
            "follower_count": self.data.profile.follower_count,
            "following_count": self.data.profile.following_count,
            "post_count": self.data.profile.post_count,
            "is_verified": self.data.profile.is_verified,
            "is_private": self.data.profile.is_private
        }
        return hashlib.sha256(json.dumps(profile_data, sort_keys=True).encode()).hexdigest()
    
    def _hash_posts_data(self) -> str:
        """Posts verisi için hash oluştur."""
        posts_data = []
        for post in self.data.posts:
            post_info = {
                "post_id": post.post_id,
                "timestamp": post.timestamp,
                "like_count": post.like_count,
                "comment_count": post.comment_count,
                "media_count": len(post.media)
            }
            posts_data.append(post_info)
        
        return hashlib.sha256(json.dumps(posts_data, sort_keys=True).encode()).hexdigest()
    
    def _hash_stories_data(self) -> str:
        """Stories verisi için hash oluştur."""
        stories_data = []
        for story in self.data.stories:
            story_info = {
                "story_id": story.story_id,
                "timestamp": story.timestamp,
                "view_count": story.view_count,
                "media_type": story.media_type
            }
            stories_data.append(story_info)
        
        return hashlib.sha256(json.dumps(stories_data, sort_keys=True).encode()).hexdigest()
    
    def _hash_comments_data(self) -> str:
        """Comments verisi için hash oluştur."""
        comments_data = []
        for comment in self.data.comments:
            comment_info = {
                "comment_id": comment.comment_id,
                "post_id": comment.post_id,
                "timestamp": comment.timestamp,
                "like_count": comment.like_count
            }
            comments_data.append(comment_info)
        
        return hashlib.sha256(json.dumps(comments_data, sort_keys=True).encode()).hexdigest()
    
    def _hash_dms_data(self) -> str:
        """Direct messages verisi için hash oluştur."""
        dms_data = []
        for dm in self.data.direct_messages:
            dm_info = {
                "message_id": dm.message_id,
                "conversation_id": dm.conversation_id,
                "timestamp": dm.timestamp,
                "message_type": dm.message_type
            }
            dms_data.append(dm_info)
        
        return hashlib.sha256(json.dumps(dms_data, sort_keys=True).encode()).hexdigest()
    
    def _calculate_confidence_score(self) -> float:
        """
        Verinin güvenilirlik skorunu hesaplar.
        Çeşitli faktörlere göre 0.0-1.0 arası skor verir.
        """
        score = 0.0
        
        # Temel veri varlığı kontrolü
        if self.data.profile:
            score += 0.2
        
        if len(self.data.posts) > 0:
            score += 0.2
        
        if len(self.data.engagement_metrics) > 0:
            score += 0.2
        
        # Veri tutarlılığı kontrolü
        if self.data.profile.post_count == len(self.data.posts):
            score += 0.1
        elif abs(self.data.profile.post_count - len(self.data.posts)) <= 5:
            score += 0.05  # Küçük fark kabul edilebilir
        
        # Zaman damgası tutarlılığı
        if self.data.data_export_timestamp:
            score += 0.1
        
        # Etkileşim verisi tutarlılığı
        if len(self.data.comments) > 0 or len(self.data.direct_messages) > 0:
            score += 0.1
        
        # Doğrulanmış hesap bonusu
        if self.data.profile.is_verified:
            score += 0.1
        
        return min(score, 1.0)
    
    def _determine_verification_method(self) -> str:
        """
        Verinin nasıl doğrulandığını belirler.
        """
        # Engagement metrics varsa muhtemelen resmi export
        if len(self.data.engagement_metrics) > 0:
            return "official_data_export"
        
        # Sadece temel veriler varsa scraping olabilir
        if len(self.data.posts) > 0 and len(self.data.stories) == 0:
            return "api_scraping"
        
        # Comprehensive veri varsa data export
        if (len(self.data.posts) > 0 and 
            len(self.data.comments) > 0 and 
            len(self.data.direct_messages) > 0):
            return "comprehensive_data_export"
        
        return "manual_verification"