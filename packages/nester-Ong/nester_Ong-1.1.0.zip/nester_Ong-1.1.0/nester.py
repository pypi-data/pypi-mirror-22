# -*- coding: cp936 -*-

"""���ǵ�һ����ҵ�����ڶ����б�ĵ���������ȡ"""

def print_m(the_list,level):
        for item in the_list:
                if isinstance(item,list):
                        print_m(item,level+1)
                else:
                        for tab_stop in range(level):
                             print"\t",
                        print(item)

