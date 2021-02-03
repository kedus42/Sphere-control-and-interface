**Set up instructions:**\
Create a new ros package titled sphere_control in the catkin workspace of both your local machine and the sphere\
Delete the CMakeLists.txt and package.xml files that will be cretaed by default in the package's directory\
Clone the repository into the now empty sphere_control package of both the local machine and the sphere\
Change the absolute path in line 107 of src/joystick_control_client.py to: "the absolute path containing your repo/src/joystick.png"\
You only need to do the previous step on your machine\
Build with catkin_make\
Connect the sphere and your machine to the same network\
Run roscore on both your machine and the sphere\
Export the ROS master of the sphere to the master on your machine by running the export command below on the sphere\
First replace "URI" with your machine's ROS_MASTER_URI which will likely be http://username:11311/\
If not, find the URI listed under the info printed by roscore\
        export ROS_MASTER_URI="URI"\
Run "roslaunch sphere_control launch_local.launch" on your machine\
Run "roslaunch sphere_control launch_sphere.launch" on the sphere\
