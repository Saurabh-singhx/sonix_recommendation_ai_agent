# test_tools.py
import asyncio
from app.core.database import connect_db, disconnect_db
from app.agents.recommendation_agent.tools import (
    get_users_recent_liked_songs,
    get_most_repeated_song,
    get_user_recent_completed_songs,
    get_users_recent_skipped_songs,
    get_song_by_genre,
    get_songs_by_likes,
    get_user_taste_summary,
    get_todays_trending_song,
    get_songs_by_tags,
    get_songs_by_mood,
    get_songs_by_energy_level
)

async def get_most_repeated_song_test():
    await connect_db()                           
    print("DB connected")
    
    result = await get_most_repeated_song.ainvoke({})
    print(result)
    
    await disconnect_db()                       

async def get_users_recent_liked_songs_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_users_recent_liked_songs.ainvoke("9579e799-e046-4d6a-a0b6-f9fa79017205")
    print(result)
    
    await disconnect_db()    

async def get_user_recent_completed_songs_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_user_recent_completed_songs.ainvoke("9579e799-e046-4d6a-a0b6-f9fa79017205")
    print(result)
    
    await disconnect_db()

async def get_users_recent_skipped_songs_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_users_recent_skipped_songs.ainvoke("9579e799-e046-4d6a-a0b6-f9fa79017205")
    print(result)
    
    await disconnect_db() 

async def get_song_by_genre_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_song_by_genre.ainvoke("Pop")
    print(result)
    
    await disconnect_db() 

async def get_songs_by_likes_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_songs_by_likes.ainvoke({})
    print(result)
    
    await disconnect_db() 

async def get_user_taste_summary_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_user_taste_summary.ainvoke({"userId":'9579e799-e046-4d6a-a0b6-f9fa79017205'})
    print(result)
    
    await disconnect_db() 

async def get_todays_trending_song_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_todays_trending_song.ainvoke({})
    print(result)
    
    await disconnect_db() 

async def get_songs_by_tags_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_songs_by_tags.ainvoke({"input_tags": ["english"]})
    print(result)
    
    await disconnect_db() 

async def get_songs_by_mood_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_songs_by_mood.ainvoke({"input_mood": "Romantic"})
    print(result)
    
    await disconnect_db() 

async def get_songs_by_energy_level_test():
    await connect_db()                            
    print("DB connected")
    
    result = await get_songs_by_energy_level.ainvoke({"input_energy_level": "High"})
    print(result)
    
    await disconnect_db() 

asyncio.run(get_songs_by_energy_level_test())