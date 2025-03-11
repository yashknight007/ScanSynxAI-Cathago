
# ScanSynxAI

Hii ! DO you need help with documents scanning and matching? Here we are get 20 free credits to scan and match them powered with Bert Ai.

## ✔ User Authentication 🔒 
With Django's powerful built in ORM for User Authentication and Admin Panel. Its Safe and Secure. With Profile Section to display user credits, past scans, and requests.

## ✔ Credit System 🪙
Each user gets 20 free scans per day (auto-reset at midnight).
Users can request additional credits if they exceed their limit.
Admins can approve or deny credit requests.
Each document scan deducts 1 credit from the user’s balance.

## ✔ Document Scanning & Matching 🧠 
Users can upload a plain text file for scanning.
System scans with the help of an intelligent combination of text extraction and OCR and matches with the help of Bert AI model to find similarity.

## ✔ Smart Analytics Dashboard 📊 
Admin can track the number of scans per user per day.
Identify most common scanned document topics.
View top users by scans and credit usage.
Generate credit usage statistics for admins
## ✔ API Endpoints

| Method/Endpoint             | Description                                                           |
| ----------------- | ------------------------------------------------------------------ |
| ✔a. POST/auth/register | User registration |
| ✔b. POST/auth/login | User login (Session-based) |
| ✔c. GET/user/profile | Get user profile & credits |
| ✔d. POST/scan | Upload document for scanning (uses 1 credit) |
| ✔e. GET/matches/:docId | Get matching documents |
| ✔f. POST/credits/request | Request admin to add credits |
| ✔g. GET/admin/analytics | Get analytics for admins |
##  🏗 Tech Stack 

- **Frontend:** HTML, CSS, JavaScript (No frameworks)
- **Backend:** Django (Python)
- **Database:** SQLite
- **Authentication:** Username-password login (hashed)
- **Matching Algorithm:** Tf-IDF, Cosine Similarity
- **Bonus AI Model:** Bert ("all-MiniLM-L6-v2")
  
![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-4.0-green?style=flat-square)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)

