# coding=utf-8
import codecs
import logging
import tensorflow as tf
import gzip
import json
import numpy as np
import os
import lib.read_utils as read_utils
import random
from tensorflow.contrib import learn
import datetime
import lib.my_log as mylog

mylog.logger.info("test")


# 从文件中读取问题集合
# 返回句子和标签



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


def test1():
    # read_files("../data/sq/annotated_fb_data_train-1.txt")
    # read_fb("1111.json")

    fb1 = free_base()
    fb1.init_fb()
    print(fb1.entitys.__len__())
    r = fb1.find_fb_by_id("012_0k9")
    print(r)

    return


# ======================================================================common
# 直接从gzip中读取文本
def read_rdf_from_gzip(file_name=r"../data/freebase/100_classic_book_collection.json.gz"):
    g2 = ""
    try:
        with gzip.open(filename=file_name, mode="rt", encoding="utf-8") as g:
            gs = []
            for g1 in g:
                gs.append(str(g1))
            g2 = "".join(gs)
            # print(g2)
    except Exception as e1:
        mylog.logger.info(e1)
    return g2


# =======================================================================simple questions
def test2():
    d = DataClass("test")
    d.compare()
    # d = DataClass("debug")
    # e1 = d.find_entity("100_classic_book_collection"+".json.gz")
    # print(e1)
    # print(d.batch_iter(2))


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


