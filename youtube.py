import pandas as pd
from time import sleep
import os
from selenium import webdriver # for interacting with website
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_url_in_chrome(url, mode='headless'):
    #print(f'Opening {url}')
    if mode == 'headed':
        print('HEADED MODE')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    elif mode == 'headless':   
        print('HEADLESS MODE')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    driver.get(url)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')))
    sleep(3)
    return driver

def accept_T_and_C(driver):
    # Click 'Accept All'
    driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()
    
    # # Click 'I agree' https://stackoverflow.com/questions/64846902/how-to-get-rid-of-the-google-cookie-pop-up-with-my-selenium-automation
    # driver.switch_to.frame(driver.find_element(By.XPATH,("//iframe[contains(@src, 'consent.google.com')]")))
    # sleep(1)
    # driver.find_element(By.XPATH,'//*[@id="introAgreeButton"]/span/span').click()
    sleep(3)
    # driver.refresh()
    
def get_transcript(driver, mode):
    
    driver.implicitly_wait(10)
    
    if mode=='headed':
        try:
            print('Accepting Terms and Conditions')
            accept_T_and_C(driver)
        except:
            print("No T&Cs to accept.")
            sleep(10)
        
        print("Opening transcript")
        # Click 'More actions'
        driver.find_element(By.XPATH,'//*[@id="expand"]').click()
        
        # Click 'Open transcript'
        driver.find_element(By.XPATH,'//*[@id="primary-button"]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()
        sleep(3)

    
    elif mode=='headless':
        # Click 'More actions'
        try:
            driver.find_element(By.XPATH,"//button[@aria-label='More actions']")[1].click()
        except:
            sleep(3)
            driver.refresh()
            get_transcript(driver, mode)
        
        # Click 'open transcript'
        try:
            driver.find_element(By.XPATH,"//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item").click()
        except:
            sleep(3)
            driver.refresh()
            get_transcript(driver, mode)
    
    # Get all transcript text
    print("Copying transcript ")
    # n=1
    # transcript_element = driver.find_element(By.XPATH,(f'//*[@id="segments-container"]/ytd-transcript-segment-renderer{n}/div'))
    # transcript = transcript_element.text

    # return transcript
    max_n=1000
    all_transcripts = []
    try:
        for n in range(1, max_n + 1):
            transcript_element = driver.find_element(By.XPATH, f'//*[@id="segments-container"]/ytd-transcript-segment-renderer[{n}]/div')
            print(transcript_element.text)
            transcript = transcript_element.text
            all_transcripts.append(transcript)
    except:
        print("No more transcripts to copy")

    return all_transcripts

def transcript2df(all_transcripts):
    all_data = []

    for transcript in all_transcripts:
        transcript = transcript.split('\n')
        # Ensure the transcript has an even number of elements
        if len(transcript) % 2 != 0:
            raise ValueError("Invalid transcript format")

        # Extract timestamps and text
        transcript_timestamps = transcript[::2]
        transcript_text = transcript[1::2]

        # Ensure both arrays have the same length
        if len(transcript_timestamps) != len(transcript_text):
            raise ValueError("Timestamps and text arrays must have the same length")

        all_data.extend(list(zip(transcript_timestamps, transcript_text)))

    # Create DataFrame
    df = pd.DataFrame(all_data, columns=['timestamp', 'text'])
    return df

def main(url, mode='headless'):
    driver = open_url_in_chrome(url, mode)
    
    transcript = get_transcript(driver, mode)
    
    driver.close()
    	
    df = transcript2df(transcript)
    
    # Existing list of unique ingredients
    if not os.path.exists("./output"):
        os.makedirs("./output")

    print('Saving transcript ')
    path_to_transcript = "./output/"
    df.to_csv(f"{path_to_transcript}my_transcript_timestamped.csv", index=False) 
    with open(f"{path_to_transcript}my_transcript_text_only.txt", "w") as text_file:
        print(" ".join(" ".join(df.text.values).split()), file=text_file)
    print(f"Transcript saved to: {path_to_transcript}")


def return_summary(product1,product2):

    product_search = product1 + "vs" + product2 # + "comparison with transcript"
    url = "https://www.youtube.com/results?search_query=" + product_search

    driver = open_url_in_chrome(url,'headless')

    accept_T_and_C(driver)

    video_name = driver.find_element(By.XPATH,'//*[@id="video-title"]/yt-formatted-string')
    print(video_name.text)

    wait = WebDriverWait(driver, 3)

    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located
    driver.find_element(By.XPATH,'//*[@id="chips"]/yt-chip-cloud-chip-renderer[3]').click()
    sleep(3)
    wait.until(visible((By.XPATH, "//*[@id='video-title']")))
    driver.find_element(By.XPATH,"//*[@id='video-title']").click()
    
    # Assuming driver is your WebDriver instance
    xpath = '//*[@id="inline-preview-player"]/div[3]/div[2]/div/a'

    # Wait for the element to be present in the DOM
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))

    # Extract the href attribute value
    youtube_link = element.get_attribute("href")

    return youtube_link

def obtain_transcript(producto1,producto2):
    url=return_summary(producto1,producto2)
    print(f'El link a usar es {url}')
    # url = "https://www.youtube.com/watch?v=IS-n2Cf3qMM"
    mode = 'headed'
    main(url, mode)
    