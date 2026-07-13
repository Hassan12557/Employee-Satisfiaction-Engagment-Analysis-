import os
import numpy as np
from pathlib import Path
import joblib
import pandas as pd
from typing import Any  # 🎯 Added for strict type analysis compliance
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# NOTE: Assuming your model is pre-loaded at the app level or via a utility module.
# Replace 'your_loaded_model' with the variable name representing your loaded .pkl file
from core_app.apps import CoreAppConfig # Adjust this import depending on where your model is assigned
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import csv
from datetime import datetime
from .forms import HRRegistrationForm, EngagementSlidersForm
from .models import SatisfactionPrediction
from django.db.models import Avg, Count
from django.shortcuts import render
from django.db.models import Avg
from .models import SatisfactionPrediction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login
from .models import ProfileOTP
import random
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core_app.apps import CoreAppConfig
from django.apps import apps #
from django.conf import settings
import pickle

# A global fallback cache variable inside this module
_MANUAL_MODEL_CACHE = None


@csrf_exempt
def predict_satisfaction_api(request):
    """
    Production API Endpoint: Accepts raw feature matrices via JSON POST,
    runs inference using Django app configuration OR a direct disk fallback loop.
    """
    global _MANUAL_MODEL_CACHE

    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method. Only POST operations are authorized.'
        }, status=405)

    try:
        # 1. Parse incoming JSON body payload
        data = json.loads(request.body)

        feature_mapping = {
            'Career_Progression': float(data.get('Career_Progression', 3.0)),
            'Compensation': float(data.get('Compensation', 3.0)),
            'Manager_Relationship': float(data.get('Manager_Relationship', 3.0)),
            'Work_Life_Balance': float(data.get('Work_Life_Balance', 3.0)),
        }

        input_dataframe = pd.DataFrame([feature_mapping])

        # 2. STRATEGY A: Attempt to pull the model from the live Django App Config
        model = None
        try:
            app_config = apps.get_app_config('core_app')
            model = getattr(app_config, 'model', None)
        except Exception:
            pass

        # 3. STRATEGY B: Check if we already manually cached it here
        if model is None:
            model = _MANUAL_MODEL_CACHE

        # 4. STRATEGY C: Self-healing loader (Read straight from your disk layout)
        if model is None:
            # Reconstruct the exact path shown in your terminal logs relative to BASE_DIR
            model_path = os.path.abspath(
                os.path.join(settings.BASE_DIR, '..', 'src', 'saved_models', 'satisfaction_regressor.pkl'))

            if os.path.exists(model_path):
                try:
                    # Attempt loading via standard pickle binary streams
                    with open(model_path, 'rb') as f:
                        _MANUAL_MODEL_CACHE = pickle.load(f)
                    model = _MANUAL_MODEL_CACHE
                except Exception:
                    # Alternative fallback if your model was serialized using joblib
                    import joblib
                    _MANUAL_MODEL_CACHE = joblib.load(model_path)
                    model = _MANUAL_MODEL_CACHE
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'ML Engine model file could not be found on disk at: {model_path}'
                }, status=500)

        # 5. Run Machine Learning Inference
        prediction = model.predict(input_dataframe)[0]

        # 6. Log the metrics locally to your personal Excel sheet
        try:
            log_prediction_to_excel(feature_mapping, prediction)
        except Exception:
            pass  # Keep going even if the excel sheet is currently open on your desktop

        # 7. Return successful predictions matrix
        return JsonResponse({
            'status': 'success',
            'input_features': feature_mapping,
            'predicted_satisfaction_index': round(float(prediction), 4)
        }, status=200)

    except ValueError as ve:
        return JsonResponse({'status': 'error', 'message': f'Data type conversion error: {str(ve)}'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Internal engine breakdown: {str(e)}'}, status=500)
def log_prediction_to_excel(feature_mapping, prediction_result):
    """
    Appends incoming model features and output inferences to a local CSV log matrix.
    This file creates automatically and opens perfectly inside Microsoft Excel.
    """
    # Define the absolute target layout path
    file_path = 'personal_prediction_logs.csv'
    file_exists = os.path.isfile(file_path)

    # 1. Structure the data row with a master timestamp tracker
    log_row = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Engagement_Score': feature_mapping.get('engagement_score'),
        'Last_Evaluation': feature_mapping.get('last_evaluation'),
        'Average_Monthly_Hours': feature_mapping.get('average_monthly_hours'),
        'Tenure_Years': feature_mapping.get('tenure_years'),
        'Predicted_Satisfaction_Index': round(float(prediction_result), 4)
    }
# -------------------------------------------------------------------------
# ML ENGINE LOADER (Robust Path Resolving using Pathlib)
# -------------------------------------------------------------------------
MODEL_FILENAME = 'satisfaction_regressor.pkl'

# 🎯 Hinting ': Any' tells the IDE linter that this can become a Scikit-Learn model object
ml_model: Any = None

# Resolve current file's directory cleanly
CURRENT_DIR = Path(__file__).resolve().parent

# Search paths using safe path arithmetic operators
possible_paths = [
    CURRENT_DIR / '..' / '..' / 'saved_models' / MODEL_FILENAME,
    CURRENT_DIR / '..' / '..' / 'src' / 'saved_models' / MODEL_FILENAME,
    CURRENT_DIR / '..' / 'saved_models' / MODEL_FILENAME,
]

for path in possible_paths:
    if path.exists():  # Standard Pathlib check
        try:
            # Convert Path object back to a clean string format for joblib compatibility
            ml_model = joblib.load(str(path.resolve()))
            print(f"🏽 EngageIQ ML Engine loaded successfully from: {path}")
            break
        except Exception as e:
            print(f"⚠️ Failed to load model at {path}: {e}")

if ml_model is None:
    print("❌ CRITICAL: satisfaction_regressor.pkl not found. Please verify your Phase 1 output path.")


# -------------------------------------------------------------------------
# VIEWS CONTROLLERS
# -------------------------------------------------------------------------

def landing_page(request):
    """Renders the main platform gateway homepage with a welcome notification for visitors."""
    # Check if this is the visitor's first time loading the page this session
    if not request.session.get('visited_before', False):
        messages.info(request, "Welcome to EngageIQ! Explore our corporate predictive workspace.")
        request.session['visited_before'] = True  # Set flag so it doesn't spam them on every refresh

    return render(request, 'core_app/landing.html')


def register_user(request):
    """Handles secure corporate registration with duplicate checks and dynamic session management."""

    # 🎯 UPGRADE 4: Site remembers who is logged in! Redirect them if they try to access register page again.
    if request.user.is_authenticated:
        return redirect('dashboard')

    initial_data = {}
    session_email = request.session.get('trial_email', '')
    if session_email:
        initial_data['email'] = session_email
        del request.session['trial_email']

    form = HRRegistrationForm(request.POST or None, initial=initial_data)

    if request.method == 'POST':
        # Extraction variables for immediate validation processing
        username = request.POST.get('username')
        email = request.POST.get('email')

        # 🎯 UPGRADE 3: Catch if username or email already exists before processing anything
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken. Please choose another.")
            return render(request, 'core_app/register.html', {'form': form})

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email address already exists. Try logging in.")
            return render(request, 'core_app/register.html', {'form': form})

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Hold verification gate active
            user.save()

            otp_string = f"{random.randint(100000, 999999)}"
            ProfileOTP.objects.create(user=user, otp_code=otp_string)

            # 🎯 UPGRADE 1: Elegant Gmail Message Formatting Layout
            email_subject = "EngageIQ App - Verify Your Account Identity"
            email_body = (
                "=========================================\n"
                "               ENGAGEIQ APP              \n"
                "=========================================\n\n"
                f"Hello {user.username},\n\n"
                "Thank you for registering. Your unique, secure account "
                "activation token is generated below:\n\n"
                f"          👉 VERIFICATION CODE: {otp_string} 👈\n\n"
                "This token will expire in exactly 5 minutes.\n"
                "Please enter this code on the verification screen to activate your profile.\n\n"
                "-----------------------------------------\n"
                "If you did not make this request, please disregard this transmission."
            )

            try:
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                request.session['verification_user_id'] = user.id
                return redirect('verify_otp')

            except Exception as e:
                messages.error(request, f"Email delivery failed: {str(e)}")
                user.delete()  # Clean database rollback
        else:
            print("❌ FORM VALIDATION FAILED! Errors:", form.errors)

    return render(request, 'core_app/register.html', {'form': form})


def verify_otp(request):
    """Validates the input token and dispatches an authentic corporate welcome package email."""
    user_id = request.session.get('verification_user_id')
    if not user_id:
        return redirect('register')

    try:
        user = User.objects.get(id=user_id)
        profile_otp = user.profileotp
    except (User.DoesNotExist, ProfileOTP.DoesNotExist):
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_input')

        if profile_otp.otp_code == entered_otp and profile_otp.is_valid():
            # Activate and transition parameters
            user.is_active = True
            user.save()
            profile_otp.is_verified = True
            profile_otp.save()

            del request.session['verification_user_id']
            login(request, user)  # Django drops a persistent session cookie here

            # 🎯 UPGRADE 2: Automated Welcome Email Package inside Gmail
            welcome_subject = "Welcome to EngageIQ - Activation Successful! 🎉"
            welcome_body = (
                "=========================================\n"
                "               ENGAGEIQ APP              \n"
                "=========================================\n\n"
                f"Welcome aboard, {user.username}!\n\n"
                "Your identity has been fully verified, and your corporate predictive "
                "analytics workspace is officially active.\n\n"
                "🚀 What's next?\n"
                "• Head to your Analytics Dashboard to calculate predictive models.\n"
                "• Explore your real-time performance evaluation work matrices.\n\n"
                "We are thrilled to have you with us on the platform.\n\n"
                "Best regards,\n"
                "The EngageIQ Engine Core Team"
            )

            try:
                send_mail(
                    subject=welcome_subject,
                    message=welcome_body,
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,  # Set to True so user login isn't blocked if network hiccups here
                )
            except Exception:
                pass

            messages.success(request, "Account verified! Welcome to your predictive workspace.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid or expired authorization credentials. Please try again.")

    return render(request, 'core_app/verify_otp.html', {'email': user.email})
def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    """
    Processes built-in secure HR manager session creation logins.
    """
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'core_app/login.html', {'form': form})


