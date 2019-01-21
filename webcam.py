import cv2,time,pandas
from datetime import datetime
first_frame=None
status_list=[None,None]
#index out of range when the first loop is executed for index number -2
times=[None,None]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0)


while True:
    check,frame=video.read()
    status=0

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
#assign first frame to the variable
    thresh_frame=cv2.threshold(delta_frame, 30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None, iterations=2)

    (_,cnts,_)=cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) <100:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        #x,y,w,z alloted automatically as in the cnts tuple
        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),3)
    status_list.append(status)

    status_list=status_list[-2:]


    if status_list[-1]==1 and status_list[-2]==0: #chekcing the last and the second last thing stored in the list
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

        interval=times[-1]-times[-2]
        print(interval)
        distance=25 #covered by the camera. in metres
        speed=distance/interval
        speed=speed* 3.6
        print("spees is:"+ speed) #convert it into km/hr
        if speed> 40:
            print( "Over Speeding")

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("thresh_delta", thresh_frame)
    cv2.imshow("Colour Frame", frame)

    key=cv2.waitKey(1)
    #print(gray)
    #print(delta_frame)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break


#print(status_list)
print(times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows
