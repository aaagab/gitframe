import re
import git_helpers.git_utils as git
import utils.message as msg
import sys

class Regex_obj():
    def __init__(self, group_string):
        self.type=""
        self.group_string=group_string
        self.reg_arr=group_string[1:-1].split(")(")
        self.string="".join(self.reg_arr)
        self.match=False

class Version_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(\d+)(\.)(\d+)(\.)(\d+)((-r)?)($)")
        self.type="version"
        self.tag_prefix="v"
        self.set_text(txt)

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            if self.matching_obj:
                self.match=True
                self.major=self.matching_obj.group(2)
                self.minor=self.matching_obj.group(4)
                self.patch=self.matching_obj.group(6)
                if self.matching_obj.group(7) == "-r":
                    self.recommended=True
                else:
                    self.recommended=False
                self.major_minor=self.major+"."+self.minor
                self.major_minor_patch=self.major_minor+"."+self.patch
                self.tag=self.tag_prefix+self.text
            else:
                self.match=False
                self.major=""
                self.minor=""
                self.patch=""
                self.major_minor=""
                self.tag=""
                self.recommended=""
        
        return self

    def set_text_if_tag_match(self, tag):
        if len(tag) > len(self.tag_prefix):
            if tag[:len(self.tag_prefix)] == self.tag_prefix:
                self.set_text(tag[len(self.tag_prefix):])
        return self

class Master_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(master)($)")
        self.type=self.reg_arr[1]
        self.set_text(txt)

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            self.location=""
            if self.matching_obj:
                self.match=True
            else:
                self.location=""
                self.match=False

        return self

class Develop_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(develop)($)")
        self.type=self.reg_arr[1]
        self.set_text(txt)
        self.location=""

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            if self.matching_obj:
                self.match=True
            else:
                self.location=""
                self.match=False

        return self

class Features_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(fts)(-)(.+)($)")
        self.type="features"
        self.set_text(txt)
        self.location=""
        self.abbrev=self.reg_arr[1]

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            if self.matching_obj:
                self.match=True
                self.keywords=self.matching_obj.group(4)
            else:
                self.location=""
                self.match=False
                self.keywords=""

        return self

class Draft_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(dft)(-)(.+)($)")
        self.type="draft"
        self.set_text(txt)
        self.location=""
        self.abbrev=self.reg_arr[1]

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            if self.matching_obj:
                self.match=True
                self.keywords=self.matching_obj.group(4)
            else:
                self.location=""
                self.match=False
                self.keywords=""

        return self

class Support_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(spt)(-)(\d+)(\.)(X)(\.)(X)($)")
        self.type="support"
        self.set_text(txt)
        self.location=""
        self.abbrev=self.reg_arr[1]

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            if self.matching_obj:
                self.match=True
                self.major=self.matching_obj.group(4)
            else:
                self.location=""
                self.match=False
                self.major=""

        return self

    def get_new_branch_name(self, major):
        return self.abbrev+"-"+major+".X.X"

class Hotfix_regex(Regex_obj):
    def __init__(self, txt=""):
        Regex_obj.__init__(self, r"(^)(hfx)(-)(\d+)(\.)(X)(\.)(X)(-)(.+)($)")
        self.type="hotfix"
        self.set_text(txt)
        self.location=""
        self.abbrev=self.reg_arr[1]

    def set_text(self, txt):
        if txt != "":
            self.text=txt
            self.matching_obj=re.match(self.group_string, txt)
            if self.matching_obj:
                self.match=True
                self.major=self.matching_obj.group(4)
                self.keywords=self.matching_obj.group(10)
            else:
                self.match=False
                self.major=""
                self.keywords=""
                self.tag=""

        return self

    def get_new_branch_name(self, major, keywords):
        return self.abbrev+"-"+major+".X.X-"+keywords.replace(" ","_")

def get_element_regex(branch_name=""):
    if not branch_name:
        branch_name=git.get_active_branch_name()

    regexes=get_all_branch_regex_classes(branch_name)

    for reg in regexes:
        if reg.match:
            return reg

    error_unknown_regex(regexes)
    
def error_unknown_regex(regexes):
    txt_regexes=""
    for reg in regexes:
        txt_regexes+="\t"+reg.string+"\n"

    msg.user_error(
        "Branch '"+regexes[0].text+"' type unknown.",
        "Authorized Branch Names are :\n"+txt_regexes
    )
    sys.exit(1)

def get_all_branch_regex_classes(branch_name=""):
    regexes=[]

    regexes.append(Master_regex(branch_name))
    regexes.append(Develop_regex(branch_name))
    regexes.append(Features_regex(branch_name))
    regexes.append(Support_regex(branch_name))
    regexes.append(Hotfix_regex(branch_name))
    regexes.append(Draft_regex(branch_name))

    return regexes

def copy_reg_branch_obj(reg_obj):
    regexes=get_all_branch_regex_classes()

    for reg in regexes:
        if reg.type == reg_obj.type:
            reg.set_text(reg_obj.text)
            return reg

    error_unknown_regex(regexes)
    