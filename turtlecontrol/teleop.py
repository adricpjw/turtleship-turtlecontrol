import rclpy
import turtlecontrol.crossing_cv2
from rclpy.node import Node
from sensor_msgs.msg import Joy

# Button & Axes Indexes
BUTTONA =  0
BUTTONB =  1
BUTTONX = 3
BUTTONY = 4
BUTTONLB = 6
BUTTONRB = 7
BUTTONVIEW= 10
BUTTONMENU = 11
BUTTONXBOX = 12
BUTTONLJOY = 13
BUTTONRJOY = 14
BUTTONSS = 15
LJOYX = 0
LJOYY = 1
RJOYX = 2
RJOYY = 3
RTRIG = 4
LTRIG = 5
DPADX = 6
DPADY = 7

class TeleopCmd(Node) :

    def __init__(self):
        super().__init__('teleop_cmd')
        self.initParams()
        self.initPubSub()
        self.stop = 0
        self.prev_buttons = None
        self.prev_axes = None

    def initParams(self):
        self.declare_parameters(
            namespace='',
            parameters=[
                ('timeout',10),
                ('velocity',100),
            ])
    def initPubSub(self):
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.callback,
            10
        )
        self.subscription

    def callback(self, msg):
        #Check if prev state == current state
        if (self.prev_buttons == msg.buttons):
            return

        # Handle stop signal
        self.stop = msg.buttons[BUTTONB] 
            
        # Run crossing detection
        if msg.buttons[BUTTONA]:
            turtlecontrol.crossing_cv2.CrossingDetection.detectPedCrossing()


        self.prev_buttons = msg.buttons
        self.prev_axes = msg.axes




def main(args=None):
    rclpy.init(args=args)

    teleopCmd = TeleopCmd()

    rclpy.spin(teleopCmd)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teleopCmd.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()