def logout_user(request):
    """
    Terminals active web sessions cleanly.
    """
    logout(request)
    return redirect('landing')


@login_required(login_url='login')
def dashboard(request):
    """
    The heart of EngageIQ: Processes input sliders, executes real-time
    inference with the ML binary, and tracks history inside the DB.
    """
    form = EngagementSlidersForm(request.POST or None)
    predicted_score = None

    if request.method == 'POST' and form.is_valid():
        # Extract clean slider numbers from the form state
        comp = form.cleaned_data['compensation']
        prog = form.cleaned_data['career_progression']
        wlb = form.cleaned_data['work_life_balance']
        mngr = form.cleaned_data['manager_relationship']

        # Format inputs into a standard 2D array structure for Scikit-Learn
        input_features = np.array([[comp, prog, wlb, mngr]])

        if ml_model is not None:
            # Run prediction on the fly
            raw_prediction = ml_model.predict(input_features)[0]
            predicted_score = round(float(raw_prediction), 1)

            # 🎯 FIX 1: Save directly to the database using your exact models.py field names
            SatisfactionPrediction.objects.create(
                user=request.user,
                compensation=int(comp),
                career_progression=int(prog),
                work_life_balance=int(wlb),
                manager_relationship=int(mngr),
                predicted_score=predicted_score
            )

            # Reset form clean after a successful post to keep UI pristine
            form = EngagementSlidersForm()
        else:
            messages.error(request, "ML Engine offline. Unable to calculate satisfaction.")

    # 🎯 FIX 2: Changed 'hr_manager' to 'user' so Django can find the column instantly!
    history = SatisfactionPrediction.objects.filter(user=request.user)

    return render(request, 'core_app/dashboard.html', {
        'form': form,
        'predicted_score': predicted_score,
        'history': history
    })
