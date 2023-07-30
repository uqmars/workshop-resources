from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # Create the command to launch the listener
    start_listener = Node(
        package="demo_package",
        executable="twist_listener",
        name="twist_subsriber"
    )

    start_talker = Node(
        package = "demo_package",
        executable = "twist_talker",
        name = "twist_publisher"
    )
    
    ld = LaunchDescription()
    ld.add_action(start_listener)
    ld.add_action(start_talker)
    return ld


