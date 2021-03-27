from .constants import get_config

GROUP1 = get_config('LISTBOX/group1')
GROUP2 = get_config('LISTBOX/group2')

# CLASS1 = get_config('LISTBOX/class1')
# CLASS2 = get_config('LISTBOX/class2')

TASK_NAME = get_config('Class_Mapping/task_name')
CLASS_NAME = get_config('Class_Mapping/class_name')

def SH_NAME(id):
    return get_config('GROUP/group%d'%id)[0]