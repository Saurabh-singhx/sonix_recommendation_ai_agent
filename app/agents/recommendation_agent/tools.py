from app.core.database import db
from langchain_core.tools import tool
from typing import List
import logging; 

logger = logging.getLogger(__name__)

from functools import wraps

def db_tool_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return f"Error: could not complete {func.__name__.replace('_', ' ')}, please try again."
    return wrapper


@tool
async def get_all_artist_name()->str:
    """fetch all available artist name"""
    artist = await db.artist.find_many()
    if not artist:
        return "no artist found"
    return "\n".join(a.artist_name for a in artist)

@tool
@db_tool_errors
async def get_song_by_genre(input_genre:str) -> str:
    """fetch song by genre"""
    songs_by_genre = await db.song.find_many(
        take=20,                                             #<------fix here
        where={
            "genre":input_genre
        },
        include={
            "artist":True,
            "aiProfile":True
        }
    )

    if not songs_by_genre:
        return f"no songs found for {input_genre} genre"
    
    return "\n".join(
        f"song_id:{s.song_id}, song_name:{s.song_title}, song_tags:{s.tags}, song_genre:{s.genre}, "
        f"song_artist:{s.artist.artist_name if s.artist else 'unknown'}, "
        f"song_language:{s.aiProfile.language if s.aiProfile else 'unknown'}, "
        f"song_energy: {s.aiProfile.energy_level if s.aiProfile else 'unknown'}, "
        for s in songs_by_genre
    )

@tool
@db_tool_errors
async def get_songs_by_popularity_score() -> str:  #   <<<====-----==== Need fixing
    """fetch top 20 songs by their popularity score"""
    songs_by_popularity = await db.song.find_many(
        take=20,
        order={
            "popularity_score":"desc"
        },
        select={
            "song_id":True,
            "song_title":True,
            "tags":True,
            "popularity_score":True,
            "artist":{
                "select":{
                    "artist_name":True
                }
            },
            "aiProfile":{
                "select":{
                    "language":True
                }
            }
        }
    )

    return "\n".join(f"song_id:{s.song_id}, song_Name:{s.song_title}, song_tags:{s.tags}, songs_popularity:{s.popularity_score}"
        f"song_artist:{s.artist.artist_name if s.artist else 'unknown'}, " 
        f"song_language:{s.aiProfile.language if s.aiProfile else 'unknown'}" 
        for s in songs_by_popularity
    )

@tool
@db_tool_errors
async def get_songs_by_likes() -> str:
    """fetch top 20 liked songs of all time"""
    song_by_like = await db.song.find_many(
        take=20,
        order={
            "likedByUsers": {
                "_count": "desc"
            }
        },
        include={
            "artist":True,
            "aiProfile":True,
            "likedByUsers":True
        }
    )

    if not song_by_like:
        return "no liked song found"

    return "\n".join(
        f"song_id:{s.song_id}, song_name:{s.song_title}, song_tags:{s.tags}, song_genre:{s.genre}, "
        f"song_artist:{s.artist.artist_name if s.artist else 'unknown'}, "
        f"song_language:{s.aiProfile.language if s.aiProfile else 'unknown'}, "
        f"song_energy: {s.aiProfile.energy_level if s.aiProfile else 'unknown'}, "
        f"total_likes: {len(s.likedByUsers) if s.likedByUsers else 0}, "
        for s in song_by_like
    )

@tool
@db_tool_errors
async def get_user_taste_summary(userId:str)->str:
    """fetch users song taste summary"""
    taste_summary = await db.user.find_unique(
        where={
            "user_id":userId
        },
        include={
            "tasteSummaries":True
        }
    )

    if not taste_summary:
        return "no taste summary for this user"
    
    return f"user taste summary:{taste_summary.tasteSummaries[0].summary_text if taste_summary.tasteSummaries else "no summary added for this user"}"

