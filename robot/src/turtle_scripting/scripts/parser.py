#!/usr/bin/env python
import rospy 

def main():
    # Initialize this node with ROS.
    rospy.init_node('turtle_scripting')
    # TODO: Do stuff here
    pass

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        # Thrown when the node is shut down.
        pass