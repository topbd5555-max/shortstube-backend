import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name = "pkdjkcxn",
  api_key = "627556877651319",
  api_secret = "r3adZjJLaLwCcXwltLVFfBfDhfc"
)

MONGO_URI = "mongodb://parvez12:Pk5480000@ac-93nonf4-shard-00-00.kouagcv.mongodb.net:27017,ac-93nonf4-shard-00-01.kouagcv.mongodb.net:27017,ac-93nonf4-shard-00-02.kouagcv.mongodb.net:27017/?ssl=true&replicaSet=atlas-14ly8k-shard-0&authSource=admin&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['shortstube']
videos_collection = db['videos']

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def download_and_upload(video_url):
    temp_filename = "temp_tiktok.mp4"
    print(f"📥 Getting video from API for: {video_url}")
    
    try:
        # TikWM ফ্রী API দিয়ে ভিডিও লিংক বের করা
        api_url = f"https://www.tikwm.com/api/?url={video_url}"
        response = requests.get(api_url).json()
        
        if response.get('code') == 0:
            play_url = response['data']['play']
            
            # API থেকে MP4 ডাউনলোড করা
            print("⏳ Downloading MP4...")
            vid_response = requests.get(play_url)
            with open(temp_filename, "wb") as f:
                f.write(vid_response.content)
            
            print("☁️ Uploading to Cloudinary...")
            upload_result = cloudinary.uploader.upload(temp_filename, resource_type="video")
            secure_url = upload_result.get('secure_url')
            
            os.remove(temp_filename)
            return secure_url
        else:
            print("❌ API Error: Video not found.")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return None

def run_tiktok_bot():
    print("🚀 TikTok API Bot Started...")
    driver = setup_driver()
    
    try:
        driver.get("https://www.tiktok.com/explore")
        time.sleep(5)
        
        video_links = []
        scrolls = 0
        while len(video_links) < 5 and scrolls < 10:
            elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
            for el in elements:
                href = el.get_attribute('href')
                if href and href not in video_links:
                    video_links.append(href)
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(3)
            scrolls += 1
            
        for i, current_url in enumerate(video_links[:5]):
            print(f"--- Processing TikTok Video {i+1} ---")
            cloudinary_mp4_url = download_and_upload(current_url)
            
            if cloudinary_mp4_url:
                video_data = {
                    "title": f"TikTok Video {i+1}",
                    "original_url": current_url,
                    "video_url": cloudinary_mp4_url,
                    "source": "tiktok"
                }
                videos_collection.insert_one(video_data)
                print(f"✅ Saved to DB: {cloudinary_mp4_url}")
                
    except Exception as e:
        print(f"❌ TikTok Bot Error: {e}")
    finally:
        driver.quit()
        print("🏁 TikTok Bot Finished!")

if __name__ == "__main__":
    run_tiktok_bot()