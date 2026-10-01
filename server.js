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
      noCheckCertificates: true
    });

    let videoUrl = null;

    if (info.url) {
      videoUrl = info.url;
    } else if (info.formats && info.formats.length > 0) {
      videoUrl = info.formats[0].url;
    }

    res.json({
      success: true,
      title: info.title,
      thumbnail: info.thumbnail,
      videoUrl: videoUrl
    });

  } catch (e) {
    console.error(e);

    res.status(500).json({
      success: false,
      error: e.toString()
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});