import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from docs.models import UploadedDocument, UserProfile  # Import your models
from django.utils import timezone
from docs.models import CreditRequest,DocumentScan,CreditUsage
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum
from datetime import timedelta, date


def landing_page(request):
    return render(request, "landing.html")
def dashboard(request):
    return render(request, "dashboard.html")
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already taken"}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User registered successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Proper decoding of JSON
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # Django session login
                request.session.set_expiry(86400)  # Session expires in 1 day
                return JsonResponse({"message": "Login successful"})

            return JsonResponse({"error": "Invalid credentials"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Function to manage user credits (20 credits reset daily)
def get_user_credits(request):
    today_date = now().date().isoformat()

    if request.session.get("credits_date") != today_date:
        request.session["credits"] = 20
        request.session["credits_date"] = today_date

    return request.session.get("credits", 20)


@csrf_exempt
def profile_view(request):
    if not request.user.is_authenticated:  # Manually check authentication
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    if request.method == "GET":
        user_profile = request.user.userprofile  # Access the UserProfile
        return JsonResponse({
            "username": request.user.username,
            "credits": user_profile.credits
        }, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def list_credit_requests(request):
    if request.method == "GET":
        requests = CreditRequest.objects.filter(user=request.user).values("id", "requested_credits", "status", "created_at")
        return JsonResponse({"credit_requests": list(requests)}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt
@login_required
def scan_upload(request):
    if request.method == "POST":
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        # Fetch user profile and check credits
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if user_profile.credits <= 0:
            return JsonResponse({"error": "Insufficient credits"}, status=400)

        # Handle file upload
        if "file" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        uploaded_file = request.FILES["file"]

        # Save file to media storage
        file_path = default_storage.save(f"uploads/{uploaded_file.name}", ContentFile(uploaded_file.read()))

        # Save file details in the database
        document = UploadedDocument.objects.create(
            file=file_path,  
            uploaded_at=timezone.now(),
            user=request.user  
        )
        document.save()

        # Deduct 1 credit and save
        user_profile.credits -= 1
        user_profile.save()

        return JsonResponse({
            "message": "File uploaded successfully",
            "file_path": document.file.url,
            "remaining_credits": user_profile.credits
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)



def get_uploaded_documents(request):
    if request.method == "GET":
        user = request.user  # Get the logged-in user

        # Fetch all documents uploaded by this user
        documents = UploadedDocument.objects.filter(user=user).values(
            "id", "file", "uploaded_at"
        )

        return JsonResponse({"documents": list(documents)}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)




@csrf_exempt
@login_required
def request_credits(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            requested_credits = data.get("requested_credits")

            if not isinstance(requested_credits, int) or requested_credits <= 0:
                return JsonResponse({"error": "Invalid credit amount"}, status=400)

            # Create a new credit request
            CreditRequest.objects.create(user=request.user, requested_credits=requested_credits)

            return JsonResponse({
                "message": "Credit request submitted successfully",
                "requested_credits": requested_credits,
                "status": "pending"
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
@user_passes_test(lambda u: u.is_staff)  # Only admins can approve
def approve_credit_request(request, request_id):
    if request.method == "POST":
        try:
            credit_request = CreditRequest.objects.get(id=request_id, status="pending")
            credit_request.status = "approved"
            credit_request.approved_at = now()
            credit_request.save()

            # Grant credits to the user
            user_profile = credit_request.user.userprofile  # Access the UserProfile
            user_profile.credits += credit_request.requested_credits
            user_profile.save()

            return JsonResponse({"message": "Credit request approved", "new_credits": user_profile.credits})

        except CreditRequest.DoesNotExist:
            return JsonResponse({"error": "Credit request not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@staff_member_required
def admin_analytics(request):
    if request.method == "GET":
        # 🟢 Basic Analytics
        analytics_data = {
            "total_users": User.objects.count(),
            "total_documents_uploaded": UploadedDocument.objects.count(),
            "total_credit_requests": CreditRequest.objects.count(),
            "approved_credit_requests": CreditRequest.objects.filter(status="approved").count(),
            "pending_credit_requests": CreditRequest.objects.filter(status="pending").count(),
        }

        # 🟢 Track the number of scans per user per day (last 7 days)
        today = now().date()
        scans_per_day = (
            DocumentScan.objects.filter(scanned_at__date__gte=today - timedelta(days=6))
            .values("user__username", "scanned_at__date")
            .annotate(scan_count=Count("id"))
            .order_by("scanned_at__date")
        )

        # 🟢 Identify most common scanned document topics
        most_common_topics = (
            DocumentScan.objects.values("topic")
            .annotate(count=Count("topic"))
            .order_by("-count")[:5]
        )

        # 🟢 View top users by scans
        top_users_by_scans = (
            DocumentScan.objects.values("user__username")
            .annotate(scan_count=Count("id"))
            .order_by("-scan_count")[:5]
        )

        # 🟢 View top users by credit usage
        top_users_by_credits = (
            CreditUsage.objects.values("user__username")
            .annotate(total_credits=Sum("credits_used"))
            .order_by("-total_credits")[:5]
        )

        # 🟢 Add the detailed analytics data
        analytics_data.update({
            "scans_per_day": list(scans_per_day),
            "most_common_topics": list(most_common_topics),
            "top_users_by_scans": list(top_users_by_scans),
            "top_users_by_credits": list(top_users_by_credits),
        })

        return JsonResponse({"analytics": analytics_data}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)
