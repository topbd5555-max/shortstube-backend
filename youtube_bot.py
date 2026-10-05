import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import yt_dlp
import cloudinary
import cloudinary.uploader

# ১. তোমার Cloudinary ক্রেডেনশিয়াল বসাও
cloudinary.config(
  cloud_name = "pkdjkcxn",
  api_key = "627556877651319",
  api_secret = "r3adZjJLaLwCcXwltLVFfBfDhfc"
)

# ২. তোমার MongoDB লিংক বসাও
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
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def download_and_upload(video_url):
    temp_filename = "temp_video.mp4"
    ydl_opts = {
        'outtmpl': temp_filename,
        'format': 'best',
        'quiet': True
    }
    
    print(f"📥 Downloading: {video_url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        print("☁️ Uploading to Cloudinary...")
        upload_result = cloudinary.uploader.upload(temp_filename, resource_type="video")
        secure_url = upload_result.get('secure_url')
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        return secure_url
    except Exception as e:
        print(f"❌ Error: {e}")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return None

def run_youtube_bot():
    print("🚀 YouTube Bot Started...")
    driver = setup_driver()
    
    try:
        driver.get("https://www.youtube.com/shorts/")
        time.sleep(5)
        
        # নির্দিষ্ট ভিডিও লিংক খুঁজে বের করার নতুন সিস্টেম
        video_links = []
        scrolls = 0
        while len(video_links) < 5 and scrolls < 10:
            elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/shorts/']")
            for el in elements:
                href = el.get_attribute('href')
                if href and href != "https://www.youtube.com/shorts/" and href not in video_links:
                    video_links.append(href)
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)
            scrolls += 1
            
        for i, current_url in enumerate(video_links[:5]):
            print(f"--- Processing Video {i+1} ---")
            cloudinary_mp4_url = download_and_upload(current_url)
            
            if cloudinary_mp4_url:
                video_data = {
                    "title": f"YouTube Shorts {i+1}",
                    "original_url": current_url,
                    "video_url": cloudinary_mp4_url,
                    "source": "youtube"
                }
                videos_collection.insert_one(video_data)
                print(f"✅ Saved to DB: {cloudinary_mp4_url}")
                
    except Exception as e:
        print(f"❌ YouTube Bot Error: {e}")
    finally:
        driver.quit()
        print("🏁 YouTube Bot Finished!")

if __name__ == "__main__":
    run_youtube_bot()