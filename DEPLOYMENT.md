# Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud (FREE)

### Steps:

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Connect your GitHub repository**
   - Click "New app"
   - Select your repository: `AKHIL/data-analysis-pipeline`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

4. **Add your OpenAI API Key**
   - Click "Advanced settings"
   - Add environment variable: `OPENAI_API_KEY` = `your-key-here`
   - Add: `DATA_PIPELINE_MODE` = `embedded`

5. **Click "Deploy"**

### Your app will be live at:
`https://your-app-name.streamlit.app`

✅ **This URL works on mobile phones!**

---

## 📱 Access from Phone (Local Network)

If running locally on your PC:

1. **Find your PC's IP address**
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., `192.168.1.100`)

2. **Run Streamlit**
   ```bash
   streamlit run streamlit_app.py --server.address 0.0.0.0
   ```

3. **Access from phone browser**
   ```
   http://YOUR_IP_ADDRESS:8501
   ```
   Example: `http://192.168.1.100:8501`

⚠️ **Both devices must be on the same WiFi network**

---

## 🔧 Alternative: Deploy to Render (FREE)

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
6. Add environment variables (OPENAI_API_KEY, etc.)

---

## ❌ Why NOT Vercel?

Vercel doesn't support Streamlit because:
- Streamlit needs a persistent Python server process
- Vercel only supports serverless functions (short-lived)
- Streamlit's WebSocket connections don't work with Vercel's architecture

**Use Streamlit Cloud instead - it's made for Streamlit apps!**
