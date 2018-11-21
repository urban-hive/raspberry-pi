#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import *
import time

#global variable
pre_latitude =47.3977622
pre_longitude=8.5456163
latitude =0.0
longitude=0.0



def setGuidedMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='GUIDED') #return true or false
    except rospy.ServiceException, e:
        print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e
        
def setStabilizeMode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        flightModeService = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isModeChanged = flightModeService(custom_mode='STABILIZE') #return true or false
    except rospy.ServiceException, e:
        print "service set_mode call failed: %s. GUIDED Mode could not be set. Check that GPS is enabled"%e

def setLandMode():
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
        #http://wiki.ros.org/mavros/CustomModes for custom modes
        isLanding = landService(altitude = 0, latitude=pre_latitude , longitude=pre_longitude, min_pitch = 0, yaw = 0)
    except rospy.ServiceException, e:
        print "service land call failed: %s. The vehicle cannot land "%e
          
def setArm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(True)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s"%e
        
def setDisarm():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(False)
    except rospy.ServiceException, e:
        print "Service arm call failed: %s"%e


def setTakeoffMode():
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
        takeoffService(altitude = 2, latitude=pre_latitude , longitude=pre_longitude , min_pitch = 0, yaw = 0)
    except rospy.ServiceException, e:
        print "Service takeoff call failed: %s"%e


def setWaypointMode(a,b):
    rospy.wait_for_service('/mavros/cmd/takeoff')
    try:
        takeoffService = rospy.ServiceProxy('/mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL) 
        takeoffService(altitude = 0, latitude=a , longitude=b , min_pitch = 0, yaw = 0)
    except rospy.ServiceException, e:
        print "Service takeoff call failed: %s"%e    
    



def globalPositionCallback(globalPositionCallback):
    global latitude
    global longitude
    latitude = globalPositionCallback.latitude
    longitude = globalPositionCallback.longitude
    #print ("longitude: %.7f" %longitude)
    #print ("latitude: %.7f" %latitude)

def menu():
    print "Caution!!!:You have to modify pre_la,pre_lo parameter in this python file"
    print "1: to set mode to GUIDED"
    print "2: to set mode to STABILIZE"
    print "3: to set mode to ARM the drone"
    print "4: to set mode to First TAKEOFF"
    print "5: to set mode to move to HOME"
    print "6: to set mode to WAYPOINT"
    print "7: must insert 5 , before press LANDING"
    print "8: print GPS coordinates"
    print "9: to set mode to DISARM the drone"
    
def myLoop():
    x='1'
    while ((not rospy.is_shutdown())and (x in ['1','2','3','4','5','6','7','8','9'])):
        menu()
        x = raw_input("Enter your input: ");
        if (x=='1'):
            setGuidedMode()
        elif(x=='2'):
            setStabilizeMode()
        elif(x=='3'):
            setArm()
        elif(x=='9'):
            setDisarm()
        elif(x=='4'):
            
            setTakeoffMode()
        elif(x=='5'):
            setLandMode()
            time.sleep(1)
            setTakeoffMode()      
        elif(x=='7'):
            setLandMode()
        elif(x=='6'):
            
            #a = input("Enter latitude: ");
            #b = input("Enter longitude: ");
            a, b = map(float, raw_input('enter: latitude , longitude: ').split(','))
            setLandMode()
            time.sleep(1)
            setWaypointMode(a,b)
        elif(x=='8'):
            global latitude
            global longitude
            print ("latitude: %.7f" %latitude)
            print ("longitude: %.7f" %longitude)
        
        else: 
            print "Exit"
        
        
    

if __name__ == '__main__':
    rospy.init_node('dronemap_node', anonymous=True)
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPositionCallback)
    # spin() simply keeps python from exiting until this node is stopped
    
    #listener()
    myLoop()
#rospy.spin()
