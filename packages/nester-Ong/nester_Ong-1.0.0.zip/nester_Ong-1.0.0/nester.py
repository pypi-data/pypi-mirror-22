# -*- coding: cp936 -*-

"""���ǵ�һ����ҵ�����ڶ����б�ĵ���������ȡ"""

def print_m(the_list):
        for item in the_list:
                if isinstance(item,list):
                        print_m(item)
                else:
                        print(item)

