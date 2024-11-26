from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
	return LaunchDescription(
		[
			Node(
				package='robotarm_control_package',
				executable='robotarm_controller_node', output='screen'),
			Node(
				package='robotarm_control_package',
				executable='task_manager', output='screen'),
			ExecuteProcess(
				cmd=['python3', './gui/main/main.py'],
				output='screen'
			),
			ExecuteProcess(
				cmd=['python3', './vision/main/vision_main.py'],
				output='screen'
			)
		]
	)
