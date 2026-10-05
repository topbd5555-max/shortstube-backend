const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// .env ফাইল থেকে সিক্রেট ডাটা লোড করা
dotenv.config();

const app = express();
app.use(express.json());

// ==========================================
// 🛡️ ANTI-HACKER SECURITY LAYERS
// ==========================================
app.use(helmet());
app.use(cors());

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: { error: "Onek beshi request kora hoyeche, kisu khon por abr try korun!" }
});
app.use(limiter);

const verifyApiKey = (req, res, next) => {
    const clientKey = req.header('x-api-key');
    if (!clientKey || clientKey !== process.env.API_SECRET_KEY) {
        return res.status(403).json({ error: "Access Denied! Hacking try kora nishedh 🛑" });
    }
    next();
};

// ==========================================
// 📂 DATABASE SCHEMA (ভিডিও সেভ করার ছাঁচ)
// ==========================================
const videoSchema = new mongoose.Schema({
    title: { type: String, required: true },
    videoUrl: { type: String, required: true },
    platform: { type: String, required: true }, // YouTube ba TikTok
    createdAt: { type: Date, default: Date.now }
});
const Video = mongoose.model('Video', videoSchema);

// ==========================================
// 🚀 API ROUTES 
// ==========================================
app.get('/', (req, res) => {
    res.send('ShortsTube Secure Backend is Running! 🚀');
});

// ভিডিও ডাটাবেস থেকে দেখার API
app.get('/api/videos', verifyApiKey, async (req, res) => {
    try {
        const videos = await Video.find().sort({ createdAt: -1 });
        res.json({ message: "Success!", videos });
    } catch (error) {
        res.status(500).json({ error: "Video load korte problem hoyeche." });
    }
});

// পাইথন বট থেকে নতুন ভিডিও সেভ করার POST API
app.post('/api/videos', verifyApiKey, async (req, res) => {
    try {
        const { title, videoUrl, platform } = req.body;
        const newVideo = new Video({ title, videoUrl, platform });
        await newVideo.save();
        res.status(201).json({ message: "Video saved successfully! 🎉", video: newVideo });
    } catch (error) {
        res.status(500).json({ error: "Video save korte problem hoyeche." });
    }
});

// ==========================================
// 🌐 SERVER START & DATABASE CONNECTION
// ==========================================
const PORT = process.env.PORT || 5000;

mongoose.connect(process.env.MONGO_URI)
    .then(() => {
        console.log('✅ MongoDB Atlas (Database) Connected Successfully! 🎉');
        
        app.listen(PORT, () => {
            console.log(`✅ Server is securely running on http://localhost:${PORT}`);
            console.log(`🔒 Anti-Hacker layers (Helmet, Rate-Limit, API Key) are ACTIVE.`);
        });
    })
    .catch((err) => {
        console.error('❌ MongoDB Connection Error:', err);
    });