import rclpy
from rclpy.node import Node as ROSNode
from nav_msgs.msg import Odometry
# from ignition.msgs.pose_pb2 import Pose
# from ignition.msgs.vector3d_pb2 import Vector3d
# from ignition.transport import Node as IGNNode
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import os

class OdometrySubscriber(ROSNode):

    def __init__(self):
        super().__init__('odometry_subscriber')

        self.qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.subscription = self.create_subscription(Odometry,'odom', self.publish_pose, self.qos_profile)
        self.subscription  # prevent unused variable warning
        # self.ignition_node = IGNNode()
        self.world_name = 'maze'


    def publish_pose(self, odometry):
        # position = Vector3d()
        # position.x = odometry.pose.pose.position.x
        # position.y = odometry.pose.pose.position.y
        # position.z = odometry.pose.pose.position.z

        # position_message = Pose()
        # position_message.name = "husarion_rosbot"
        # position_message.position.CopyFrom(position)

        # self.ignition_node.request(position_message, service="/world/"+self.world_name+"/set_pose", timeout=300, reptype="ignition.msgs.Boolean")
        # print("ign service -s /world/empty/set_pose --reqtype ignition.msgs.Pose  --reptype ignition.msgs.Boolean  --timeout 300 --req 'name: \"husarion_rosbot\", position: {x: "+str(odometry.pose.pose.position.x)+", y: "+str(odometry.pose.pose.position.y)+", z: 0.0432}'")

        print("Odometry x:" +str(odometry.pose.pose.position.x) + " y: " + str(odometry.pose.pose.position.y))

        os.system("ign service -s /world/maze/set_pose --reqtype ignition.msgs.Pose  --reptype ignition.msgs.Boolean  --timeout 300 --req 'name: \"husarion_rosbot\", position: {x: "
                  +str(odometry.pose.pose.position.x)+", y: "+str(odometry.pose.pose.position.y)+", z: 0.0432}, orientation: {x: "
                  +str(odometry.pose.pose.orientation.x)+", y: "+str(odometry.pose.pose.orientation.y)+", z: "+str(odometry.pose.pose.orientation.z)+", w: "+str(odometry.pose.pose.orientation.w)+"}'")


def main(args=None):
    rclpy.init(args=args)

    odometry_subscriber = OdometrySubscriber()

    rclpy.spin(odometry_subscriber)

if __name__ == '__main__':
    main()
