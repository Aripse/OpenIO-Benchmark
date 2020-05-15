# importing libraries
import subprocess
import sys


# a function to 'openio cluster list' command
def list_openio_cluster_ist():
    cmd_cluster_list = "openio cluster list"

    # using the Popen function to execute the command and store the result in temp.
    # it returns a tuple that contains the  data and the error if any.
    temp = subprocess.Popen(cmd_cluster_list.split(), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding="utf8")
    # we use the communicate function to fetch the output
    cluster_list_data, error_cluster_list= temp.communicate(input=None, timeout=None)
    result_list = []
    result_list = cluster_list_data.split('\n')

    result_list.pop(0)
    types = result_list.pop(0)
    tmp = types.split('|')
    tags = list()
    for i in tmp[1:-1]:
        tags.append(i.replace(" ", ""))

    columns = list()
    displays = list()
    for line in result_list[1:-2]:
        columns = line.replace(" ", "").split('|')

        columns.pop(0)
        columns.pop(-1)
        tmp = list()
        for i in range(len(tags)):
            tmp.append("{}={}".format(tags[i], columns[i]))
        displays.append(tmp)
    for elt in range(len(displays)):
        print(','.join(displays[elt]))

def verify_all_processes_are_up_and_running():
    gridinit_cmd_status = "gridinit_cmd status"

    # using the Popen function to execute the command and store the result in temp.
    # it returns a tuple that contains the  data and the error if any.
    status_output = subprocess.Popen(gridinit_cmd_status.split(), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, encoding="utf8")
    # we use the communicate function to fetch the output
    status_output_data, status_output_error_= status_output.communicate(input=None, timeout=None)

    result_list_status = list()
    result_list_status = status_output_data.split('\n')

    tags_status = list()
    tags_status = result_list_status.pop(0)
    # remove multiple spaces in the  columns header and split bye the remaining(only one) character space
    tags_status = ' '.join(tags_status.split()).split(" ")

    columns_status = list()
    displays_status = list()
    for line in result_list_status[0:-1]:
        columns_status = ' '.join(line.split()).split(" ")

        tmp = list()
        for i in range(len(tags_status)):
            tmp.append("{}={}".format(tags_status[i], columns_status[i]))
        displays_status.append(tmp)
    for elt in range(len(displays_status)):
        print(','.join(displays_status[elt]))


list_openio_cluster_ist()
print()
verify_all_processes_are_up_and_running()