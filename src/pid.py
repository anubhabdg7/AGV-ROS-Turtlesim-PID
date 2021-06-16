#!/usr/bin/env python3

# Author- anubhab 

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import matplotlib.pyplot as plt

class Turtlepid:


    def __init__(self) :
        rospy.init_node('turtle_pid',anonymous=True)
        self.vel_pub=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
        self.pose_sub=rospy.Subscriber('/turtle1/pose',Pose,self.update)
        self.v=Twist()
        self.p=Pose()
        

    def update(self,data):
        self.p=data
    def move(self):
        print("Enter the x-coordinate of the point where you want to move to:")
        x=float(input())
        y=float(input("Enter the y-coordinate of the point where you want to move to"))
        d=100
        d_prev=0
        s=0
        self.t=0
        dw_prev=0
        sw=0

        while(1):
            
            self.v.linear.y=0
            self.v.linear.z=0
            self.v.angular.x=0
            self.v.angular.y=0

            print("x=")
            print(self.p.x)
            print("y=")
            print(self.p.y)

            d=math.sqrt((x-self.p.x)*(x-self.p.x)+(y-self.p.y)*(y-self.p.y))
            diff=d-d_prev
            s+=diff
            d_prev=d

            dw=(-self.p.theta+math.atan2(y-self.p.y,x-self.p.x))
            diffw=dw-dw_prev
            sw+=diffw
            dw_prev=dw

            self.v.angular.z=0.2*dw+0.0000001*sw+0.0000003*diffw
            
            
            self.v.linear.x=0.1*d+0.0000002*s+0.0000007*diff
            self.vel_pub.publish(self.v)
        #self.v.angular.z=0
        #self.v.linear.x=0
        #self.vel_pub.publish(self.v)
        
            
        rospy.spin()





if __name__  == '__main__':
        try:
            h=Turtlepid()
            h.move() 
        except rospy.ROSInterruptException: pass
