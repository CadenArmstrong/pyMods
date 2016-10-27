# Author: Caden Armstrong
# PyMods
# A python tool for working with islandora CRUD and MODS

from subprocess import call
import glob

def fetch_pids(namespace=None,collection=None,content_model=None,dsid=None,withdsid=True,solr=None):
    """ Fetch the pids of stuff"""

    call_list = ["drush","islandora_datastream_crud_fetch_fids","--user=admin"]

    if namespace is not None:
        call_list.append("--namespace="+namespace)
    if collection is not None:
        call_list.append("--collection="+collection)
    if content_model is not None:
        call_list.append("--content_model="+content_model)
    if dsid is not None:
        if withdsid:
            call_list.append("--with_dsid="+dsid)
        else:
            call_list.append("--without_dsid="+dsid)
    if solr is not None:
        call_list.append("--namespace="+namespace)

    call(call_list) 

def fetch_mods(pid_path,dest):
    """ Fetch the mods files given a list of pids"""

    call_list = ["drush","islandora_datastream_crud_fetch_datastreams","--user=admin","--pid_file="+pid_path,"--dsid=MODS","--datastreams_directory="+dest]
    call(call_list)


def modify_mods(mods_directory):
    """ Modifies the mods files"""
    
    files = glob.glob(mods_directory+"/*")
    for f in files:
        with open(f) as curfile:
            # Mods editing goes here
            pass

def push_mods(mods_files):
    """ Pushes modified mods files""" 

    call_list = ["drush","islandora_datastream_crud_push_datastream","--user=admin","--datastream_mimetype=application/xml","--datastreams_source_directory="+mods_files,"--datastreams_crud_log=/tmp/crud.log"]
