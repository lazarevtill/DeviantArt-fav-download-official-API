# 🎨 DeviantArt API Setup Guide

This guide will help you set up the **Official DeviantArt API** to download your favorites properly and reliably.

## 🌟 Why Use the Official API?

✅ **Reliable** - No more broken scrapers when DeviantArt changes their website  
✅ **Authorized** - Official access method sanctioned by DeviantArt  
✅ **High-Quality** - Access to full-resolution images when available  
✅ **No Restrictions** - Proper authentication bypasses many content restrictions  
✅ **Rate Limiting** - Built-in respect for DeviantArt's servers  

## 🚀 Quick Start

### Step 1: Register Your Application

1. **Go to DeviantArt Developers Portal**:
   ```
   https://www.deviantart.com/developers/
   ```

2. **Click "Register Application"**

3. **Fill in the Application Form**:
   - **Application Name**: `My Favorites Downloader`
   - **Description**: `Personal tool to download my DeviantArt favorites`
   - **Website URL**: `http://localhost` (if required)
   - **Redirect URI**: `http://localhost:8080/callback`
   - **Application Type**: Choose appropriate type

4. **Submit and Save Credentials**:
   - Copy your **Client ID**
   - Copy your **Client Secret**
   - Keep these safe - you'll need them!

### Step 2: Run the Downloader

1. **Install Dependencies**:
   ```bash
   pip install requests beautifulsoup4
   ```

2. **Run the API Downloader**:
   ```bash
   python api_downloader.py
   ```

3. **Follow the Setup Wizard**:
   - The script will guide you through OAuth setup
   - It will open your browser for authorization
   - Enter your Client ID and Client Secret when prompted
   - Authorize the application in your browser
   - Copy the authorization code back to the script

4. **Enter Username and Download**:
   - Enter the DeviantArt username whose favorites you want to download
   - The script will download all accessible favorites

## 🔧 How OAuth 2.0 Works

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Your App  │    │ DeviantArt  │    │    User     │
│             │    │   Server    │    │  (Browser)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       │ 1. Authorization  │                   │
       │    Request        │                   │
       ├──────────────────>│                   │
       │                   │                   │
       │                   │ 2. User Login &   │
       │                   │    Authorization  │
       │                   │<─────────────────>│
       │                   │                   │
       │ 3. Authorization  │                   │
       │    Code           │                   │
       │<──────────────────┤                   │
       │                   │                   │
       │ 4. Access Token   │                   │
       │    Request        │                   │
       ├──────────────────>│                   │
       │                   │                   │
       │ 5. Access Token   │                   │
       │<──────────────────┤                   │
       │                   │                   │
       │ 6. API Calls with │                   │
       │    Access Token   │                   │
       ├──────────────────>│                   │
```

## 📁 What Gets Downloaded

The API downloader will attempt to get the best quality available:

1. **Full-Size Images** - When available and authorized
2. **Preview Images** - High-quality previews (usually still quite large)
3. **Large Thumbnails** - As fallback for restricted content

Files are saved with the format:
```
{artist}_{title}_{deviation_id}.{extension}
```

## ⚠️ Important Notes

### Content Access Levels

- **Public Content**: ✅ Full access
- **Mature Content**: ✅ Access with proper authentication
- **Premium Gallery**: ❓ May require premium membership
- **Exclusive Content**: ❓ May require special access rights

### Rate Limiting

The script includes built-in delays to respect DeviantArt's servers:
- 0.5 seconds between API calls
- 0.5 seconds between downloads

### Token Management

- Access tokens are saved to `deviantart_tokens.json`
- Tokens are automatically reused on subsequent runs
- If tokens expire, the script will prompt for re-authentication

## 🆚 API vs Web Scraping Comparison

| Feature | Web Scraping | Official API |
|---------|-------------|--------------|
| **Reliability** | ❌ Breaks when site changes | ✅ Stable interface |
| **Authentication** | ❌ Cookie-based, fragile | ✅ OAuth 2.0, secure |
| **Rate Limiting** | ❌ Manual implementation | ✅ Built-in respect |
| **Content Access** | ❌ Limited by restrictions | ✅ Proper access levels |
| **Image Quality** | ❌ Often just previews | ✅ Best available quality |
| **Maintenance** | ❌ Requires constant updates | ✅ Self-maintaining |

## 🔍 Troubleshooting

### "API access test failed"
- Check your Client ID and Client Secret
- Make sure you authorized the application
- Try re-running the authentication flow

### "No favorites found"
- Make sure the username is correct
- Check if the user's favorites are public
- Verify your API access includes the necessary scopes

### "Download failed" errors
- Some content may still be restricted
- Premium content may require premium membership
- Network issues can cause temporary failures

### "Invalid redirect URI"
- Make sure you used exactly: `http://localhost:8080/callback`
- Check for typos in your application registration

## 🎯 Next Steps

1. **Run the API downloader**: `python api_downloader.py`
2. **Set up your OAuth application** following the prompts
3. **Download your favorites** with proper authentication
4. **Enjoy high-quality, reliable downloads**! 🎉

---

**Need Help?** Check the DeviantArt API documentation at: https://www.deviantart.com/developers/ 