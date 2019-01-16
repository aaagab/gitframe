#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_tags_commits(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "commit": "git commit --allow-empty -m 'empty'",
        "clean_compare": "git checkout develop; git reset --hard start_develop; git branch -D test",
        "direpa_task_conf": conf["direpa_task_conf"]
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} Hello
        {commit}
        git tag commit1
        git push origin commit1
        {commit}
        git tag commit2
        git push origin commit2
        {commit}
        git tag -a commit3 -m "commit3"
        git push origin commit3
        {commit}
        git tag -a commit4 -m "commit4"
        git push origin commit4

        # git tag
        {cmd}
        _out:# Commit for commit1 on local
        _out:# Commit for commit1 on remote

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.tags_commits import Tags_commits

    commits_obj=Tags_commits("all")
    print(commits_obj.get_tag_commit("commit1", "local"))
    print(commits_obj.get_tag_commit("commit1", "remote"))
    