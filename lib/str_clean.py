# -*- coding: cp936 -*-
l = "��z11��"
l1 = l[1:len(l)-1]
print(l1)


def strQ2B(ustring):
    """ȫ��ת���"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # ȫ�ǿո�ֱ��ת��
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # ȫ���ַ������ո񣩸��ݹ�ϵת��
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """���תȫ��"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # ��ǿո�ֱ��ת��
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # ����ַ������ո񣩸��ݹ�ϵת��
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring


b = strQ2B("���123abc����԰��������~!����()<>��3213#@��#5345#%��#")
print(b)

c = strB2Q("���123abc����԰")
print(c)