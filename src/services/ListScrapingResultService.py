import time
from src.repositories.ScrapingSourceRepository import get_source_url
from src.utils.Scraper import Scraper

class ListScrapingResultService:

    def __init__(self, input):
        self.input = input

    def get_scrap_from_source(self, source_id):

        url = get_source_url(source_id)
        if not url:
            return {'message': "Error: Url was not found", 'success': False}

        if source_id == "1":
            result, hits = self.get_leaks_scrap(self.input,url)
            return {'data': result, 'hits': hits, 'success': True}
        
        elif source_id == "2":
            result,hits = self.get_world_scrap(self.input,url)
            return {'data': result, 'hits': hits, 'success': True}
        
        elif source_id == "3":
            result,hits = self.get_ofac_scrap(self.input,url)
            return {'data': result, 'hits': hits, 'success': True}
        
        else:
            return {'message': "Error: Url was not found", 'success': False}

    @classmethod
    def get_leaks_scrap(self,input,url):
        try:
            scrapper_leaks = Scraper(url)
            scrapper_leaks.check_policy('//input[@type="checkbox"]',"/html/body/div[6]/div[1]/div/div/div/form/div/div[2]/button")
            scrapper_leaks.fill_input_text_by_XPATH(input, '/html/body/div[3]/div[1]/div/form/input[1]')            
            records=scrapper_leaks.get_tbody_table_from_div("/html/body/div[5]/div[2]/div[1]/div[2]/div[1]")
            header=scrapper_leaks.get_thead_table_from_div("/html/body/div[5]/div[2]/div[1]/div[2]/div[1]")
            scrapper_leaks.stop()

            if not isinstance(records, list):
                return [],0
            
            hits = len(records)

            header = [h.title() for h in header[0]]
            json_data = [
                {"id": index+1, **dict(zip(header, record))}  
                for index, record in enumerate(records)
            ]
            return json_data,hits
        except Exception as e:
            print("errror: ", e)
            return [],0
        
    
    @classmethod
    def get_world_scrap(self,input,url):
        try:
            scrapper_world = Scraper(url)
            time.sleep(3)
            scrapper_world.fill_input_text_by_XPATH(input,'//input[@id="category"]')
            records=scrapper_world.get_tbody_table_from_div('//*[@id="k-debarred-firms"]/div[3]')
            header=scrapper_world.get_thead_table_from_div('/html/body/div[3]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div[5]/div[2]/div/div/div[3]/div[2]/div')
            scrapper_world.stop()

            if not isinstance(records, list):
                return []

            sub_headers = [h.title() for h in header[1]]
            header = [h.title() for h in header[0]]
            json_data = []
            hits = len(records)
            for index, record in enumerate(records):
                
                entry = {
                    h: r for i, (h, r) in enumerate(zip(header[:4], record[:4])) if i != 1
                }
                
                sub_entry = dict(zip(sub_headers, record[4:6]))
                entry[header[4]] = sub_entry
                entry[header[5]] = record[6]
                entry['id'] = index+1
                json_data.append(entry)
            return json_data,hits
        except Exception as e:
            return [],0
        
    @classmethod
    def get_ofac_scrap(self,input,url):
        try:
            scrapper_ofac = Scraper(url)
            scrapper_ofac.fill_input_text_by_XPATH(input,'//*[@id="ctl00_MainContent_txtLastName"]')
            time.sleep(2)
            records=scrapper_ofac.get_tbody_table_from_div('//*[@id="scrollResults"]')
            header=scrapper_ofac.get_tbody_table_from_div('//*[@id="ctl00_MainContent_pnlResults"]/div[1]')
            scrapper_ofac.stop()

            if not isinstance(records, list):
                return [],0
            
            hits = len(records)
            header = [h.title().replace("(S)", "(s)") for h in header[0]]
            json_data = [
                {"id": index+1, **dict(zip(header, record))}  
                for index, record in enumerate(records)
            ]
            return json_data,hits
        except Exception as e:
            return [],0