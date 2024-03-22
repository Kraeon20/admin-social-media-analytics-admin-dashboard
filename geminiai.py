import google.generativeai as genai

# genai.configure(api_key='AIzaSyACALRtMI6ZauQYJEP9F4bW0Spbnam55MY')


# model = genai.GenerativeModel('gemini-pro')
# user_input = input("Say something...\n")
# response = model.generate_content(user_input)

# response_text = response.text

# print(response_text)



genai.configure(api_key='AIzaSyACALRtMI6ZauQYJEP9F4bW0Spbnam55MY')

def get_gemini_response(userr):
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(userr)
    response_text = response.text

    return response_text




reply = get_gemini_response('hi')

print(reply)