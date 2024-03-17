import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login




page_id = os.environ.get('FACEBOOK_PAGE_ID')
access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')


def get_facebook_total_post_likes(page_id, access_token):
    # Construct the API endpoint URL to fetch posts
    api_endpoint_posts = f"https://graph.facebook.com/{page_id}/posts?fields=likes.limit(0).summary(true)&access_token={access_token}"

    total_likes = 0

    try:
        # Send a GET request to the API endpoint
        response = requests.get(api_endpoint_posts)
        data = response.json()

        # Iterate through each post and sum up the likes
        for post in data.get('data', []):
            likes_summary = post.get('likes', {}).get('summary', {})
            total_likes += likes_summary.get('total_count', 0)

        return total_likes

    except Exception as e:
        print(f"Error fetching total likes: {e}")
        return None
    


def get_facebook_follower_count(page_id, access_token):
    # Construct the API endpoint URL
    api_endpoint = f"https://graph.facebook.com/{page_id}?fields=fan_count&access_token={access_token}"

    try:
        # Send a GET request to the API endpoint
        response = requests.get(api_endpoint)
        data = response.json()

        # Extract the follower count from the response
        follower_count = data.get('fan_count')

        return follower_count

    except Exception as e:
        print(f"Error fetching follower count: {e}")
        return None


def get_facebook_total_post_comments(page_id, access_token):
    api_endpoint_posts = f"https://graph.facebook.com/{page_id}/posts?fields=comments.limit(0).summary(true)&access_token={access_token}"

    total_comments = 0

    try:
        response = requests.get(api_endpoint_posts)
        data = response.json()

        for post in data.get('data', []):
            comments_summary = post.get('comments', {}).get('summary', {})
            total_comments += comments_summary.get('total_count', 0)

        return total_comments

    except Exception as e:
        print(f"Error fetching total comments: {e}")
        return None



def get_instagram_follower_count():
    return 1


def get_twitter_follower_count():
    return 1


def get_instagram_post_likes():
    return 2


def get_twitter_post_likes():
    return 1


def get_instagram_post_comments():
    return 1

def get_twitter_post_comments():
    return 1
