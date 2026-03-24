@echo off
REM Run Streamlit accessible from local network

echo ========================================
echo  Streamlit - Network Access Mode
echo ========================================
echo.
echo  This will start Streamlit and allow
echo  connections from other devices on
echo  your network (phone, tablet, etc.)
echo.
echo  Access from phone: http://YOUR_IP:8501
echo.
echo  To find your IP, run: ipconfig
echo.
echo ========================================
echo.

streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
