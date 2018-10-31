#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_regex_obj(conf):
    set_test_steps(conf,"""
        {step} Regex_obj
        {cmd}
        _out:(^)(\d+)(\.)(\d+)(\.)(\d+)(\.)($)
        _out:['^', '\\\\d+', '\\\\.', '\\\\d+', '\\\\.', '\\\\d+', '\\\\.', '$']
        _out:^\d+\.\d+\.\d+\.$

        {step} Feature_regex empty_txt
        {cmd}
        _out:feature
        _out:(^)(feature)(-)(.+)($)
        _out:['^', 'feature', '-', '.+', '$']
        _out:^feature-.+$

        {step} Feature_regex with_txt
        {cmd}
        _out:feature
        _out:new_function

        {step} Master_regex
        {cmd}
        _out:master
        _out:^master$

        {step} Develop_regex
        {cmd}
        _out:develop
        _out:^develop$
        
        {step} Version_regex
        {cmd}
        _out:version
        _out:^\d+\.\d+\.\d+$
        _out:1
        _out:2
        _out:3
        _out:1.2
        
        {step} Release_regex
        {cmd}
        _out:release
        _out:^release-\d+?\.\d+?\.0$
        _out:1
        _out:2
        _out:1.2
        
        {step} Support_regex
        {cmd}
        _out:support
        _out:^support-\d+?\.\d+?\.X$
        _out:1
        _out:2
        _out:1.2
        
        {step} Hotfix_regex
        {cmd}
        _out:hotfix
        _out:^hotfix-\d+?\.\d+?\.X-.+$
        _out:1
        _out:2
        _out:1.2
        _out:my_repair

        {step} validate_branch_name
        {cmd}
        _out:master
        _out:develop
        _out:feature-new_function
        _out:release-1.0.0
        _out:support-1.0.X
        _out:hotfix-1.0.X-repair
        _out:× Branch 'test' type unknown.
        _fail:

        {step} get_branch_type
        {cmd}
        _out:master
        _out:develop
        _out:feature
        _out:release
        _out:support
        _out:hotfix
    """)

    test_processor(conf)


if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "src":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_script)

    if sys.argv[1] == "Regex_obj":
        from git_helpers.regex_obj import Regex_obj
        reg_obj=Regex_obj(r"(^)(\d+)(\.)(\d+)(\.)(\d+)(\.)($)")

        print(reg_obj.group_string)
        print(reg_obj.reg_arr)
        print(reg_obj.string)

    elif sys.argv[1] == "Feature_regex":
        from git_helpers.regex_obj import Feature_regex
        if sys.argv[2] == "empty_txt":
            obj_regex=Feature_regex()

            print(obj_regex.type)
            print(obj_regex.group_string)
            print(obj_regex.reg_arr)
            print(obj_regex.string)
        elif sys.argv[2] == "with_txt":
            obj_regex=Feature_regex("feature-new_function")
            print(obj_regex.type)
            print(obj_regex.keywords)
    elif sys.argv[1] == "Master_regex":
        from git_helpers.regex_obj import Master_regex
        obj_regex=Master_regex()
        print(obj_regex.type)
        print(obj_regex.string)
    elif sys.argv[1] == "Develop_regex":
        from git_helpers.regex_obj import Develop_regex
        obj_regex=Develop_regex()
        print(obj_regex.type)
        print(obj_regex.string)
    elif sys.argv[1] == "Version_regex":
        from git_helpers.regex_obj import Version_regex
        obj_regex=Version_regex("1.2.3")
        print(obj_regex.type)
        print(obj_regex.string)
        print(obj_regex.major)
        print(obj_regex.minor)
        print(obj_regex.patch)
        print(obj_regex.major_minor)
    elif sys.argv[1] == "Release_regex":
        from git_helpers.regex_obj import Release_regex
        obj_regex=Release_regex("release-1.2.0")
        print(obj_regex.type)
        print(obj_regex.string)
        print(obj_regex.major)
        print(obj_regex.minor)
        print(obj_regex.major_minor)
    elif sys.argv[1] == "Support_regex":
        from git_helpers.regex_obj import Support_regex
        obj_regex=Support_regex("support-1.2.X")
        print(obj_regex.type)
        print(obj_regex.string)
        print(obj_regex.major)
        print(obj_regex.minor)
        print(obj_regex.major_minor)
    elif sys.argv[1] == "Hotfix_regex":
        from git_helpers.regex_obj import Hotfix_regex
        obj_regex=Hotfix_regex("hotfix-1.2.X-my_repair")
        print(obj_regex.type)
        print(obj_regex.string)
        print(obj_regex.major)
        print(obj_regex.minor)
        print(obj_regex.major_minor)
        print(obj_regex.keywords)

    elif sys.argv[1] == "validate_branch_name":
        from git_helpers.regex_obj import get_element_regex
        print(get_element_regex('master').text)
        print(get_element_regex('develop').text)
        print(get_element_regex('feature-new_function').text)
        print(get_element_regex('release-1.0.0').text)
        print(get_element_regex('support-1.0.X').text)
        print(get_element_regex('hotfix-1.0.X-repair').text)
        print(get_element_regex('test').text)

    elif sys.argv[1] == "get_branch_type":
        from git_helpers.regex_obj import get_element_regex
        print(get_element_regex('master').type)
        print(get_element_regex('develop').type)
        print(get_element_regex('feature-new_function').type)
        print(get_element_regex('release-1.0.0').type)
        print(get_element_regex('support-1.0.X').type)
        print(get_element_regex('hotfix-1.0.X-repair').type)
        
    