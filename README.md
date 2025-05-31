# 🎨 DeviantArt Favorites Downloader

A reliable Python script to download all your DeviantArt favorites using the **official DeviantArt API** with OAuth 2.0 authentication.

## ✨ Features

- ✅ **Official API** - Uses DeviantArt's official API (no web scraping!)
- 🔐 **OAuth 2.0 Authentication** - Secure, authorized access
- 📥 **Full Collection Download** - Downloads all your favorites with pagination
- 🖼️ **High Quality Media** - Gets the best available resolution for images and videos
- 🎬 **Video Support** - Downloads MP4, WebM, MOV, and other video formats
- 📊 **Progress Tracking** - Shows download progress and summary
- 🛡️ **Rate Limited** - Respectful to DeviantArt's servers
- 💾 **Token Persistence** - Saves authentication for future runs

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Set Up OAuth Application

1. Go to [DeviantArt Developer Portal](https://www.deviantart.com/developers/)
2. Click "Register Application"
3. Fill in the form:
   - **Application Name**: `My Favorites Downloader`
   - **Description**: `Personal tool to download my DeviantArt favorites`
   - **Redirect URI**: `http://localhost:8080/callback`
4. Save your **Client ID** and **Client Secret**

### 3. Run the Downloader

```bash
python api_downloader.py
```

The script will guide you through:
- OAuth application setup
- Browser-based authentication
- Automatic downloading of all favorites

## 📁 Output

Downloaded media files are saved to `DeviantArt_API_Downloads/` with descriptive filenames:
```
{artist}_{title}_{deviation_id}.{extension}
```

Supported formats:
- **Images**: JPG, PNG, GIF, WebP
- **Videos**: MP4, WebM, MOV, AVI, MKV, FLV, M4V, WMV

## 🔧 How It Works

1. **OAuth Setup**: Registers your application with DeviantArt
2. **Authentication**: Opens browser for secure login and authorization
3. **Token Management**: Saves access tokens for future use
4. **Collection Fetch**: Uses `/collections/all` API endpoint with pagination
5. **Download**: Gets highest quality images available for each favorite

## 📊 Success Rate

In testing, the downloader achieved a **99.7% success rate** (1,141 out of 1,145 favorites downloaded successfully). Failed downloads are typically due to:
- Deleted content
- Premium/restricted access content
- Network timeouts

## 🛠️ Advanced Usage

See [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for:
- Detailed setup instructions
- Troubleshooting tips
- API documentation links
- OAuth flow explanation

## 🔒 Security & Privacy

- Uses official DeviantArt OAuth 2.0 flow
- Tokens are stored locally in `deviantart_tokens.json`
- No credentials are hardcoded or transmitted insecurely
- Respects DeviantArt's rate limits and terms of service

## 🆚 Why This Approach?

| Feature | Web Scraping | Official API |
|---------|-------------|--------------|
| **Reliability** | ❌ Breaks with site changes | ✅ Stable interface |
| **Authentication** | ❌ Cookie-based, fragile | ✅ OAuth 2.0, secure |
| **Rate Limiting** | ❌ Manual implementation | ✅ Built-in respect |
| **Content Access** | ❌ Limited by restrictions | ✅ Proper access levels |
| **Image Quality** | ❌ Often just previews | ✅ Best available quality |
| **Maintenance** | ❌ Requires constant updates | ✅ Self-maintaining |

## 📝 Requirements

- Python 3.6+
- `requests` library
- DeviantArt account
- Registered OAuth application

## 🎉 Success Story

This project successfully downloaded **1,141 high-quality media files** from a large DeviantArt favorites collection, including:
- Full-resolution images (when available)
- High-quality videos in various formats
- Animated GIFs
- High-quality previews for restricted content
- Proper file naming and organization

## 🤝 Contributing

This is a personal tool, but feel free to fork and adapt for your needs!

## 📄 License

Apache-2.0 license - Feel free to use and modify as needed. 