#!/usr/bin/env python3
"""
Official DeviantArt API Favorites Downloader
Uses the official DeviantArt API with OAuth 2.0 authentication
Much more reliable than web scraping!
"""

import requests
import json
import time
import re
import webbrowser
from urllib.parse import urlparse, urlencode, parse_qs
from pathlib import Path
import base64
import hashlib
import secrets


class DeviantArtAPIDownloader:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()
        
        # API endpoints
        self.api_base = "https://www.deviantart.com/api/v1/oauth2"
        self.auth_base = "https://www.deviantart.com/oauth2"
        
        # Set up session headers
        self.session.headers.update({
            'User-Agent': 'DeviantArt-Favorites-Downloader/1.0',
            'Accept': 'application/json',
        })

        # Create download directory
        self.download_dir = Path("DeviantArt_API_Downloads")
        self.download_dir.mkdir(exist_ok=True)

        # Keep track of downloaded files
        self.downloaded_files = set()
        self.failed_downloads = []

    def setup_oauth_app(self):
        """Guide user through setting up OAuth application"""
        print("🔧 Setting up DeviantArt API Access")
        print("=" * 60)
        print()
        print("To use the official DeviantArt API, you need to:")
        print("1. Go to: https://www.deviantart.com/developers/")
        print("2. Click 'Register Application'")
        print("3. Fill in the form:")
        print("   - Application Name: 'My Favorites Downloader'")
        print("   - Description: 'Download my DeviantArt favorites'")
        print("   - Redirect URI: 'http://localhost:8080/callback'")
        print("4. Submit the form")
        print("5. Copy the Client ID and Client Secret")
        print()
        
        # Open the registration page
        print("📋 Opening DeviantArt developer registration page...")
        webbrowser.open("https://www.deviantart.com/developers/")
        
        print()
        print("After registering your application, enter the credentials:")
        
        while True:
            self.client_id = input("Enter your Client ID: ").strip()
            if self.client_id:
                break
            print("❌ Client ID cannot be empty")
        
        while True:
            self.client_secret = input("Enter your Client Secret: ").strip()
            if self.client_secret:
                break
            print("❌ Client Secret cannot be empty")
        
        print("✅ OAuth application configured!")
        return True

    def generate_pkce_challenge(self):
        """Generate PKCE code verifier and challenge for OAuth"""
        # Generate a random code verifier
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        
        # Create the code challenge
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        return code_verifier, code_challenge

    def authenticate(self):
        """Perform OAuth 2.0 authentication flow"""
        print("\n🔐 Starting OAuth 2.0 Authentication")
        print("=" * 50)
        
        # Generate PKCE parameters
        code_verifier, code_challenge = self.generate_pkce_challenge()
        
        # Prepare authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': 'http://localhost:8080/callback',
            'scope': 'user browse',  # Basic user access and browsing
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        auth_url = f"{self.auth_base}/authorize?" + urlencode(auth_params)
        
        print("📋 Opening authorization page in your browser...")
        print(f"If it doesn't open automatically, go to:")
        print(f"{auth_url}")
        print()
        
        webbrowser.open(auth_url)
        
        print("After authorizing the application, you'll be redirected to:")
        print("http://localhost:8080/callback?code=...")
        print()
        print("Copy the 'code' parameter from the URL and paste it here:")
        
        while True:
            auth_code = input("Enter the authorization code: ").strip()
            if auth_code:
                break
            print("❌ Authorization code cannot be empty")
        
        # Exchange authorization code for access token
        print("🔄 Exchanging authorization code for access token...")
        
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': 'http://localhost:8080/callback',
            'code': auth_code,
            'code_verifier': code_verifier
        }
        
        try:
            response = self.session.post(f"{self.auth_base}/token", data=token_data)
            
            if response.status_code == 200:
                token_info = response.json()
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                if self.access_token:
                    print("✅ Authentication successful!")
                    
                    # Update session headers with access token
                    self.session.headers['Authorization'] = f'Bearer {self.access_token}'
                    
                    # Save token info for future use
                    self.save_tokens(token_info)
                    return True
                else:
                    print("❌ Failed to get access token")
                    return False
            else:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error during authentication: {e}")
            return False

    def save_tokens(self, token_info):
        """Save tokens and credentials to file for future use"""
        # Include client credentials for re-authentication
        token_data = dict(token_info)
        token_data['client_id'] = self.client_id
        token_data['client_secret'] = self.client_secret
        
        token_file = Path("deviantart_tokens.json")
        with open(token_file, 'w') as f:
            json.dump(token_data, f, indent=2)
        print(f"💾 Tokens and credentials saved to {token_file}")

    def load_tokens(self):
        """Load saved tokens and credentials"""
        token_file = Path("deviantart_tokens.json")
        if token_file.exists():
            try:
                with open(token_file, 'r') as f:
                    token_info = json.load(f)
                
                # Load OAuth credentials
                self.client_id = token_info.get('client_id')
                self.client_secret = token_info.get('client_secret')
                
                # Load tokens
                self.access_token = token_info.get('access_token')
                self.refresh_token = token_info.get('refresh_token')
                
                if self.access_token and self.client_id and self.client_secret:
                    self.session.headers['Authorization'] = f'Bearer {self.access_token}'
                    print(f"✅ Loaded saved credentials and tokens")
                    return True
                else:
                    print(f"⚠ Incomplete credentials in saved tokens")
                    return False
            except Exception as e:
                print(f"⚠ Error loading tokens: {e}")
        
        return False

    def test_api_access(self):
        """Test API access with current token"""
        try:
            response = self.session.get(f"{self.api_base}/user/whoami")
            if response.status_code == 200:
                user_info = response.json()
                username = user_info.get('username', 'Unknown')
                print(f"✅ API access verified for user: {username}")
                return True
            else:
                print(f"❌ API access test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing API access: {e}")
            return False

    def get_user_favorites(self, username, limit=24, offset=0):
        """Get user's favorites using the API"""
        try:
            params = {
                'username': username,
                'limit': limit,
                'offset': offset,
                'mature_content': 'true'  # Include mature content
            }
            
            # Use the correct endpoint for getting all favorites
            response = self.session.get(f"{self.api_base}/collections/all", params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get favorites: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting favorites: {e}")
            return None

    def get_all_favorites(self, username):
        """Get ALL user's favorites with pagination"""
        print(f"📥 Fetching all favorites for user: {username}")
        
        all_deviations = []
        offset = 0
        limit = 24  # Max allowed by API for collections
        
        while True:
            print(f"  Fetching batch {offset//limit + 1} (offset: {offset})...")
            
            favorites_data = self.get_user_favorites(username, limit=limit, offset=offset)
            
            if not favorites_data:
                break
            
            deviations = favorites_data.get('results', [])
            
            if not deviations:
                print("  No more favorites found")
                break
            
            all_deviations.extend(deviations)
            print(f"  Found {len(deviations)} favorites in this batch")
            
            # Check if there are more
            has_more = favorites_data.get('has_more', False)
            if not has_more:
                print("  Reached end of favorites")
                break
            
            offset += limit
            time.sleep(0.5)  # Be respectful to the API
        
        print(f"🎯 Total favorites found: {len(all_deviations)}")
        return all_deviations

    def download_deviation(self, deviation):
        """Download a single deviation (images and videos)"""
        try:
            title = deviation.get('title', 'Unknown')
            author = deviation.get('author', {}).get('username', 'Unknown')
            deviation_id = deviation.get('deviationid', 'unknown')
            
            print(f"  📥 {title} by {author}")
            
            # Try to get the best download URL
            download_url = None
            content_type = "image"  # Default assumption
            
            # Method 1: Check if there's a download URL (best quality)
            if 'content' in deviation and 'src' in deviation['content']:
                download_url = deviation['content']['src']
                # Check if it's a video based on the URL or file size
                if any(vid_ext in download_url.lower() for vid_ext in ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv', '.m4v', '.wmv']):
                    content_type = "video"
            
            # Method 2: Check for video-specific content
            elif 'videos' in deviation and deviation['videos']:
                # DeviantArt sometimes has a videos array
                videos = deviation['videos']
                if isinstance(videos, list) and videos:
                    # Get the highest quality video
                    video = videos[-1] if videos else videos[0]
                    download_url = video.get('src')
                    content_type = "video"
            
            # Method 3: Try preview URLs (if download not available)
            elif 'preview' in deviation and 'src' in deviation['preview']:
                download_url = deviation['preview']['src']
                if any(vid_ext in download_url.lower() for vid_ext in ['.mp4', '.webm', '.mov']):
                    content_type = "video"
            
            # Method 4: Try thumbs as last resort
            elif 'thumbs' in deviation and deviation['thumbs']:
                # Get the largest thumbnail
                thumbs = deviation['thumbs']
                if isinstance(thumbs, list) and thumbs:
                    download_url = thumbs[-1].get('src')  # Last one is usually largest
            
            if not download_url:
                print(f"    ❌ No download URL found")
                self.failed_downloads.append(f"{title} by {author}")
                return False
            
            # Create filename
            filename = self.sanitize_filename(f"{author}_{title}_{deviation_id}")
            file_ext = self.guess_file_extension(download_url)
            full_filename = f"{filename}.{file_ext}"
            file_path = self.download_dir / full_filename
            
            # Skip if already downloaded
            if file_path.exists():
                print(f"    ✓ Already exists")
                return True
            
            # Download the file
            content_emoji = "🎬" if content_type == "video" else "📥"
            print(f"    {content_emoji} Downloading: {full_filename}")
            
            # Remove authorization header for media download
            headers = dict(self.session.headers)
            if 'Authorization' in headers:
                del headers['Authorization']
            
            # Use longer timeout for videos
            timeout = 60 if content_type == "video" else 30
            
            response = requests.get(download_url, headers=headers, stream=True, timeout=timeout)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = file_path.stat().st_size
                size_mb = file_size / (1024 * 1024)
                if content_type == "video":
                    print(f"    ✅ Downloaded video: {size_mb:.1f} MB")
                else:
                    print(f"    ✅ Downloaded: {file_size:,} bytes")
                self.downloaded_files.add(full_filename)
                return True
            else:
                print(f"    ❌ Download failed: HTTP {response.status_code}")
                self.failed_downloads.append(f"{title} by {author}")
                return False
                
        except Exception as e:
            print(f"    ❌ Error downloading: {e}")
            title = deviation.get('title', 'Unknown')
            author = deviation.get('author', {}).get('username', 'Unknown')
            self.failed_downloads.append(f"{title} by {author}")
            return False

    def sanitize_filename(self, filename):
        """Create a safe filename"""
        # Remove invalid characters
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return safe_filename[:200]  # Limit length

    def guess_file_extension(self, url):
        """Guess file extension from URL"""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Image formats
        if '.jpg' in path or '.jpeg' in path:
            return 'jpg'
        elif '.png' in path:
            return 'png'
        elif '.gif' in path:
            return 'gif'
        elif '.webp' in path:
            return 'webp'
        # Video formats
        elif '.mp4' in path:
            return 'mp4'
        elif '.webm' in path:
            return 'webm'
        elif '.mov' in path:
            return 'mov'
        elif '.avi' in path:
            return 'avi'
        elif '.mkv' in path:
            return 'mkv'
        elif '.flv' in path:
            return 'flv'
        elif '.m4v' in path:
            return 'm4v'
        elif '.wmv' in path:
            return 'wmv'
        else:
            return 'jpg'  # Default

    def download_all_favorites(self, username):
        """Main function to download all favorites"""
        print(f"🚀 Starting download of all favorites for: {username}")
        print(f"📁 Download directory: {self.download_dir.absolute()}")
        print("=" * 80)
        
        # Get all favorites
        all_favorites = self.get_all_favorites(username)
        
        if not all_favorites:
            print("❌ No favorites found or error occurred")
            return
        
        print(f"\n🎯 Processing {len(all_favorites)} favorites...")
        print("=" * 80)
        
        # Download each favorite
        for i, deviation in enumerate(all_favorites):
            print(f"\n[{i+1}/{len(all_favorites)}]", end=" ")
            self.download_deviation(deviation)
            
            # Small delay to be respectful
            time.sleep(0.5)
        
        # Print summary
        print(f"\n" + "=" * 80)
        print(f"📊 DOWNLOAD SUMMARY")
        print(f"=" * 80)
        print(f"Total favorites: {len(all_favorites)}")
        print(f"Successfully downloaded: {len(self.downloaded_files)}")
        print(f"Failed downloads: {len(self.failed_downloads)}")
        
        if self.failed_downloads:
            print(f"\n❌ Failed downloads:")
            for failed in self.failed_downloads[:10]:
                print(f"  - {failed}")
            if len(self.failed_downloads) > 10:
                print(f"  ... and {len(self.failed_downloads) - 10} more")
        
        print(f"\n📁 Files saved to: {self.download_dir.absolute()}")
        
        if len(self.downloaded_files) > 0:
            print(f"🎉 Successfully downloaded {len(self.downloaded_files)} images and videos!")


def main():
    print("🎨 Official DeviantArt API Favorites Downloader")
    print("=" * 80)
    print("Using the official DeviantArt API with OAuth 2.0")
    print("Much more reliable than web scraping!")
    print()
    
    downloader = DeviantArtAPIDownloader()
    
    # Try to load saved tokens and credentials
    tokens_loaded = downloader.load_tokens()
    
    if not tokens_loaded:
        # Need to set up OAuth app and authenticate
        print("🔧 No saved credentials found. Setting up OAuth application...")
        if not downloader.setup_oauth_app():
            print("❌ Failed to set up OAuth application")
            return
        
        if not downloader.authenticate():
            print("❌ Failed to authenticate")
            return
    else:
        # Test if the loaded tokens still work
        print("🔍 Testing saved authentication...")
        if not downloader.test_api_access():
            print("⚠ Saved tokens expired or invalid. Re-authenticating...")
            
            # If we have client credentials, just re-authenticate
            if downloader.client_id and downloader.client_secret:
                if not downloader.authenticate():
                    print("❌ Re-authentication failed")
                    return
            else:
                # Need to set up OAuth app again
                print("🔧 Setting up OAuth application...")
                if not downloader.setup_oauth_app():
                    print("❌ Failed to set up OAuth application")
                    return
                
                if not downloader.authenticate():
                    print("❌ Failed to authenticate")
                    return
        else:
            print("✅ Saved authentication is still valid!")
    
    # Get username
    username = input("\nEnter the DeviantArt username to download favorites from: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return
    
    # Download all favorites
    downloader.download_all_favorites(username)


if __name__ == "__main__":
    main() 