import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os


class VotingReader():

    def __init__(self, session, voting):
        self.session = session
        self.voting = voting
        self.url_path = f"https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia={self.session}&NrGlosowania={self.voting}"
        self.download_dir = os.path.dirname(__file__) + f'/voting_data'
        

    def download_results(self):
        chrome_options = Options()
        chrome_options.add_argument('headless')
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory' : self.download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'plugins.always_open_pdf_externally': True})
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url_path)
        pdf_file = driver.find_element_by_link_text('Wyniki indywidualne').click()
        time.sleep(1)
        driver.quit()

    def save_table(self):    
        df = pd.read_html(self.url_path)
        df = pd.DataFrame(df[0])
        df.to_csv(f'voting_data/session{self.session}_voting{self.voting}')
        return 'table read and saved!'


session_number = 1

while True:
    
    voting_number = 1
    try:
        while True:
            vote_reader = VotingReader(session_number, voting_number)
            try:
                vote_reader.download_results()
                vote_reader.save_table()
            except:
                break
            voting_number += 1
            time.sleep(1)
    except:
        break
    session_number += 1
    time.sleep(3) 
"""  
session_number = 1
while True:
    voting_number = 1
    try:
        if session_number > 29:
            raise 'End of session list'
        else:
            pass
        while True:
            vote_reader = VotingReader(session_number, voting_number)
            try:
                if voting_number > 10:
                    raise 'End of voting list'
                else:
                    print(f'Posiedzenie: {session_number}, Glosowanie: {voting_number}')
            except:
                break
            voting_number += 1
            time.sleep(1)
    except:
        break       
    session_number += 1
"""             



