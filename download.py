import os
import json
import subprocess
import tempfile
import urllib.parse
from http.server import BaseHTTPRequestHandler
import yt_dlp

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve HTML for root path
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALL-IN-ONE VIDEO DOWNLOADER</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            border: 2px solid #00ff88;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #00ff88;
            font-size: 32px;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
        
        .subtitle {
            color: #ccc;
            margin-bottom: 20px;
        }
        
        .url-box {
            margin: 20px 0;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #00ff88;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        input[type="text"]:focus {
            outline: none;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
        }
        
        .quality-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 20px 0;
        }
        
        .quality-btn {
            padding: 15px;
            border: 2px solid #555;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
        }
        
        .quality-btn:hover {
            border-color: #00ff88;
            transform: scale(1.05);
        }
        
        .quality-btn.active {
            background: rgba(0, 255, 136, 0.2);
            border-color: #00ff88;
        }
        
        .format-buttons {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        
        .format-btn {
            flex: 1;
            padding: 15px;
            border: 2px solid #555;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            font-size: 18px;
            transition: all 0.3s;
        }
        
        .format-btn:hover {
            border-color: #ff8800;
            transform: scale(1.05);
        }
        
        .format-btn.active {
            background: rgba(255, 136, 0, 0.2);
            border-color: #ff8800;
        }
        
        .download-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #00ff88, #0088ff);
            border: none;
            border-radius: 15px;
            color: white;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            margin: 30px 0;
            transition: all 0.3s;
        }
        
        .download-btn:hover:not(:disabled) {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 136, 255, 0.5);
        }
        
        .download-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .progress-section {
            display: none;
            margin: 20px 0;
            padding: 20px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            border: 2px solid #0088ff;
        }
        
        .progress-bar {
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #0088ff);
            width: 0%;
            transition: width 0.5s;
        }
        
        .status {
            text-align: center;
            margin: 10px 0;
            color: #00ff88;
            font-weight: bold;
        }
        
        .console {
            background: black;
            color: #00ff88;
            padding: 15px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 12px;
            height: 200px;
            overflow-y: auto;
            margin: 20px 0;
            display: none;
            border: 1px solid #00ff88;
        }
        
        .message {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
            display: none;
        }
        
        .success {
            background: rgba(0, 255, 136, 0.2);
            border: 2px solid #00ff88;
            color: #00ff88;
        }
        
        .error {
            background: rgba(255, 0, 0, 0.2);
            border: 2px solid #ff4444;
            color: #ff4444;
        }
        
        .test-urls {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }
        
        .test-url {
            background: rgba(0, 136, 255, 0.2);
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .test-url:hover {
            background: rgba(0, 136, 255, 0.4);
            transform: translateY(-2px);
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 15px;
            }
            
            .quality-buttons {
                grid-template-columns: repeat(2, 1fr);
            }
            
            h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 ALL-IN-ONE VIDEO DOWNLOADER</h1>
            <p class="subtitle">YouTube • Instagram • Facebook • TikTok • Twitter • 100+ Sites</p>
            <p style="color: #ff8800; font-size: 14px; margin-top: 10px;">
                ⚡ Hosted on Vercel • Fast & Reliable
            </p>
        </div>
        
        <div class="url-box">
            <input type="text" id="videoUrl" placeholder="🌐 Paste ANY video URL here...">
            
            <div class="test-urls">
                <div class="test-url" onclick="setTestUrl('youtube')">📺 YouTube Test</div>
                <div class="test-url" onclick="setTestUrl('instagram')">📷 Instagram Test</div>
                <div class="test-url" onclick="setTestUrl('tiktok')">🎵 TikTok Test</div>
            </div>
        </div>
        
        <div class="quality-buttons">
            <div class="quality-btn active" onclick="selectQuality('360p')">360p</div>
            <div class="quality-btn" onclick="selectQuality('480p')">480p</div>
            <div class="quality-btn" onclick="selectQuality('720p')">720p HD</div>
            <div class="quality-btn" onclick="selectQuality('1080p')">1080p FHD</div>
            <div class="quality-btn" onclick="selectQuality('best')">👑 Best</div>
            <div class="quality-btn" onclick="selectQuality('worst')">⚡ Fast</div>
        </div>
        
        <div class="format-buttons">
            <div class="format-btn active" onclick="selectFormat('mp4')">🎥 MP4 Video</div>
            <div class="format-btn" onclick="selectFormat('mp3')">🎵 MP3 Audio</div>
        </div>
        
        <button class="download-btn" id="downloadBtn" onclick="startDownload()">
            ⚡ START DOWNLOAD
        </button>
        
        <div class="progress-section" id="progressSection">
            <div class="status" id="progressText">Click START DOWNLOAD to begin</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="status" id="progressPercent">0%</div>
            
            <div class="console" id="console">
                > Ready to download...
            </div>
            
            <button onclick="toggleConsole()" style="
                width: 100%;
                padding: 10px;
                background: rgba(0, 255, 136, 0.2);
                border: 1px solid #00ff88;
                color: #00ff88;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 10px;
            ">
                📜 Show/Hide Console
            </button>
        </div>
        
        <div class="message success" id="successMessage">
            ✅ Download Successful!
        </div>
        
        <div class="message error" id="errorMessage">
            ❌ Download Failed!
        </div>
        
        <div class="footer">
            <p style="color: #888; margin-bottom: 15px;">
                ⚡ Powered by Vercel Serverless Functions
            </p>
            <button onclick="testDownload()" style="
                padding: 12px 25px;
                background: #0088ff;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
                margin: 5px;
            ">
                🧪 Test Download
            </button>
        </div>
    </div>
    
    <script>
        let selectedQuality = '360p';
        let selectedFormat = 'mp4';
        
        // Test URLs
        const testUrls = {
            'youtube': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'instagram': 'https://www.instagram.com/p/CrY1Kz0vCkE/',
            'tiktok': 'https://www.tiktok.com/@example/video/1234567890'
        };
        
        // Quality selection
        function selectQuality(quality) {
            selectedQuality = quality;
            document.querySelectorAll('.quality-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            addConsole(`Quality set to: ${quality}`);
        }
        
        // Format selection
        function selectFormat(format) {
            selectedFormat = format;
            document.querySelectorAll('.format-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            addConsole(`Format set to: ${format.toUpperCase()}`);
        }
        
        // Set test URL
        function setTestUrl(platform) {
            document.getElementById('videoUrl').value = testUrls[platform];
            addConsole(`Test URL set for: ${platform}`);
        }
        
        // Add to console
        function addConsole(text) {
            const consoleEl = document.getElementById('console');
            consoleEl.innerHTML += `\\n> ${text}`;
            consoleEl.scrollTop = consoleEl.scrollHeight;
        }
        
        // Toggle console
        function toggleConsole() {
            const consoleEl = document.getElementById('console');
            if (consoleEl.style.display === 'none') {
                consoleEl.style.display = 'block';
            } else {
                consoleEl.style.display = 'none';
            }
        }
        
        // Show messages
        function showSuccess(msg) {
            const el = document.getElementById('successMessage');
            el.textContent = msg;
            el.style.display = 'block';
            setTimeout(() => el.style.display = 'none', 5000);
        }
        
        function showError(msg) {
            const el = document.getElementById('errorMessage');
            el.textContent = msg;
            el.style.display = 'block';
            setTimeout(() => el.style.display = 'none', 5000);
        }
        
        function hideMessages() {
            document.getElementById('successMessage').style.display = 'none';
            document.getElementById('errorMessage').style.display = 'none';
        }
        
        // Start download
        async function startDownload() {
            const url = document.getElementById('videoUrl').value.trim();
            
            if (!url) {
                showError('Please enter a URL');
                return;
            }
            
            if (!url.startsWith('http')) {
                showError('Please enter a valid URL');
                return;
            }
            
            const btn = document.getElementById('downloadBtn');
            const progressSection = document.getElementById('progressSection');
            
            btn.disabled = true;
            btn.innerHTML = '🔄 Processing...';
            progressSection.style.display = 'block';
            hideMessages();
            
            addConsole(`Starting download...`);
            addConsole(`URL: ${url.substring(0, 50)}...`);
            addConsole(`Quality: ${selectedQuality}`);
            addConsole(`Format: ${selectedFormat}`);
            
            // Update progress
            document.getElementById('progressFill').style.width = '10%';
            document.getElementById('progressPercent').textContent = '10%';
            document.getElementById('progressText').textContent = 'Processing URL...';
            
            try {
                // Make request to download endpoint
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        url: url,
                        quality: selectedQuality,
                        format: selectedFormat
                    })
                });
                
                document.getElementById('progressFill').style.width = '50%';
                document.getElementById('progressPercent').textContent = '50%';
                document.getElementById('progressText').textContent = 'Downloading...';
                
                if (response.ok) {
                    const blob = await response.blob();
                    
                    document.getElementById('progressFill').style.width = '90%';
                    document.getElementById('progressPercent').textContent = '90%';
                    document.getElementById('progressText').textContent = 'Finalizing...';
                    
                    // Create download link
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = downloadUrl;
                    
                    // Get filename from headers or generate
                    const contentDisposition = response.headers.get('Content-Disposition');
                    let filename = 'download';
                    if (contentDisposition) {
                        const match = contentDisposition.match(/filename="(.+)"/);
                        if (match) filename = match[1];
                    } else {
                        filename = `video_${Date.now()}.${selectedFormat}`;
                    }
                    
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(downloadUrl);
                    
                    document.getElementById('progressFill').style.width = '100%';
                    document.getElementById('progressPercent').textContent = '100%';
                    document.getElementById('progressText').textContent = 'Download Complete!';
                    
                    addConsole(`✅ Download complete: ${filename}`);
                    showSuccess(`Downloaded: ${filename}`);
                    
                } else {
                    const error = await response.text();
                    addConsole(`❌ Server error: ${error}`);
                    showError(`Download failed: ${error}`);
                }
                
            } catch (error) {
                addConsole(`❌ Network error: ${error.message}`);
                showError(`Network error: ${error.message}`);
            } finally {
                btn.disabled = false;
                btn.innerHTML = '⚡ START DOWNLOAD';
                
                // Reset progress after delay
                setTimeout(() => {
                    document.getElementById('progressFill').style.width = '0%';
                    document.getElementById('progressPercent').textContent = '0%';
                }, 3000);
            }
        }
        
        // Test download
        function testDownload() {
            document.getElementById('videoUrl').value = testUrls.youtube;
            addConsole('Test URL loaded. Click START DOWNLOAD to test.');
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('progressSection').style.display = 'block';
            addConsole('✅ ALL-IN-ONE DOWNLOADER READY');
            addConsole('🌐 Supports YouTube, Instagram, TikTok, Facebook, etc.');
            addConsole('⚡ Powered by Vercel Serverless Functions');
        });
    </script>
