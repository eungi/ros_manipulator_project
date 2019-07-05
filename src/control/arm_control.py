#!/usr/bin/env python

import rospy
import control_class
import utils

from sensor_msgs.msg import JointState
from std_msgs.msg import String, Int8
from visualization_msgs.msg import Marker

def perception_node(data) :
	global shape

	if data.data == 0 :
		shape = 'Not Detected'

	elif data.data == 1 :
		shape = 'Triangle'

	elif data.data == 2 :
		shape = 'Rectangle'

	elif data.data == 3 :
		shape = 'Pentagon'

	elif data.data == 4 :
		shape = 'Hexagon'


def controller() :
	rospy.init_node('arm_control', anonymous=True)
	rate = rospy.Rate(10)

	joint = rospy.Publisher('joint_states', JointState, queue_size=10)
	marker = rospy.Publisher('visualization_marker', Marker, queue_size=100)
	arm_pose = rospy.Publisher('arm_pose_marker', Marker, queue_size=100)
	arm_path = rospy.Publisher('arm_path_marker', Marker, queue_size=100)

	rospy.Subscriber("robotmaker/shape_arm", Int8, perception_node)

	global shape
	shape = 'Not Detected'

	control_ = control_class.Control()
	utils_ = utils.Utils()

	while not rospy.is_shutdown():
		if control_.drawing_flag == 'false' :
			if control_.shape_ != shape :
				control_.shape_ = shape
				print(control_.shape_)

				if shape != 'Not Detected' :
					control_.drawing_flag = 'true'
					control_.path_planning(utils_.return_waypoint(control_.shape_))
					control_.step = 0

		if control_.drawing_flag == 'true' and len(control_.draw_path) > 0 :
			# drawing (inverce kinematics)
			# print(control_.step//control_.path_interval, control_.step%control_.path_interval)
			if control_.step < (len(control_.draw_path)*control_.path_interval)-1 :
				control_.step += 1
			else :
				control_.drawing_flag = 'false'
				#control_.draw_path = []

		joint.publish(utils_.make_JointState_topic(control_.pose_t, control_.joint_names))
		marker.publish(utils_.shape_topic(utils_.return_waypoint(control_.shape_)))
		arm_path.publish(utils_.path_visualization_topic(control_.draw_path))
		arm_pose.publish(utils_.arm_pose_topic(control_.T_point))


if __name__ == "__main__":
	try :
		controller()
	except rospy.ROSInterruptException :
		pass