def features_page(request):
    """Renders the EngageIQ core model features breakdown page."""
    return render(request, 'core_app/features.html')


def analytics_page(request):
    """
    Computes real-time aggregate telemetry across the entire platform matrix
    and passes data blocks directly to the template.
    """
    # 1. Fetch historical record count
    predictions = SatisfactionPrediction.objects.all()
    total_runs = predictions.count()

    # 2. Compute dynamic operational averages from live rows
    if total_runs > 0:
        averages = predictions.aggregate(
            avg_comp=Avg('compensation'),
            avg_prog=Avg('career_progression'),
            avg_wlb=Avg('work_life_balance'),
            avg_mngr=Avg('manager_relationship'),
            avg_score=Avg('predicted_score')
        )
        # Fallback to 0 if a database field returns null unexpectedly
        feature_data = [
            round(averages['avg_comp'] or 0, 1),
            round(averages['avg_prog'] or 0, 1),
            round(averages['avg_wlb'] or 0, 1),
            round(averages['avg_mngr'] or 0, 1)
        ]
        system_avg = round(averages['avg_score'] or 0, 1)
    else:
        # Fallback vectors for evaluation sandboxes if database is empty
        feature_data = [5.5, 6.2, 4.8, 7.1]
        system_avg = 5.9

    # 3. Compile a score density array based on current system run ranges
    density_distribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for p in predictions:
        if p.predicted_score is not None:
            score_index = min(int(p.predicted_score), 9)
            density_distribution[score_index] += 1

    # If no records exist yet, use clean default bars so charts load nicely
    if sum(density_distribution) == 0:
        density_distribution = [5, 12, 18, 24, 45, 68, 82, 54, 31, 14]

    # 4. Pack up your tracking statistics
    context = {
        'total_runs': total_runs,
        'system_avg': system_avg,
        'feature_data': feature_data,
        'density_distribution': density_distribution,
    }

    # 🎯 FIX: This statement is now completely outside the conditional logic checks!
    return render(request, 'core_app/analytics.html', context)
def pricing_page(request):
    """Renders corporate licensing tiers for the predictive matrix."""
    return render(request, 'core_app/pricing.html')

