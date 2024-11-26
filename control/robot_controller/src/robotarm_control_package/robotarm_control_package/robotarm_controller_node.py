import rclpy as rp
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from robot_msgs.action import RobotOrder
from robot_msgs.msg import RobotState
from std_msgs.msg import Bool

import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
from xarm import version
from xarm.wrapper import XArmAPI

class RobotMain(object):
    """Robot Main Class"""
    
    # Function for Robot Run
    def home(self):
        

    def near_zig_0(self):
        
    def near_zig_1(self):
        
           
    def near_zig_2(self):
        

    def zig_0_hold(self):
        
    def zig_1_hold(self):
        
    def zig_2_hold(self):
        
    
    def select_zig(self, zig_num):
        

    def zig_to_press(self):
        
            
    def press_to_cupBefore(self):
        

    def cup_holder(self):
        
       
      
    def press_to_cupAfter(self):
           
            


            
    def drop_topping(self, pin):
        
    def topping_waypoint_for(self):
        

    def cup_to_topping_0(self):
        
    def cup_to_topping_1(self):
        

      
    def cup_to_topping_2(self):
        
        

    def cup_to_topping(self, toppings):
        


    def topping_to_press_waypoint(self):
        
        
    

    def pressing(self):
        

    
    def pressing_rolling(self):
        
        
    def pressing_half(self):
        
        
    def pressing_rolling_forMiddle(self):
        

    def press_down(self):
       
    def press_up(self):
        

    def cut_icecream(self):
       
        
    
    def press_to_zig(self):
        
        
        
        # POS: zig_2_above

    def to_zig_0(self):
        
    def to_zig_1(self):
        
    def to_zig_2(self):
        
        
    def to_zig(self,zig_num):
        

    def cup_front(self):
        

    def trash(self):
        

    def off(self):
       



class RobotActionServer(Node):
    def __init__(self, robot):
        super().__init__('robot_control_action_server')
        self.action_server = ActionServer(self, RobotOrder, 'robot_order', self.execute_callback)

        self.robot = robot
        
        # self.robot_main.order_msg = {}
        # self.robot_main.order_msg = {'makeReq': {'jigNum': 'A'}}
        # self.robot_main.order_msg['makeReq']['cupNum'] = 'B'
        # self.robot_main.order_msg['makeReq']['topping'] = '1'

    def execute_callback(self, goal_handle):
        feedback_msg = RobotOrder.Feedback()
        feedback_msg.message = 'start making icecream'
        goal_handle.publish_feedback(feedback_msg)


        order_msg = goal_handle.request
        order_type = order_msg.order_type
        tray_num = order_msg.tray_num
        toppings = order_msg.topping_num
        topping_type = order_msg.topping_type


        if order_type == 'icecreaming':
            print('making icecream')
            # --------------icecream start--------------------
           
            feedback_msg.message = 'home'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.home()
            feedback_msg.message = 'home finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'select_zig'
            goal_handle.publish_feedback(feedback_msg)
            print(tray_num)
            self.robot.select_zig(tray_num)
            # self.robot.zig_0_hold()
            feedback_msg.message = 'select_zig finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'zig_to_press'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.zig_to_press()       
            feedback_msg.message = 'zig_to_press finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'press_to_cupBefore'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.press_to_cupBefore()
            feedback_msg.message = 'press_to_cupBefore finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'cup_holder'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.cup_holder()
            feedback_msg.message = 'cup_holder finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'press_to_cupAfter'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.press_to_cupAfter()
            feedback_msg.message = 'press_to_cupAfter finish'
            goal_handle.publish_feedback(feedback_msg)

            if topping_type == 1:           #middle topping
                feedback_msg.message = 'topping_waypoint_for'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.topping_waypoint_for()
                feedback_msg.message = 'topping_waypoint_for finish'
                goal_handle.publish_feedback(feedback_msg)
                
                feedback_msg.message = 'topping_to_press_waypoint'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.topping_to_press_waypoint()
                feedback_msg.message = 'topping_to_press_waypoint finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'pressing_half'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.pressing_half()
                feedback_msg.message = 'pressing_half finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'cup_to_topping'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.cup_to_topping(toppings)
                # self.robot.cup_to_topping_0()
                feedback_msg.message = 'cup_to_topping finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'press_down'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.press_down()
                feedback_msg.message = 'press_down finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'topping_to_press_waypoint'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.topping_to_press_waypoint()
                feedback_msg.message = 'topping_to_press_waypoint finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'pressing_rolling_forMiddle'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.pressing_rolling_forMiddle()
                feedback_msg.message = 'pressing_rolling_forMiddle finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'press_up'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.press_up()
                feedback_msg.message = 'press_up finish'
                goal_handle.publish_feedback(feedback_msg)

            elif topping_type == 2:         # bottom topping
                feedback_msg.message = 'topping_waypoint_for'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.topping_waypoint_for()
                feedback_msg.message = 'topping_waypoint_for finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'cup_to_topping'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.cup_to_topping(toppings)
                # self.robot.cup_to_topping_0()
                feedback_msg.message = 'cup_to_topping finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'press_down'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.press_down()
                feedback_msg.message = 'press_down finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'topping_to_press_waypoint'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.topping_to_press_waypoint()
                feedback_msg.message = 'topping_to_press_waypoint finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'pressing_rolling'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.pressing_rolling()
                feedback_msg.message = 'pressing_rolling finish'
                goal_handle.publish_feedback(feedback_msg)

                feedback_msg.message = 'press_up'
                goal_handle.publish_feedback(feedback_msg)
                self.robot.press_up()
                feedback_msg.message = 'press_up finish'
                goal_handle.publish_feedback(feedback_msg)

                

            feedback_msg.message = 'press_to_zig'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.press_to_zig()	
            feedback_msg.message = 'press_to_zig finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = f'to_zig_{tray_num}'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.to_zig(tray_num)
            # self.robot.to_zig_0()
            feedback_msg.message = f'to_zig_{tray_num} finish'
            goal_handle.publish_feedback(feedback_msg)
            # >> if user takes ice cream,
            #time.sleep(5)

            feedback_msg.message = 'cup_front'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.cup_front()	
            feedback_msg.message = 'cup_front finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'trash'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.trash()
            feedback_msg.message = 'trash finish'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'home'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.home()
            feedback_msg.message = 'home'
            goal_handle.publish_feedback(feedback_msg)

            feedback_msg.message = 'off'
            goal_handle.publish_feedback(feedback_msg)
            self.robot.off()
            feedback_msg.message = 'off finish'
            goal_handle.publish_feedback(feedback_msg)



        goal_handle.succeed()
        result = RobotOrder.Result()
        result.result = 'successfully finished'
        print('successfully made icecream')
        return result

