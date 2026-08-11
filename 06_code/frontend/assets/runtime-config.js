// Public API endpoint for the GitHub Pages website. Local Flask runs use /api.
if (window.location.hostname.endsWith("github.io")) {
  window.LEARNSPHERE_API_BASE = "https://learnsphere-ai-ekanath2417.onrender.com/api";
}
