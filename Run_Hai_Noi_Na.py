#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import cos, sin, sqrt

class MoveCircle():
    def __init__(self):        
        rospy.init_node('move_circle_node', anonymous=False, log_level=rospy.DEBUG)
        rospy.loginfo("To stop Turtlebot press CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.odom_callback)
        self.move_cmd = Twist()
        self.current_pose_x = 0
        self.current_pose_y = 0
        self.tol = 0
        self.goal_pose_x = 0
        self.goal_pose_y = 0
 
    def odom_callback(self, odom_data):
        self.current_pose_x = odom_data.pose.pose.position.x
        self.current_pose_y = odom_data.pose.pose.position.y
        #print('Current', self.current_pose_x, self.current_pose_y)

    def move_circle(self, vel_x, vel_z):        
        r = rospy.Rate(10)           
        self.move_cmd.linear.x = vel_x
        self.move_cmd.angular.z = vel_z
        r.sleep()

    def check_stop(self):
        delta_x = self.goal_pose_x - self.current_pose_x
        delta_y = self.goal_pose_y - self.current_pose_y
        error = sqrt(delta_x ** 2 + delta_y ** 2)
        rospy.logdebug(error)
        if error <= self.tol:
           return True
        else:
           return False

    def set_goal(self, tol):
        self.goal_pose_x = self.current_pose_x
        self.goal_pose_y = self.current_pose_y
        #print('goal', self.goal_pose_x, self.goal_pose_y)
        self.tol = tol

    def go_to_goal(self):
        self.move_circle(0.5, 0.5)
        for i in range(0,50000):
            self.cmd_vel_pub.publish(self.move_cmd)

        while not rospy.is_shutdown():
            if self.check_stop():
                self.shutdown()
                break
            else:
                self.cmd_vel_pub.publish(self.move_cmd)          


    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

 
if __name__ == '__main__':
    try:
        Circle_Class = MoveCircle()
        Circle_Class.set_goal(0.15)
        Circle_Class.go_to_goal()
    except:
        rospy.loginfo(" MoveCircle node terminated.")
