🚀 How It Works
1️⃣ User System
Register/Login as a User or Admin
Users can upload plain text documents
View profile to track scans & credits
2️⃣ Credit System
20 free scans/day (auto-reset at midnight)
Users can request more credits from admins
Admins can approve/deny credit requests
3️⃣ Document Scanning & Matching
Upload a document → System checks for similar stored documents
Uses word frequency, Levenshtein distance, and AI models
Bonus: AI-powered matching with OpenAI, Gemini, or DeepSeek
4️⃣ Smart Analytics Dashboard
📊 Admin Panel Features:
✔ Track daily scans per user
✔ Identify top scanned topics
✔ View top users by scans & credits used
✔ Generate credit usage reports

⚡ API Endpoints
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	User login (session-based)
GET	/user/profile	Get user profile & credits
POST	/scan	Upload document for scanning (uses 1 credit)
GET	/matches/:docId	Get matching documents
POST	/credits/request	Request admin to add credits
GET	/admin/analytics	View analytics dashboard
🏗 Tech Stack
💻 Frontend: HTML, CSS, JavaScript (No frameworks)
🛠 Backend: Python (Django/Flask)
🗄 Database: SQLite (or JSON files for lightweight storage)
📂 File Storage: Locally stored documents
🔐 Authentication: Secure hashed password login
📖 Text Matching: Levenshtein Distance, Word Frequency

🎯 Bonus Features
✨ AI-powered document matching (OpenAI, Gemini, DeepSeek)
✨ Automated credit reset at midnight
✨ User activity logs (track scans & credit usage)
✨ Admin dashboard with reports
✨ Export user scan history

⚙ Setup Instructions
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/YOUR_GITHUB_USERNAME/document-scanner-matching.git
cd document-scanner-matching
2️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
3️⃣ Run the Server
sh
Copy
Edit
python manage.py runserver
🔗 Open http://127.0.0.1:8000 in your browser

🛡 Security Measures
✔ Password hashing for secure logins
✔ Role-based authentication (Users vs. Admins)
✔ Rate limiting to prevent abuse
✔ CSRF protection for secure API requests

📸 Screenshots & Demo

🎥 Watch the Demo Video

📜 License
This project is open-source under the MIT License.

🤝 Contributors
👤 Your Name - GitHub Profile
👤 Other Contributors

🚀 Final Submission
Submit your GitHub repo with:
✔ ✅ Complete Code (Frontend + Backend)
✔ 📄 README.md (with setup, API, features)
✔ 📝 Sample Documents (for testing)
✔ 📸 Screenshots / 🎥 Demo Video

🏆 Evaluation Criteria
✔ Functionality: Credit system & document matching
✔ Performance: Handling multiple users
✔ Security: Password hashing & rate limiting
✔ Scalability: Multi-user local server support
✔ Code Quality: Modular, well-documented
✔ Bonus AI: AI-powered document matching

🔥 Start Contributing Now!
💻 Fork the repo & submit PRs! Let’s build something amazing. 🚀
