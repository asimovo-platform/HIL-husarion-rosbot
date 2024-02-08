from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    robot_name = 'husarion_rosbot'
    use_sim_time = LaunchConfiguration('use_sim_time')

    bridge_node = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        name='bridge_node',
        output='screen',
        parameters = [{'use_sim_time': use_sim_time}],
        arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                      #'/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
                   '/scan/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked',
                   '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
                      #'/model/husarion_rosbot/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
                      #'/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model',
                      #'/model/husarion_rosbot/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
                      #'/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU'
                   ],
        remappings=[
                    #('/joint_state', '/joint_states'),
                    #('/model/husarion_rosbot/odometry', '/odom/raw'),
                    #('/model/husarion_rosbot/tf', '/tf')])
            ])

    lidar_tf2 = Node(
                package = 'tf2_ros',
                executable = 'static_transform_publisher',
                name = 'lidar_stf',
                parameters = [{'use_sim_time': use_sim_time}],
                arguments = [
                    '0', '0', '0', '0', '0', '0', '1','laser', 'husarion_rosbot/base_link/laser'
                ]
            )
    imu_tf2 = Node(
                package = 'tf2_ros',
                executable = 'static_transform_publisher',
                name = 'imu_stf',
                parameters = [{'use_sim_time': use_sim_time}],
                arguments = [
                    '0', '0', '0', '0', '0', '0', '1','imu_link', 'husarion_rosbot/base_link/imu_sensor'
                ]
            )
            
    return LaunchDescription([
        DeclareLaunchArgument(name='use_sim_time', default_value='True', description='Flag to enable use_sim_time'),
	bridge_node,
	lidar_tf2,
    #imu_tf2
    ])