class RobotStatePublisher(Node):
    def __init__(self, arm):
        super().__init__('robot_state_publisher')
        self.arm = arm

        self.robot_publisher = self.create_publisher(RobotState, '/robot_state', 10)
        self.timer_period = 0.2
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.RobotState = RobotState()

    def timer_callback(self):
        angle = self.arm.get_servo_angle()
        self.RobotState.angles = angle[1]

        position = self.arm.get_position()
        self.RobotState.position_code = position[0]
        self.RobotState.positions = position[1]

        temperatures = self.arm.temperatures
        self.RobotState.temperatures = temperatures

        self.robot_publisher.publish(self.RobotState)


class RobotInterruptSubscriber(Node):
    def __init__(self, arm):
        super().__init__('robot_interrupt_subscriber')
        self.arm = arm
        self.suspend_subscriber = self.create_subscription(Bool, '/robot_interrupt', self.robot_interrupt_callback, 10)
        self.robot_move_flag = True

    def robot_interrupt_callback(self, msg):
        # if self.robot_move_flag == False and msg.data == True:
        if msg.data == True:
            self.arm.set_state(3)
            self.robot_move_flag == True
        
        # elif self.robot_move_flag == True and msg.data == False:
        elif msg.data == False:
            self.arm.set_state(0)
            self.robot_move_flag == False

            



def main(args=None):
    robot = RobotMain(arm)

    
    robot_action_server = RobotActionServer(robot = robot)
    robot_state_publisher = RobotStatePublisher(arm = arm)
    robot_interrupt_subscriber = RobotInterruptSubscriber(arm = arm)

    executor = MultiThreadedExecutor()
    executor.add_node(robot_action_server)
    executor.add_node(robot_state_publisher)
    executor.add_node(robot_interrupt_subscriber)

    try:
        executor.spin()

    finally:
        executor.shutdown()
        robot_action_server.destroy_node()
        robot_state_publisher.destroy_node()
        rp.shutdown()

if __name__ == '__main__':
    main()
