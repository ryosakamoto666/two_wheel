#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import RPM2_Time
from nav_msgs.msg import Odometry

wr = 0.03825	# Wheel Radius [m]
d  = 0.00615	# Wheel-Center distance [m]

def odom(msg):
	global last_x,last_y,last_th,last_Time,now_Time
	R_data = msg.r_data
	L_data = msg.l_data
	now_Time = rospy.Time.now()
	dt = now_Time - last_Time
	dt = dt.secs + dt.nsecs/10.0**9

	vr = round(R_data,2)*((2*math.pi)/60.0) * wr
	vl = round(L_data,2)*((2*math.pi)/60.0) * wr
	w = (vr-vl)/(2*d)

	dL_r = vr*dt
	dL_l = vl*dt
	dth = w *dt
	dL = (dL_r + dL_l)/2

	diff_Time = now_Time - start_Time
	Odom.header.stamp.secs = diff_Time.secs
	Odom.header.stamp.nsecs = diff_Time.nsecs

	if abs(dth) < 0.01 or dth==0.0 :
		Odom.pose.pose.position.x = last_x + dL * math.cos(last_th+(dth/2))
		Odom.pose.pose.position.y = last_y + dL * math.sin(last_th+(dth/2))
	else :
		p = dL/dth
		dL1 = 2*p*math.sin(dth/2)
		Odom.pose.pose.position.x = last_x + dL1 * math.cos(last_th+(dth/2))
		Odom.pose.pose.position.y = last_y + dL1 * math.sin(last_th+(dth/2))

	Odom.pose.pose.orientation.z = last_th + dth
	Odom.twist.twist.linear.x = (vr + vl)/2
	Odom.twist.twist.angular.z = w
	pub.publish(Odom)

	last_x = Odom.pose.pose.position.x
	last_y = Odom.pose.pose.position.y
	last_th = Odom.pose.pose.orientation.z
	last_Time = now_Time

if __name__=="__main__":
	try:
		rospy.init_node("Odom")
		rospy.Subscriber("/rpm_data", RPM2_Time, odom)
		pub=rospy.Publisher("/Odometry", Odometry, queue_size=2)
		Odom=Odometry()

		last_x = 0.0
		last_y = 0.0
		last_th = 0.0
		start_Time = rospy.Time.now()
		last_Time = start_Time

		rospy.spin()

	except rospy.ROSInterruptException: pass
