from config import DEVOPS_TOOLS
from app.pkgs.devops.gitlab_tools import get_file_content as gitlab_get_file_content
from app.pkgs.devops.local_tools import get_file_content as local_get_file_content
from app.pkgs.devops.gitlab_tools import trigger_pipeline as gitlab_trigger_pipeline
from app.pkgs.devops.local_tools import trigger_pipeline as local_trigger_pipeline


def get_file_content(file_path, branch_name, repopath):
    try: 
        if DEVOPS_TOOLS == 'local':
            return local_get_file_content(file_path, branch_name, repopath)
        elif DEVOPS_TOOLS == 'gitlab':
            return gitlab_get_file_content(file_path, branch_name, repopath)
    except Exception as e:
        return False, ""

def trigger_pipeline(branch_name, repopath):
    try: 
        if DEVOPS_TOOLS == 'local':
            return local_trigger_pipeline(branch_name, repopath)
        elif DEVOPS_TOOLS == 'gitlab':
            return gitlab_trigger_pipeline(branch_name, repopath)
    except Exception as e:
        return False, ""