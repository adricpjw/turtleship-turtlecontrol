from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('turtlecontrol'),
        'config',
        'params.yaml'
        )

    joy_node = Node(
        package = "joy",
        executable = "joy_node",
    )

    teleop_node = Node(
        package = "turtlecontrol",
        executable = "teleop",
        name = "teleop_cmd",
        parameters=[config]
    )

    ld.add_action(joy_node)
    ld.add_action(teleop_node)
    return ld