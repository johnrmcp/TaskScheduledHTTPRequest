import requests
import time
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env file if it exists

# List of environment variables, see .env to modify
api_url = os.getenv("API_URL") # Host URI
max_retries = int(os.getenv("MAX_RETRIES", 3))  # Default to 3 if not set
retry_delay = int(os.getenv("RETRY_DELAY", 5))  # Default to 5 if not set


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Configure the format of the message - begin with time, then display message
    filename='order_sync.log',  # Optional: Log to a file
    filemode='a'  # Append to the log file
)

if api_url is None: # Log basic URI check
    logging.error("API_URI environment variable not set.")
    exit(1)

logging.info("Beginning Order Sync... ")

for attempt in range(max_retries): # Loops for the amount of retries for a given request
    try:
        response = requests.get(api_url, verify=False)  # Disable SSL verification , NEEDS to be removed before entering production environment
        response.raise_for_status() 
        logging.info(f"API request successful on attempt {attempt + 1}!") # If attempt succeeds, this prints which attempt it succeeded on
        # Process the response if needed (though your GET request doesn't return data)
        break  # Exit the loop if successful
    except requests.exceptions.RequestException as e: 
        logging.error(f"Error during API request (attempt {attempt + 1}/{max_retries}): {e}") # If attempt fails, this prints which attempt failed
        if attempt < max_retries - 1:
            logging.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay) # Waits before trying again
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        break  # No point in retrying for unexpected errors
else:
    logging.error(f"Failed to reach the API after {max_retries} attempts.")

logging.info("Order Sync Finished.")