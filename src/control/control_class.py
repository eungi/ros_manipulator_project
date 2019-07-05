#!/usr/bin/env python

import rospy
import numpy as np
import utils

class Control() :
	def __init__(self) :
		self.goal = np.zeros(11)
		self.pose_t = np.zeros(11)

		self.joint_names = ['base_joint', 'lid_joint', 'arm01_joint', 
				    'arm02_joint', 'arm03_joint', 
				    'gripper_base_joint', 'sub_gripper_base_joint', 
				    'gear_support_joint', 'sub_gear_support_joint', 
				    'gripper_joint', 'sub_gripper_joint']

		self.shape_ = 'Not Detected'
		self.drawing_flag = 'false'

		self.Zero_point = [-0.06, 0.02, 0.8]
		self.T_point = [-0.06, 0.02, 0.8]

		self.draw_path = []
		self.path_interval = 30
		self.step = 0

	def path_planning(self, waypoints) :
		full_path = []

		# zero-pose -> first waypoint (waypoints[0])
		full_path.append(self.path_interval_slice(self.Zero_point, waypoints[0]))
		
		# first waypoint -> last waypoint
		for i in range(len(waypoints)-1) :
			full_path.append(self.path_interval_slice(waypoints[i], waypoints[i+1]))

		# waypoints[0] -> last waypoint (len(waypoints)+1)
		full_path.append(self.path_interval_slice(waypoints[0], self.Zero_point))

		self.draw_path = full_path

	def path_interval_slice(self, start_pt, end_pt) :
		local_path = []

		dx = (end_pt[0] - start_pt[0]) / self.path_interval
		dy = (end_pt[1] - start_pt[1]) / self.path_interval
		dz = (end_pt[2] - start_pt[2]) / self.path_interval

		#local_path.append(start_pt)

		for d in range(self.path_interval) :
			pt_x = start_pt[0] + (d+1)*dx
			pt_y = start_pt[1] + (d+1)*dy
			pt_z = start_pt[2] + (d+1)*dz
			local_path.append([pt_x, pt_y, pt_z])

		return local_path
