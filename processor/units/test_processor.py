#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_processor(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        'this_pass':"mock_pass",
        'new_cmd':conf["direpa_app"]+"/"+conf["filen_app"]+" "+conf["tmp"]["opt"]+" "+conf["diren_test"],
        'heredoc_var': "This is my var",
        'hello':"HeredocHelloVar",
        "block_user_input": """
            _out:Enter user name [q to quit]:
            _type:user_name
            _out:# local name set to "marty"
            _out:Enter user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
            _type:test@thistest.com:/srv/git/
        """   
    })

    set_task_steps(conf,"""
        # cmd with line space above does not need a description

        {info} {info} is for description
        {info} {step} set the parameters for {cmd} and also display step with number on launching test window and test window
        {info} {cmd} relaunch this script and execute the part stored in main, it takes his arguments from step
        {info} {dep} signifies that the next cmds needs another test to be uncommented to continue
        {info} line can be commented to ignore certain parts
        {info} '_output': wait for this output to be displayed in test window  
        {info} '_type': send keystroke to the test window
        {info} '_to_fail': when a cmd is failing it sends an error code if it is detected the individual test is stopped
        {info} if to fail is set then error code is ignored. And if a message is written after to fail, then the message is also display on the launching test window
        {info} '_time': default time is set in seconds in config/config.json and it allows to exit the test after a certain waiting time for the current cmd.
        {info} Sometimes the time needs to be increased for network command or long process, so you use the _time: tag
        {info} _time:15 for 15 seconds
        {info} _time:00:15:00 for 15 minutes

        {cmd}
        _out:no arguments for {cmd}

        {step} step divider
        {info} empty step with two parameters [step, divider]

        {step} ""step divider""
        {info} empty step with title, you need to surround {step} value with quotes

        {step} "step 'divider"
        {info} test with inserted single quote
        {cmd}

        {step} 'step "divider'
        {info} test with inserted double quote
        {cmd}

        {step} _here - sdf
        # {step} # ('_here - sdf
        {info} test with special symbol, they are avoid for parameters
        {cmd}

        {step}
        {info} empty step with no parameters

        {step} basic_prompt
        {info} when {step} is present on top of {cmd}, then {cmd} take his own parameter
        {info} then it calls the script with the parameters 
        {cmd}
        {info} the tree prompts above have been called by a block it is a variable place holder inside heredoc
        {info} it has the form of {block_...}, it allows to repeat block of commads that are set in set_task_vars
        {block_user_input}

        {step} using_sudo_pass
        {cmd}
        _out:test@thistest.com's password:
        _type:{this_pass}
        _out:test@thistest.com's password:
        _type:{this_pass}

        {step} failing command
        echo "failing command party"
        party
        _out:failing command party
        _fail:party does not exist, failure anticipated

        {step} test_var_heredoc
        {cmd}
        _out:Type Heredoc Var [q to quit]:
        _type:{heredoc_var}
        _out:{hello}{not_a_var}
        _out:{hello}
        _out:This test is executed after test_var_heredoc

        {step} test_depends_of
        {info} test depends of a previous command that needs to be activated
        {dep} test_var_heredoc
        {cmd}

        # {step} time
        # {cmd}
        # {info} time command force the test to wait at least the required time and it overrides the max time wait.
        # _out:# wait 3 seconds
        # _time:5
        # _out:# wait 20 seconds
        # _time:25
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    import utils.message as msg
    from utils.prompt import prompt
    import getpass
    import time

    argument=""
    if not len(sys.argv) > 1:
        print("no arguments for {cmd}")
    else:
        argument=sys.argv[1]

        # if remote and local_remote and local:
        if argument == "basic_prompt":
            prompt("Enter user name")
            msg.info("local name set to \"marty\"")
            prompt("Enter user email")
            msg.info("local email set to \"test@test.com\"")
            prompt("Enter origin repository")
            msg.info("Repository set to \"git@thisroot.com:/srv/git/\"")

        elif argument == "using_sudo_pass":
            getpass.getpass("test@thistest.com's password: ")
            getpass.getpass("test@thistest.com's password: ")

        elif argument == "test_var_heredoc":
            prompt("Type Heredoc Var")
            print("HeredocHelloVar{not_a_var}")
            print("HeredocHelloVar")

        elif argument == "test_depends_of":
            print("This test is executed after test_var_heredoc")

        elif argument == "time":
            seconds=3
            msg.info("wait "+str(seconds)+" seconds")
            time.sleep(seconds)
            msg.info("end wait "+str(seconds)+" seconds")
            seconds=20
            msg.info("wait "+str(seconds)+" seconds")
            time.sleep(seconds)
            msg.info("end wait "+str(seconds)+" seconds")
 