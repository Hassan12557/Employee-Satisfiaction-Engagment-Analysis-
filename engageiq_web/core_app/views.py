import os
import joblib
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import HRRegistrationForm, EngagementSlidersForm
from .models import SatisfactionPrediction

# -------------------------------------------------------------------------
# ML ENGINE LOADER (Robust Path Resolving)
# -------------------------------------------------------------------------
MODEL_FILENAME = 'satisfaction_regressor.pkl'
ml_model = None

# Search across common relative paths based on project structure
possible_paths = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'saved_models', MODEL_FILENAME)),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'saved_models', MODEL_FILENAME)),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'saved_models', MODEL_FILENAME)),
]

for path in possible_paths:
    if os.path.exists(path):
        try:
            ml_model = joblib.load(path)
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
    """
    Renders the premium dark-grid hero landing page layout.
    """
    # If a corporate email is sent via the "Free Trial" text field, forward it to register
    trial_email = request.GET.get('trial_email', '')
    if trial_email:
        request.session['trial_email'] = trial_email
        return redirect('register')

    return render(request, 'core_app/landing.html')


def register_user(request):
    """
    Handles sign-ups and triggers your verification pop-up modal.
    """
    # Grab pre-filled email from free trial landing action if it exists
    initial_data = {}
    session_email = request.session.get('trial_email', '')
    if session_email:
        initial_data['email'] = session_email
        # Clear it from the session so it doesn't linger permanently
        del request.session['trial_email']

    form = HRRegistrationForm(request.POST or None, initial=initial_data)
    show_verification_modal = False

    if request.method == 'POST' and form.is_validate():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False  # Inactive until email verification modal confirms
        user.save()

        # Intercept redirection to trigger your "Verify your email" template pop-up
        show_verification_modal = True

    return render(request, 'core_app/register.html', {
        'form': form,
        'show_verification_modal': show_verification_modal
    })


def login_user(request):
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
        # Extract clean slider numbers (1.0 to 10.0) from the form state
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

            # Instantly save record into database mapped to this logged-in HR account
            prediction_record = form.save(commit=False)
            prediction_record.hr_manager = request.user
            prediction_record.predicted_satisfaction = predicted_score
            prediction_record.save()

            # Reset form clean after a successful post to keep UI pristine
            form = EngagementSlidersForm()
        else:
            messages.error(request, "ML Engine offline. Unable to calculate satisfaction.")

    # Retrieve historical audit trails to render your bottom table analytics view
    history = SatisfactionPrediction.objects.filter(hr_manager=request.user)

    return render(request, 'core_app/dashboard.html', {
        'form': form,
        'predicted_score': predicted_score,
        'history': history
    })