</body>
</html>
            '''
            
            self.wfile.write(html.encode('utf-8'))
            return
            
        # Handle API requests
        elif self.path.startswith('/api/download'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            url = data.get('url')
            quality = data.get('quality', 'best')
            format_type = data.get('format', 'mp4')
            
            if not url:
                self.send_error(400, "URL required")
                return
            
            try:
                # Create temporary directory for download
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Setup yt-dlp options
                    ydl_opts = {
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'quiet': True,
                        'no_warnings': True,
                        'noplaylist': True,
                    }
                    
                    if format_type == 'mp3':
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        })
                    else:
                        # Video format selection
                        if quality == 'worst':
                            ydl_opts['format'] = 'worst'
                        elif quality == '360p':
                            ydl_opts['format'] = 'best[height<=360]'
                        elif quality == '480p':
                            ydl_opts['format'] = 'best[height<=480]'
                        elif quality == '720p':
                            ydl_opts['format'] = 'best[height<=720]'
                        elif quality == '1080p':
                            ydl_opts['format'] = 'best[height<=1080]'
                        else:  # best
                            ydl_opts['format'] = 'best'
                    
                    # Download using yt-dlp
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        
                        # Find the downloaded file
                        downloaded_files = os.listdir(tmpdir)
                        if not downloaded_files:
                            self.send_error(500, "No file downloaded")
                            return
                        
                        file_path = os.path.join(tmpdir, downloaded_files[0])
                        
                        # Read file content
                        with open(file_path, 'rb') as f:
                            file_content = f.read()
                        
                        # Get filename
                        filename = os.path.basename(file_path)
                        
                        # Send response
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/octet-stream')
                        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                        self.send_header('Content-Length', str(len(file_content)))
                        self.end_headers()
                        
                        self.wfile.write(file_content)
                        
            except Exception as e:
                self.send_error(500, f"Download error: {str(e)}")
                return
            
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        self.do_GET()