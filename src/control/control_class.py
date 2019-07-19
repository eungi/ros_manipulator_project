#!/usr/bin/env python

import rospy
import numpy as np
import math
import utils

from geometry_msgs.msg import PoseStamped

class Control() :
	def __init__(self) :
		self.goal = np.zeros(11)
		self.pose_t = np.zeros(11)

		self.joint_names = ['base_joint', 'lid_joint', 'arm01_joint', 
				    'arm02_joint', 'arm03_joint', 
				    'gripper_base_joint', 'sub_gripper_base_joint', 
				    'gear_support_joint', 'sub_gear_support_joint', 
				    'gripper_joint', 'sub_gripper_joint']

		self.link_lengths = [[0.0, 0.0, 0.12], 
				     [0.00499, 0.025, 0.08499999999999999], 
				     [0.0, 0.0, 0.23500000000000001], 
				     [0.0, 0.0, 0.01500000000000001], 
				     [0.025009999999999998, 0.015000000000000001, 0.23000000000000004], 
				     [0.03, 0.01, 0.12]]

		self.joint_angles = [0, 0, 0, 0, 0, 0]

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

		for d in range(self.path_interval) :
			pt_x = start_pt[0] + (d+1)*dx
			pt_y = start_pt[1] + (d+1)*dy
			pt_z = start_pt[2] + (d+1)*dz
			local_path.append([pt_x, pt_y, pt_z])

		return local_path

	def drawing(self) :
		goal_pt = self.draw_path[self.step//self.path_interval][self.step%self.path_interval]
		self.inverse_kinematics(goal_pt)
		
		self.T_point = self.forward_kinematics()

		self.pose_t[:5] = self.joint_angles[1:]

	def forward_kinematics(self) :
		A_before = 1
		P_before = [0, 0, 0]

		for i in range(len(self.joint_angles)) :
			if i == 0 or i == 1  :
				A = [[np.cos(self.joint_angles[i]), -np.sin(self.joint_angles[i]), 0], 
				     [np.sin(self.joint_angles[i]), np.cos(self.joint_angles[i]), 0], 
				     [0, 0, 1]]
			elif i == 3 :
				A = [[1, 0, 0], 
				     [0, np.cos(self.joint_angles[i]), np.sin(self.joint_angles[i])], 
				     [0, -np.sin(self.joint_angles[i]), np.cos(self.joint_angles[i])]]
			elif i == 4 :
				A = [[np.cos(3.14 - self.joint_angles[i]), -np.sin(3.14 - self.joint_angles[i]), 0], 
				     [np.sin(3.14 - self.joint_angles[i]), np.cos(3.14 - self.joint_angles[i]), 0], 
				     [0, 0, 1]]
			else :
				A = [[1, 0, 0], 
				     [0, np.cos(self.joint_angles[i]), -np.sin(self.joint_angles[i])], 
				     [0, np.sin(self.joint_angles[i]), np.cos(self.joint_angles[i])]]

			P = P_before + np.dot(np.dot(A_before, A), self.link_lengths[i])

			P_before = P
			A_before = np.dot(A_before, A)

		return P_before

	def inverse_kinematics(self, goal_pt) :
		#

		self.joint_angles = [0, 0.2, -0.5, 1.585, 0.4, 0]
		#self.joint_angles = [0, theta1, theta2, theta3, theta4, theta5]
















