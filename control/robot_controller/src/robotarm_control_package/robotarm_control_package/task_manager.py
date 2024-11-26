import rclpy as rp
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from robot_msgs.action import RobotOrder
from robot_msgs.msg import UserOrder, RobotState, Vision, ResponseUserOrder
from std_msgs.msg import Bool

from datetime import datetime
import time
import json

from database.connect.connectMysql import *



# IcecreamDict = {}
# cursor = conn.cursor()
# cursor.execute('SELECT iceName, iceCode FROM ICECREAM')
# for (icename, icecode) in cursor.fetchall():
#     IcecreamDict[icename] = icecode
# cursor.execute('SELECT toppingName, toppingCode FROM ICECREAM')
# for (toppingname, toppingcode) in cursor.fetchall():
#     IcecreamDict[icename] = icecode
# cursor.close()

IcecreamDict = {'Chocolate':1, 'Vanilla':2, 'Strawberry':3}
ToppingDict = {'Chocoball':1, 'Caramel':2, 'Strawberry Topping':3}
ToppingTypeDict = {'Middle':1, 'Bottom':2}

class TaskManager(Node):
    def __init__(self, conn, cursor):
        super().__init__('taskManager')
        
        self.action_client = ActionClient(self, RobotOrder, 'robot_order')
        self.order_subscriber = self.create_subscription(UserOrder, '/user_order', self.user_order_callback, 10)
        self.to_user_msg_publisher = self.create_publisher(ResponseUserOrder, '/user_order_response', 10)
        self.order_timer = self.create_timer(1, self.order_timer_callback)
        
        self.order_queue = []
        self.order_acting = False
        
        self.tray_status = [0,0,0]

        self.conn = conn
        self.cursor = cursor
    
    def get_tray_num_and_icecream(self):
        try:
            tray_num = []
            tray_icecream = []
            for index, value in enumerate(self.tray_status):
                if value != 0:
                    tray_num.append(index)
                    tray_icecream.append(value)
            print(tray_num, tray_icecream)
            return tray_num, tray_icecream
        except:
            return None, None
        

    def user_order_callback(self, msg):
        action = msg.action
        # icecream = IcecreamDict[msg.icecream]
        icecream = msg.icecream
        # topping = [ToppingDict[topping] for topping in msg.topping] # 한글리스트를 숫자로 변환
        topping = msg.topping       # 숫자 리스트로 바로 입력
        topping_type = ToppingTypeDict[msg.topping_type]

        res_msg = ResponseUserOrder()

        if len(self.order_queue) == 0:
            self.order_queue.append([action, icecream, topping, topping_type])
            print('order queue :',len(self.order_queue))

            res_msg.content = f'주문접수완료-{len(self.order_queue)}개 처리중'
            self.to_user_msg_publisher.publish(res_msg)

            
        elif self.order_queue[0][0] == 'icecreaming' and action == 'icecreaming':
            self.order_queue.append([action, icecream, topping, topping_type])
            print('order queue :',len(self.order_queue))

            res_msg.content = f'주문접수완료-{len(self.order_queue)}개 처리중'
            self.to_user_msg_publisher.publish(res_msg)
        
        else:
            res_msg.content = '주문접수실패-아이스크림제조가 끝나고 명령 해주세요'
            self.to_user_msg_publisher.publish(res_msg)
    
    def order_timer_callback(self):
        # print('timer')
        if self.order_acting == True:
            return
        
        if len(self.order_queue) == 0:
            return
        
        tray_num, tray_icecream = self.get_tray_num_and_icecream()
        print('traynum:',tray_num, 'icecream:',tray_icecream)

        if tray_num is None:
            return
        if len(tray_num) == 0:
            return
        if not 0 < tray_num[0] < 7:
            return
        
        res_msg = ResponseUserOrder()

        if tray_icecream[0] == self.order_queue[0][1]: #아이스크림 주문과 올려진 맛이 같다면
            #아이스크림 일치 알림
            res_msg.content = f'주문 아이스크림 일치-{tray_icecream[0]}'
            self.to_user_msg_publisher.publish(res_msg)

            self.update_sale_database(tray_icecream[0],self.order_queue[0][2])

            print('아이스크림 일치')
            self.order_acting = True
            self.send_goal(self.order_queue[0], tray_num[0])
            #데이터베이스 업로드
            
        
        elif tray_icecream[0] is not None:
            #아이스크림 불일치 알림
            res_msg.content = f'주문 아이스크림 불일치-{tray_icecream[0]}'
            self.to_user_msg_publisher.publish(res_msg)

            self.update_sale_database(tray_icecream[0],self.order_queue[0][2])

            print('아이스크림 불일치')
            self.order_acting = True
            self.send_goal(self.order_queue[0], tray_num[0])
            #데이터베이스 업로드
            


    def send_goal(self, msg, tray_num):
        goal_msg = RobotOrder.Goal()
        goal_msg.order_type = msg[0]    #action
        goal_msg.tray_num = tray_num     #tray_num
        goal_msg.topping_num = msg[2]  #topping
        goal_msg.topping_type = msg[3]    #topping_type
        print(goal_msg)
        
        self.action_client.wait_for_server()

        self.send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            print('goal rejected')
            return

        print('goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        
        print(result)

        self.order_queue.pop(0)
        print('order queue :',len(self.order_queue))

        time.sleep(3)

        self.order_acting = False

        # if len(self.order_queue) > 0:
        #     self.order_acting = True
        #     self.send_goal(self.order_queue[0])
        

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        print(feedback)
    
    def update_sale_database(self, icecream, topping_code):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('SELECT MAX(salesCode) FROM SALES')
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            max_id = 0
        # icecream = IcecreamDict[icecream] # 아이스크림이 한글일경우 숫자로 변환
        topping_code_json = json.dumps(list(topping_code))
        sql_query = '''insert into `SALES` values(%s, %s, %s, %s, %s, %s, %s);'''
        self.cursor.execute(sql_query, (max_id+1, None,icecream,topping_code_json,None,None,now_time))
        print('order successfully inserted!')
        self.conn.commit()

class TemperatureHandler(Node):
    def __init__(self, conn, cursor):
        super().__init__('temperature_handler')
        self.temperature_subscriber = self.create_subscription(RobotState, '/robot_state', self.robot_state_callback, 10)
        self.conn = conn
        self.cursor = cursor
        
    
    def robot_state_callback(self, msg):
        temperature_state = 0
        temperatures = list(msg.temperatures)
        for temperature in temperatures:
            if temperature > 50:
                temperature_state = 1
        
        # print(temperatures)
        # print(temperature_state)
        
        if temperature_state == 1:
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('SELECT MAX(statusNum) FROM ARIS_TEMP_STATUS')
            max_id = self.cursor.fetchone()[0]
            if max_id is None:
                max_id = 0
            print(max_id)
            sql_query = '''insert into 
                        `ARIS_TEMP_STATUS` (
                            `statusNum`, 
                            motor1, 
                            motor2, 
                            motor3, 
                            motor4, 
                            motor5, 
                            motor6, 
                            `statusDate`
                        )
                        values
                        (
                            %s, %s, %s, %s, %s, %s, %s, %s
                        );'''
            self.cursor.execute(sql_query, (max_id+1, temperatures[0],temperatures[1],temperatures[2],temperatures[3],temperatures[4],temperatures[5], now_time))
            print('temperature successfully inserted!')
            self.conn.commit()

class VisionSubscriber(Node):
    def __init__(self, task):
        super().__init__('vision_subscriber')
        self.vision_subscriber = self.create_subscription(Vision, '/vision', self.vision_callback, 10)
        self.robot_interrupt_publisher = self.create_publisher(Bool, '/robot_interrupt', 10)
        self.task = task

    def vision_callback(self, msg):
        self.task.tray_status = msg.jig_icecream

        robot_interrupt = Bool()
        robot_interrupt.data = False

        hand = msg.hand
        hand_position = msg.hand_position

        if hand == True:
            robot_interrupt.data = True
                
        self.robot_interrupt_publisher.publish(robot_interrupt)

        
        
def main(args=None):
    cursor = conn.cursor()

    rp.init(args=args)
    task_manager = TaskManager(conn, cursor)
    temperature_handler = TemperatureHandler(conn, cursor)
    vision_subscriber = VisionSubscriber(task_manager)

    executor = MultiThreadedExecutor()
    executor.add_node(task_manager)
    executor.add_node(temperature_handler)
    executor.add_node(vision_subscriber)

    try:
        executor.spin()

    finally:
        executor.shutdown()
        task_manager.destroy_node()
        temperature_handler.destroy_node()
        rp.shutdown()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()