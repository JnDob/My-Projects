import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Initialize geocoder
geolocator = Nominatim(user_agent="myGeocoder")

# Function to geocode addresses
def geocode_address(address, retries=3):
    for _ in range(retries):
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except GeocoderTimedOut:
            print(f"Timeout occurred for address: {address}. Retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"Error geocoding address '{address}': {str(e)}")
            return None, None
    return None, None

def main():
    # File paths
    input_path = 'C:\\Users\\your_filepath\\addresses.csv'
    output_path = 'C:\\Users\\your_filepath\\addresses_gps.csv'

    try:
        # Read addresses from CSV file
        addresses_df = pd.read_csv(input_path)
    except FileNotFoundError as e:
        print(f"Error reading input file: {str(e)}")
        return
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

    # Ensure the 'address' column exists
    if 'address' not in addresses_df.columns:
        print("The input CSV file must contain an 'address' column.")
        return

    # Prepare lists to store latitude and longitude
    latitudes = []
    longitudes = []

    # Geocode addresses and store coordinates in new columns
    for i, address in enumerate(addresses_df['address']):
        lat, lon = geocode_address(address)
        latitudes.append(lat)
        longitudes.append(lon)
        print(f"Processed {i+1}/{len(addresses_df)}: {address} -> {lat}, {lon}")
        time.sleep(1)  # Add delay to respect Nominatim usage policies

    # Add latitude and longitude to the DataFrame
    addresses_df['latitude'] = latitudes
    addresses_df['longitude'] = longitudes

    try:
        # Save results to new CSV file
        addresses_df.to_csv(output_path, index=False)
        print(f"Geocoding completed and results saved to: {output_path}")
    except Exception as e:
        print(f"Error saving output file: {str(e)}")

if __name__ == "__main__":
    main()
