cmake_minimum_required(VERSION 2.8.3)
project(ros_manipulator_project)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
#find_package(catkin REQUIRED COMPONENTS
  #controller_manager
  #diff_drive_controller
  #gazebo_ros
  #gazebo_ros_control
  #joint_state_publisher
  #position_controllers
  #robot_state_publisher
  #rqt_robot_steering
  #rviz
  #xacro
#)
find_package(catkin REQUIRED COMPONENTS roscpp sensor_msgs)


## Declare a catkin package
catkin_package()

#install(DIRECTORY launch urdf stl rviz DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(parse_and_publish src/parse_and_publish.cpp)
target_link_libraries(parse_and_publish ${catkin_LIBRARIES})
#add_dependencies(parse_and_publish std_msgs)
