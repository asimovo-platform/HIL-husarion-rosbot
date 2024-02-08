import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share_dir = launch_ros.substitutions.FindPackageShare(package='simple_obstacle_world').find('simple_obstacle_world') + '/'
  
    gazebo_launch_node = launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.AnyLaunchDescriptionSource([
                    os.path.join(get_package_share_directory('ros_ign_gazebo'), 'launch', 'ign_gazebo.launch.py')
                ]),
                launch_arguments = {'ign_args': ['-r -v 4 ' + pkg_share_dir + 'worlds/simple_obstacle.world']}.items()
            )
            # -s --headless-rendering

    return launch.LaunchDescription([
        launch_ros.actions.SetParameter(name='use_sim_time', value=True),
        gazebo_launch_node,
    ])
