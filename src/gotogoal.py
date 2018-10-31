#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        
        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.theta = round(self.pose.theta, 4)

    def euclidean_distance(self, goal_pose):
        # Distance from the turtle to the point
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def steering_angle(self, goal_pose):
        # Turtle angle calculation
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)


    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        # Get the input from the user.
        goal_pose.x = input("Set your x goal: ")
        goal_pose.y = input("Set your y goal: ")

        # Please, insert a number slightly greater than 0.01 
        distance_tolerance = input("Set your tolerance: ")

        vel_msg = Twist()


        if goal_pose.x < 0:
            rospy.loginfo("Valor de x invalido, fora do campo")
            rospy.loginfo("Ajustado para 0")
            goal_pose.x = 0
        if goal_pose.x > 11:
            rospy.loginfo("Valor de x invalido, fora do campo")
            rospy.loginfo("Ajustado para 11")
            goal_pose.x = 11
        if goal_pose.y < 0:
            rospy.loginfo("Valor de v invalido, fora do campo")
            rospy.loginfo("Ajustado para 0")
            goal_pose.y = 0
        if goal_pose.y > 11:
            rospy.loginfo("Valor de y invalido, fora do campo")
            rospy.loginfo("Ajustado para 11")
            goal_pose.y = 11
        if distance_tolerance < 0.1:
            rospy.loginfo("Valor de tolerancia invalido , ajustado para 0.1")
            distance_tolerance = 0.1
       
       # Adjust angle of turtle
        while self.steering_angle(goal_pose) > self.pose.theta:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)
        while self.steering_angle(goal_pose) < self.pose.theta:
            vel_msg.linear.x = 0    
            vel_msg.angular.z = -1
            self.velocity_publisher.publish(vel_msg)

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # Make the turtle walk to the point
        while self.euclidean_distance(goal_pose) >= distance_tolerance:
            vel_msg.linear.x = 1
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # End of mission
        rospy.loginfo("Missão concluida!")
        

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass