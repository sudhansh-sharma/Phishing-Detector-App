from django.shortcuts import render, redirect
from django.contrib import messages
import numpy as np
import pickle
from .FeaturesExtraction import Extract_Features 
from .dnn_app_utils_v3 import L_model_forward
import os

currentDir = os.path.dirname(__file__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

#helper Function
def predictUrl(X, parameters):
    m = 1
    n = len(parameters) // 2 # number of layers in the neural network
    p = np.zeros((1, m),dtype=int)
    
    # Forward propagation
    prob, caches = L_model_forward(X, parameters)
    print(prob)
    if prob > 0.5:
        return "Phishing"
    else:
        return "Legitimate"

def check(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        
        pathParams = os.path.join(currentDir, 'trainedPhishingParameters.pickle')
        loaded_params = None

        with open(pathParams, "rb") as file:
            loaded_params = pickle.load(file)
            
        try:
            url = url.lower()
            
            if 'http' not in url:
                url = 'https://www.'+ url
                
            url = url.split('com')[0]+ 'com/'

            obj = Extract_Features(url)
            test_features = obj.Extract()

            test = np.array(test_features)
            test = np.reshape(test,(test.shape[0],1))
            ans = predictUrl(test,loaded_params)

            if ans == "Phishing":
                print("Inside Phishing.")
                if test_features.count(-1) > 0:
                    messages.warning(request, "Try Something Else.")
                else:
                    messages.error(request, "Phishing Website: " + url)

            elif ans == "Legitimate":
                print("Inside Legitimate.")
                if -1 in test_features:
                    messages.warning(request, "Try Something Else.")
                else:
                    messages.success(request, "Legitimate Website: " + url)

        except:
            messages.error(request, "There was Some Error in Prediction... Please Try Again")

    return redirect('/')