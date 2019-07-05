#!/usr/bin/env python

import rospy
import numpy as np

from sensor_msgs.msg import JointState
from std_msgs.msg import Header, ColorRGBA
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion, Pose, Point, Vector3

class Control :
	def __init__(self) :
		self.goal = np.zeros(11)
		self.pose_t = np.zeros(11)

		self.joint_names = ['base_joint', 'lid_joint', 'arm01_joint', 'arm02_joint', 'arm03_joint', 'gripper_base_joint', 'sub_gripper_base_joint', 'gear_support_joint', 'sub_gear_support_joint', 'gripper_joint', 'sub_gripper_joint']

		self.shape_ = 'Not Detected'
		self.drawing_flag = 'false'

		self.draw_path = []

		self.Zero_point = [-0.06, 0.02, 0.8]
		self.T_point = [-0.06, 0.02, 0.8]

		self.waypoint_z = 0.25
		self.Triangle_waypoint = [[0., 0.5], [0.2, 0.25], [-0.2, 0.25]]
		self.Rectangle_waypoint = [[0.1, 0.4], [0.1, 0.25], [-0.1, 0.25], [-0.1, 0.4]]
		self.Pentagon_waypoint = [[0., 0.42], [0.1, 0.35], [0.07, 0.25], [-0.07, 0.25], [-0.1, 0.35]]
		self.Hexagon_waypoint = [[0., 0.42], [0.07, 0.37], [0.07, 0.31], [0., 0.26], [-0.07, 0.31], [-0.07, 0.37]]

	def make_JointState_topic(self, _pose) :
		pose = JointState()
		pose.header = Header()
		pose.header.stamp = rospy.Time.now()
		pose.name = self.joint_names
		pose.position = _pose
		pose.velocity = []
		pose.effort = []

		return pose

	def shape_topic(self, shape) :
		marker_ = Marker()
		marker_.type = Marker.SPHERE_LIST	# LINE_STRIP
		marker_.scale = Vector3(0.02, 0.02, 0.02)
		marker_.header = Header(frame_id='base_link')
		marker_.color = ColorRGBA(0.0, 1.0, 0.0, 0.8)
		for pt in shape :
			p = Point()
			p.x = pt[0]
			p.y = pt[1]
			p.z = self.waypoint_z
			marker_.points.append(p)

		return marker_

	def arm_pose_topic(self, _pose) :
		marker = Marker(
                		type = Marker.SPHERE,
                		id = 0,
				lifetime = rospy.Duration(1.5),
				pose = Pose(Point(_pose[0], _pose[1], _pose[2]), Quaternion(0, 0, 0, 1)),
				scale = Vector3(0.04, 0.04, 0.04),
				header = Header(frame_id='base_link'),
				color = ColorRGBA(1.0, 0.0, 1.0, 0.8))

		return marker

	def return_waypoint(self) :
		if self.shape_ == 'Not Detected' : return []
		elif self.shape_ == 'Triangle' : return self.Triangle_waypoint
		elif self.shape_ == 'Rectangle' : return self.Rectangle_waypoint
		elif self.shape_ == 'Pentagon' : return self.Pentagon_waypoint
		elif self.shape_ == 'Hexagon' : return self.Hexagon_waypoint
		else : return []

	def path_planning(self) :

		# self.draw_path = path
		pass
