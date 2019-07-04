#!/usr/bin/env python

import rospy
import numpy as np

from sensor_msgs.msg import JointState
from std_msgs.msg import Header

class Control :
	def __init__(self) :
		self.goal = np.zeros(11)
		self.pose_t = np.zeros(11)

		self.joint_names = ['base_joint', 'lid_joint', 'arm01_joint', 'arm02_joint', 'arm03_joint', 'gripper_base_joint', 'sub_gripper_base_joint', 'gear_support_joint', 'sub_gear_support_joint', 'gripper_joint', 'sub_gripper_joint']

		self.shape_ = 'Not Detected'
		self.drawing_flag = 'false'

		self.draw_path = []

		self.Triangle_waypoint = []
		self.Rectangle_waypoint = []
		self.Pentagon_waypoint = []
		self.Hexagon_waypoint = []

	def make_JointState_topic(self, _pose) :
		pose = JointState()
		pose.header = Header()
		pose.header.stamp = rospy.Time.now()
		pose.name = self.joint_names
		pose.position = _pose
		pose.velocity = []
		pose.effort = []

		return pose

	def path_planning(self) :

		# self.draw_path = path
		pass