# =======================================================================DataClass
class DataClass:
    # ---------------------freebase
    entitys = []
    relations = []
    # ---------------------DataClass
    train_path = "../data/simple_questions/annotated_fb_data_train-1.txt"
    entity1_list = []  # id
    entity1_value_list = []  # 值

    relation_list = []  # 单词版
    entity2_list = []
    question_list = []
    question_list_index = []  # 数字索引版
    relation_list_index = []

    train_question_list_index = []  # 数字索引版
    train_relation_list_index = []
    test_question_list_index = []  # 数字索引版
    test_relation_list_index = []

    fb = []

    # ----------------------分割数据，预处理，转换成index形式

    def get_split_list(self, sentence_list):
        """
        将句子列表的所有空格隔开的单词全部取出来
        :param sentence:
        :return:
        """
        q_words = []
        for q in sentence_list:
            # q = str(q).replace("\n\r", " ")
            q_words_list = q.split(" ")
            for word in q_words_list:
                q_words.append(word)
        return q_words

    def get_split_list_per_line(self, sentence_list):
        """
        将句子列表中的空格隔开的字符串改成以list形式
        :param sentence_list:
        :return:
        """
        all_stence = []
        for sentence in sentence_list:
            one_sentence = []
            # q = str(q).replace("\n\r", " ")
            q_words_list = sentence.split(" ")
            for word in q_words_list:
                one_sentence.append(word)
            all_stence.append(one_sentence)
        return all_stence

    def __init__(self,mode = "debug"):
        """
        mode = debug(1行数据调试);test(测试模式);small();

        :param mode:
        """
        # ---------------------初始化实体
        self.entity1_list = []
        self.relation_list = []
        self.entity2_list = []
        self.question_list = []
        if mode == "test":
            self.init_simple_questions(file_name="../data/simple_questions/annotated_fb_data_train.txt")
            # self.init_simple_questions(file_name="../data/simple_questions/annotated_fb_data_test.txt")
            # self.init_simple_questions(file_name="../data/simple_questions/annotated_fb_data_valid.txt")
            # self.init_fb("../data/freebase/")
        elif mode == "small":
            self.init_simple_questions(file_name="../data/simple_questions/annotated_fb_data_train-small.txt")
            self.init_fb("../data/freebase/")
        else:
            self.init_simple_questions(file_name="../data/simple_questions/annotated_fb_data_train-1.txt")
            self.init_fb("../data/freebase/")

        # 将问题和关系的字符串变成以空格隔开的一个单词的list

        # total_list = self.question_list + self.relation_list
        q_words = self.get_split_list(self.question_list)
        q_words.extend(self.get_split_list(self.relation_list))


        self.converter = read_utils.TextConverter(q_words)
        self.converter.save_to_file_raw(
            "../data/vocab/" + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + str(".txt"))
        # self.converter.save_to_file("model/converter.pkl")
        # print(self.converter)

        # 将问题/关系转换成index的系列表示
        self.max_document_length = max([len(x.split(" ")) for x in self.question_list])  # 获取单行的最大的长度
        # 预处理问题和关系使得他们的长度的固定的？LSTM应该不需要固定长度？

        self.question_list_split = self.get_split_list_per_line(self.question_list)
        self.relation_list_split = self.get_split_list_per_line(self.relation_list)
        for q_l_s in self.question_list_split:
            self.question_list_index.append(self.converter.text_to_arr_list(q_l_s))
        # self.relation_list_index = self.converter.text_to_arr(self.relation_list_split)
        for _ in self.relation_list_split:
            self.relation_list_index.append(self.converter.text_to_arr_list(_))
        # 第一版本先padding到max长度
        for s in self.question_list_index:
            padding = self.max_document_length - len(s)
            for index in range(padding):
                s.append(self.max_document_length - 1)  # 用最后一个单词 补齐
            s = np.array(s)
        for s in self.relation_list_index:
            padding = self.max_document_length - len(s)
            for index in range(padding):
                s.append(self.max_document_length - 1)  # 用最后一个单词 补齐
            s = np.array(s)
            # print(1)
        # 按比例分割训练和测试集
        rate = 0.8
        self.train_question_list_index, self.test_question_list_index = \
            self.cap_nums(self.question_list_index, rate)
        self.train_relation_list_index, self.test_relation_list_index = \
            self.cap_nums(self.relation_list_index, rate)
        print("init finish!")

    # ---------------------load_all_train_data
    def load_all_train_data(self):
        """

        :return:返回问题集合,答案集合（关系集合）
        """
        all_data = []

        return self.question_list, self.relation_list

    # ---------------------web questions

    def init_simple_questions(self, file_name):
        line_list = []
        idx = 0

        # www.freebase.com/m/04whkz5	www.freebase.com/book/written_work/subjects	www.freebase.com/m/01cj3p
        # what is the book e about
        with codecs.open(file_name, mode="r", encoding="utf-8") as read_file:
            try:
                for line in read_file.readlines():
                    idx += 1
                    line_seg = line.split('\t')
                    # www.freebase.com/m/04whkz5
                    entity1 = line_seg[0].split('/')[2]
                    relation1 = line_seg[1].replace("www.freebase.com/", "").replace("/", "_").replace("_", " ")
                    entity2 = line_seg[2].split('/')[2]
                    question = line_seg[3].replace("\r\n", "")

                    self.entity1_list.append(entity1)
                    self.relation_list.append(relation1)
                    self.entity2_list.append(entity2)
                    self.question_list.append(question)
                    # check it
                    line_list.append(line)
            except Exception as e:
                print("index = ", idx)
                logging.error("error ", e)
        logging.info("load embedding finish!")

    # ---------------------freebase
    def init_fb(self, file_name="../data/freebase/"):
        file_name1 = "freebase_entity.txt"
        file_name2 = "freebase_rdf.txt"
        file_name3 = "freebase_relation_clear.txt"
        # 装载entity_id
        with codecs.open(file_name+file_name1, mode="r", encoding="utf-8") as read_file:
            for line in read_file.readlines():
                self.entitys.append(line.replace("\n", "").replace("/m/",""))
        print("entitys len:"+str(len(self.entitys)))
        # 装载freebase的关系
        with codecs.open(file_name+file_name3, mode="r", encoding="utf-8") as read_file:
            for line in read_file.readlines():
                self.relations.append(line.replace("\n", "").replace("/"," ").replace("_"," "))
        print("relations len:" + str(len(self.relations)))

    def compare(self):
        # 寻找simple questions 不在freebase中的
        print("compare============e1")
        for e1 in self.entity1_list:
            if e1 not in self.entitys:
                print(e1)
                self.just_log("../data/simple_questions/entitys_not_in_fb.txt",e1)
        print("compare============r1")
        for e1 in self.relation_list:
            if e1 not in self.relations:
                self.just_log("../data/simple_questions/relations_not_in_fb.txt", e1)
        print("compare============")
    def init_relation_fb(self, file_name="../data/freebase/freebase_relation_clear.txt"):
        """
        从文件中加载所有的关系然后作为词汇的候选列表
        :return:
        """
        # self.relation_list
        with codecs.open(file_name, mode="r", encoding="utf-8") as read_file:
            for line in read_file.readlines():
                self.relation_list.append(line.replace("\r\n", ""))
                # print("init_relation_fb")

    # 根据entity_id获取entity
    def find_entity(self,entity_id):
        """
        从文件系统中获取实体
        :return:
        """
        file_path = r"D:\ZAIZHI\freebase-data\topic-json"
        file_txt = read_rdf_from_gzip(file_path+"\\"+entity_id)
        json_file = json.loads(file_txt)
        id = ""
        ps = []
        try:
            id = json_file["id"]
            property_list = json_file["property"]
            for p in property_list:
                ps.append(p)
        except Exception as e1:
            print("error ", e1)
        finally:
            return id, ps

    def get_relations_except_one(self,entity_id,ps_to_except):
        """
        获取除了指定关系外的所有关系
        :param entity_id:
        :param ps:
        :return:
        """
        id,ps=self.find_entity(entity_id)
        if id == "":
            return []
        ps_to_return = []
        for p in ps:
            if p not in ps_to_except:
                ps_to_return.append(p)
        return ps_to_return

    # 获取除了指定关系外的随机一个关系
    def get_one_relations_except_ps(self,entity_id,ps_to_except):
        """
        获取除了指定关系外的随机一个关系
        :param entity_id:
        :param ps:
        :return:
        """
        id,ps=self.find_entity(entity_id)
        if id == "":
            return []
        ps_to_return = []
        for p in ps:
            if p not in ps_to_except:
                ps_to_return.append(p)
        index = random.randint(0,len(ps_to_return)-1)
        return ps_to_return[index]

    def exist_in_fb_by_id(self, id):
        """
        是否存在freebase中
        :param id:
        :return:
        """
        exist = False
        for e1 in self.entitys:
            if str(e1) == str(id):
                exist = True
                print(e1, id)
        return exist
    # --------------------- 在annotated_fb_data_train等三个文件中找出所有的id然后去 entity_id里面找

    # --------------------生成batch
    def batch_iter(self, question_list_index, relation_list_index, batch_size=100):
        """
        生成指定batch_size的数据
        :param batch_size:
        :return:
        """
        x = question_list_index.copy()
        y = relation_list_index.copy()
        x_new = []
        y_new = []
        z_new = []
        length = len(x)
        shuffle_indices = np.random.permutation(np.arange(length))  # 打乱样本
        # print("shuffle_indices", str(shuffle_indices))
        total = 0
        for index in shuffle_indices:
            x_new.append(x[index])
            y_new.append(y[index])
            total += 1
            if total >= batch_size:
                break
        # 根据y 生成z，也就是错误的关系,当前先做1:1的比例
        # rate = 1
        r_si = reversed(shuffle_indices)
        r_si = list(r_si)
        # print(r_si)
        total = 0
        for index in r_si:
            z_new.append(y[index])
            total += 1
            if total >= batch_size:
                break
        print("len: " + str(len(x_new)) + "  " + str(len(y_new)) + " " + str(len(z_new)))

        return np.array(x_new), np.array(y_new), np.array(z_new)

    # --------------------按比例分割
    def cap_nums(self, y, rate=0.8):
        y = y.copy()
        y = np.array(y)
        s = 0
        total_len = len(y)
        total_index = total_len * rate + 1
        e = int(total_index)

        reverseIndex = int(total_len - total_index)
        # print(reverseIndex)
        # 正向截取
        # 逆向
        y1 = y[s:e]  # [ > s and <= e  ]
        # print(type(y1))

        y2 = y[:reverseIndex]

        # print(total_len)
        print("split into 2 " + str(len(y1)) + " " + str(len(y2)))
        return y1, y2
    def just_log(self,file_name,msg):
        f1_writer = codecs.open(file_name, mode="a", encoding="utf-8")
        f1_writer.write(msg + "\n")
        f1_writer.close()
        print(1)

# =======================================================================clear data
def clear_relation():
    print("-->clear_relation")
    file_name = "../data/freebase/freebase_relation.txt"
    print(file_name)
    lines = set()
    with codecs.open(file_name, mode="r", encoding="utf-8") as read_file:
        for line in read_file.readlines():
            line = line.strip()
            if line not in lines:
                lines.add(line)
            else:
                print("exist")
    f1_writer = codecs.open("../data/freebase/freebase_relation_clear.txt", mode="w", encoding="utf-8")
    for l in lines:
        f1_writer.write(l + "\n")
    f1_writer.close()
    print(1)


if __name__ == "__main__":
    test2()
    # clear_relation()
