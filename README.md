# NarrowAI 🔍🤖

**NarrowAI** is an AI-powered reconnaissance tool designed for ethical hackers, cybersecurity enthusiasts. It automates the process of gathering target information and enriches the results with an AI-powered vulnerability analysis using Google's Gemini model.

---

## 👤 Author  
Tareq Abu Khashabeh (@DRX0)

---

## 🧠 Features

- WHOIS lookup  
- DNS record fetching  
- Subdomain enumeration  
- Email extraction from homepage  
- Common port scanning with service and version detection  
- AI-powered analysis and vulnerability summary (powered by Google Gemini)  
- Interactive AI chat for follow-up questions about the scan results  

---

## 🛠️ Installation

1. Clone this repository:

```bash
git clone https://github.com/Tareq-Abukhashabeh/NarrowAI.git
cd NarrowAI

Install required Python packages:
pip install -r requirements.txt
```
---

## 🔑 Gemini API Setup
NarrowAI uses Google's Gemini AI for advanced vulnerability analysis. To use the AI features, you need to:

Sign up or log in to Google Gemini (Google Cloud's generative AI platform).

Create a project and enable the Gemini API.

Generate an API key.

Open the file narrowai.py and replace the placeholder GEMINI_API_KEY value with your actual API key:
```bash
GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
```
Without this API key, NarrowAI will run the recon steps but skip AI-powered analysis.

---

## 🚀 Usage
Run the tool against a target domain or IP:
```bash
python3 narrowai.py <target>
```
---

## 📂 Output
The tool will save the recon report and AI analysis in:

output/report.txt
You can open this file anytime to review detailed results.

---

## 💬 Interactive AI Chat
After the scan and analysis complete, NarrowAI launches an interactive chat mode. You can ask follow-up questions about vulnerabilities, open ports, or general security advice based on the scan results.

Type exit or quit to leave the chat.

---

## 🧪 Planned Enhancements
 Web-based GUI: Build a clean, responsive web interface for launching scans, reviewing results, and interacting with the AI.

 HTML/PDF Report Export: Automatically generate visually formatted reports in HTML and downloadable PDF formats.

 Database Integration: Store scan data and AI analyses in a local or remote database for history tracking, filtering, and re-analysis.

---

## ⚠️ Disclaimer
This tool is intended for educational and authorized penetration testing only.
Do not use it against any system you do not have explicit permission to test. Unauthorized use may be illegal and unethical.

---

## 📄 License
This project is licensed under the MIT License.


---

## 📞 Contact
Created by Tareq Abu Khashabeh (@DRX0)
GitHub: https://github.com/Tareq-Abukhashabeh



