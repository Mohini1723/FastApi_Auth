from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import ObjectId
from app.schemas import ServerCreate, ServerUpdate, ServerResponse, UserInDB
from app.database import db
from app.auth import get_current_user

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.get("/", response_model=List[ServerResponse])
async def get_servers(current_user: UserInDB = Depends(get_current_user)):
    servers = await db.servers.find({"owner_email": current_user.email}).to_list(100)
    return [ServerResponse(**server, id=str(server["_id"])) for server in servers]

@router.post("/", response_model=ServerResponse)
async def create_server(server: ServerCreate, current_user: UserInDB = Depends(get_current_user)):
    server_data = server.dict()
    server_data["owner_email"] = current_user.email
    result = await db.servers.insert_one(server_data)
    created_server = await db.servers.find_one({"_id": result.inserted_id})
    return ServerResponse(**created_server, id=str(created_server["_id"]))

@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(server_id: str, current_user: UserInDB = Depends(get_current_user)):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
        
    server = await db.servers.find_one({"_id": obj_id, "owner_email": current_user.email})
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return ServerResponse(**server, id=str(server["_id"]))

@router.put("/{server_id}", response_model=ServerResponse)
async def update_server(
    server_id: str, 
    server_update: ServerUpdate, 
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
    
    update_data = {k: v for k, v in server_update.dict().items() if v is not None}
    
    if update_data:
        result = await db.servers.update_one(
            {"_id": obj_id, "owner_email": current_user.email},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Server not found")
            
    updated_server = await db.servers.find_one({"_id": obj_id})
    return ServerResponse(**updated_server, id=str(updated_server["_id"]))

@router.delete("/{server_id}")
async def delete_server(server_id: str, current_user: UserInDB = Depends(get_current_user)):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
        
    result = await db.servers.delete_one({"_id": obj_id, "owner_email": current_user.email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"message": "Server deleted successfully"}
