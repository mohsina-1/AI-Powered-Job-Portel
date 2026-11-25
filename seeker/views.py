from pypdf import PdfReader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import JobSeekerProfile, Job, JobApplication, EmployerProfile



def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.first_name = name
            user.save()

            messages.success(request, 'Registration successful!')
            return redirect('register')

    return render(request, 'seeker/register.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'seeker/login.html')
@login_required
def dashboard(request):
    return render(request, 'seeker/dashboard.html')


def user_logout(request):
    auth_logout(request)
    return redirect('login') 
@login_required
def profile(request):
    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.education = request.POST.get('education')
        profile.skills = request.POST.get('skills')
        profile.experience = request.POST.get('experience')

        profile.save()

        messages.success(request, 'Profile saved successfully!')
        return redirect('profile')

    return render(request, 'seeker/profile.html', {
        'profile': profile
    })


@login_required
def upload_resume(request):
    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        resume = request.FILES.get('resume')

        if resume and resume.name.lower().endswith('.pdf'):
            profile.resume = resume
            profile.save()

            messages.success(request, 'Resume uploaded successfully!')
            return redirect('upload_resume')

        else:
            messages.error(request, 'Please upload a PDF file.')

    return render(request, 'seeker/upload_resume.html')
@login_required
def job_search(request):
    jobs = Job.objects.all()

    title = request.GET.get('title', '')
    location = request.GET.get('location', '')
    skills = request.GET.get('skills', '')

    if title:
        jobs = jobs.filter(title__icontains=title)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if skills:
        jobs = jobs.filter(skills__icontains=skills)

    return render(request, 'seeker/jobs.html', {
        'jobs': jobs
    })
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        application, created = JobApplication.objects.get_or_create(
            user=request.user,
            job=job
        )

        if created:
            messages.success(request, 'Job application submitted successfully!')
        else:
            messages.info(request, 'You have already applied for this job.')

    return redirect('job_search')
@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        user=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'seeker/applications.html', {
        'applications': applications
    })
@login_required
def delete_application(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(
            JobApplication,
            id=application_id,
            user=request.user
        )
        application.delete()
        messages.success(request, 'Application deleted successfully!')

    return redirect('applications')
def employer_register(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        phone = request.POST.get('phone')
        company_address = request.POST.get('company_address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('employer_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('employer_register')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=company_email
        )

        EmployerProfile.objects.create(
            user=user,
            company_name=company_name,
            company_email=company_email,
            phone=phone,
            company_address=company_address
        )

        messages.success(request, 'Employer registered successfully!')
        return redirect('employer_login')

    return render(request, 'seeker/employer_register.html')
def employer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            if EmployerProfile.objects.filter(user=user).exists():
                auth_login(request, user)
                messages.success(request, 'Welcome Employer!')
                return redirect('employer_dashboard')
            else:
                messages.error(request, 'Employer account not found!')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'seeker/employer_login.html')
@login_required
def employer_dashboard(request):
    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    return render(request, 'seeker/employer_dashboard.html')
@login_required
def create_job(request):
    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    if request.method == 'POST':
        Job.objects.create(
            title=request.POST.get('title'),
            company=request.POST.get('company'),
            location=request.POST.get('location'),
            skills=request.POST.get('skills'),
            description=request.POST.get('description'),
            employer=request.user.employerprofile
        )

        messages.success(request, 'Job posted successfully!')
        return redirect('employer_dashboard')

    return render(request, 'seeker/create_job.html')
@login_required
def view_applicants(request):
    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    applications = JobApplication.objects.filter(
        job__employer__user=request.user
    ).select_related(
        'user', 'job', 'user__jobseekerprofile'
    ).order_by('-applied_at')

    search_skill = request.GET.get('skills', '')
    search_job = request.GET.get('job_title', '')

    if search_skill:
        applications = applications.filter(
            user__jobseekerprofile__skills__icontains=search_skill
        )

    if search_job:
        applications = applications.filter(
            job__title__icontains=search_job
        )

    return render(
        request,
        'seeker/employer_applicants.html',
        {
            'applications': applications,
            'search_skill': search_skill,
            'search_job': search_job
        }
    )
@login_required
def manage_jobs(request):
    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    jobs = Job.objects.filter(
        employer=request.user.employerprofile
    )

    return render(
        request,
        'seeker/manage_jobs.html',
        {'jobs': jobs}
    )
@login_required
def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(
            Job,
            id=job_id,
            employer=request.user.employerprofile
        )
        job.delete()
        messages.success(request, 'Job deleted successfully!')

    return redirect('manage_jobs')
@login_required
def edit_job(request, job_id):
    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user.employerprofile
    )

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.location = request.POST.get('location')
        job.skills = request.POST.get('skills')
        job.description = request.POST.get('description')
        job.save()

        messages.success(request, 'Job updated successfully!')
        return redirect('manage_jobs')

    return render(request, 'seeker/edit_job.html', {'job': job})
@login_required
def ai_resume_analyzer(request):
    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    extracted_text = ""
    detected_skills = []

    if profile.resume:
        try:
            pdf = PdfReader(profile.resume.path)

            for page in pdf.pages:
                extracted_text += page.extract_text() or ""

        

            skills_list = [
                'Python', 'Java', 'HTML', 'CSS',
                'JavaScript', 'Django', 'SQL',
                'React', 'C++', 'Machine Learning'
            ]

            for skill in skills_list:
                if skill.lower() in extracted_text.lower():
                    detected_skills.append(skill)

        except Exception:
            messages.error(request, 'Unable to read the resume.')

    return render(request, 'seeker/resume_analyzer.html', {
        'detected_skills': detected_skills,
        'extracted_text': extracted_text
    })
@login_required
def ai_job_recommendations(request):
    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    recommended_jobs = []

    if profile.skills:
        user_skills = [
            skill.strip().lower()
            for skill in profile.skills.split(',')
        ]

        for job in Job.objects.all():
            job_skills = job.skills.lower()

            if any(skill in job_skills for skill in user_skills):
                recommended_jobs.append(job)

    return render(
        request,
        'seeker/ai_recommendations.html',
        {'recommended_jobs': recommended_jobs}
    )
@login_required
def application_management(request):
    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    applications = JobApplication.objects.filter(
        job__employer__user=request.user
    ).select_related('user', 'job').order_by('-applied_at')

    return render(
        request,
        'seeker/application_management.html',
        {'applications': applications}
    )


@login_required
def update_application_status(request, application_id):
    if request.method != 'POST':
        return redirect('application_management')

    if not EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_login')

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        job__employer__user=request.user
    )

    new_status = request.POST.get('status')

    if new_status in ['Accepted', 'Rejected', 'Pending']:
        application.status = new_status
        application.save()
        messages.success(request, 'Application status updated successfully!')

    return redirect('application_management')
@login_required
def skill_gap_analysis(request):
    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    jobs = Job.objects.all()

    selected_job = None
    matching_skills = []
    missing_skills = []

    job_id = request.GET.get('job_id')

    if job_id:
        selected_job = get_object_or_404(Job, id=job_id)

        candidate_skills = [
            skill.strip().lower()
            for skill in profile.skills.split(',')
            if skill.strip()
        ]

        required_skills = [
            skill.strip()
            for skill in selected_job.skills.split(',')
            if skill.strip()
        ]

        for skill in required_skills:
            if skill.lower() in candidate_skills:
                matching_skills.append(skill)
            else:
                missing_skills.append(skill)

    return render(
        request,
        'seeker/skill_gap_analysis.html',
        {
            'jobs': jobs,
            'selected_job': selected_job,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills
        }
    )