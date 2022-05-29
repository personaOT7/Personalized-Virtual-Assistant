import time, os, webbrowser, random, requests, bs4, wikipediaapi, re, urllib, io, speech_recognition, pyaudio, pickle  
import cv2
import numpy as np
import streamlit as st
from datetime import date
from gtts import gTTS
from pyowm.owm import OWM
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from googletrans import Translator
from console.utils import wait_key
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from deepface import DeepFace


#Add a title 
from PIL import Image
image = Image.open(r'C:\Users\gopik\Downloads\14.jpg')

col1, col2 = st.columns( [0.8, 0.2])
with col1:
    st.title("Personalized Virtual Assistant")   
with col2:
    st.image(image,  width=150)

#Add an expander to the app 
with st.expander("About the App"):
     st.write("""
        This Web App is created to provide access to the personalized assistant services through face recognition, to ensure data               privacy is maintained. It performs tasks that eases the daily activity of users and involves personal information to the registered and recognized user
     """)
        
#Add sidebar to the app
st.sidebar.markdown("### Face Recognizing Personal Assistant")
st.sidebar.markdown(" The whole model follows the step in order of  User Registration , Face Detection , Image Pre Processing , Facial Features Extraction , Face Recognition and Authentication , Virtual Assistant Interaction and Result to Users Query")

#Add subtitle to the main interface of the app
st.markdown("Welcome to the personalized face recognition assistant where customized tasks performed by a personalized assistant  is accessible through face recognition.")

st.info('Replying emails, private notes, to do lists, and other customised services with privacy only through IDA')

#Add image to the app
image = Image.open('13.jpg')
st.image(image, caption='Face Recognition')

    
sr = speech_recognition


thepath = os.path.dirname(os.path.abspath(__file__))

