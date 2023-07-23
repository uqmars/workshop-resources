import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

class TwistPublisher(Node):
    def __init__(self):
        # Initialise the node
        super().__init__("twist_publisher")
        # Next, create the publisher element
        
        # First element: message type, topic name, QOS
        self.twistPub_ = self.create_publisher(Twist, "/cmd_vel", 10);
        # For now send constant velocity command every 0.5 seconds
        # Every 0.5 seconds the timer will call timer_cb
        self.timer_ = self.create_timer(0.5, self.timer_cb)
    
    def timer_cb(self):
        msg = Twist()
        msg.linear.x = 1.0 #Travel in linear direction of 1 ms
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        # Publish the message
        self.twistPub_.publish(msg)
        # Print something so we know its working
        self.get_logger().info("Sending Twist")

def main(args=None):
    rclpy.init(args=args)
    twistPub = TwistPublisher()
    rclpy.spin(twistPub)
    twistPub.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

