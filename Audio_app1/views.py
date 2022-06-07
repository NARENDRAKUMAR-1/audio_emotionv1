from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

import joblib
import librosa
import pandas as pd 
import numpy as np
import os

from pydub import AudioSegment 
from pydub.utils import make_chunks 


from . forms import AudioForm


def index(request):
    return HttpResponse("Hello, world. We are Emotional beings.")


def home(request):
    return render(request, 'home.html')


def feature_extractor(file):
    audio, sample_rate = librosa.load(file, res_type = 'kaiser_fast') # res_type?
    
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
#     // why is this 40 and what's this actually

    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
#     transpose of the mean ?
    
    return mfccs_scaled_features

def analyse_audio(request):
    
    folder = 'media/documents'

    # segment the audio file uploaded

    file1 = os.listdir(folder)
    print("file1 ", file1    )
    file1 = 'media/documents/' + str(file1[0])
    myaudio = AudioSegment.from_file(file1, "wav") 
    chunk_length_ms = 8000 # pydub calculates in millisec 
    chunks = make_chunks(myaudio,chunk_length_ms) #Make chunks of 8 sec 
    for i, chunk in enumerate(chunks): 
        chunk_name = "{0}.wav".format(i) 
        print ("exporting", chunk_name) 
        chunk.export("media/documents/{}".format(chunk_name), format="wav") 


    myfiles=os.listdir(folder)
    myfiles = myfiles[:-1]
    print("files ", myfiles)

    audio_dataset_path = r'media/documents'
    extracted_features =[]

    for file in myfiles:
        file_name =os.path.join(os.path.abspath(audio_dataset_path) + '/'+file )
        
    
        data = feature_extractor(file_name)
        extracted_features.append(data)

    model = joblib.load("./rf_emotion_model1.joblib")
    y_pred = model.predict(extracted_features)

    emotion_map = {0: 'angry',
    1: 'calm',
    2: 'disgust',
    3: 'fearful',
    4: 'happy',
    5: 'neutral',
    6: 'sad',
    7: 'surprised'}

    print("len pred ", len(y_pred))

    y_pred = [ emotion_map[x] for x in y_pred ]

    # delete the files
    folder = 'media/documents'
    for filenm in os.listdir(folder):
        file_path = os.path.join(folder, filenm)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        
    return render(request, 'result.html', {'class': y_pred, 'split_interval':int(chunk_length_ms/1000) })
    


def Audio_store(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES or None)

        if(form.is_valid()):
            form.save()
            # return HttpResponse(" Successfully Uploaded the file")

            print("success uploaded")

            return render(request, 'trigger.html')

    else:
        form=AudioForm()
        print("some error in upload")
    
    return render(request, 'aud.html', {'form': form})

