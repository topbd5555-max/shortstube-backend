const express = require("express");
const cors = require("cors");
const ytdl = require("youtube-dl-exec");

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

    const info = await ytdl(url, {
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

    return res.json({
      success: true,
      title: info.title || "",
      thumbnail: info.thumbnail || "",
      videoUrl: videoUrl || ""
    });

  } catch (err) {
    console.error(err);

    return res.status(500).json({
      success: false,
      error: err.toString()
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});