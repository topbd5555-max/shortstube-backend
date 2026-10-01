const express = require("express");
const cors = require("cors");
const ytDlp = require("yt-dlp-exec");

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    status: "ShortsTube Backend Running"
  });
});

app.get("/video-info", async (req, res) => {
  try {
    const url = req.query.url;

    if (!url) {
      return res.status(400).json({
        success: false,
        error: "URL required"
      });
    }

    const info = await ytDlp(url, {
      dumpSingleJson: true,
      noWarnings: true,
      noCheckCertificates: true,
      preferFreeFormats: true
    });

    let videoUrl = null;

    if (info.url) {
      videoUrl = info.url;
    } else if (info.formats && info.formats.length > 0) {
      const format =
        info.formats.find(f => f.url) ||
        info.formats[0];

      videoUrl = format.url;
    }

    res.json({
      success: true,
      title: info.title || "",
      thumbnail: info.thumbnail || "",
      videoUrl: videoUrl
    });

  } catch (e) {
    console.error("FULL ERROR:", e);

    res.status(500).json({
      success: false,
      error: e.message || e.toString(),
      stack: e.stack
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});