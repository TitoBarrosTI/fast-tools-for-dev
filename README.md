
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## 🔎 About  
Fast Tools for Devs is a lightweight utility desktop app built with **Python + PySide6**.  
It provides quick-access tools developers often need during daily work: password generation, Base64 utilities, GUID creation, hashing, and text search.  
Simple, clean, fast, and designed for productivity.

---

## ✨ Features
```
- Password generator  
- Hash generator
- Base64 file decoder + image preview  
- Image → Base64 converter
```

---

## 🚀 Installation
```bash
git clone https://github.com/titobarrosti/fast-tools-for-dev.git
cd fast-tools-for-dev
pip install -r requirements.txt
python main.py
```
---
## 📋 Requirements

Python 3.12
PySide6
Standard libraries: secrets, base64, os, sys

To install all dependencies, run:
```
pip install -r requirements.txt
```
---

## 📦 Build Executable
```bash
pyinstaller --noconsole --onefile main.py
```

## 📁 Project Structure
```
fast-tools-for-dev/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
```
---
## 🛣️ Roadmap
 ```
 Text Search Tool (under development)
 GUID Generator
 ```

## 📄 License
MIT License — see [LICENSE]