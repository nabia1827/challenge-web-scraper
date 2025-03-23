from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC

class Scraper:
    def __init__(self, url):
        options = Options()
        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

    def check_policy(self, check_xpath, button_xpath):
        try:
            checkbox = self.driver.find_element(By.XPATH, check_xpath)
            checkbox.click()
        
            submit_button = self.driver.find_element(By.XPATH, button_xpath)
            submit_button.click()

            return 200
        except Exception as e:
            print("Error policy: ", e)
            return e

    
    def fill_input_text_by_XPATH(self,input_value, x_path):
        try:
            input_text = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, x_path))
            )
            input_text.clear()
            input_text.send_keys(input_value)
            input_text.send_keys(Keys.ENTER)
            return 200
        except Exception as e:
            print("Error input: ", e)
            return e
        
    def get_thead_table_from_div(self, x_path):
        try:
            records = []
            wait = WebDriverWait(self.driver, 10)

            grid_content = wait.until(EC.presence_of_element_located(
                (By.XPATH, x_path)
            ))
            
            table = grid_content.find_element(By.TAG_NAME, "table")
            tbody = table.find_element(By.TAG_NAME, "thead")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "th")
                row_data = [cell.text for cell in cells]
                records.append(row_data)

            return records
        except Exception as e:
            print("Error thead: ", e)
            return e


            
    def get_tbody_table_from_div(self,x_path): #"div.k-grid-content.k-auto-scrollable"
        try:
            records = []
            wait = WebDriverWait(self.driver, 10)

            grid_content = wait.until(EC.presence_of_element_located(
                (By.XPATH, x_path)
            ))
            
            table = grid_content.find_element(By.TAG_NAME, "table")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text for cell in cells]
                records.append(row_data)

            return records
        except Exception as e:
            print("Error tbody: ", e)
            return e

    def stop(self):
        self.driver.quit()
        return