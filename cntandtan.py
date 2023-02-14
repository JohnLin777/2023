import cv2
import numpy


def find_nearest_points(point, points,no):
    distances = numpy.linalg.norm(points - point, axis=1)
    nearest_indices = numpy.argsort(distances)[no]
    return points[nearest_indices[0]]
def calculate_area(point, nearest_points):
    v1 = nearest_points[1] - nearest_points[0]
    v2 = point - nearest_points[0]
    return numpy.linalg.norm(numpy.cross(v1, v2)) / 2
def empty(v):
    pass
def pointt(vertices):
    for le in range(len(vertices)):#對點進行標示
                        qw=0
                        cv2.circle(frame1,vertices[le,0],5,(255,0,0),cv2.FILLED)
                        az=vertices[le,0,qw]
                        if az==0:
                            continue
                        az=str(az)
                        cv2.putText(frame1,az,vertices[le,0],cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        qw=1
                        ae=vertices[le,0,qw]
                        if ae==0:
                            continue
                        ae=str(ae)
                        cv2.putText(frame1,ae,[int(az)+70,int(ae)],cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
def lr(left,right):
    rate=left/right
    if rate==float("inf"):
        rate=1
    elif rate>=1.7 and rate !=float("inf"):
        rate=2
    elif rate <=1.7 and rate >1.5:
        rate =1.6
    elif rate <=1.5 and rate >1.3:
        rate =1.4
    elif rate <=1.3 and rate >1.1:
        rate =1.2
    elif rate <=1.1 and rate >0.9:
        rate =1
    elif rate <=0.9 and rate >0.7:
        rate =0.8
    elif rate <=0.7 and rate >0.5:
        rate =0.6
    elif rate <=0.5 and rate >0.3:
        rate =0.4
    elif rate <=0.3 and rate >0:
        rate =0
    return rate 


cv2.namedWindow('trackbar')
cv2.resizeWindow('trackbar',640,320) 
#cv2.createTrackbar('hue min','trackbar',0,179,empty)
cv2.createTrackbar('hue max','trackbar',273,400,empty)
cv2.createTrackbar('sat min','trackbar',275,400,empty)
cv2.createTrackbar('sat max','trackbar',270,550,empty)
#cv2.createTrackbar('val min','trackbar',0,255,empty)
#cv2.createTrackbar('val max','trackbar',255,255,empty)


cap=cv2.VideoCapture("road.mp4")
mat=numpy.ones((5,5),numpy.uint8)

while True:
    ret,frame=cap.read()
    if ret:
        #hi=cv2.getTrackbarPos('hue min','trackbar')
        ha=cv2.getTrackbarPos('hue max','trackbar')
        si=cv2.getTrackbarPos('sat min','trackbar')
        sa=cv2.getTrackbarPos('sat max','trackbar')
       # vi=cv2.getTrackbarPos('val min','trackbar')
        #va=cv2.getTrackbarPos('val max','trackbar')

        low=numpy.array([0,0,70])#0,0,70
        upp=numpy.array([179,45,235])#179,40,210
        frame=frame[25:425,:550]
        frame1=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #frame1=cv2.dilate(frame1,mat,iterations=2)
       # frame1=cv2.erode(frame1,mat,iterations=3)

        frame1=cv2.inRange(frame1,low,upp)
        frame=cv2.bitwise_not(frame,frame,mask=frame1)
        frame1=cv2.Canny(frame1,150,700)
        #frame1=cv2.line(frame1,(0,ha),(si,sa),(255,255,255),1)
        #frame1=cv2.line(frame1,(0,ha+30),(si,sa),(255,255,255),1)
        #frame1=cv2.line(frame1,(550,ha),(550-si,sa),(255,255,255),1)
        #frame1=cv2.line(frame1,(550,ha+30),(550-si,sa),(255,255,255),1)

        aa=0
        rate1=[0.0]
        rate=[0.0]
        xyx=[0]
        for i in range(5):
            rate.append(0.0)
        contours,hierachy=cv2.findContours(frame1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            if len(cnt)<=1:
                #forward
                print('fffffffff')
                continue
            else:
                if len(cnt)>1098:
                    #forward
                    print('  f f f f')
                    break
                nearest_points1= find_nearest_points((si,sa), cnt,0)  
                if ((nearest_points1[0][0]-si)**2 + (nearest_points1[0][1]-sa)**2)**0.5<=ha:
                    print('      nonono')
                    print('fffff')

                    #forward
                    
                    break

                else:
                    cv2.circle(frame1,(si,sa),ha,(255,0,0),3)
                    cv2.circle(frame1,(nearest_points1[0][0],nearest_points1[0][1]),5,(255,0,0),cv2.FILLED)                 
                    cv2.circle(frame1,(si,sa),5,(255,0,0),cv2.FILLED)

                    rate[2]=rate[3]
                    rate[3]=rate[4]
                    rate[4]=rate[5] 
                    rate[5]=nearest_points1[0][0]
                    if (rate[2] or rate[3] or rate[4] or rate[5])<275 or (rate[2] or rate[3] or rate[4] or rate[5])>275:
                        print('forward')

                    #if (xyx[0] or xyx[1] or xyx[2] or xyx[3])<275 and (xyx[0] or xyx[1] or xyx[2] or xyx[3])>275:
                        #aa=1
                    elif (rate[4] or rate[5])!=275:
                        #forward
                        print('turn')
                        
            rate[1]=rate[2]
            rate[2]=rate[3]
            rate[3]=rate[4]
            rate[4]=rate[5]
            #rate[5]=lr(left,right)
            a=rate.count(rate[1])
            b=rate.count(rate[2])
            c=rate.count(rate[3])
            d=rate.count(rate[4])
            e=rate.count(rate[5])
            outt=lr((rate[1]*a+rate[2]*b+rate[3]*c+rate[4]*d+rate[5]*e),(a+b+c+d+e))
            if outt==0:
                outt=1
            #print(outt)
            #print("qwqw",(a+b+c+d+e))
        cv2.imshow('video1',frame1)
        #cv2.imshow('video2',frame)

    else:
        break
    if cv2.waitKey(100) == ord(' '):
        break