#!/usr/bin/env python
import actionlib
import turtle_scripting.msg
from instruction import Instruction


class MoveTurtleActionServer():
    '''
    class responsible for action server and associated functions
    '''
    def __init__(self):
        self.action_server = actionlib.self.action_server = actionlib.SimpleActionServer(
            # the action's name
            "move_turtle", 
            # Actionlib generates this object for us
            turtle_scripting.msg.MoveTurtleAction,
            # callback function for when action server receives a goal
            execute_cb=self.callback,
            auto_start=False)
        self.action_server.start()
    
    def callback(self, goal):
        '''
        passed as an arg to another function, called after work is done
        '''
        feedback = turtle_scripter.msg.MoveTurtleFeedback()
        result = turtle_scripter.msg.MoveTurtleResult()
        script_path = goal.script_path
        
        # read script file line-by-line
        file = open(script_path)
        lines = file.readlines()

        # parse information into their own variables, store in instructions queue
        self.instruct_queue = []
        for line in lines:
            self.instruct_queue.append(Instruction(line))
