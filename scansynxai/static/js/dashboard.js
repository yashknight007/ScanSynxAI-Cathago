document.addEventListener('DOMContentLoaded', function() {
    loadProfile();
    loadUploadedDocuments();

    document.getElementById('uploadForm').onsubmit = async function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        const response = await fetch(scanUploadUrl, {
            method: 'POST',
            body: formData,
            credentials: 'include'
        });
        const result = await response.json();
        document.getElementById('uploadMessage').innerText = result.message || result.error;
        if (result.message) {
            loadUploadedDocuments(); // Refresh document list after upload
        }
    };

    document.getElementById('creditRequestForm').onsubmit = async function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        // Convert requested_credits to a number
        const requestBody = {
            requested_credits: parseInt(data.requested_credits, 10)
        };
    
        // Log the request body
        console.log('Request Body:', requestBody);
    
        try {
            const response = await fetch(requestCreditsUrl, {
                method: 'POST',
                body: JSON.stringify(requestBody),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include'
            });
            
            const result = await response.json();
            console.log('Response:', result);  // Log the response
            document.getElementById('creditRequestMessage').innerText = result.message || result.error;
        } catch (error) {
            console.error('Error:', error);  // Log any errors
            document.getElementById('creditRequestMessage').innerText = 'An error occurred';
        }
    };

    document.getElementById('documentSelect').onchange = async function() {
        const docId = this.value;
        if (docId) {
            const response = await fetch(`/matches/${docId}/`, { credentials: 'include' });
            const data = await response.json();
            const list = document.getElementById('matchesList');
            list.innerHTML = '';
            data.matches.forEach(match => {
                const listItem = document.createElement('li');
                listItem.innerText = `Matched Document ID: ${match.matched_document_id}, TF-IDF Score: ${match.tfidf_score.toFixed(2)}, AI Score: ${match.ai_score.toFixed(2)}`;
                list.appendChild(listItem);
            });
        }
    };
});

async function loadProfile() {
    const response = await fetch(profileViewUrl, { credentials: 'include' });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById('username').innerText = `Username: ${data.username}`;
        document.getElementById('credits').innerText = `Credits: ${data.credits}`;
    }
}

async function loadUploadedDocuments() {
    const response = await fetch(getUploadedDocumentsUrl, { credentials: 'include' });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
    } else {
        const list = document.getElementById('uploadedDocumentsList');
        const select = document.getElementById('documentSelect');
        list.innerHTML = '';
        select.innerHTML = '<option value="">Select a document</option>';
        data.documents.forEach(doc => {
            const listItem = document.createElement('li');
            listItem.innerText = `Document ID: ${doc.id}, Uploaded At: ${new Date(doc.uploaded_at).toLocaleString()}`;
            list.appendChild(listItem);

            const option = document.createElement('option');
            option.value = doc.id;
            option.innerText = `Document ID: ${doc.id}`;
            select.appendChild(option);
        });
    }
}

function downloadScanHistory() {
    const list = document.getElementById('uploadedDocumentsList');
    let text = "Your Scan History:\n\n";
    list.querySelectorAll('li').forEach(item => {
        text += item.innerText + "\n";
    });

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'scan_history.txt';
    a.click();
    URL.revokeObjectURL(url);
}

// Function to get CSRF token from cookies
// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Make the request
fetch('/credits/request', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    credentials: 'include',
    body: JSON.stringify({
        requested_credits: numberOfCredits  // Replace with actual number
    })
});