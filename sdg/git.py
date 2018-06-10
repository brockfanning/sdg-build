# -*- coding: utf-8 -*-
"""
Functions for interacting with the git repository

@author: dashton
"""

import re
import os
# None-standard library
import git
# Local modules
from sdg.path import input_path  # local package

# %% Faster but not using right now
# 
# def get_last_update(obj, repo):
#     commit = next(repo.iter_commits(paths=obj.path, max_count=1))
#     git_date = str(commit.committed_datetime.date())
#     return {'file': obj.path, 'sha':commit.hexsha, 'date': git_date}
# 
# repo = git.Repo("data", search_parent_directories=True) 
# tree = repo.tree()
# 
# %time git_update = [get_last_update(obj, repo) for obj in tree['data']]
# 
# %% Get file updates


def get_git_update(inid, ftype, src_dir=''):
    """Change into the working directory of the file (it might be a submodule)
    and get the latest git history"""
    f = input_path(inid, ftype=ftype, src_dir=src_dir)
    f_dir, f_name = os.path.split(f)
    
    repo = git.Repo(f_dir, search_parent_directories=True)
    # Need to translate relative to the repo root (this may be a submodule)
    repo_dir = os.path.relpath(repo.working_dir, os.getcwd())
    f = os.path.relpath(f, repo_dir)
    
    commit = next(repo.iter_commits(paths=f, max_count=1))
    git_date = str(commit.committed_datetime.date())
    git_sha = commit.hexsha
    # Turn the remote URL into a commit URL
    remote = repo.remote().url
    remote_bare = re.sub('^.*github\.com(:|\/)', '', remote).replace('.git','')
    commit_url = 'https://github.com/'+remote_bare+'/commit/'+git_sha
    
    return {'date': git_date,
            'sha': git_sha,
            'file': f,
            'id': inid,
            'commit_url': commit_url}
 



def get_git_updates(inid, src_dir=''):
    """
    
    Args:
        inid: str. The id of the indicator in short form. e.g. '2-1-2'.
        src_dir: str. Project root directory
        
    Returns:
        A dict with the required metadata fields
    """
    meta_update = get_git_update(inid=inid, ftype='meta', src_dir=src_dir)
    data_update = get_git_update(inid=inid, ftype='data-wide', src_dir=src_dir)
    
    return {'national_data_update_url_text': data_update['date'] + ': see changes on GitHub',
            'national_data_update_url': data_update['commit_url'],
            'national_metadata_update_url_text': meta_update['date'] + ': see changes on GitHub',
            'national_metadata_update_url': meta_update['commit_url']
            }
