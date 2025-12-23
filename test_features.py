import httpx
import asyncio
import sys

BASE_URL = "http://127.0.0.1:8000"

async def test_full_flow():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # 1. Auth Flow
        email = "test_features@example.com"
        password = "newpassword"
        
        # Register
        print(f"1. Registering: {email}")
        response = await client.post("/register", json={"email": email, "password": password})
        if response.status_code == 200:
            print("   Registered successfully")
        elif response.status_code == 400 and "registered" in response.text:
            print("   Already registered")
        else:
            print(f"   Failed: {response.text}")
            sys.exit(1)

        # Login
        print("2. Logging in")
        response = await client.post("/login", data={"username": email, "password": password})
        if response.status_code != 200:
            print(f"   Login failed: {response.text}")
            sys.exit(1)
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   Logged in successfully")

        # 2. Profile Management
        print("3. Updating Profile")
        profile_data = {
            "first_name": "Test",
            "last_name": "User",
            "age": 25,
            "phone": "1234567890"
        }
        response = await client.put("/users/me", json=profile_data, headers=headers)
        if response.status_code == 200 and response.json()["first_name"] == "Test":
             print("   Profile updated successfully")
        else:
             print(f"   Profile update failed: {response.text}")
             sys.exit(1)

        # 3. Server CRUD
        print("4. Creating Server")
        server_data = {"name": "Test Server", "ip_address": "192.168.1.1"}
        response = await client.post("/servers/", json=server_data, headers=headers)
        if response.status_code == 200:
            server_id = response.json()["id"]
            print(f"   Server created: {server_id}")
        else:
            print(f"   Server creation failed: {response.text}")
            sys.exit(1)

        print("5. Getting Servers")
        response = await client.get("/servers/", headers=headers)
        if response.status_code == 200 and len(response.json()) > 0:
            print(f"   Got {len(response.json())} servers")
        else:
            print(f"   Get servers failed: {response.text}")
            sys.exit(1)
            
        print("6. Deleting Server")
        response = await client.delete(f"/servers/{server_id}", headers=headers)
        if response.status_code == 200:
            print("   Server deleted successfully")
        else:
            print(f"   Delete server failed: {response.text}")
            sys.exit(1)
            
        print("Verification Suite Passed!")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
