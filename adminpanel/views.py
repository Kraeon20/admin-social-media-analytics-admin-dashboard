import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
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
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import re


load_dotenv()

# page_id = os.getenv('FACEBOOK_PAGE_ID')
# access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
# gemini_api_key = os.getenv('GEMINI_API_KEY')

page_id = '238443226023972'
access_token = 'EAAQfAQe5IP0BOyu4eOtxFZAHJYZAIzyVZAaixoXLGRviegj84PZBQgmDuCDX8YN8gZAx3ZBQmwNot3DCxRFJEgSfvt0qOczdAqoLr4D320d05LWJNZCjhGpXxsoSMgm008oNhGID92rsbHZC1ziSTL7eRuJRhXZAiD36K9t2CltbHMJnyoZCbc9OImCqhrW9sYTK6nqGXlsX4slgyGWwmlCcEdKC6ZArj6CRbsZD'
gemini_api_key = os.getenv('GEMINI_API_KEY')



# print(os.getenv('FACEBOOK_PAGE_ID'))
# print(os.getenv('FACEBOOK_ACCESS_TOKEN'))
# print(os.getenv('GEMINI_API_KEY'))


@csrf_exempt
@login_required
def dashboard(request):
    
    user_first_name = request.user.first_name


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
    


    data = {
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
    }


    # Example usage of Gemini AI
    gemini_response = None
    if request.method == 'POST':
        user_input = request.POST.get('query')
        if user_input:
            # Call a function to process the user input (e.g., send it to Gemini AI)
            gemini_response = get_gemini_response(user_input, data)
            return JsonResponse({'response': gemini_response})
        else:
            return JsonResponse({'error': 'No query provided'}, status=400)
    else:
        # Handle other types of requests (GET)
        pass

    # Pass total_likes to the template context
    context = {
        'user_first_name': user_first_name,
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
            # Invalid login attempt, add a message
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')





def process_data_query(user_input, data):
    # Extract relevant data based on the user query
    response_text = ""

    if "followers" in user_input.lower():
        response_text += f"Total followers across all platforms: {data['total_followers']}\n"
        for platform in data['platforms']:
            response_text += f"{platform['name']} followers: {platform['followers']}\n"

    if "likes" in user_input.lower():
        response_text += f"Total likes across all platforms: {data['total_likes']}\n"
        for platform in data['platforms']:
            response_text += f"{platform['name']} likes: {platform['likes']}\n"

    if "comments" in user_input.lower():
        response_text += f"Total comments across all platforms: {data['total_comments']}\n"
        for platform in data['platforms']:
            response_text += f"{platform['name']} comments: {platform['comments']}\n"

    # More sophisticated logic based on types of queries
    if "average engagement" in user_input.lower():
        # Calculate average engagement for each platform
        for platform in data['platforms']:
            engagement = (platform['followers'] + platform['likes'] + platform['comments']) / 3
            response_text += f"Average engagement for {platform['name']}: {engagement}\n"

    if "most engaging platform" in user_input.lower():
        # Determine the most engaging platform
        most_engaging_platform = max(data['platforms'], key=lambda x: x['average'])
        response_text += f"The most engaging platform is {most_engaging_platform['name']} with an average engagement of {most_engaging_platform['average']}\n"

    if "platform with highest followers" in user_input.lower():
        # Determine the platform with the highest number of followers
        platform_with_highest_followers = max(data['platforms'], key=lambda x: x['followers'])
        response_text += f"The platform with the highest number of followers is {platform_with_highest_followers['name']} with {platform_with_highest_followers['followers']} followers\n"

    # Add more sophisticated logic for other types of queries here...

    if not response_text:
        response_text = "I'm sorry, I couldn't find relevant data for your query."

    return response_text




def get_gemini_response(user_input, data):
    # Check if the user input is related to data
    data_related_queries = ["followers", "likes", "comments"]
    if any(query in user_input.lower() for query in data_related_queries):
        # Process data-related queries
        response_text = process_data_query(user_input, data)
    else:
        # If the query is not related to data, use Gemini AI for response
        response_text = generate_gemini_response(user_input)
    
    # Format the response with paragraphs and bold text
    response_text = format_response(response_text)
    
    return response_text

def format_response(response_text):
    # Remove any random characters (including asterisks)
    response_text = re.sub(r'[^a-zA-Z0-9\s\.,!?]', '', response_text)
    
    # Split the response into paragraphs
    paragraphs = response_text.split("\n\n")
    
    # Format each paragraph
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Remove leading and trailing whitespace
        paragraph = paragraph.strip()
        formatted_paragraphs.append(paragraph)
    
    # Join paragraphs back together with newlines
    formatted_response = "\n".join(formatted_paragraphs)
    
    return formatted_response





def generate_gemini_response(user_input):
    # Your existing code to generate response from Gemini AI
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_input)
    response_text = response.text
    return response_text


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the form but retrieve the user object
            user = form.save(commit=False)
            # Assign values to additional fields
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            # Save the user object with additional fields
            user.save()
            # Redirect to the login page or any other appropriate page
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'login.html', {'form': form})




# Create your views here.
@login_required
def settings(request):
    # If user is admin, redirect to admin settings
    if request.user.is_superuser:
        return redirect('admin_settings')
    # If user is not admin, render normal settings page
    return render(request, 'settings.html')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='dashboard')
def admin_settings(request):
    if request.method == 'POST' and 'delete_subuser' in request.POST:
        subuser_id = request.POST.get('subuser_id')
        try:
            subuser = User.objects.get(pk=subuser_id)
            subuser.is_active = False
            subuser.save()
            messages.success(request, "Subuser deactivated successfully.")
            return JsonResponse({'success': True, 'subuser_id': subuser_id})
        except User.DoesNotExist:
            messages.error(request, "Subuser not found.")
            return JsonResponse({'success': False})
    
    subusers = User.objects.exclude(pk=request.user.pk)
    context = {'subusers': subusers}
    return render(request, 'admin_settings.html', context)


def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('settings')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return redirect('settings')




@login_required
def logout_view(request):
    logout(request)
    return redirect('login')