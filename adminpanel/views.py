import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from dotenv import load_dotenv
from .utils import (get_facebook_follower_count,
                    get_facebook_total_post_likes, 
                    get_instagram_follower_count,
                    get_facebook_total_post_comments,
                    get_instagram_post_likes, 
                    get_twitter_follower_count,
                    get_twitter_post_likes, 
                    get_instagram_post_comments,
                    get_twitter_post_comments)
import google.generativeai as genai
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



load_dotenv()


page_id = '238443226023972'
access_token = 'EAAQfAQe5IP0BO9lTs6OXHU2FU7k3zDPZB1ZAiW5aNeATtD2NvXB9LeLqUMUb75xU7LeV5lGIo4pSAcak2OYtZCfG8reCt66lZADRA03x0tCQn6RGU345XWCNLg0RTnn4NUWZARACOBMCMdVBd2DCGThkzhCuKFfpXVmniMkrNwV0hItYbHZBaenx7RKHpr80efBaP4tEQZAREYkECvcGPE9UjOYvKOtR8YZD'
gemini_api_key=genai.configure(api_key='AIzaSyACALRtMI6ZauQYJEP9F4bW0Spbnam55MY')

@csrf_exempt
@login_required
def dashboard(request):
    if request.method == 'POST':
        user_input = request.POST.get('query')
        if user_input:
            # Call a function to process the user input (e.g., send it to Gemini AI)
            gemini_response = get_gemini_response(user_input)
            return JsonResponse({'response': gemini_response})
        else:
            return JsonResponse({'error': 'No query provided'}, status=400)
    else:
        # Handle other types of requests (GET)
        pass

    # total followers accross all platforms
    total_followers = (get_facebook_follower_count(page_id, access_token) +
                       get_twitter_follower_count() +
                       get_instagram_follower_count())
    
    # total likes accross all platforms
    total_likes = (get_facebook_total_post_likes(page_id, access_token) +
                   get_instagram_post_likes() +
                   get_twitter_post_likes())
    
    total_comments = (get_facebook_total_post_comments(page_id, access_token) +
                      get_instagram_post_comments() +
                      get_twitter_post_comments())
    

    # Fetch data for each platform
    facebook_followers = get_facebook_follower_count(page_id, access_token)
    instagram_followers = get_instagram_follower_count()
    twitter_followers = get_twitter_follower_count()

    facebook_likes = get_facebook_total_post_likes(page_id, access_token)
    instagram_likes = get_instagram_post_likes()
    twitter_likes = get_twitter_post_likes()

    facebook_comments = get_facebook_total_post_comments(page_id, access_token)
    instagram_comments = get_instagram_post_comments()
    twitter_comments = get_twitter_post_comments()

    # Calculate averages
    facebook_avg = round((facebook_followers + facebook_likes + facebook_comments) / 3)
    instagram_avg = round((instagram_followers + instagram_likes + instagram_comments) / 3)
    twitter_avg = round((twitter_followers + twitter_likes + twitter_comments) / 3)
    
    # Create a list of platform objects
    platforms = [
        {'name': 'Facebook', 'followers': facebook_followers, 'likes': facebook_likes, 'comments': facebook_comments, 'average': facebook_avg},
        {'name': 'Instagram', 'followers': instagram_followers, 'likes': instagram_likes, 'comments': instagram_comments, 'average': instagram_avg},
        {'name': 'Twitter', 'followers': twitter_followers, 'likes': twitter_likes, 'comments': twitter_comments, 'average': twitter_avg}
    ]

    # Sort platforms based on average engagement (descending order)
    platforms.sort(key=lambda x: x['average'], reverse=True)
    
    # Example usage of Gemini AI
    gemini_response = None
    if request.method == 'POST':
        user_input = request.POST.get('query')
        if user_input:
            # Call a function to process the user input (e.g., send it to Gemini AI)
            gemini_response = get_gemini_response(user_input)
            return JsonResponse({'response': gemini_response})
        else:
            return JsonResponse({'error': 'No query provided'}, status=400)
    else:
        # Handle other types of requests (GET)
        pass

    # Pass total_likes to the template context
    context = {
        'facebook_followers': facebook_followers,
        'instagram_followers': instagram_followers,
        'twitter_followers': twitter_followers,
        'facebook_likes': facebook_likes,
        'instagram_likes': instagram_likes,
        'twitter_likes': twitter_likes,
        'facebook_comments': facebook_comments,
        'instagram_comments': instagram_comments,
        'twitter_comments': twitter_comments,
        'total_followers': total_followers,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'platforms': platforms,
        'gemini_response': gemini_response,
    }
    
    return render(request, 'dashboard.html', context)




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Handle invalid login
            pass
    return render(request, 'login.html')





def get_gemini_response(user_input):
    # Your existing code to generate response from Gemini AI
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_input)
    response_text = response.text
    return response_text




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page or any other appropriate page
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'login.html', {'form': form})





@login_required
def logout_view(request):
    logout(request)
    return redirect('login')