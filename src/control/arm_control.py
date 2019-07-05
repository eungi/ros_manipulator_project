#!/usr/bin/env python

import rospy
import control_class

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

	rospy.Subscriber("robotmaker/shape_arm", Int8, perception_node)

	global shape
	shape = 'Not Detected'

	control_ = control_class.Control()

	while not rospy.is_shutdown():
		if control_.drawing_flag == 'false' :
			if control_.shape_ != shape :
				control_.shape_ = shape
				print(control_.shape_)

			if shape != 'Not Detected' :
				control_.drawing_flag = 'true'
				control_.path_planning()

		if control_.drawing_flag == 'true' and len(control_.draw_path) > 0 :
			print('draw start')

		joint.publish(control_.make_JointState_topic(control_.pose_t))
		marker.publish(control_.shape_topic(control_.return_waypoint()))
		arm_pose.publish(control_.arm_pose_topic(control_.T_point))


if __name__ == "__main__":
	try :
		controller()
	except rospy.ROSInterruptException :
		pass
