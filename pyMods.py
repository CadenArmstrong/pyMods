# Author: Caden Armstrong
# PyMods
# A python tool for working with islandora CRUD and MODS

from subprocess import call
import glob
import xml.etree.ElementTree as ET # phones home

def fetch_pids(dest, namespace=None,collection=None,content_model=None,dsid=None,withdsid=True,solr=None):
    """ dest->(String) full path to plain text file where pids will be stored
        namespace->(String) namespace to search
        collection->(String) collection to search
        content_model->(String) content model to search
        dsid->(String) id of a datastream
        withdsid->(Boolean) true=with disd, false=cannot have dsid
        solr->(String) a solr query to search with
        
        This function uses the CRUD to perform a search and return the pids of islandora objects.
        If multiple search options are chosen, they are AND operated together."""

    call_list = ["drush","islandora_datastream_crud_fetch_pids","--user=admin", "--pid_file="+dest]

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
    print(call_list)
    call(call_list) 

def fetch_mods(pid_path,dest):
    """ pid_path->(String) full path to the pids file
        dest->(String) destination to fetch the datastreams to.

        
        Fetch the mods files given a list of pids"""

    call_list = ["drush","islandora_datastream_crud_fetch_datastreams","--user=admin","--pid_file="+pid_path,"--dsid=MODS","--datastreams_directory="+dest]
    call(call_list)


def modify_mods(mods_directory,backup=None):
    """ mods_directory->(String) path to directory containing new MODS files
        backup->(boolean) directory to copy original MODS files to
        
        modifies the MODS records
        """
    
    if backup is not None:
        backup_call = ["cp",mods_directory,backup]
        call(backup_call)
    files = glob.glob(mods_directory+"/*")
    for f in files:
        tree = ET.parse(f)
        root = tree.getroot()
        for child in root:
            if "abstract" in child.tag:
                child.text = "Caden's test text"
        tree.write(f)

def push_mods(mods_files):
    """ mods_files->(string) directory containing modified MODS files
        
        Pushes modified mods files to islandora""" 

    call_list = ["drush","islandora_datastream_crud_push_datastreams","--user=admin","--datastreams_mimetype=application/xml","--datastreams_source_directory="+mods_files,"--datastreams_crud_log=/tmp/crud.log"]
    call(call_list)

if __name__ == "__main__":

    pid_location = "/home/vagrant/test1pids.txt"
    mods_location = "/home/vagrant/testdir"
    collection = "islandora:test3"
    fetch_pids(pid_location,collection=collection)
    fetch_mods(pid_location,mods_location)
    modify_mods(mods_location)
    push_mods(mods_location)
