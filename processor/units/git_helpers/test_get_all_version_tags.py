#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_get_all_version_tags(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_test_src}

        {step} tag_sort    
        {cmd}
        _out:['1.0.0', '1.1.0', '1.2.1', '2.0.0', '2.1.0', '3.0.0', '3.1.0']

        {step} tag_sort_index    
        {cmd}
        _out:[4, 1, 0, 3, 6, 5, 2]

        {step} get_all_version_tags
        git tag v1.2.1    
        git tag v1.12.1
        git tag    
        {cmd}
        _out:['1.2.1', '1.12.1']
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    arr_test=['1.2.1', '1.1.0', '3.1.0', '2.0.0', '1.0.0', '3.0.0', '2.1.0']
    if sys.argv[1] == "tag_sort":
        from git_helpers.get_all_version_tags import tag_sort
        print(tag_sort(arr_test))

    elif sys.argv[1] == "tag_sort_index":
        from git_helpers.get_all_version_tags import tag_sort_index
        print(tag_sort_index(arr_test))

    elif sys.argv[1] == "get_all_version_tags":
        from git_helpers.get_all_version_tags import get_all_version_tags
        print(get_all_version_tags())
  
