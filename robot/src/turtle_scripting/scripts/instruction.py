#!/usr/bin/env python

class Instruction():
    '''
    define class to store an instruction's data as variables
    '''
    def __init__(self, instr):
        self.instr = instr
        self.pos_x = self.find_val("pos_x", "pos_y")
        self.pos_y = self.find_val("pos_y", "rot_x")
        self.rot_x = self.find_val("rot_x", "rot_y")
        self.rot_y = self.find_val("rot_y", "interval")
        self.interval = self.find_val("interval", "")
    
    def find_val(self, word1, word2):
        return float(self.instr[self.instr.find(word1)+len(word1)+1:self.instr.find(word2)-1])
    
    def __str__(self):
        return (str(self.pos_x) + ", " + str(self.pos_y) + ", " + str(self.rot_x) + ", " + str(self.rot_y) + ", " + str(self.interval))
