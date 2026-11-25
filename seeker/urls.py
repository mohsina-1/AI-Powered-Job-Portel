from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
path('logout/', views.user_logout, name='logout'),
path('profile/', views.profile, name='profile'),
path('upload-resume/', views.upload_resume, name='upload_resume'),
path('jobs/', views.job_search, name='job_search'),
path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
path('applications/', views.my_applications, name='applications'),
path('employer-register/', views.employer_register, name='employer_register'),
path('employer-login/', views.employer_login, name='employer_login'),
path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
path('create-job/', views.create_job, name='create_job'),
path('employer-applicants/', views.view_applicants, name='view_applicants'),
path('application-management/', views.application_management, name='application_management'),
path('update-application-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
path('manage-jobs/', views.manage_jobs, name='manage_jobs'),
path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
path('delete-application/<int:application_id>/', views.delete_application, name='delete_application'),
path('ai-resume-analyzer/', views.ai_resume_analyzer, name='ai_resume_analyzer'),
path('ai-recommendations/', views.ai_job_recommendations, name='ai_job_recommendations'),
path('skill-gap-analysis/', views.skill_gap_analysis, name='skill_gap_analysis'),
]