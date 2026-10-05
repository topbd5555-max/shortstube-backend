import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import yt_dlp
import cloudinary
import cloudinary.uploader

# ১. তোমার Cloudinary ড্যাশবোর্ড থেকে এই ৩টা জিনিস কপি করে বসাও
cloudinary.config(
  cloud_name = "pkdjkcxn",
  api_key = "627556877651319",
  api_secret = "r3adZjJLaLwCcXwltLVFfBfDhfc"
)

# ২. তোমার MongoDB লিংক
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
    temp_filename = "temp_tiktok.mp4"
    ydl_opts = {
        'outtmpl': temp_filename,
        'format': 'best',
        'quiet': True
    }
    
    print("📥 Downloading TikTok MP4 with yt-dlp...")
    try:
        # টিকটক ভিডিও ডাউনলোড
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        print("☁️ Uploading to Cloudinary...")
        # Cloudinary তে আপলোড
        upload_result = cloudinary.uploader.upload(temp_filename, resource_type="video")
        secure_url = upload_result.get('secure_url')
        
        # গিটহাবের সার্ভার থেকে টেম্পোরারি ফাইল ডিলিট করে দেওয়া
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        return secure_url
    except Exception as e:
        print(f"❌ Error in processing video: {e}")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return None

def run_tiktok_bot():
    print("🚀 TikTok Cloudinary Bot Started...")
    driver = setup_driver()
    
    try:
        driver.get("https://www.tiktok.com/foryou")
        time.sleep(5) # পেজ লোড হওয়ার জন্য ওয়েট
        
        for i in range(5): # আপাতত টেস্ট করার জন্য ৫টা ভিডিও
            print(f"--- Processing TikTok Video {i+1} ---")
            current_url = driver.current_url
            
            # MP4 ডাউনলোড ও Cloudinary আপলোডের ফাংশন কল করা
            cloudinary_mp4_url = download_and_upload(current_url)
            
            if cloudinary_mp4_url:
                video_data = {
                    "title": f"TikTok Video {i+1}",
                    "original_url": current_url,
                    "video_url": cloudinary_mp4_url, # Cloudinary-র ডাইরেক্ট MP4 লিংক
                    "source": "tiktok"
                }
                
                videos_collection.insert_one(video_data)
                print(f"✅ Saved direct MP4 to Database: {cloudinary_mp4_url}")
            
            # পরের ভিডিওতে যাওয়ার জন্য স্ক্রল করা
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(3)
            
    except Exception as e:
        print(f"❌ TikTok Bot Error: {e}")
    finally:
        driver.quit()
        print("🏁 TikTok Bot Finished!")

if __name__ == "__main__":
    run_tiktok_bot()
    