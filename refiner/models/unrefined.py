from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class InstagramProfile(BaseModel):
    username: str
    full_name: str
    bio: Optional[str] = None
    follower_count: int
    following_count: int
    post_count: int
    is_verified: bool = False
    is_private: bool = False
    profile_pic_url: Optional[str] = None

class PostMedia(BaseModel):
    media_type: str  # photo, video, carousel
    url: str
    thumbnail_url: Optional[str] = None

class InstagramPost(BaseModel):
    post_id: str
    caption: Optional[str] = None
    timestamp: str
    like_count: int
    comment_count: int
    media: List[PostMedia]
    location: Optional[str] = None
    hashtags: List[str] = []

class InstagramStory(BaseModel):
    story_id: str
    timestamp: str
    media_type: str  # photo, video
    view_count: int
    media_url: str

class InstagramComment(BaseModel):
    comment_id: str
    post_id: str
    text: str
    timestamp: str
    like_count: int = 0
    author_username: str

class InstagramDM(BaseModel):
    message_id: str
    conversation_id: str
    sender_username: str
    recipient_username: str
    message_text: Optional[str] = None
    timestamp: str
    message_type: str  # text, media, link

class InstagramEngagement(BaseModel):
    date: str
    profile_views: int
    reach: int
    impressions: int
    website_clicks: int = 0

class InstagramData(BaseModel):
    user_id: str
    profile: InstagramProfile
    posts: List[InstagramPost] = []
    stories: List[InstagramStory] = []
    comments: List[InstagramComment] = []
    direct_messages: List[InstagramDM] = []
    engagement_metrics: List[InstagramEngagement] = []
    data_export_timestamp: str