from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base model for SQLAlchemy
Base = declarative_base()

class UserProfileRefined(Base):
    __tablename__ = 'user_profiles'
    
    user_id = Column(String, primary_key=True)
    username_hash = Column(String, nullable=False)  # Hashed for privacy
    full_name_hash = Column(String, nullable=False)  # Hashed for privacy
    bio_length = Column(Integer, nullable=True)  # Length instead of actual bio
    follower_count = Column(Integer, nullable=False)
    following_count = Column(Integer, nullable=False)
    post_count = Column(Integer, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_private = Column(Boolean, default=False)
    account_age_days = Column(Integer, nullable=True)
    data_export_date = Column(DateTime, nullable=False)
    
    posts = relationship("PostRefined", back_populates="user")
    stories = relationship("StoryRefined", back_populates="user")
    comments = relationship("CommentRefined", back_populates="user")
    engagement_metrics = relationship("EngagementMetricRefined", back_populates="user")

class PostRefined(Base):
    __tablename__ = 'posts'
    
    post_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    caption_length = Column(Integer, nullable=True)  # Length instead of actual caption
    post_date = Column(DateTime, nullable=False)
    like_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    media_count = Column(Integer, nullable=False)
    has_location = Column(Boolean, default=False)
    hashtag_count = Column(Integer, default=0)
    engagement_rate = Column(Float, nullable=True)  # Calculated metric
    
    user = relationship("UserProfileRefined", back_populates="posts")
    media_items = relationship("MediaRefined", back_populates="post")

class MediaRefined(Base):
    __tablename__ = 'media'
    
    media_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(String, ForeignKey('posts.post_id'), nullable=False)
    media_type = Column(String, nullable=False)  # photo, video, carousel
    
    post = relationship("PostRefined", back_populates="media_items")

class StoryRefined(Base):
    __tablename__ = 'stories'
    
    story_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    story_date = Column(DateTime, nullable=False)
    media_type = Column(String, nullable=False)
    view_count = Column(Integer, nullable=False)
    
    user = relationship("UserProfileRefined", back_populates="stories")

class CommentRefined(Base):
    __tablename__ = 'comments'
    
    comment_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    post_id = Column(String, nullable=False)
    comment_length = Column(Integer, nullable=False)  # Length instead of actual text
    comment_date = Column(DateTime, nullable=False)
    like_count = Column(Integer, default=0)
    author_username_hash = Column(String, nullable=False)  # Hashed for privacy
    
    user = relationship("UserProfileRefined", back_populates="comments")

class DirectMessageRefined(Base):
    __tablename__ = 'direct_messages'
    
    message_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    conversation_id_hash = Column(String, nullable=False)  # Hashed for privacy
    message_length = Column(Integer, nullable=True)  # Length instead of actual message
    message_date = Column(DateTime, nullable=False)
    message_type = Column(String, nullable=False)
    is_sender = Column(Boolean, nullable=False)  # True if user sent, False if received

class EngagementMetricRefined(Base):
    __tablename__ = 'engagement_metrics'
    
    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    metric_date = Column(DateTime, nullable=False)
    profile_views = Column(Integer, nullable=False)
    reach = Column(Integer, nullable=False)
    impressions = Column(Integer, nullable=False)
    website_clicks = Column(Integer, default=0)
    
    user = relationship("UserProfileRefined", back_populates="engagement_metrics")

class HashtagUsageRefined(Base):
    __tablename__ = 'hashtag_usage'
    
    usage_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    hashtag_hash = Column(String, nullable=False)  # Hashed hashtag for privacy
    usage_count = Column(Integer, nullable=False)
    first_used = Column(DateTime, nullable=False)
    last_used = Column(DateTime, nullable=False)

class ActivityPatternRefined(Base):
    __tablename__ = 'activity_patterns'
    
    pattern_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('user_profiles.user_id'), nullable=False)
    hour_of_day = Column(Integer, nullable=False)  # 0-23
    day_of_week = Column(Integer, nullable=False)  # 0-6 (Monday=0)
    post_count = Column(Integer, default=0)
    story_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    dm_count = Column(Integer, default=0)