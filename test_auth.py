import httpx
import asyncio
import sys

BASE_URL = "http://127.0.0.1:8000"

async def test_auth_flow():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # 1. Register
        email = "test@example.com"
        password = "strongpassword"
        print(f"Registering user: {email}")
        response = await client.post("/register", json={"email": email, "password": password})
        if response.status_code == 400 and "already registered" in response.text:
             print("User already registered, proceeding to login.")
        else:
             print(f"Register Response: {response.status_code} - {response.json()}")
             if response.status_code != 200:
                 print("Registration failed")
                 sys.exit(1)

        # 2. Login
        print("Logging in...")
        response = await client.post("/login", data={"username": email, "password": password})
        print(f"Login Response: {response.status_code} - {response.json()}")
        if response.status_code != 200:
            print("Login failed")
            sys.exit(1)
        
        token_data = response.json()
        if "access_token" not in token_data:
            print("No access token in response")
            sys.exit(1)
        
        token = token_data["access_token"]
        print("Received Token")

        # 3. Protected Route
        print("Accessing protected route...")
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/users/me", headers=headers)
        print(f"Protected Route Response: {response.status_code} - {response.json()}")
        if response.status_code != 200:
            print("Protected route access failed")
            sys.exit(1)
            
        user_data = response.json()
        if user_data["email"] != email:
            print("User data mismatch")
            sys.exit(1)
            
        print("Verification Successful!")

if __name__ == "__main__":
    asyncio.run(test_auth_flow())
