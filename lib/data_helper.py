# coding=utf-8
import codecs
import logging
import tensorflow as tf
import gzip
import json
import numpy as np
import os


# 从文件中读取问题集合
# 返回句子和标签
def read_annotated_fb_data_train(file_name):
    line_list = []
    idx = 0
    entity1_list = []
    relation_list = []
    entity2_list = []
    question_list = []

    with codecs.open(file_name, mode="r", encoding="utf-8") as read_file:
        try:
            for line in read_file.readlines():
                idx += 1
                line_seg = line.split('\t')
                # www.freebase.com/m/04whkz5
                entity1 = line_seg[0].split('/')[2]
                relation1 = line_seg[1].replace("www.freebase.com/", "")
                entity2 = line_seg[2].split('/')[2]
                question = line_seg[3].replace("\r\n", "")

                entity1_list.append(entity1)
                relation_list.append(relation1)
                entity2_list.append(entity2)
                question_list.append(question)
                # check it
                line_list.append(line)
        except Exception as e:
            print("index = ", idx)
            logging.error("error ", e)
    logging.info("load embedding finish!")
    return entity1_list, relation_list, entity2_list, question_list


class free_base:
    entitys = []

    def init_fb(self, file_name="../data/freebase/freebase_entity.txt"):
        with codecs.open(file_name, mode="r", encoding="utf-8") as read_file:
            for line in read_file.readlines():
                self.entitys.append(line.replace("\r\n", ""))

    def find_fb_by_id(self, id):
        exist = False

        for e1 in self.entitys:

            if str(e1) == str(id):
                exist = True
                print(e1, id)
        return exist


def read_fb(entity_name):
    file_name = "../data/freebase/freebase_entity.txt"
    return


# 从文件中压缩包中读取指定的entity
def find_fb_by_id2(entity_name):
    print("-->entity_name")
    file_name = "../data/freebase/freebase_entity.txt"
    print(file_name)
    lines = []
    with codecs.open(file_name, mode="r", encoding="utf-8") as read_file:
        for line in read_file.readlines():
            lines.append(line)

    return


def test1():
    # read_files("../data/sq/annotated_fb_data_train-1.txt")
    # read_fb("1111.json")

    fb1 = free_base()
    fb1.init_fb()
    print(fb1.entitys.__len__())
    r = fb1.find_fb_by_id("012_0k9")
    print(r)

    return

# =======================================================================simple questions
def test2():
    d = DataClass()
    d.init_simple_questions()

def read_file(file_name):
    """
    读取文件返回行的list
    :param file_name:
    :return:
    """
    idx = 0
    lines = []
    with codecs.open(file_name, mode="r", encoding="utf-8") as file:
        try:
            for line in file.readlines():
                idx += 1
                lines.append(line)
        except Exception as e:
            print("index = ", idx)
            logging.error("error ", e)
    return lines


class DataClass:

    train_path = "../data/sq/annotated_fb_data_train-1.txt"
    entity1_list = [] # id
    entity1_value_list = [] # 值
    relation_list = []
    entity2_list = []
    question_list = []
    fb = []

    def __init__(self):

        print(1)

    def init_simple_questions(self):
        """
        TODO: 需要给出entity1_list的具体text，暂时不需要
        :return:
        """
        self.entity1_list, self.relation_list, self.entity2_list, self.question_list =\
            read_annotated_fb_data_train(self.train_path)
        # length = len(entity1_list)
        # for index in range(1,length):
        #     entity1_list[index]
        # for e in self.entity1_list:
        #     ok,result = self.fb.find_fb_by_id(e)





    def init_freebase(self):
        self.fb = free_base()

    def convert2embedding(self,input_data,VOCAB_SIZE,HIDDEN_SIZE):
        embedding = tf.get_variable("embedding", [VOCAB_SIZE, HIDDEN_SIZE])
        # 原本的batch_size*num_steps个单词ID
        # 转为单词向量，转化后输入层维度是batch_size*num_steps*hidden_size
        inputs = tf.nn.embedding_lookup(embedding, input_data)
        return inputs


def train_batch_iter(data,batch_size):
    """
    获得batch_size个样本以及他们的label
    :param data:数据源
    :param batch_size:样本个数
    :return: x = []  # [[一个question],[]]
              y = []  # label [[e1,r,e2],] e1,e2是实体，r是关系
    """
    x = []  # [[一个question],[]]
    y = []  # label [[e1,r,e2],] e1,e2是实体，r是关系



    return x, y


if __name__ == "__main__":
    test2()
