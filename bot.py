import time
import requests
import yt_dlp

# Backend API URL & Key
API_URL = "http://localhost:5000/api/videos"
API_KEY = "ShortsTube_Pro_Max_Secret_2026"

# যে ইউটিউব শর্টস বা ভিডিওগুলোর লিংক তুমি ট্র্যাক করতে চাও (একাধিক লিংক রাখতে পারো)
target_urls = [
    "https://www.youtube.com/shorts/M7FIvfx5J10",
    # ভবিষ্যতে এখানে আরও নতুন নতুন লিংক বা চ্যানেল যোগ করতে পারবে
]

def fetch_and_send(video_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Unknown Video')
            fetched_url = info.get('url', video_url)
            
            # ডাটাবেসে পাঠানোর ডেটা
            video_data = {
                "title": title,
                "videoUrl": fetched_url,
                "platform": "YouTube"
            }
            
            headers = {
                "x-api-key": API_KEY,
                "Content-Type": "application/json"
            }
            
            # ব্যাকএন্ডে পোস্ট রিকোয়েস্ট পাঠানো
            response = requests.post(API_URL, json=video_data, headers=headers)
            
            if response.status_code == 201:
                print(f"✅ Success Saved: {title}")
            else:
                print(f"❌ Backend Error: {response.json().get('error')}")
                
    except Exception as e:
        print(f"❌ Error fetching video: {str(e)}")

# ==========================================
# 🔄 CONTINUOUS BOT RUNNING LOOP
# ==========================================
if __name__ == "__main__":
    print("🤖 ShortsTube Continuous Bot Started Successfully! 🚀")
    print("💡 Bot bondho korte chaile keyboard theke 'Ctrl + C' chapo.")
    
    while True:
        print("\n-----------------------------------------")
        print("🔄 Notun cycle shuru holo... Video check kora hocche...")
        
        for url in target_urls:
            fetch_and_send(url)
            # প্রতিটা লিংকের মাঝে ৩ সেকেন্ড বিরতি
            time.sleep(3)
            
        print("⏳ Sob link check kora sesh. Porer cycle shuru hobar age 1 second wait korchi...")
        
        # পুরো লিস্ট চেক করার পর বট কতক্ষণ ঘুমাবে (এখানে ৬০ সেকেন্ড বা ১ মিনিট দেওয়া আছে)
        # তুমি চাইলে সময় বাড়াতে বা কমাতে পারো (যেমন: ৫ মিনিট করতে চাইলে 300 লিখবে)
        time.sleep(1)