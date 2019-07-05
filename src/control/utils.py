#!/usr/bin/env python

import rospy

from sensor_msgs.msg import JointState
from std_msgs.msg import Header, ColorRGBA
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion, Pose, Point, Vector3

class Utils :
	def __init__(self) :
		self.waypoint_z = 0.25

		self.Triangle_waypoint = [[0., 0.5, self.waypoint_z], 
					  [0.2, 0.25, self.waypoint_z], 
					  [-0.2, 0.25, self.waypoint_z],
					  [0., 0.5, self.waypoint_z]]

		self.Rectangle_waypoint = [[0.1, 0.4, self.waypoint_z], 
					   [0.1, 0.25, self.waypoint_z], 
					   [-0.1, 0.25, self.waypoint_z], 
					   [-0.1, 0.4, self.waypoint_z], 
					   [0.1, 0.4, self.waypoint_z]]

		self.Pentagon_waypoint = [[0., 0.42, self.waypoint_z], 
					  [0.1, 0.35, self.waypoint_z], 
					  [0.07, 0.25, self.waypoint_z], 
					  [-0.07, 0.25, self.waypoint_z], 
					  [-0.1, 0.35, self.waypoint_z], 
					  [0., 0.42, self.waypoint_z]]

		self.Hexagon_waypoint = [[0., 0.42, self.waypoint_z], 
					 [0.07, 0.37, self.waypoint_z], 
					 [0.07, 0.31, self.waypoint_z], 
					 [0., 0.26, self.waypoint_z], 
					 [-0.07, 0.31, self.waypoint_z], 
					 [-0.07, 0.37, self.waypoint_z], 
					 [0., 0.42, self.waypoint_z]]

	def make_JointState_topic(self, _pose, joint_names) :
		pose = JointState()
		pose.header = Header()
		pose.header.stamp = rospy.Time.now()
		pose.name = joint_names
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
		marker_.lifetime = rospy.Duration(1.5)
		for pt in shape :
			p = Point()
			p.x = pt[0]
			p.y = pt[1]
			p.z = pt[2]	# self.waypoint_z
			marker_.points.append(p)

		return marker_

	def path_visualization_topic(self, paths) :
		marker_ = Marker()
		marker_.type = Marker.SPHERE_LIST	# LINE_STRIP
		marker_.scale = Vector3(0.01, 0.01, 0.01)
		marker_.header = Header(frame_id='base_link')
		marker_.color = ColorRGBA(1.0, 1.0, 0.0, 0.8)
		marker_.lifetime = rospy.Duration(1.5)
		for path in paths :
			for pt in path :
				p = Point()
				p.x = pt[0]
				p.y = pt[1]
				p.z = pt[2]	# self.waypoint_z
				marker_.points.append(p)

		return marker_

	def arm_pose_topic(self, _pose) :
		marker = Marker(type = Marker.SPHERE,
                		id = 0,
				lifetime = rospy.Duration(1.5),
				pose = Pose(Point(_pose[0], _pose[1], _pose[2]), 
					    Quaternion(0, 0, 0, 1)),
				scale = Vector3(0.04, 0.04, 0.04),
				header = Header(frame_id='base_link'),
				color = ColorRGBA(1.0, 0.0, 1.0, 0.8))

		return marker

	def return_waypoint(self, shape_) :
		if shape_ == 'Not Detected' : return []
		elif shape_ == 'Triangle' : return self.Triangle_waypoint
		elif shape_ == 'Rectangle' : return self.Rectangle_waypoint
		elif shape_ == 'Pentagon' : return self.Pentagon_waypoint
		elif shape_ == 'Hexagon' : return self.Hexagon_waypoint
		else : return []
