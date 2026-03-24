# Quick Start Guide

## 🚀 Run Streamlit Locally

### 1. Install dependencies
```bash
pip install -r requirements-full.txt
```

### 2. Set your OpenAI API key
```bash
# Windows Command Prompt
set OPENAI_API_KEY=your-key-here
set DATA_PIPELINE_MODE=embedded

# Windows PowerShell
$env:OPENAI_API_KEY="your-key-here"
$env:DATA_PIPELINE_MODE="embedded"
```

### 3. Run the app
```bash
streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser

---

## 📱 Access from Phone (Same WiFi)

### 1. Find your PC's IP address
```bash
ipconfig
```
Look for IPv4 Address (e.g., 192.168.1.100)

### 2. Run Streamlit with network access
```bash
# Windows Command Prompt
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501

# Or use this script
run_streamlit_network.bat
```

### 3. Access from phone
```
http://YOUR_IP:8501
```
Example: http://192.168.1.100:8501

---

## 🌐 Deploy to Streamlit Cloud

See DEPLOYMENT.md for full instructions

---

## 🐛 Troubleshooting

### App not loading?
- Check if OPENAI_API_KEY is set
- Verify all dependencies are installed
- Check console for error messages

### Can't access from phone?
- Ensure both devices on same WiFi
- Check Windows Firewall settings
- Try: `netsh advfirewall firewall add rule name="Streamlit" dir=in action=allow protocol=TCP localport=8501`

### Mobile display issues?
- The app uses custom CSS for mobile responsiveness
- Try rotating phone to landscape
- Use latest browser (Chrome/Safari recommended)
