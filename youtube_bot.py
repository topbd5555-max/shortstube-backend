import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

# Database Setup
MONGO_URI ="mongodb://parvez12:Pk5480000@ac-93nonf4-shard-00-00.kouagcv.mongodb.net:27017,ac-93nonf4-shard-00-01.kouagcv.mongodb.net:27017,ac-93nonf4-shard-00-02.kouagcv.mongodb.net:27017/?ssl=true&replicaSet=atlas-14ly8k-shard-0&authSource=admin&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['shortstube']
videos_collection = db['videos']

def setup_driver():
    options = Options()
    # GitHub a cholar jonno ai 4ta line must
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def run_youtube_bot():
    print("🚀 YouTube Bot Started in Background...")
    driver = setup_driver()
    
    try:
        driver.get("https://www.youtube.com/shorts/")
        time.sleep(5)
        
        # 10 ta video scrape kore auto off hoye jabe (GitHub free minute bachate)
        for i in range(10):
            print(f"Scraping YouTube Video {i+1}...")
            
            current_url = driver.current_url
            
            # Database a save korar jonno data
            video_data = {
                "title": f"YouTube Shorts {i+1}",
                "url": current_url,
                "source": "youtube"
            }
            
            videos_collection.insert_one(video_data)
            print(f"✅ YouTube Video {i+1} Saved to DB!")
            
            # Nicher video te scroll kora
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(3)
            
    except Exception as e:
        print(f"❌ YouTube Bot Error: {e}")
    finally:
        driver.quit()
        print("🏁 YouTube Bot Finished Task & Sleeping!")

if __name__ == "__main__":
    run_youtube_bot()