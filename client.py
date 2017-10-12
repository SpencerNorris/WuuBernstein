#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
Description: Script for Wuu-Bernstein client.
'''

import sys

@app.route("/client")
def client():
    #Command functions
    def tweet() :
        print "Tweeting..."
        #pass

    def show() :
        print "Showing..."
        #pass

    def block():
        print "Blocking..."
        #pass

    def unblock():
        print "Unblocking..."
        #pass
    
    command = {
                'tweet': tweet,
                'show': show,
                'block': block,
                'unblock': unblock,
            }

    VALID_COMMANDS = ['view', 'tweet', 'block', 'unblock', 'exit']
    while(1):
        input_var = raw_input("Enter a command: ")
        if not input_var.lower() in VALID_COMMANDS:
            print("Invalid command!\n")
            print input_var.lower()
            continue
        elif input_var.lower() == 'exit':
            break
        else:
            command[input_var.lower()]()
        return 0

if __name__ == '__main__':
    #app.run()
    sys.exit(client())
