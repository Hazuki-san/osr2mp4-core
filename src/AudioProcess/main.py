from multiprocessing import Process

from scipy.io.wavfile import write
import numpy as np
from pydub import AudioSegment
from pydub import exceptions
import time
from collections import namedtuple
import os.path

Empty = AudioSegment.empty()
Empty = AudioSegment.silent(duration=1)
Empty.export("blank.mp3",format="mp3")


class Position(namedtuple('Position', 'x y')):
        pass

def read(f,type1):
        if f[-1] == "3":
                    if type1 == "song":
                        a = AudioSegment.from_mp3(f)
                        a = a - 10
                    else:
                        a = AudioSegment.from_mp3(f)
        else:
            a = AudioSegment.from_file(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
                y = y.reshape((-1, 2))
        if a.channels == 1:
                y1 = np.zeros((len(y), 2), dtype=y.dtype)
                y1[:, 0] = y
                y1[:, 1] = y
                y = y1
        return a.frame_rate, np.float32(y) / 2**(a.sample_width * 8 - 1)

def pydubtonumpy(a):
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
                y = y.reshape((-1, 2))
        if a.channels == 1:
                y1 = np.zeros((len(y), 2), dtype=y.dtype)
                y1[:, 0] = y
                y1[:, 1] = y
                y = y1
        return a.frame_rate, np.float32(y) / 2**(a.sample_width * 8 - 1)

def tryCatch(audio,audio1,checked):
        try:
                audio, audio1 = read(checked,"")
        except exceptions.CouldntDecodeError:
                audio, audio1 = read("blank.mp3","")
                print("Decoding Error: Now Creating a blank file.mp3")
        return audio,audio1
def checkAudio(sPath,dPath,beatmap,audio_name):
            song = beatmap + audio_name
            checked = []
            fileNames = [sPath + "normal-hitnormal",sPath + "combobreak",sPath + "spinnerbonus",sPath + "spinnerspin",sPath + "normal-hitnormal",sPath+"spinnerspin",sPath+"soft-slidertick"]
            fileNames2 = [dPath + "normal-hitnormal",dPath + "combobreak",dPath + "spinnerbonus",dPath + "spinnerspin",dPath + "normal-hitnormal",dPath+"spinnerspin",dPath+"soft-slidertick"]
            fileTypes = ".mp3",".wav"
            for x in range(6):
                if os.path.exists(sPath):
                    if os.path.exists(fileNames[x] + fileTypes[0]):
                        print("true")
                        checked.append(fileNames[x] + fileTypes[0])
                        print("Adding: " + fileNames[x] + fileTypes[0] + " from skin path: " )
                        
                    elif os.path.exists(fileNames[x] + fileTypes[1]):
                        checked.append(fileNames[x] + fileTypes[1])
                        print("Adding: " + fileNames[x] + fileTypes[1] + " from skin path: ")
                    else:
                       if os.path.exists(fileNames2[x] + fileTypes[0]):
                           checked.append(fileNames2[x] + fileTypes[0])
                           print("Adding: " + fileNames2[x] + fileTypes[0] + " from default skin path")
                       elif os.path.exists(fileNames2[x] + fileTypes[1]):
                            checked.append(fileNames2[x] + fileTypes[1])
                            print("Adding: " + fileNames2[x] + fileTypes[1] + " from default skin path")
                else:
                       if os.path.exists(fileNames2[x] + fileTypes[0]):
                           print(x)
                           checked.append(fileNames2[x] + fileTypes[0])
                           print("Adding: " + fileNames2[x] + fileTypes[0] + " from default skin path")
                       elif os.path.exists(fileNames2[x] + fileTypes[1]):
                            checked.append(fileNames2[x] + fileTypes[1])
                            print("Adding: " + fileNames2[x] + fileTypes[1] + " from default skin path")

            rate, z = read(song,"song")
            ratey, y = 2,2
            rateM, m = 3,3
            ratesb, b = 4,4
            ratesc, c = 5,5
            rateS, s = 6,6
            rateT, t = 7,7
            ratey, y  = tryCatch(ratey,y,checked[0])
            rateM, m = tryCatch(rateM,m,checked[1])
            ratesb, b = tryCatch(ratesb,b,checked[2])
            ratesc, c = tryCatch(ratesc,c,checked[3])
            rateS, s = tryCatch(rateS,s,checked[4])
            rateT, t = tryCatch(rateT,t,checked[5])

            if "wav" in checked[5]:
                    
                spinSound = AudioSegment.from_wav(checked[5]) 
            else:  
                spinSound = AudioSegment.from_mp3(checked[5])

            return rate,y,rate,z,rateM,m,ratesb,b,ratesc,c,rateS,s,spinSound,rateT,t
        



def parseData():

        a = open("beatmap.txt", "r")

        beatmap_info = eval(a.read())
        Info = namedtuple("Info", "time combo combostatus showscore score accuracy clicks hitresult timestamp id hp more")
        Circle = namedtuple("Circle", "state deltat followstate sliderhead x y")
        Slider = namedtuple("Slider", "followstate hitvalue tickend x y")
        Spinner = namedtuple("Spinner", "rotate progress bonusscore hitvalue")

        a = open("resultinfo.txt", "r")
        my_info = eval(a.read())
        return my_info, beatmap_info


def processAudio(my_info,beatmap_info,skin_path,offset,endtime,default_skinP,beatmap_path,audio_name):
        rate,y,rate,z,rateM,m,ratesb,b,ratesc,c,rateS,s,spinSound,rateT,tick = checkAudio(skin_path,default_skinP,beatmap_path,audio_name)
        start=time.time()
        tmpVal = 0
        spinBonusTime = 0
        spinRotationTime = 0
        length_bonus = len(b)/ratesb
        length_spin = len(c)/ratesc
        spinSpeedup = 6
        speedup_dict = {}
        
        for x in range(6,0,-2):
            fr = spinSound.frame_rate + int(spinSound.frame_rate / (x - 0.5))
            faster_senpai = spinSound._spawn(spinSound.raw_data, overrides={'frame_rate': fr})
            faster_senpai_export = faster_senpai.set_frame_rate(44100)
            faster_rate , faster_c = pydubtonumpy(faster_senpai_export)
            speedup_dict["sound_" + str(x)] =  faster_c

        slider_duration = 0
        arrow_time = 0
        arrow_time_list = []
        countT = 0
        sliderTime = []
        repeatedTime = []
        durationTime = []
        endTime = []
        tmpSpinVal = 0
        for bp in range(len(beatmap_info)):
                if "slider" in beatmap_info[bp]["type"]:
                        #print(beatmap_info[bp]['slider ticks'])
                        sliderTime.append(beatmap_info[bp]["time"])
                        repeatedTime.append(beatmap_info[bp]["repeated"])
                        durationTime.append(beatmap_info[bp]["duration"])
                        endTime.append(beatmap_info[bp]["end time"])
        for x in range(len(my_info)):
            start_index = int(my_info[x].time/1000 * rate)
            if type(my_info[x].more).__name__ == "Slider":
                if my_info[x].more.hitvalue==10:
                        z[start_index:start_index + len(tick)] += tick * 0.5
                        print(my_info[x].time)  
            if type(my_info[x].more).__name__ == "Circle":
                spinSpeedup = 6
                if my_info[x].more.sliderhead == True:
                        arrow_time_list = []
                        if len(sliderTime) > 0:
                            for a in range(repeatedTime[0]):
                                        arrow_time_list.append(sliderTime[0] + durationTime[0] * (a+1))
                            start_index2 = int(my_info[x].time/1000 * rate)
                            z[start_index2:start_index2 + len(s)] += s * 0.5

                            for abc in arrow_time_list:
                                    start_index2 = int(abc/1000 * rate)
                                    z[start_index2:start_index2+ len(s)] += s * 0.5
                            durationTime.pop(0)
                            sliderTime.pop(0)
                            endTime.pop(0)
                            repeatedTime.pop(0)
                        '''
                        if len(sliderTime) == 1:
                            start_index2 = int(sliderTime[0]/1000 * rate)
                            z[start_index2:start_index2 + len(s)] += s * 0.5 
                            start_index2 = int(endTime[0]/1000 * rate)
                            z[start_index2:start_index2 + len(s)] += s * 0.5'''
                        continue
                        

                        

                if my_info[x].hitresult == None:
                        pass

                elif my_info[x].hitresult > 0:
                        

                        z[start_index:start_index + len(y)] += y * 0.5
                elif my_info[x].hitresult == 0:
                        

                        z[start_index:start_index + len(m)] += m * 0.5



            elif type(my_info[x].more).__name__ == "Spinner":
                if int(my_info[x].more.rotate) >= 180 or int(my_info[x].more.rotate) <= -180:
                    if my_info[x].time/1000 < spinRotationTime:
                        pass
                    else:
                        z[start_index:start_index + len(speedup_dict["sound_" + str(spinSpeedup)])] += speedup_dict["sound_" + str(spinSpeedup)] * 0.5
                        spinRotationTime = my_info[x].time/1000 + length_spin
                        if my_info[x].more.progress > tmpSpinVal + 0.1 and spinSpeedup > 2:
                            spinSpeedup -= 2
                        tmpSpinVal = my_info[x].more.progress

                if my_info[x].more.bonusscore  > 0:
                    
                    if my_info[x].more.bonusscore != tmpVal:
                        tmpVal = my_info[x].more.bonusscore
                        z[start_index:start_index + len(b)] += b * 0.5
                        '''
                   else:
                            if x <= len(my_info) - 1 and my_info[x+1].more.bonusscore == 0:
                                print("ELSE: Added Hit sounds to {} that ends at {}".format(my_info[x].time,my_info[x].time + len(b)))
                                z[start_index:start_index + len(b)] += b * 0.5
                                spinBonusTime = my_info[x].time/1000 + length_bonus
                            continue'''

        if offset >= 0:
            rendtime = endtime - offset
            out = z[int(offset/1000*rate):]
        else:
            offset = -offset
            rendtime = endtime + offset
            out = np.zeros((len(z) + int(offset/1000 * rate), 2), dtype=z.dtype)
            out[int(offset/1000 * rate):] = z

        if endtime != -1:
            out = out[:int(rendtime/1000 * rate)]


        write('z.mp3', rate, out)
        
        end=time.time()
        print(end-start)


def create_audio(my_info, beatmap_info, offset, endtime, audio_name, mpp):
    from global_var import Paths, SkinPaths
    beatmap_path = Paths.beatmap
    default_skinP = SkinPaths.default_path
    skin_path = SkinPaths.path

    if mpp >= 1:
        audio_args = (my_info,beatmap_info,skin_path,offset,endtime,default_skinP,beatmap_path,audio_name,)
        audio = Process(target=processAudio, args=audio_args)
        audio.start()
        return audio
    else:
        processAudio(my_info,beatmap_info,skin_path,offset,endtime,default_skinP,beatmap_path,audio_name)
        return None

if __name__ == '__main__':
    res, beat = parseData()
    #args = my_info,beatmap_info,skin_path,offset,endtime,default_skinP,beatmap_path,audio_name
    processAudio(res, beat, "C:\\Users\\Shiho\\Desktop\\Projects\\osr2mp4\\res\\skin\\", -550, -1,
                 "C:/Users/Shiho/Downloads/skin/", "C:\\Users\\Shiho\\Downloads\\Compressed\\F\\", "Tengaku.mp3")

