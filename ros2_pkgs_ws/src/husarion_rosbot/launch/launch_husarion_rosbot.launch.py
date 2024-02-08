import launch
import launch_ros
import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='husarion_rosbot').find('husarion_rosbot') + '/'

    model_path = os.path.join(pkg_share, 'src/rosbot.urdf')
    
    spawn_red_robot = launch_ros.actions.Node(
        package='ros_ign_gazebo',
        executable='create',
        name = 'robot_spawner',
        arguments = ['-name', 'husarion_rosbot',
                    #'-x', '0.5',
                    #'-y', '-3.0',
                    #'-x', '8',
                    '-x', '0',
                    '-y', '0',
                    '-z', '0.1',
                    '-R', '0.0',
                    '-P', '0.0',
                    '-Y', '0.0',
                    '-file', model_path],
        output='screen'
    )
    
    return launch.LaunchDescription([
        launch.actions.SetEnvironmentVariable(name = 'SDF_PATH', value = [launch.substitutions.EnvironmentVariable('SDF_PATH', default_value=''), pkg_share+'src'] ),
        launch_ros.actions.SetParameter(name='use_sim_time', value=True),
        spawn_red_robot
    ])
