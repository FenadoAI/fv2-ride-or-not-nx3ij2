#!/usr/bin/env python3

import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8001/api"

async def test_car_api():
    """Test the car rating API endpoints"""
    async with aiohttp.ClientSession() as session:

        print("🧪 Testing Car Rating API")
        print("=" * 40)

        # Test 1: Get random car
        print("1️⃣ Testing GET /cars/random")
        try:
            async with session.get(f"{BASE_URL}/cars/random") as response:
                if response.status == 200:
                    car_data = await response.json()
                    print(f"✅ Got random car: {car_data['year']} {car_data['make']} {car_data['model']}")
                    car_id = car_data['id']
                else:
                    print(f"❌ Failed with status: {response.status}")
                    return
        except Exception as e:
            print(f"❌ Error: {e}")
            return

        # Test 2: Vote "hot" on the car
        print("\n2️⃣ Testing POST /cars/vote (hot)")
        try:
            vote_data = {
                "car_id": car_id,
                "vote_type": "hot"
            }
            async with session.post(f"{BASE_URL}/cars/vote", json=vote_data) as response:
                if response.status == 200:
                    vote_result = await response.json()
                    car_info = vote_result['car']
                    print(f"✅ Hot vote recorded!")
                    print(f"   Score: {car_info['hot_percentage']}% Hot")
                    print(f"   Votes: {car_info['hot_votes']} hot, {car_info['not_votes']} not")
                else:
                    print(f"❌ Failed with status: {response.status}")
                    return
        except Exception as e:
            print(f"❌ Error: {e}")
            return

        # Test 3: Vote "not" on the same car
        print("\n3️⃣ Testing POST /cars/vote (not)")
        try:
            vote_data = {
                "car_id": car_id,
                "vote_type": "not"
            }
            async with session.post(f"{BASE_URL}/cars/vote", json=vote_data) as response:
                if response.status == 200:
                    vote_result = await response.json()
                    car_info = vote_result['car']
                    print(f"✅ Not vote recorded!")
                    print(f"   Score: {car_info['hot_percentage']}% Hot")
                    print(f"   Votes: {car_info['hot_votes']} hot, {car_info['not_votes']} not")
                else:
                    print(f"❌ Failed with status: {response.status}")
                    return
        except Exception as e:
            print(f"❌ Error: {e}")
            return

        # Test 4: Get another random car to verify randomness
        print("\n4️⃣ Testing randomness - GET /cars/random again")
        try:
            async with session.get(f"{BASE_URL}/cars/random") as response:
                if response.status == 200:
                    car_data2 = await response.json()
                    print(f"✅ Got another car: {car_data2['year']} {car_data2['make']} {car_data2['model']}")
                    if car_data2['id'] != car_id:
                        print("✅ Randomness working - different car returned")
                    else:
                        print("⚠️  Same car returned (could be random chance)")
                else:
                    print(f"❌ Failed with status: {response.status}")
        except Exception as e:
            print(f"❌ Error: {e}")

        print("\n🎉 API testing complete!")

if __name__ == "__main__":
    asyncio.run(test_car_api())