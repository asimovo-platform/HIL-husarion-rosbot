import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='navigation_stack').find('navigation_stack') + '/'
    robot_pkg_share = launch_ros.substitutions.FindPackageShare(package='husarion_rosbot').find('husarion_rosbot') + '/'
    model_path = os.path.join(robot_pkg_share, 'src/rosbot.urdf')
    rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': launch.substitutions.Command(['xacro ', model_path])}]
    )    
    
    bridge_node = launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.AnyLaunchDescriptionSource([pkg_share + 'launch/launch_bridge.launch.py'])
    )
                       
    robot_localization_node = launch_ros.actions.Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), 
       {'use_sim_time': launch.substitutions.LaunchConfiguration('use_sim_time')}])
       
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', launch.substitutions.LaunchConfiguration('rvizconfig')],
    )
    
    # slam_toolbox_node =  launch.actions.IncludeLaunchDescription(
    #    launch.launch_description_sources.AnyLaunchDescriptionSource([
    #        os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
    #    ]),
    # )
    slam_toolbox_node = launch_ros.actions.Node(
        parameters=[os.path.join(pkg_share, 'config/mapper_params_online_async.yaml'),
       {'use_sim_time': launch.substitutions.LaunchConfiguration('use_sim_time')}],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')
        
    nav2_bringup_node =  launch.actions.IncludeLaunchDescription( 
        launch.launch_description_sources.AnyLaunchDescriptionSource([
            os.path.join(get_package_share_directory( 'nav2_bringup' ), 'launch', 'navigation_launch.py')
        ]),
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=rviz_config_path, description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True', description='Flag to enable use_sim_time'),
        robot_state_publisher_node,
        bridge_node,
        #robot_localization_node,
        rviz_node,
        slam_toolbox_node,
        #nav2_bringup_node
    ])
