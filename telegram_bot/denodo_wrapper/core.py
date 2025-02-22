"""
This implementation is synchronous and will block the event loop if called directly in an async context. 
TODO: run it in a separate thread (using asyncio.to_thread or loop.run_in_executor).
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def upload_file(file_path):
    """
    Upload the given file to a remote endpoint using Selenium.
    
    This function uses Chrome WebDriver in headless mode as an example.
    Ensure that ChromeDriver is installed and in your PATH.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    
    # Setup ChromeDriver service (adjust executable_path if needed)
    service = Service()  # Use default settings if chromedriver is in your PATH
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to the upload page endpoint (adjust URL accordingly)
        driver.get("https://example.com/upload")
        
        # Locate the file input element (assumes the element has an id "file-upload")
        file_input = driver.find_element(By.ID, "file-upload")
        
        # Send the file path to the file input element
        file_input.send_keys(str(file_path))
        
        # Optionally, click a submit button (assumes an element with id "submit-button")
        submit_button = driver.find_element(By.ID, "submit-button")
        submit_button.click()
        
        # Wait for the upload to finish (you might use WebDriverWait in production)
        time.sleep(5)
    except Exception as e:
        print(f"Error during file upload: {e}")
    finally:
        driver.quit()
