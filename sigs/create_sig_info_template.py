import os

import yaml
import sys


def load_yaml(file_path):
    """
    load yaml
    :param file_path: yaml file path
    :return: content of yaml
    """
    with open(file_path, encoding="utf-8") as fp:
        try:
            content = yaml.load(fp.read(), Loader=yaml.Loader)
        except yaml.MarkedYAMLError as e:
            print(e)
            sys.exit(1)
    return content


def get_sig_owners_path(sig_name):
    cur_path = os.popen("pwd").read().replace("\n", "")
    sig_path = os.path.join(cur_path, sig_name)
    if not os.path.exists(sig_path):
        print("%s is not exist" % sig_path)
        sys.exit(1)
    owners_path = os.path.join(sig_path, "OWNERS")
    return sig_path, owners_path


def make_template_file_data_and_write(sig_name, sig_path, owners_path):
    content = {}
    content["name"] = sig_name
    content["description"] = "TO_BE_CLARIFIED"
    content["created_on"] = "2019-12-31"
    content["mailing_list"] = "TO_BE_CLARIFIED"
    content["meeting_url"] = "TO_BE_CLARIFIED"
    content["mature_level"] = "startup"
    content["mentors"] = [{"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED", "email": "TO_BE_CLARIFIED"}]

    # if sig_info.yaml exists
    if os.path.exists(os.path.join(sig_path, "sig-info.yaml")):
        sig_info_content = load_yaml(os.path.join(sig_path, "sig-info.yaml"))
        content["description"] = sig_info_content.get("description") if sig_info_content.get("description") else "TO_BE_CLARIFIED"
        content["meeting_url"] = sig_info_content.get("meeting_url") if sig_info_content.get("meeting_url") else "TO_BE_CLARIFIED"
        content["mailing_list"] = sig_info_content.get("mailing_list") if sig_info_content.get("mailing_list") else "TO_BE_CLARIFIED"

        mts_in_sig_info = []
        for i in sig_info_content.get("maintainers"):
            mts_in_sig_info.append(i["gitee_id"])

        v = []
        for m in decode_owners(owners_path):
            if m in mts_in_sig_info:
                for mr in sig_info_content.get("maintainers"):
                    if m == mr["gitee_id"]:
                        v.append({
                            "gitee_id": m, "name": mr.get("name") if mr.get("name") else "TO_BE_CLARIFIED",
                            "organization": mr.get("organization") if mr.get("organization") else "TO_BE_CLARIFIED",
                            "email": mr.get("email") if mr.get("email") else "TO_BE_CLARIFIED",
                        })
            else:
                v.append({"gitee_id": m, "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED",
                          "email": "TO_BE_CLARIFIED"})

        if len(v) == 0:
            content["maintainers"] = [
                {"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED",
                 "email": "TO_BE_CLARIFIED"}]
        else:
            content["maintainers"] = v

    else:
        v = []
        for m in decode_owners(owners_path):
            v.append({"gitee_id": m, "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED",
                      "email": "TO_BE_CLARIFIED"})

        if len(v) == 0:
            content["maintainers"] = [
                {"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED",
                 "email": "TO_BE_CLARIFIED"}]
        else:
            content["maintainers"] = v

    repos = []
    for root, dirs, files in os.walk(sig_path):
        if len(dirs) == 0:
            if len(files) == 0:
                break
            for f in files:
                if root.count("/") > 2 and f.endswith(".yaml"):
                    repos.append(root.split("/")[-2] + '/' + f.split(".yaml")[0])
                else:
                    continue
    if len(repos) == 0:
        content["repositories"] = [{"repo": ["example/repos1", "example/repos2"], "committers": [{"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED", "email": "TO_BE_CLARIFIED"}],
                                    "contributors": [{"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED", "email": "TO_BE_CLARIFIED"}],}, {"repo": ["example/repos1", "example/repos2"],}, ]
    else:
        content["repositories"] = [{"repo": repos, "committers": [{"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED", "email": "TO_BE_CLARIFIED"}],
                                    "contributors": [{"gitee_id": "--xxx--", "name": "TO_BE_CLARIFIED", "organization": "TO_BE_CLARIFIED", "email": "TO_BE_CLARIFIED"}], }]
    write_yaml_to_sig(sig_path, content)


def decode_owners(owners_path):
    if os.path.exists(owners_path):
        c = load_yaml(owners_path)
        return c["maintainers"]
    else:
        return []


def write_yaml_to_sig(dst_path, data):
    file_path = os.path.join(dst_path, "sig-info.yaml")
    with open(file_path, 'w', encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=yaml.Dumper, sort_keys=False)


# you can use "python3 create_single_siginfo.py sig_name(example: security)" to auto make a sig_info.yaml for a sig,
# make sure you trigger this command after you enter the "community/sigs" directory
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Required 1 parameters! The sig_name need to be transferred in sequence.')
        sys.exit(1)
    sig = sys.argv[1]
    s_path, o_path = get_sig_owners_path(sig)
    make_template_file_data_and_write(sig, s_path, o_path)

