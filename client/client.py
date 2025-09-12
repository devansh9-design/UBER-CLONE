import requests
import json
from typing import Dict, Any

class MiniUberClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def ping(self, data: str = "ping") -> Dict[str, Any]:
        """Send ping request to the server"""
        url = f"{self.base_url}/api/ping"
        payload = {"data": data}
        try:
            response = self.session.post(
                url, 
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def health_check(self) -> Dict[str, Any]:
        """Check server health"""
        url = f"{self.base_url}/api/health"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Health check failed: {str(e)}"}

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        url = f"{self.base_url}/api/users/"
        try:
            response = self.session.post(
                url,
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Create user failed: {str(e)}"}

    def get_users(self) -> Dict[str, Any]:
        """Get all users"""
        url = f"{self.base_url}/api/users/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Get users failed: {str(e)}"}

    def create_ride(self, ride_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new ride"""
        url = f"{self.base_url}/api/rides/"
        try:
            response = self.session.post(
                url,
                json=ride_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Create ride failed: {str(e)}"}

    def get_available_rides(self) -> Dict[str, Any]:
        """Get available rides"""
        url = f"{self.base_url}/api/rides/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Get rides failed: {str(e)}"}

    def accept_ride(self, ride_id: int, driver_id: int) -> Dict[str, Any]:
        """Accept a ride"""
        url = f"{self.base_url}/api/rides/{ride_id}/accept"
        try:
            response = self.session.put(
                url,
                params={"driver_id": driver_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Accept ride failed: {str(e)}"}

    def start_ride(self, ride_id: int) -> Dict[str, Any]:
        """Start a ride"""
        url = f"{self.base_url}/api/rides/{ride_id}/start"
        try:
            response = self.session.put(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Start ride failed: {str(e)}"}

    def complete_ride(self, ride_id: int, fare: float, distance_km: float, duration_minutes: int) -> Dict[str, Any]:
        """Complete a ride"""
        url = f"{self.base_url}/api/rides/{ride_id}/complete"
        try:
            response = self.session.put(
                url,
                params={
                    "fare": fare,
                    "distance_km": distance_km,
                    "duration_minutes": duration_minutes
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Complete ride failed: {str(e)}"}

    def get_user_rides(self, user_id: int, user_type: str = "passenger") -> Dict[str, Any]:
        """Get rides for a specific user"""
        url = f"{self.base_url}/api/rides/{user_type}/{user_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Get user rides failed: {str(e)}"}


def main():
    """Example usage of the client"""
    client = MiniUberClient()
    
    print("🚗 Mini-Uber Client Demo")
    print("=" * 40)
    
    # Test health check
    print("1. Health Check:")
    health = client.health_check()
    print(f"   {json.dumps(health, indent=2)}")
    
    # Test ping with correct data
    print("\n2. Ping Test:")
    response = client.ping("ping")
    print(f"   {json.dumps(response, indent=2)}")
    
    # Get existing users first
    print("\n3. Get Existing Users:")
    users = client.get_users()
    if isinstance(users, list):
        print(f"   Found {len(users)} users in database")
        for i, user in enumerate(users[:3]):  # Show first 3 users
            role = "🚗 Driver" if user.get('is_driver') else "🙋 Rider"
            print(f"   {role} {user.get('full_name')} (ID: {user.get('id')})")
        
        # Use existing users for demo
        rider_user = None
        driver_user = None
        
        for user in users:
            if not user.get('is_driver') and rider_user is None:
                rider_user = user
            elif user.get('is_driver') and driver_user is None:
                driver_user = user
        
        if rider_user and driver_user:
            print(f"\n   Using existing users for demo:")
            print(f"   🙋 Rider: {rider_user['full_name']} (ID: {rider_user['id']})")
            print(f"   🚗 Driver: {driver_user['full_name']} (ID: {driver_user['id']})")
            
            # Test create ride with existing user
            print("\n4. Create Ride Request:")
            ride_data = {
                "passenger_id": rider_user['id'],
                "pickup_address": "123 Main Street, New York, NY",
                "pickup_latitude": 40.7128,
                "pickup_longitude": -74.0060,
                "destination_address": "456 Broadway, New York, NY",
                "destination_latitude": 40.7589,
                "destination_longitude": -73.9851
            }
            ride_response = client.create_ride(ride_data)
            print(f"   {json.dumps(ride_response, indent=2, default=str)}")
            
            # Test get available rides
            print("\n5. Get Available Rides:")
            available_rides = client.get_available_rides()
            print(f"   {json.dumps(available_rides, indent=2, default=str)}")
            
            # Test accept ride (if ride creation was successful)
            if isinstance(ride_response, dict) and "id" in ride_response:
                print("\n6. Driver Accepts Ride:")
                accept_response = client.accept_ride(ride_response["id"], driver_user["id"])
                print(f"   {json.dumps(accept_response, indent=2, default=str)}")
                
                # Test start ride
                print("\n7. Driver Starts Ride:")
                start_response = client.start_ride(ride_response["id"])
                print(f"   {json.dumps(start_response, indent=2, default=str)}")
                
                # Test complete ride
                print("\n8. Driver Completes Ride:")
                complete_response = client.complete_ride(
                    ride_response["id"], 
                    fare=25.50, 
                    distance_km=8.5, 
                    duration_minutes=22
                )
                print(f"   {json.dumps(complete_response, indent=2, default=str)}")
                
                # Test get user ride history
                print(f"\n9. Get Rider's Ride History:")
                rider_rides = client.get_user_rides(rider_user["id"], "passenger")
                print(f"   Rider has {len(rider_rides) if isinstance(rider_rides, list) else 0} rides")
                
                print(f"\n10. Get Driver's Ride History:")
                driver_rides = client.get_user_rides(driver_user["id"], "driver")
                print(f"   Driver has {len(driver_rides) if isinstance(driver_rides, list) else 0} rides")
            
        else:
            print("   ⚠️ Need at least one rider and one driver in database")
            
            # Try to create new users with unique emails
            print("\n4. Attempting to Create New Users:")
            import time
            timestamp = int(time.time())
            
            # Create unique rider
            rider_data = {
                "email": f"demo.rider.{timestamp}@example.com",
                "username": f"demo_rider_{timestamp}",
                "full_name": f"Demo Rider {timestamp}",
                "phone_number": f"+123456{timestamp}",
                "is_driver": False
            }
            rider_response = client.create_user(rider_data)
            print(f"   New Rider: {json.dumps(rider_response, indent=2, default=str)}")
            
            # Create unique driver
            driver_data = {
                "email": f"demo.driver.{timestamp}@example.com",
                "username": f"demo_driver_{timestamp}",
                "full_name": f"Demo Driver {timestamp}",
                "phone_number": f"+123457{timestamp}",
                "is_driver": True
            }
            driver_response = client.create_user(driver_data)
            print(f"   New Driver: {json.dumps(driver_response, indent=2, default=str)}")
    
    else:
        print(f"   Error getting users: {users}")

    print("\n" + "="*40)
    print("🎉 Demo completed!")
    print("Visit http://localhost:8000/docs to try the API interactively!")


if __name__ == "__main__":
    main()
