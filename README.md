
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

## 🛠 Installation Guide

🔹 1. Clone the Repository  
```sh
git clone https://github.com/yashknight007/ScanSynxAI-Cathago.git
```
🔹 2. Create & Activate Virtual Environment
```sh
# Create virtual environment (Windows)
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source .venv/bin/activate
```
🔹 3. Install Dependencies
```sh
pip install -r requirements.txt
```
🔹 4. Apply Migrations
```sh
cd ScanSynxAI
python manage.py makemigrations
python manage.py migrate
```
🔹 5. Create Superuser (For Admin Panel)
```sh
python manage.py createsuperuser
```
🔹 6. Run the Development Server
```sh
python manage.py runserver
```
## 🚀Visit: http://127.0.0.1:8000
## 🎥 Project Demo
🔗 [Watch Demo on Google Drive](https://drive.google.com/file/d/1s2XDhonIIWJBxpa5cjWYezloFOOPJbtA/view?usp=sharing)

## 🔍 API Testing
```sh
C:\Users\yashk>curl -X POST http://127.0.0.1:8000/auth/register/ -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"email\": \"test@example.com\", \"password\": \"testpass\"}"
{"error": "Username already taken"}

C:\Users\yashk>curl -X POST "http://127.0.0.1:8000/auth/login/" -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"testpass\"}" -c cookies.txt
{"message": "Login successful"}

C:\Users\yashk>curl -X GET "http://127.0.0.1:8000/user/profile/" -H "Content-Type: application/json" -b cookies.txt
{"username": "testuser", "credits": 39}

C:\Users\yashk>curl -X POST "http://127.0.0.1:8000/scan/upload/" -F "file=@C:\Users\yashk\OneDrive\Documents\gfgcertificate.pdf" -b cookies.txt
{"message": "File uploaded successfully", "file_path": "/media/uploads/gfgcertificate_eBoYkAB.pdf", "remaining_credits": 38}

C:\Users\yashk>curl -X GET "http://127.0.0.1:8000/documents/" -b cookies.txt
{"documents": [{"id": 1, "file": "uploads/Yashx.pdf", "uploaded_at": "2025-03-06T02:06:51.935Z"}, {"id": 2, "file": "uploads/Yashx_WitV0u5.pdf", "uploaded_at": "2025-03-06T02:06:55.904Z"}, {"id": 3, "file": "uploads/gfgcertificate.pdf", "uploaded_at": "2025-03-06T04:02:48.963Z"}, {"id": 4, "file": "uploads/Offer letter_CSRBOX_signed.pdf", "uploaded_at": "2025-03-09T12:30:37.282Z"}

C:\Users\yashk>curl -X GET "http://127.0.0.1:8000/matches/1/" -b cookies.txt
{"doc_id": 1, "matches": [{"matched_document_id": 2, "tfidf_score": 1.000000000000001, "ai_score": 0.9999998211860657, "ocr_score": 1.000000000000013}, {"matched_document_id": 3, "tfidf_score": 0.021885171210384285, "ai_score": 0.2797359824180603, "ocr_score": 0.02157162670707309}, {"matched_document_id": 4, "tfidf_score": 0.03217790257946981, "ai_score": 0.2590469717979431, "ocr_score": null}

C:\Users\yashk>curl -X POST "http://127.0.0.1:8000/credits/request" -H "Content-Type: application/json" -d "{\"requested_credits\": 10}" -b cookies.txt
{"message": "Credit request submitted successfully", "requested_credits": 10, "status": "pending"}
```
For Admin 
```sh
To find csrf token 
C:\Users\yashk>curl -c cookies.txt -b cookies.txt -s "http://127.0.0.1:8000/admin/login/" | findstr csrfmiddlewaretoken
<form action="/admin/login/" method="post" id="login-form"><input type="hidden" name="csrfmiddlewaretoken" value="zQaE1NwSEt8NQnPuYSVwOKmKQ5SdNDAJqX1FRym5bvWM2bshFXG6b1eOPUpEi407">

C:\Users\yashk>curl -X POST "http://127.0.0.1:8000/admin/login/" ^
More?      -H "Content-Type: application/x-www-form-urlencoded" ^
More?      -H "Referer: http://127.0.0.1:8000/admin/login/" ^
More?      -H "X-CSRFToken: zJ6OPHujRruV6JmATPou9MWLDJWMiTy1mInR6VqQIlIYgEv2JPrud4h8LR7E122M" ^
More?      -b cookies.txt -c cookies.txt ^
More?      --data "csrfmiddlewaretoken=zQaE1NwSEt8NQnPuYSVwOKmKQ5SdNDAJqX1FRym5bvWM2bshFXG6b1eOPUpEi407&username=yashk&password=Y@shking3"

C:\Users\yashk>curl -b cookies.txt -X GET http://127.0.0.1:8000/admin/analytics/
{"analytics": {"total_users": 2, "total_documents_uploaded": 6, "total_credit_requests": 3, "approved_credit_requests": 2, "pending_credit_requests": 1,
```





