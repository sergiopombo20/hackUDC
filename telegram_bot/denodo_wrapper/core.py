import time
import requests
from docker_wrapper import copy_to_container, remove_container, compose_up_service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

DENODO_PLATFORM_CHATBOT_NAME = 'denodo-platform-chatbot'
DENODO_AI_CHATBOT_NAME = 'denodo-ai-sdk-chatbot'
DENODO_PLATFORM_CHATBOT_DST_DIR = '/home'

def update_data_catalog(driver, wait):
    try:
        driver.get("http://localhost:9090/denodo-data-catalog")
        
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "user")))
        user_field.send_keys("admin")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin")

        sign_in_button = driver.find_element(By.XPATH, "//button[contains(.,'Sign in')]")
        sign_in_button.click()

        admin_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'menu.administration$Menu')]/div[contains(@class, 'rc-menu-submenu-title')]")
        ))
        admin_menu.click()

        sync_vdp_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'menu.administration.syncVdp$Menu')]/span[contains(@class, 'rc-menu-item-container')]")
        ))
        sync_vdp_option.click()

        continue_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'Button___primary_______406') and .//span[text()='Continue']]")
        ))
        continue_button.click()
        time.sleep(0.5)
        continue_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'Button___primary_______406') and .//span[text()='Continue']]")
        ))
        continue_button.click()
        time.sleep(0.5)
        continue_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'Button___primary_______406') and .//span[text()='Continue']]")
        ))
        continue_button.click()

        success_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Web services synchronized')]")
        ))

        if success_message:
            return True
    except Exception as e:
        print(f"Error during data catalog upload: {e}")
        return False
    
    return False

def upload_to_design_studio(file_path, driver, wait):
    file_without_extension = file_path.stem

    try:
        driver.get("http://localhost:9090/denodo-design-studio")
        
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "user")))
        user_field.send_keys("admin")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("admin")

        sign_in_button = driver.find_element(By.XPATH, "//button[contains(.,'Sign in')]")
        sign_in_button.click()

        admin_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'menu.administration$Menu')]/div[@class='rc-menu-submenu-title']")
        ))
        admin_menu.click()
        
        db_management = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'menu.administration.databaseManagement$Menu')]/span[@class='rc-menu-item-container']")
        ))
        db_management.click()

        new_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'Button___action_______64')]/span[contains(., 'New')]")
        ))
        new_button.click()

        name_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='name']")
        ))
        name_input.send_keys(file_path.stem.lower())
        
        ok_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Ok']]")
        ))
        ok_button.click()

        success_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'successfully created')]")
        ))

        file_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'menu.file$Menu')]/div[@class='rc-menu-submenu-title']")
        ))
        file_menu.click()
        new_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class, 'Navbar_menuItemText_______50') and contains(., 'New')]")
        ))
        new_option.click()
        data_source_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class, 'Navbar_menuItemText_______50') and contains(., 'Data source')]")
        ))
        data_source_option.click()
        files_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class, 'Pills_navLink_______353') and text()='FILES']")
        ))
        files_tab.click()
        delimited_file_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@title='Delimited file' and @role='button']")
        ))
        delimited_file_option.click()


        name_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'col-6')]/input[@name='name']")
        ))
        name_input.send_keys(file_without_extension)
        select_element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[@name=\"dataRoute['type']\"]")
        ))
        select = Select(select_element)
        select.select_by_value("LOCAL")

        file_path_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name=\"dataRoute['filePath']\"]")
        ))
        file_path_input.clear()
        file_path_input.send_keys(f"{DENODO_PLATFORM_CHATBOT_DST_DIR}/{file_path.name}")
        column_delimiter_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='columnDelimiter']")
        ))
        column_delimiter_input.clear()
        column_delimiter_input.send_keys(",")

        header_label = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(@id, 'checkbox-label-checkbox') and contains(text(), 'Header')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header_label)
        header_label.click()

        metadata_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class, 'Tabs_navLink_______575') and .//span[text()='Metadata']]")
        ))
        metadata_tab.click()
        
        dropdown_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//select[@name='database']")
        ))

        select = Select(dropdown_element)
        select.select_by_visible_text(file_without_extension)

        save_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'Button___action_______64') and .//i[contains(@class, 'fa-save')]]")
        ))
        save_button.click()

        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Data source saved successfully')]")
        ))

        create_base_view_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'Button___action_______64') and .//i[contains(@class, 'fa-layer-group')]]")
        ))
        create_base_view_button.click()

        success_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Df base view')]")
        ))
        if success_message:
            return True
        
    except Exception as e:
        print(f"Error during file upload to design studio: {e}")
        return False
    
    return False

def update_env_file(denodo_repository_path, vdb_names):
    try:
        env_path = denodo_repository_path/'lab-environment-containers'/'build'/'.env'
        new_vdb_names = vdb_names
        new_chatbot_vdb_names = vdb_names

        with env_path.open("r") as file:
            lines = file.readlines()

        with env_path.open("w") as file:
            for line in lines:
                if line.startswith("VDB_NAMES="):
                    file.write(f"VDB_NAMES={new_vdb_names}\n")
                elif line.startswith("DENODO_CHATBOT_SAMPLE_VDB_NAMES="):
                    file.write(f"DENODO_CHATBOT_SAMPLE_VDB_NAMES={new_chatbot_vdb_names}\n")
                else:
                    file.write(line)
        
        return True

    except Exception as e:
        print(f"Error during env file update: {e}")
        return False

def wait_until_url_is_available(url, timeout=60, interval=3):
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"URL is available: {url}")
                return True
        except requests.RequestException:
            pass
        
        print(f"Waiting for {url} to be available...")
        time.sleep(interval)
    
    print(f"Timeout reached. URL {url} is still unavailable.")
    return False

def restart_denodo_ai_sdk_chatbot_container(docker_compose_path):
    try:
        remove_container(DENODO_AI_CHATBOT_NAME)

        compose_up_service(docker_compose_path, DENODO_AI_CHATBOT_NAME)
        
        return wait_until_url_is_available('http://localhost:9992/') # TODO: Stop hardcoding
    except Exception as e:
        print(f"Error during env file update: {e}")
        return False

def upload_file(file_path, denodo_repository_path):
    """
    Upload the given file to a remote endpoint using Selenium.
    Returns True if upload succeeds, False otherwise.
    """
    copy_to_container(file_path.resolve(), DENODO_PLATFORM_CHATBOT_NAME, DENODO_PLATFORM_CHATBOT_DST_DIR) # TODO: make vars configurable

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("--start-maximized")
    
    service = Service()  # Assumes chromedriver is in your PATH
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    success = True
    if not upload_to_design_studio(file_path, driver, wait):
        return False
    
    if not update_data_catalog(driver, wait):
        return False

    driver.quit()

    if not update_env_file(denodo_repository_path, file_path.stem):
        return False
    
    docker_compose_path = denodo_repository_path/'lab-environment-containers'/'build'/'docker-compose-sample-chatbot.yml'
    
    return restart_denodo_ai_sdk_chatbot_container(docker_compose_path)
