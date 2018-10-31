#!/usr/bin/env python3
import sys
import git_helpers.git_utils as git
import utils.message as msg
import git_helpers.regex_obj as ro

# there is no support branch on releases that has the latest major
# There is only one support branch or none per major previous release
# if one support branch it must be on the latest release of previous major releases
# Support Branch name needs to be the same on local and remote

def find_related_tag_for_support_branch_name(regex_branch, all_version_tags):
    latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)
    
    found=False
    regex_release=ro.Version_regex()
    for release in latest_release_tags:
        regex_release.set_text(release)
        if regex_branch.major_minor == regex_release.major_minor:
            found=True
            break

    if not found:
        msg.user_error(
            "Support Branch name '"+regex_branch.text+"' does not contain tag from one of the latest releases '"+', '.join(latest_release_tags)+"' that matches both its Major and its Minor Number",
            "Please rename Support branch_name to match the tag of the latest release on one Major."    
        )
        sys.exit(1)
    else:
        regex_latest_release=ro.Version_regex(latest_release_tags[-1])

        # there is no support branch on releases that has the latest major
        if regex_latest_release.major_minor == regex_branch.major_minor:
            msg.user_error(
                "version.txt value in support branch '"+regex_branch.text+"' can't be equal to Latest release Major from '"+regex_latest_release.text+"'",
                "No support branch on latest major version is tolerated."
            )
            sys.exit(1)

    msg.dbg("success", sys._getframe().f_code.co_name)


def check_one_branch_support_max_per_major(regex_branches, all_version_tags):
    major_array=[]
    version_value_regex=ro.Version_regex()
    
    for i, version_value in enumerate(all_version_tags):
        version_value_regex.set_text(version_value)
        if i == 0:
            major_array.append(version_value_regex.major)
        else:
            found=False
            for maj in major_array:
                if maj == version_value_regex.major:
                    found=True
                    break

            if not found:
                major_array.append(version_value_regex.major)

    for maj in major_array:
        count=0
        for regex_branch in regex_branches:
            if regex_branch.type == "support":
                if regex_branch.major == maj:
                    count+=1

                if count > 1:
                    msg.user_error("There are "+str(count)+" support branches with major number '"+maj+"'")
                    sys.exit(1)

    msg.dbg("success", sys._getframe().f_code.co_name)
