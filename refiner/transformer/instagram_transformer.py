from typing import Dict, Any, List
from collections import defaultdict
import hashlib
from datetime import datetime, timedelta

from refiner.models.refined import Base
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.refined import (
    UserProfileRefined, PostRefined, MediaRefined, StoryRefined, 
    CommentRefined, DirectMessageRefined, EngagementMetricRefined,
    HashtagUsageRefined, ActivityPatternRefined
)
from refiner.models.unrefined import InstagramData
from refiner.utils.date import parse_timestamp
from refiner.utils.pii import hash_text

class InstagramTransformer(DataTransformer):
    """
    Transformer for Instagram data with privacy-focused refinement.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw Instagram data into SQLAlchemy model instances.
        
        Args:
            data: Dictionary containing Instagram data
            
        Returns:
            List of SQLAlchemy model instances
        """
        # Validate data with Pydantic
        instagram_data = InstagramData.model_validate(data)
        export_date = parse_timestamp(instagram_data.data_export_timestamp)
        
        models = []
        
        # Create user profile
        user_profile = self._create_user_profile(instagram_data, export_date)
        models.append(user_profile)
        
        # Process posts
        models.extend(self._create_posts(instagram_data))
        
        # Process stories
        models.extend(self._create_stories(instagram_data))
        
        # Process comments
        models.extend(self._create_comments(instagram_data))
        
        # Process direct messages
        models.extend(self._create_direct_messages(instagram_data))
        
        # Process engagement metrics
        models.extend(self._create_engagement_metrics(instagram_data))
        
        # Create hashtag usage analytics
        models.extend(self._create_hashtag_usage(instagram_data))
        
        # Create activity patterns
        models.extend(self._create_activity_patterns(instagram_data))
        
        return models
    
    def _create_user_profile(self, data: InstagramData, export_date: datetime) -> UserProfileRefined:
        """Create user profile with privacy-focused data."""
        profile = data.profile
        
        return UserProfileRefined(
            user_id=data.user_id,
            username_hash=hash_text(profile.username),
            full_name_hash=hash_text(profile.full_name),
            bio_length=len(profile.bio) if profile.bio else 0,
            follower_count=profile.follower_count,
            following_count=profile.following_count,
            post_count=profile.post_count,
            is_verified=profile.is_verified,
            is_private=profile.is_private,
            data_export_date=export_date
        )
    
    def _create_posts(self, data: InstagramData) -> List[Base]:
        """Create post records with media information."""
        models = []
        
        for post in data.posts:
            post_date = parse_timestamp(post.timestamp)
            
            # Calculate engagement rate
            total_followers = data.profile.follower_count
            engagement_rate = ((post.like_count + post.comment_count) / total_followers * 100) if total_followers > 0 else 0
            
            post_refined = PostRefined(
                post_id=post.post_id,
                user_id=data.user_id,
                caption_length=len(post.caption) if post.caption else 0,
                post_date=post_date,
                like_count=post.like_count,
                comment_count=post.comment_count,
                media_count=len(post.media),
                has_location=bool(post.location),
                hashtag_count=len(post.hashtags),
                engagement_rate=engagement_rate
            )
            models.append(post_refined)
            
            # Create media records
            for media in post.media:
                media_refined = MediaRefined(
                    post_id=post.post_id,
                    media_type=media.media_type
                )
                models.append(media_refined)
        
        return models
    
    def _create_stories(self, data: InstagramData) -> List[StoryRefined]:
        """Create story records."""
        models = []
        
        for story in data.stories:
            story_date = parse_timestamp(story.timestamp)
            
            story_refined = StoryRefined(
                story_id=story.story_id,
                user_id=data.user_id,
                story_date=story_date,
                media_type=story.media_type,
                view_count=story.view_count
            )
            models.append(story_refined)
        
        return models
    
    def _create_comments(self, data: InstagramData) -> List[CommentRefined]:
        """Create comment records with privacy protection."""
        models = []
        
        for comment in data.comments:
            comment_date = parse_timestamp(comment.timestamp)
            
            comment_refined = CommentRefined(
                comment_id=comment.comment_id,
                user_id=data.user_id,
                post_id=comment.post_id,
                comment_length=len(comment.text),
                comment_date=comment_date,
                like_count=comment.like_count,
                author_username_hash=hash_text(comment.author_username)
            )
            models.append(comment_refined)
        
        return models
    
    def _create_direct_messages(self, data: InstagramData) -> List[DirectMessageRefined]:
        """Create direct message records with privacy protection."""
        models = []
        
        for dm in data.direct_messages:
            message_date = parse_timestamp(dm.timestamp)
            
            dm_refined = DirectMessageRefined(
                message_id=dm.message_id,
                user_id=data.user_id,
                conversation_id_hash=hash_text(dm.conversation_id),
                message_length=len(dm.message_text) if dm.message_text else 0,
                message_date=message_date,
                message_type=dm.message_type,
                is_sender=(dm.sender_username == data.profile.username)
            )
            models.append(dm_refined)
        
        return models
    
    def _create_engagement_metrics(self, data: InstagramData) -> List[EngagementMetricRefined]:
        """Create engagement metric records."""
        models = []
        
        for metric in data.engagement_metrics:
            metric_date = parse_timestamp(metric.date)
            
            engagement_refined = EngagementMetricRefined(
                user_id=data.user_id,
                metric_date=metric_date,
                profile_views=metric.profile_views,
                reach=metric.reach,
                impressions=metric.impressions,
                website_clicks=metric.website_clicks
            )
            models.append(engagement_refined)
        
        return models
    
    def _create_hashtag_usage(self, data: InstagramData) -> List[HashtagUsageRefined]:
        """Analyze hashtag usage patterns."""
        models = []
        hashtag_stats = defaultdict(lambda: {'count': 0, 'first_used': None, 'last_used': None})
        
        for post in data.posts:
            post_date = parse_timestamp(post.timestamp)
            for hashtag in post.hashtags:
                hashtag_hash = hash_text(hashtag.lower())
                stats = hashtag_stats[hashtag_hash]
                stats['count'] += 1
                
                if stats['first_used'] is None or post_date < stats['first_used']:
                    stats['first_used'] = post_date
                if stats['last_used'] is None or post_date > stats['last_used']:
                    stats['last_used'] = post_date
        
        for hashtag_hash, stats in hashtag_stats.items():
            hashtag_usage = HashtagUsageRefined(
                user_id=data.user_id,
                hashtag_hash=hashtag_hash,
                usage_count=stats['count'],
                first_used=stats['first_used'],
                last_used=stats['last_used']
            )
            models.append(hashtag_usage)
        
        return models
    
    def _create_activity_patterns(self, data: InstagramData) -> List[ActivityPatternRefined]:
        """Analyze user activity patterns by hour and day."""
        models = []
        activity_patterns = defaultdict(lambda: {
            'post_count': 0, 'story_count': 0, 'comment_count': 0, 'dm_count': 0
        })
        
        # Analyze posts
        for post in data.posts:
            post_date = parse_timestamp(post.timestamp)
            key = (post_date.hour, post_date.weekday())
            activity_patterns[key]['post_count'] += 1
        
        # Analyze stories
        for story in data.stories:
            story_date = parse_timestamp(story.timestamp)
            key = (story_date.hour, story_date.weekday())
            activity_patterns[key]['story_count'] += 1
        
        # Analyze comments
        for comment in data.comments:
            comment_date = parse_timestamp(comment.timestamp)
            key = (comment_date.hour, comment_date.weekday())
            activity_patterns[key]['comment_count'] += 1
        
        # Analyze DMs
        for dm in data.direct_messages:
            dm_date = parse_timestamp(dm.timestamp)
            key = (dm_date.hour, dm_date.weekday())
            activity_patterns[key]['dm_count'] += 1
        
        for (hour, day), counts in activity_patterns.items():
            pattern = ActivityPatternRefined(
                user_id=data.user_id,
                hour_of_day=hour,
                day_of_week=day,
                post_count=counts['post_count'],
                story_count=counts['story_count'],
                comment_count=counts['comment_count'],
                dm_count=counts['dm_count']
            )
            models.append(pattern)
        
        return models