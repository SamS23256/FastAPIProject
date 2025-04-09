from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from bson import ObjectId
import motor.motor_asyncio

app = FastAPI()

# Connect to Mongo Atlas
client = motor.motor_asyncio.AsyncIOMotorClient("your_mongo_connection_string")
db = client.multimedia_db


class PlayerScore(BaseModel):
    player_name: str
    score: int


@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}


@app.put("/upload_sprite/{sprite_id}")
async def update_sprite(sprite_id: str, file: UploadFile = File(...)):
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.update_one({"_id": ObjectId(sprite_id)}, {"$set": sprite_doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"message": "Sprite updated"}


@app.get("/upload_sprite/{sprite_id}")
async def get_sprite(sprite_id: str):
    sprite = await db.sprites.find_one({"_id": ObjectId(sprite_id)})
    if not sprite:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"filename": sprite["filename"], "content": sprite["content"]}


@app.delete("/upload_sprite/{sprite_id}")
async def delete_sprite(sprite_id: str):
    result = await db.sprites.delete_one({"_id": ObjectId(sprite_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"message": "Sprite deleted"}


@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}


@app.put("/upload_audio/{audio_id}")
async def update_audio(audio_id: str, file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.update_one({"_id": ObjectId(audio_id)}, {"$set": audio_doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return {"message": "Audio file updated"}


@app.get("/upload_audio/{audio_id}")
async def get_audio(audio_id: str):
    audio = await db.audio.find_one({"_id": ObjectId(audio_id)})
    if not audio:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return {"filename": audio["filename"], "content": audio["content"]}


@app.delete("/upload_audio/{audio_id}")
async def delete_audio(audio_id: str):
    result = await db.audio.delete_one({"_id": ObjectId(audio_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return {"message": "Audio file deleted"}


@app.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}


@app.put("/player_score/{score_id}")
async def update_score(score_id: str, score: PlayerScore):
    score_doc = score.dict()
    result = await db.scores.update_one({"_id": ObjectId(score_id)}, {"$set": score_doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"message": "Score updated"}


@app.get("/player_score/{score_id}")
async def get_score(score_id: str):
    score = await db.scores.find_one({"_id": ObjectId(score_id)})
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"player_name": score["player_name"], "score": score["score"]}


@app.delete("/player_score/{score_id}")
async def delete_score(score_id: str):
    result = await db.scores.delete_one({"_id": ObjectId(score_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"message": "Score deleted"}
