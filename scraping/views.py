from django.shortcuts import render,redirect
from django.contrib import messages
import requests 
from bs4 import BeautifulSoup
from django.http import JsonResponse


# Create your views here.
def all_scrping_data(request): 
    
    goldRateData=goldrate()
    current_time=getTime()
    if request.method=="POST":        
        city= request.POST['city']  
        if city: 
             weatherData=weather(request,city)     
        else:  
             weatherData={"Error": "Please enter city name"}                  
    else:
        weatherData={}       
       
    return render(request,'scraping.html',{'goldRate':goldRateData,'weather':weatherData,'time':current_time})

def goldrate():
    url="https://www.thehindubusinessline.com/gold-rate-today"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get(url, headers=headers)        
    goldRate=dict()
    if res.status_code==200:
        soup=BeautifulSoup(res.content,'html')        
        div22Ct=soup.find('div',class_='status1')
        div24Ct=soup.find('div',class_='status2')  
        if div22Ct:
            div_text = div22Ct.get_text(strip=True)
            div_text=div_text.split('₹')
            goldRate.update({div_text[0]: div_text[1]})
        if div24Ct:
            div_text = div24Ct.get_text(strip=True)
            div_text=div_text.split('₹')
            goldRate.update({div_text[0]: div_text[1]})            
    else:       
       exit()   
    return goldRate

def weather(request,city):
    if city:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid=5095b32e11de54d3533c361ee49821d1&units=metric"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        res=requests.get(complete_url)
        weather={}
        if res.status_code==200:            
            # #parse the html
            soup=BeautifulSoup(res.content,'html.parser')  
            # # extract data
            temp=soup.find('div',class_='temp')
            data = res.json()
            main = data['main']
            weather = data['weather'][0]
            
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            weather_description = weather['description']
            weather= {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "description": weather_description
            }           
        else:
            weather={"Error": "The entered city name is not valid"}   
        
    return weather


def getTime():
    url = "https://www.timeanddate.com/worldclock/india"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # The current time is within the span tag with id="ct"
    current_time = soup.find('span', {'id': 'ct'}).text
    return current_time

def get_time(request):
    current_time = getTime()
    return JsonResponse({'current_time': current_time})



# def read_time_from_file():
#     with open('C:\\Users\\sgudala\\Downloads\\current_time.txt', 'r') as file:
#      current_time = file.read()
#     return current_time

# def all_scrping_data(request): 
#     current_time = read_time_from_file()
#     return render(request, 'scraping.html', {'time': current_time})
