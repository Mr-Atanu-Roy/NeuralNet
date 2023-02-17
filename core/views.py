from django.shortcuts import render, redirect
from django.contrib import messages
import os

import openai
import speech_recognition as sr

from .threads import *

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Load your API key from an environment variable or secret management service
openai.api_key = os.environ.get("API_KEY")


def home(request):
    
    return redirect('/chitchat')


def chitchat(request):
    try:
        query = result = ""
        context = {
            "query" : query,
            "result" : result,
        }
        if request.method == "POST" and "form1" in request.POST:
            query = request.POST.get("query")
            if query == "":
                message = "Please input some text"
                messages.error(request, message)
                result = message
                
            else:
                if cache.get(query):
                    result = cache.get(query)                
                else:
                    prompt = f"""
                    The following is a conversation with an AI assistant whose name is Synthia, she is very helpful, creative, clever, and very friendly.
                    \n\nHuman: {query}
                    \n\nAI: 
                    """
                    
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=2048,
                    temperature=0.9,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.6,
                    stop=[" Human:", " AI:"]
                    )
                    
                    result =  response["choices"][0]["text"]
                    result = result.lstrip()
                    cache.set(query, result)
            
        elif request.method == "POST" and "form2" in request.POST:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            # recognize speech using Google Speech Recognition
            try:
                query = r.recognize_google(audio)
                if query == "":
                    message = "Please say something"
                    messages.error(request, message)
                    result = message
                else:
                    if cache.get(query):
                        result = cache.get(query)
                    else:
                        prompt = f"""
                        The following is a conversation with an AI assistant whose name is Synthia, she is very helpful, creative, clever, and very friendly.
                        \n\nHuman: {query}
                        \n\nAI: 
                        """
                            
                        response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=prompt,
                        max_tokens=2048,
                        temperature=0.9,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                        stop=[" Human:", " AI:"]
                        )
                        # print(response)
                        result =  response["choices"][0]["text"]
                        result = result.lstrip()
                        cache.set(query, result)
                
            except sr.UnknownValueError:
                result = "I could not understand what you just said. Please say that again"
            except sr.RequestError as e:
                result = "Could not request results from Google Speech Recognition service; {0}".format(e)
        
        context["query"] = query
        context["result"] = result
        Speak(result).start()
            
    except Exception as e:
        print(e)
    
    
    return render(request, './core/chitchat.html', context)


def codegenie(request):
    try:
        context = {
            "query" : "write a program to find factorial of a number",
            "result" : "",
            "language" : "",
        }
        
        if request.method == "POST":
            query = request.POST.get("query")
            language = request.POST.get("language")
            
            context['language'] = language
            
            if query == "":
                messages.error(request, "Please input some text")
            else:
                if cache.get(f"{query}-{language}"):
                    result = cache.get(f"{query}-{language}")
                else:
                    if language == "html":
                        prompt = f"#{query}\n<!DOCTYPE html>"
                    else:
                        prompt = f"#{language}\n#{query}"
                    
                    response = openai.Completion.create(
                    model="code-davinci-002",
                    prompt=prompt,
                    temperature=0,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
                    result = response["choices"][0]["text"]
                    result = result.lstrip()
                    
                    cache.set(f"{query}-{language}", result)

                context['result'] = result
                context['query'] = query

    except Exception as e:
        print(e)
        
    return render(request, "./core/codegenie.html", context)


def artiflex(request):
    try:
        context = {
            "query" : "",
            "result" : "",
        }
        if request.method == "POST":
            query = request.POST.get("query")
            if query == "":
                message = "Please input some text"
                messages.error(request, message)
                    
            else:
                if cache.get(query):
                    result = cache.get(query)
                else:
                    response = openai.Image.create(
                    prompt= query,
                    n=3,
                    size="256x256"
                    )
                    # print(response)
                    imgURLS = []
                    for img in response["data"]:
                        imgURLS.append(img["url"])

                    cache.set(query, imgURLS)
                    
                    result = imgURLS
                    
                context["query"] = query
                context["result"] = result
            
    except Exception as e:
        print(e)
            
            
    return render(request, "./core/artiflex.html", context)






