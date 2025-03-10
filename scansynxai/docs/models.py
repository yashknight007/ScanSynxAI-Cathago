from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class DocumentScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100)  # Document topic
    scanned_at = models.DateTimeField(default=now)

class CreditUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credits_used = models.IntegerField()
    used_at = models.DateTimeField(default=now)

class UploadedDocument(models.Model):
    
    file = models.FileField(upload_to="uploads/")  # Store files in /media/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Track who uploaded i
    text_content = models.TextField(null=True, blank=True)  # Extracted text
    ocr_text_content = models.TextField(null=True, blank=True)  # Text extracted via OCR

    def __str__(self):
        return self.file.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"   


class Match(models.Model):
    document = models.ForeignKey(
        UploadedDocument, 
        on_delete=models.CASCADE, 
        related_name="matches_as_document"
    )
    matched_document = models.ForeignKey(
        UploadedDocument, 
        on_delete=models.CASCADE, 
        related_name="matches_as_matched_document",
        null=True,
        blank=True
    )
    tfidf_score = models.FloatField(null=True, blank=True)  # 🔹 TF-IDF Similarity Score
    ocr_score = models.FloatField(null=True, blank=True)    # 🔹 OCR-Based Similarity Score ✅
    ai_score = models.FloatField(null=True, blank=True)     # 🔹 AI Embedding Score (BERT)

    def __str__(self):
        return f"Match: {self.document.id} ↔ {self.matched_document.id} (AI: {self.ai_score:.2f}, OCR: {self.ocr_score:.2f})"


class CreditRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credit_requests")
    requested_credits = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("denied", "Denied")],
        default="pending"
    )
    created_at = models.DateTimeField(default=now)
    approved_at = models.DateTimeField(null=True, blank=True)

    def approve(self):
        if self.status == "pending":
            self.status = "approved"
            self.approved_at = now()
            self.user.userprofile.credits += self.requested_credits
            self.user.userprofile.save()
            self.save()

    def deny(self):
        if self.status == "pending":
            self.status = "denied"
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.requested_credits} credits - {self.status}"
