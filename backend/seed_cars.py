#!/usr/bin/env python3

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import requests

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Sample car data with Unsplash images
SAMPLE_CARS = [
    {
        "make": "Lamborghini",
        "model": "Aventador",
        "year": 2023,
        "image_url": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1074&q=80"
    },
    {
        "make": "Ferrari",
        "model": "F8 Tributo",
        "year": 2022,
        "image_url": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "Porsche",
        "model": "911 Turbo S",
        "year": 2023,
        "image_url": "https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1174&q=80"
    },
    {
        "make": "McLaren",
        "model": "720S",
        "year": 2022,
        "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "BMW",
        "model": "M4 Competition",
        "year": 2023,
        "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "Audi",
        "model": "R8",
        "year": 2022,
        "image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "Mercedes-AMG",
        "model": "GT 63 S",
        "year": 2023,
        "image_url": "https://images.unsplash.com/photo-1606016159991-62ab9b123cb4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "Jaguar",
        "model": "F-Type R",
        "year": 2022,
        "image_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "Aston Martin",
        "model": "DB11",
        "year": 2023,
        "image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    },
    {
        "make": "Bugatti",
        "model": "Chiron",
        "year": 2022,
        "image_url": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1074&q=80"
    }
]

async def seed_cars():
    """Seed the database with initial car data"""
    try:
        # Check if cars already exist
        existing_count = await db.cars.count_documents({})
        if existing_count > 0:
            print(f"Database already contains {existing_count} cars. Skipping seed.")
            return

        # Import Car model
        import sys
        sys.path.append(str(ROOT_DIR))
        from server import Car

        # Add cars to database
        cars_to_insert = []
        for car_data in SAMPLE_CARS:
            car = Car(**car_data)
            cars_to_insert.append(car.dict())

        result = await db.cars.insert_many(cars_to_insert)
        print(f"Successfully inserted {len(result.inserted_ids)} cars into the database.")

        # Display inserted cars
        for i, car_data in enumerate(SAMPLE_CARS):
            print(f"  {i+1}. {car_data['year']} {car_data['make']} {car_data['model']}")

    except Exception as e:
        print(f"Error seeding cars: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_cars())