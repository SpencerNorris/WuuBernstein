#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
Description: Script for Wuu-Bernstein client.
'''

import sys

def client():
    #Command functions
    def __tweet(message) :
        print "Tweeting..."
        print message
        #pass

    def __show() :
        print "Showing..."
        #pass

    def __block(message):
        print "Blocking..."
        print message
        #pass

    def __unblock(message):
        print "Unblocking..."
        print message
        #pass
    
    command = {
                'tweet': __tweet,
                'show': __show,
                'block': __block,
                'unblock': __unblock,
            }

    VALID_COMMANDS = ['view', 'tweet', 'block', 'unblock', 'exit']
    while(1):
        input_var = raw_input("Enter a command: ")
        endIndex=-1
        input_command = ""
        for i in range(len(input_var)) :
            if input_var[i] is ' ' :
                endIndex = i
                break
        if endIndex !=-1 :
            input_command = input_var[0:endIndex]
        else :
            input_command = input_var
        if not input_command.lower() in VALID_COMMANDS:
            print("Invalid command: " + input_command.lower() + "\n")
            continue
        elif input_command.lower() == 'exit':
            break
        else:
            if endIndex !=-1 :
                command[input_command.lower()](input_var[endIndex+1:])
            else : 
                command[input_command.lower()](input_var)
        return 0

if __name__ == '__main__':
    #app.run()
    sys.exit(client())
