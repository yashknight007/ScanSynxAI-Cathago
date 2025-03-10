from django.shortcuts import get_object_or_404,render
from django.db.models import Count, Sum

import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import UploadedDocument, Match
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import CreditRequest
from sentence_transformers import SentenceTransformer
import numpy as np



def extract_text_hybrid(pdf_path):
    """
    Extracts text using a hybrid approach:
    - First tries extracting normal text.
    - If no/little text is found, uses OCR on images.
    """
    extracted_text = ""

    # Step 1: Try extracting selectable text
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""

    # Debugging: Check if normal text was extracted
    print(f"🔍 Extracted Text (Normal) for {pdf_path[:50]}: {extracted_text[:500]}")

    # Step 2: If extracted text is too short, apply OCR
    if len(extracted_text.strip()) < 100:  # Adjust threshold as needed
        print("⚠️ Low text detected! Applying OCR...")
        images = convert_from_path(pdf_path)  # Convert PDF to images
        for img in images:
            extracted_text += pytesseract.image_to_string(img)  # OCR processing

    # Debugging: Check final extracted text
    print(f"🔍 Final Extracted Text for {pdf_path[:50]}: {extracted_text[:500]}")

    return extracted_text.strip()



@csrf_exempt
@login_required
def find_matches(request, doc_id):
    """Extract text from the requested document, process all others, and find matches."""
    document = get_object_or_404(UploadedDocument, id=doc_id)

    # Step 1: Extract text for the requested document if not already done
    if not document.text_content:
        pdf_path = os.path.join(default_storage.location, document.file.name)
        extracted_text = extract_text_hybrid(pdf_path)
        document.text_content = extracted_text
        document.save()

    # Step 2: Extract text for all other documents if missing
    all_documents = UploadedDocument.objects.exclude(text_content="")
    for doc in all_documents:
        if not doc.text_content:
            pdf_path = os.path.join(default_storage.location, doc.file.name)
            extracted_text = extract_text_hybrid(pdf_path)
            doc.text_content = extracted_text
            doc.save()

    # Step 3: Run Matching Algorithm
    match_documents(doc_id)

    # Step 4: Fetch and return matches
    matches = Match.objects.filter(document=document).values(
        "matched_document_id", "tfidf_score", "ai_score", "ocr_score"  # ✅ Added OCR Score
    )

    return JsonResponse({
        "doc_id": doc_id,
        "matches": list(matches)
    })





# Load AI Model once (BERT-based)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight but effective

def match_documents(new_doc_id=None):
    """Find similar documents using TF-IDF, OCR, and AI Embeddings."""
    documents = UploadedDocument.objects.exclude(text_content="").values("id", "text_content")

    if not documents:
        print("⚠️ No valid documents found!")
        return

    texts = [doc["text_content"].strip() if doc["text_content"] else "" for doc in documents]
    doc_ids = [doc["id"] for doc in documents]

    # Check if all documents are empty
    if all(text == "" for text in texts):
        print("⚠️ All documents are empty after text extraction!")
        return

    # 🔹 TF-IDF Vectorization
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError as e:
        print("⚠️ TF-IDF Error:", e)
        print("Texts being processed:", texts)  # Debugging
        return

    # 🔹 AI Embeddings (BERT)
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)

    # 🔹 Compute Cosine Similarities
    tfidf_sim_matrix = cosine_similarity(tfidf_matrix)
    ai_sim_matrix = cosine_similarity(embeddings)

    # 🚀 Update matches only for the **newly added document**
    if new_doc_id:
        new_doc_index = doc_ids.index(new_doc_id)

        for i, doc_id in enumerate(doc_ids):
            if i != new_doc_index:
                tfidf_score = float(tfidf_sim_matrix[new_doc_index][i])  # TF-IDF Score
                ai_score = float(ai_sim_matrix[new_doc_index][i])  # AI Score

                # Ensure no duplicate matches
                Match.objects.update_or_create(
                    document_id=new_doc_id,
                    matched_document_id=doc_id,
                    defaults={
                        "tfidf_score": tfidf_score,
                        "ai_score": ai_score,
                    },
                )

    print("✅ AI-based document matching completed!")