@tool
@db_tool_errors
async def get_todays_trending_song()->str:
    """fetch todays top 10 trending songs"""
    trending_songs = await db.trendingsongs.find_many(
        take=10,
        order={
            "score":"desc"
        },
        include={
            "song":{
                "include":{
                    "aiProfile":True,
                    "artist":True
                }
            }
        }
    )
    return "\n".join(
        f"song_today's_score: {s.score}, "
        f"song_id:{s.song.song_id}, song_name:{s.song.song_title}, song_tags:{s.song.tags}, song_genre:{s.song.genre}, "
        f"song_artist:{s.song.artist.artist_name if s.song.artist else 'unknown'}, "
        f"song_language:{s.song.aiProfile.language if s.song.aiProfile else 'unknown'}, "
        f"song_energy: {s.song.aiProfile.energy_level if s.song.aiProfile else 'unknown'}, "
        for s in trending_songs
    )

@tool
@db_tool_errors
async def get_most_repeated_song() -> str:
    """fetch top 20 most repeated songs"""
    grouped_songs = await db.usersongevent.group_by(
        by=["song_id"],
        where={"event_type": "REPEAT"},
        count={"song_id": True},
        order={"_count": {"song_id": "desc"}},
        take=20
    )

    if not grouped_songs:
        return "no repeated songs found"

    song_ids = [g["song_id"] for g in grouped_songs]
    count_map = {g["song_id"]: g["_count"]["song_id"] for g in grouped_songs}

    most_repeated_songs = await db.song.find_many(
        where={"song_id": {"in": song_ids}},
        include={                                   #using include because we dont have select in python prisma
            "artist": True,
            "aiProfile": True,
        }
    )

    most_repeated_songs.sort(key=lambda s: count_map.get(s.song_id, 0), reverse=True)

    return "\n".join(
        f"song_id:{s.song_id}, song_name:{s.song_title}, song_tags:{s.tags}, "
        f"repeat_count:{count_map.get(s.song_id, 0)}, "
        f"song_artist:{s.artist.artist_name if s.artist else 'unknown'}, "
        f"song_language:{s.aiProfile.language if s.aiProfile else 'unknown'}"
        for s in most_repeated_songs
    )

@tool
@db_tool_errors
async def get_users_recent_liked_songs(userId:str) ->str:
    """fetch user last 20 liked songs"""
    recent_liked_songs = await db.likedsong.find_many(
        where={
            "user_id":userId
        },
        order={
            "liked_at":"asc"
        },
        take=20,
        include={
            "song":{
                "include":{
                    "aiProfile":True,
                    "artist":True,
                }
            }
        }
    )

    if not recent_liked_songs:
        return "no liked song found for this user"
    
    return "\n".join(
        f"song_id:{s.song.song_id}, song_name:{s.song.song_title}, song_tags:{s.song.tags}, song_genre:{s.song.genre}, "
        f"song_artist:{s.song.artist.artist_name if s.song.artist else 'unknown'}, "
        f"song_language:{s.song.aiProfile.language if s.song.aiProfile else 'unknown'}"
        f"song_energy: {s.song.aiProfile.energy_level if s.song.aiProfile else 'unknown'}"
        for s in recent_liked_songs
    )

@tool
@db_tool_errors
async def get_user_recent_completed_songs(userId:str) ->str:
    """fetch users 20 recent completed songs"""
    completed_songs_details = await db.usersongevent.find_many(
        where={
            "user_id":userId,
            "event_type":"COMPLETE"
        },
        order={
            "created_at":"asc"
        },
        include={
            "song":{
                "include":{
                    "aiProfile":True,
                    "artist":True
                }
            }
        },
        take=20
    )

    if not completed_songs_details:
        return "no completed song found for this user"
    
    return "\n".join(
        f"song_id:{s.song.song_id}, song_name:{s.song.song_title}, song_tags:{s.song.tags}, song_genre:{s.song.genre}, "
        f"song_artist:{s.song.artist.artist_name if s.song.artist else 'unknown'}, "
        f"song_language:{s.song.aiProfile.language if s.song.aiProfile else 'unknown'}"
        f"song_energy: {s.song.aiProfile.energy_level if s.song.aiProfile else 'unknown'}"
        for s in completed_songs_details
    )

