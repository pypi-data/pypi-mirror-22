# -*- coding: cp936 -*-

"""���ǵ�һ����ҵ�����ڶ����б�ĵ���������ȡ"""

def print_m(the_list,indent=False,level=0):
        for item in the_list:
                if isinstance(item,list):
                        print_m(item,indent,level+1)
                else:
                        if indent:
                          for tab_stop in range(level):
                             print"\t",
                        print(item)



