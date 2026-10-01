const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    status: "ShortsTube Backend Running"
  });
});

app.get("/video-info", async (req, res) => {
  const url = req.query.url;

  res.json({
    success: true,
    url: url
  });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});