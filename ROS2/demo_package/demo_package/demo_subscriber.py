import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

class TwistSubscriber(Node):

    def __init__(self):
        super().__init__("twist_subscriber")
        self.twistSub_ = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.twist_callback,
            10)
        self.twistSub_ # Without this, we will get a warning

    def twist_callback(self, msg : Twist):
        #The message is a twist message
        #Recieved
        self.get_logger().info("RECIEVED: TWIST %f" %msg.linear.x)


def main(args=None):
    rclpy.init(args=args)
    twistSub = TwistSubscriber()
    rclpy.spin(twistSub)
    twistSub.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