@tool
@db_tool_errors
async def get_users_recent_skipped_songs(userId:str) -> str:
    """fetch users 20 recent skipped songs"""

    skipped_songs = await db.usersongevent.find_many(
        where={
            "user_id":userId,
            "event_type":"SKIP"
        },
        order={
            "created_at":"asc"
        },
        include={
            "song":{
                "include":{
                    "aiProfile":True,
                    "artist":True
                }
            }
        },
        take=20
    )

    if not skipped_songs:
        return "no skipped song found for this user"
    
    return "\n".join(
        f"song_id:{s.song.song_id}, song_name:{s.song.song_title}, song_tags:{s.song.tags}, song_genre:{s.song.genre}, "
        f"song_artist:{s.song.artist.artist_name if s.song.artist else 'unknown'}, "
        f"song_language:{s.song.aiProfile.language if s.song.aiProfile else 'unknown'}"
        f"song_energy: {s.song.aiProfile.energy_level if s.song.aiProfile else 'unknown'}"
        for s in skipped_songs
    )

# @tool
#@db_tool_errors
# async def get_songs_by_listning_duration() ->str:
#     """fetch top 20 songs by listning time"""

#     songs_details_by_listning_time = await db.song.find_many(
        
#     )

@tool
@db_tool_errors
async def get_songs_by_tags(input_tags: List[str])->str:
    """fetch songs 20 songs by tags"""

    songs_by_tags = await db.song.find_many(
        where={
            "tags":{
                "has_some":input_tags
            }
        },
        take=20,
        include={
            "aiProfile":True,
            "artist":True
        }
    )

    if not songs_by_tags:
        return f"no song found for tag : {input_tags}"
    
    return "\n".join(
        f"song_id:{s.song_id}, song_name:{s.song_title}, song_tags:{s.tags}, song_genre:{s.genre}, "
        f"song_artist:{s.artist.artist_name if s.artist else 'unknown'}, "
        f"song_language:{s.aiProfile.language if s.aiProfile else 'unknown'}, "
        f"song_energy: {s.aiProfile.energy_level if s.aiProfile else 'unknown'}, "
        for s in songs_by_tags
    )

@tool
@db_tool_errors
async def get_songs_by_mood(input_mood:str)->str:
    """fetch 20 songs by mood"""

    songs_by_mood = await db.songaiprofile.find_many(
        where={
            "mood":input_mood
        },
        take=20,
        include={
            "song":{
                "include":{
                    "artist":True
                }
            }
        }
    )

    if not songs_by_mood:
        return f"no song found for mood : {input_mood}"
    
    return "\n".join(
        f"song_id:{s.song.song_id}, song_name:{s.song.song_title}, song_tags:{s.song.tags}, song_genre:{s.song.genre}, "
        f"song_artist:{s.song.artist.artist_name if s.song.artist else 'unknown'}, "
        f"song_language:{s.language},song_energy:{s.energy_level} "
        for s in songs_by_mood
    )

@tool
@db_tool_errors
async def get_songs_by_energy_level(input_energy_level: str) -> str:
    """fetch 20 songs by energy level"""
    songs_by_energy_level = await db.songaiprofile.find_many(
            where={
                "energy_level": input_energy_level
            },
            take=20,
            include={
                "song": {
                    "include": {
                        "artist": True
                    }
                }
            }
    )

    if not songs_by_energy_level:
        return f"no song found for energy_level: {input_energy_level}"

    return "\n".join(
            f"song_id:{s.song.song_id}, song_name:{s.song.song_title}, song_tags:{s.song.tags}, song_genre:{s.song.genre}, "
            f"song_artist:{s.song.artist.artist_name if s.song.artist else 'unknown'}, "
            f"song_language:{s.language}, song_energy:{s.energy_level} "
            for s in songs_by_energy_level
    )