def speak(mytext, audio_name="speech", language = "en"):
    #speaks the text
    thevoice = gTTS(text=mytext, lang=language, slow=False)
    if os.path.exists(rf"{thepath}\audio\ {audio_name}.mp3"):
        os.remove(rf"{thepath}\audio\ {audio_name}.mp3")
    thevoice.save(rf"{thepath}\audio\ {audio_name}.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\ {audio_name}.mp3')
    mixer.music.play()

def recognize_speech_from_mic():
	global question, transcription, success, error

	recognizer = sr.Recognizer()
	microphone = sr.Microphone()

	if not isinstance(recognizer, sr.Recognizer):
		raise TypeError("`recognizer` must be `Recognizer` instance")

	if not isinstance(microphone, sr.Microphone):
		raise TypeError("`microphone` must be `Microphone` instance")

	# adjust the recognizer sensitivity to ambient noise and record audio
	# from the microphone

	print ("     (Press Spacebar to speak)")
	wait_key(" ")

	with microphone as source:
		recognizer.adjust_for_ambient_noise(source)
		print ("Listening...")
		audio = recognizer.listen(source)

	# set up the responses object
	success = True,
	error = None,
	transcription = None

	# try recognizing the speech in the recording
	# if a RequestError or UnknownValueError exception is caught,
	#     update the response object accordingly
	try:
		transcription = recognizer.recognize_google(audio)
		question = transcription.lower()
	except sr.RequestError:
		# API was unreachable or unresponsive
		success = False
		error = "The API is currently unavailable"; speak(f"{error}. Please type it.", "error")
		question = input (error + ". Please type it -> ")
	except sr.UnknownValueError:
		# speech was unintelligible
		error = "I am unable to recognize speech"; speak(f"{error}. Please type it.", "error")
		question = input (error + ". Please type it -> ")

# Textual month, day, year and time
today = date.today()
date = today.strftime("%B %d, %Y")

t = time.localtime()
hour_now = time.strftime("%H", t)
current_time = time.strftime("%H:%M:%S", t)

#For deep face analysis
face_analysis = DeepFace.analyze(img_path="dataset/testing/gopika1.jpg",
                                    actions=['emotion','age','gender','race'])
# For face recognition
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(rf"{thepath}\for_v3\recognizers\face-trainer.yml")

labels = {"person_name": 1}
with open(rf"{thepath}\for_v3\pickles\face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cam = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.7, minNeighbors=3)
    for (x, y, w, h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
        roi_color = frame[y:y+h, x:x+w]

        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)
        if conf>=4 and conf <= 85:
            #print(5: #id_)
            #print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = str(labels[id_].capitalize())
            color = (255, 255, 255)
            stroke = 2
            if "_" in name:
                name = name.replace("_", " ")
            if "-" in name:
                name = name.replace("-", " ")
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = "Face.png"
        cv2.imwrite(img_item, roi_color)

        color = (100, 0, 255) #BGR 0-255 
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        # Shows green rectangles on nose, mouth and eyes
        #subitems = smile_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in subitems:
        #   cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    # Display the resulting frame
    cv2.imshow('Detect your face and press the C key to quit',frame)
    if cv2.waitKey(99) & 0xFF == ord('c'):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()

os.system('cls')

if int(hour_now) >= 0 and int(hour_now) < 12:
    time_now = "Morning"
if int(hour_now) >= 12 and int(hour_now) < 17:
    time_now = "Afternoon"
if int(hour_now) >= 17 and int(hour_now) <= 23:
    time_now = "Evening"

message = [f"\n\nGood {time_now}, {name}. Ida here. What can I do for you?", f"\n\nHi {name}. Anything I can help you with?"]
welcome = random.choice(message)

speak (welcome, "welcome")
print (welcome)

song_source = [r"https://youtu.be/kNDkz-nThzc", r"https://youtu.be/YSF8MzeO5JE", r"https://youtu.be/gwMysFlo-08", r"https://youtu.be/Uo-GommYv7w", r"https://youtu.be/7S1Y2wcfSWM", r"https://www.youtube.com/watch?v=QHQWG_QOrMc"]
#6 songs



def asking_numbers():
    global num1, num2, num3, num4
    thecode = gTTS(text="Number 1?", lang="en", slow=False)
    if os.path.exists(rf"{thepath}\audio\ num1.mp3"):
        os.remove(rf"{thepath}\audio\ num1.mp3")
    thecode.save(rf"{thepath}\audio\num1.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num1.mp3')
    mixer.music.play()
    num1 = input("Number 1 ->")

    thecode = gTTS(text="Number 2?", lang="en", slow=False)
    if os.path.exists(rf"{thepath}\audio\ num2.mp3"):
        os.remove(rf"{thepath}\audio\ num2.mp3")
    thecode.save(rf"{thepath}\audio\num2.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num2.mp3')
    mixer.music.play()
    num2 = input("Number 2 ->")

    thecode = gTTS(text="Number 3?", lang="en", slow=False)
    if os.path.exists(rf"{thepath}\audio\ num3.mp3"):
        os.remove(rf"{thepath}\audio\ num3.mp3")
    thecode.save(rf"{thepath}\audio\num3.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num3.mp3')
    mixer.music.play()
    num3 = input("Number 3 ->")

    thecode = gTTS(text="Number 4?", lang="en", slow=False)
    if os.path.exists(rf"{thepath}\audio\ num4.mp3"):
        os.remove(rf"{thepath}\audio\ num4.mp3")
    thecode.save(rf"{thepath}\audio\num4.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num4.mp3')
    mixer.music.play()
    num4 = input("Number 4 ->")

owm = OWM('57f986613d7627ac8b937284c2e92209')
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Kerala,India')  # the observation object is a box containing a weather object
weather = observation.weather
weather.status           # short version of status (eg. 'Rain')
weather.detailed_status  # detailed version of status (eg. 'light rain')

time.sleep(1)

stop = False

while stop == False:
    
    recognize_speech_from_mic()
    query = str(question)
    print(f"What I heard-> {query}")
    
    print ("\n")

    add_div = "O.K. In case you have less than four numbers, type in 0(Zero) in the blank spaces."
    sub_mul = "No problem. In case you have less than four numbers, type in 0(Zero) in the blank spaces."
    
    if query == "add some numbers":
        speak (add_div, "add") 
        print (add_div)
        time.sleep(3)
        asking_numbers()
        sumis = int(num1) + int(num2) + int(num3) + int(num4)
        speak (f"The sum(answer) is {sumis}.")
        print (f"The sum(answer) is {sumis}.")
        time.sleep(5)
        
    elif query == "subtract some numbers":
        speak = (sub_mul, "subtract")
        print (sub_mul)
        time.sleep(3)
        asking_numbers()
        difference = int(num1) - int(num2) - int(num3) - int(num4)
        speak (f"The difference(answer) is {difference}.")
        print (f"The difference(answer) is {difference}.")
        time.sleep(5)
        
    elif query == "multiply some numbers":
        speak = (sub_mul, "multiply")
        print (sub_mul)
        time.sleep(3)
        asking_numbers()
        product = int(num1) * int(num2) * int(num3) * int(num4)
        speak (f"The product(answer) is {product}.")
        print (f"The product(answer) is {product}.")
        time.sleep(5)
        
    elif query == "divide some numbers":
        speak = (add_div, "divide")
        print (add_div)
        time.sleep(3)
        asking_numbers()
        quotient = int(num1) / int(num2) / int(num3) / int(num4)
        speak (f"The quotient(answer) is {quotient}.")
        print (f"The quotient(answer) is {quotient}.")
        time.sleep(5)
        
    elif query == "face analysis":
        print(face_analysis)
        
    elif query == "tell me the date":
        speak (f"Today's date is {date}.", "date")
        print (f"Today's date is {date}.")

    elif query == "tell me the time":
        speak (f"The time is {current_time}.", "time")
        print (f"The time is {current_time}.")

    elif query == "tell me the date and time" or query == "tell me the time and date":
        speak (f"Today's time and date are {current_time}, {date}.", "time_date") 
        print (f"Today's time and date are {current_time}, {date}.")

    elif query == "open audion lyrics" or query == "open audio lyrics":
        speak ("Alright, opening Audion Lyrics now", "audion")
        print ("Alright, opening Audion Lyrics now")
        webbrowser.open('https://studio.youtube.com/channel/UCJkg92B2ZcPlqMJkv-In_OA')

    elif "search in youtube " in query:
        splitvid_name = query.partition("youtube ")
        vid_name = str(splitvid_name[2])
        speak (f"Here are the results for {vid_name} in YouTube", "youtube-search")
        print (f"Here are the results for {vid_name} in YouTube")
        webbrowser.open(f'https://www.youtube.com/results?search_query={vid_name}')
                                     
    elif "search " in query:
        splitterm = query.partition("search ")
        term = str(splitterm[2])
        speak (f"Here are the results for {term} in Google.com", "google-search")
        print (f"Here are the results for {term} in Google.com")
        webbrowser.open("https://www.google.com/search?     q="+term+"&oq="+term+"&aqs=chrome..69i57j46j0l5j69i60.5056j0j7&sourceid=chrome&ie=UTF-8")

    elif "open website " in query:
        splitlink = query.partition("website ")
        link = str(splitlink[2])
        speak (f"Opening {link} now", "website")
        print (f"Opening {link} now")
        webbrowser.open('www.' + link +'.com')

    elif "drop the needle" in query:
        song = random.choice(song_source)
        if song == song_source[0]:
            song_name = "Darkside by Alan Walker featuring Au\Ra and Tomine Harket"
        elif song == song_source[1]:
            song_name = "Faded by Alan Walker"
        elif song == song_source[2]:
            song_name = "Heading Home by Alan Walker & Ruben"
        elif song == song_source[3]:
            song_name = "Lifeline by Lvly (Myra Granberg) feat. Emmi"
        elif song == song_source[4]:
            song_name = "The Spectre by Alan Walker"
        elif song == song_source[5]:
            song_name = "Way Way Back by Lvly (Myra Granberg)"
        else:
            song_name = "a song"
        speak (f"Playing {song_name} now", "random_song")
        print (f"Playing {song_name} now")
        webbrowser.open(song)

    elif query == "play darkside":
        speak ("Playing Darkside by Alan Walker featuring Au\Ra and Tomine Harket now", "darkside")
        print ("Playing Darkside by Alan Walker featuring Au\Ra and Tomine Harket now")
        webbrowser.open(song_source[0])

    elif query == "play faded":
        speak ("Playing Faded by Alan Walker now", "faded")
        print ("Playing Faded by Alan Walker now")
        webbrowser.open(song_source[1])

    elif query == "play heading home":
        speak ("Playing Heading Home by Alan Walker & Ruben now", "heading_home")
        print ("Playing Heading Home by Alan Walker & Ruben now")
        webbrowser.open(song_source[2])

    elif query == "play lifeline":
        speak ("Playing Lifeline by Lvly (Myra Granberg) feat. Emmi", "lifeline")
        print ("Playing Lifeline by Lvly (Myra Granberg) feat. Emmi")
        webbrowser.open(song_source[3])

    elif query == "play spectre" or query == "play the spectre":
        speak ("Playing The Spectre by Alan Walker now", "the_spectre")
        print ("Playing The Spectre by Alan Walker now")
        webbrowser.open(song_source[4])

    elif query == "play way way back":
        speak ("Playing Way Way Back by Lvly (Myra Granberg) now", "way_way_back")
        print ("Playing Way Way Back by Lvly (Myra Granberg) now")
        webbrowser.open(song_source[5])

    elif query == "what is the weather today?" or query == "what is the weather today" or query == "what is the weather?" or query == "what     is the weather":
        if weather.status == "rain" or weather.status == "snow":
            stats = f"Today, there is a chance for {weather.detailed_status}"
        elif weather.status == "clear sky":
            stats = f"Today, the weather seems to be a {weather.detailed_status}"
        else :
            stats = f"Today, the weather seems to be {weather.detailed_status}"
        speak (f"{stats} and the temperature is currently {weather.temperature('celsius')['temp']} degree celsius.", "weather")
        print (f"{stats} and the temperature is currently {weather.temperature('celsius')['temp']}°C.")
        time.sleep(2)
    
    elif query == "who created you" or query == "who is your creator":
        speak ("I was created by Gopika Nair", "creator")
        print ("I was created by Gopika Nair")
        time.sleep(2)
   
    elif query == "read the world news":
        news_url="https://news.google.com/news/rss/headlines/section/topic/WORLD"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        headline_num = 1
        for news in news_list:
                news_date = news.pubDate.text.split(" ")
                speak(news.title.text, f"news{headline_num}")
                print(news.title.text)
                print(f"\nLink to article = {news.link.text}")
                print(f"\nPublished = {news.pubDate.text}")
                print("-"*60)
                print()        
                if headline_num == 10:
                    break
                headline_num = headline_num + 1
                theresult = len(re.findall(r'\w+', news.title.text))/2.17
                time.sleep(theresult)
   
    elif query == "play chess":
        speak ("Good Luck!", "chess")
        print ("Good Luck.")
        webbrowser.open('https://chess.mobialia.com/')


    elif "what is " in query:
        search_term = query.partition("is ")
        term = (str(search_term[2]))
        if "?" in query:
            termq = term.split("?")
            term = termq[0]
        if " a " in query:
            term2 = term.split('a ')
            terma = term2[1]
            term = terma
        elif "an" in query:
            term2 = term.split('an ')
            terman = term2[1]
            term = terman
        elif "the" in query:
            term2 = term.split('the ')
            termthe = term2[1]
            term = termthe
        speak (f"Here are the results for {term}", "wiki_search")
        print ("Here are the results")

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page = wiki_wiki.page(term)
        print ("Page - Title: %s" % page.title)
        print ("Page - Summary: %s" % page.summary)
        speak ("Would you like me to read it?", "readornot")
        recognize_speech_from_mic()
        yesorno = question
        if yesorno == "yes" or yesorno == "y":
            speak(f"Alright {page.summary}")
            print("\nAlright")
            theresult = len(re.findall(r'\w+', page.summary))/2.17
            time.sleep(theresult)
        else:
            speak("Alright")
            print("\nAlright")

   
    elif query == "set an alarm":
        speak("When?", "time")
        when = input("When?(minutes) -> ")
        alarm_time_file = open(rf'{thepath}\alarm\alarm_time.txt', 'w')
        alarm_time_file.write(when)
        alarm_time_file.close()
        os.startfile(r'.\alarm\Alarm.py')

    elif query == "no" or query == "nothing" or query == "nothing bye ida" or query == "nothing by ida" or query == "nothing. bye ida" or query == "nothing. by ida":
        speak (f"Bye {name}!", "bye")
        print (f"Bye {name}")
        stop = True
        break
    
    else:
        speak ("Sorry. I don't know how to do that.", "no_clue")
        print ("Sorry. I don't know how to do that.")
    
    time.sleep(3)
    speak(f"Anything else I can help you with?", "help")
    print(f"\n\nAnything else I can help you with?")
    time.sleep(1)

print ("CLOSING NOW")
time.sleep(3)