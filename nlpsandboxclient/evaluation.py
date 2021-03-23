#!/usr/bin/env python3
# Author: Yao Yan
# Description: This script is used to evaluate the annotation by participants
# with gold standards, we will conduct the evaluation based on subcategory:
# date, person name,physical address

from abc import ABCMeta
import json
import os
import re


# take as input the location of
class Evaluation(metaclass=ABCMeta):
    """Evaluate the different types"""
    evaluation_type = None
    annotation = None
    col = None

    def __init__(self):
        self.gs_dict_seq = dict()
        self.sys_dict_seq = dict()
        self.gs_dict_token = dict()
        self.sys_dict_token = dict()
        self.loc_list = list()
        self.type_list = list()
        # noAddressType to check if participants' submission include "addressType", default is True, no addressType
        self.noAddressType = True

    def convert_annotations(self, annotations):
        if self.evaluation_type == "date":
            annotation_key = "date_annotations"
            post_path = "textDateAnnotations"
        elif self.evaluation_type == "person":
            annotation_key = "person_name_annotations"
            post_path = "textPersonNameAnnotations"
        elif self.evaluation_type == "address":
            annotation_key = "physical_location_annotations"
            post_path = "textPhysicalAddressAnnotations"
        else:
            raise ValueError("Must specify evaluation_type attribute")

        all_annotations = []
        for annotation in annotations:
            # print(annotation)
            noteid = annotation['annotationSource']['resourceSource']['name']
            for annots in annotation[post_path]:
                annots['noteId'] = os.path.basename(noteid)
                all_annotations.append(annots)

        new_annotations = {annotation_key: all_annotations}
        return new_annotations

    def convert_dict(self, sys_file, gs_file):
        with open(gs_file) as f:
            gs = json.load(f)
            gs = self.convert_annotations(gs)
            gs = gs[self.col]
        with open(sys_file) as f:
            sys = json.load(f)
            sys = self.convert_annotations(sys)
            sys = sys[self.col]

        self.sys_dict_seq = self.json_dict_seq(sys)
        self.gs_dict_seq = self.json_dict_seq(gs)
        self.sys_dict_token = self.json_dict_token(sys)
        self.gs_dict_token = self.json_dict_token(gs)

    # load the json file and convert it to a untokenised dictionary
    # with key 'noteId-start-length'
    # with value ["text"(untokened),"dateFormat"]
    def json_dict_seq(self, input):
        json_dict = {}
        for anno in input:
            noteId = anno['noteId']
            start = anno['start']
            data_loc = '{}-{}'.format(noteId, start)
            text = anno['text']
            length = anno['length']
            # dateFormat, personType, addressType
            annotation_format = anno.get(self.annotation, float('nan'))
            date_list = [text, annotation_format, length]
            json_dict[data_loc] = date_list
        return json_dict

    # load the json file and convert it to a untokenised dictionary
    # with key 'noteId-start-length'
    # with value ["text"(untokened),"dateFormat","length"]

    def json_dict_token(self, input):
        json_dict = {}
        for anno in input:
            noteId = anno['noteId']
            start = anno['start']
            text = anno['text']
            # dateFormat, personType, addressType
            # is self.annotation(dateFormat, personType, addressType) not in the
            # JSON file, use float('nan')
            annotation_format = anno.get(self.annotation, float('nan'))
            sub_text = re.split(r'\s+', text)
            for sub in sub_text:
                leng = len(sub)
                data_loc = '{}-{}-{}'.format(noteId, start, leng)
                start = start + leng + 1
                # [text, dateFormat,length]
                date_list = [sub, annotation_format, leng]
                json_dict[data_loc] = date_list
        return json_dict

    def eval(self):
        self.eval_category_instance()
        self.eval_category_token()
        final_address_eval = dict()
        final_address_eval[f"{self.evaluation_type}_location"] = self.loc_list
        final_address_eval[f"{self.evaluation_type}_type"] = self.type_list
        # print(final_address_eval)
        # expected json object for date
        # address_loc={
        #       "metric": “F1”/“precision”/“recall”,
        #       "value" (double): 0.89,
        #       "type":  “instance”/“token”
        #       "mode": “strict”/“relax”
        #       }
        # address_type={
        #       "metric": “F1”/“precision”/“recall”,
        #       "value" (double): 0.89
        #       }

        # calculate true positive

        # instance based_eval
        return final_address_eval

    # strict: length match, relax: length match +/- 2
    def eval_category_instance(self):
        sys_dict = self.sys_dict_seq
        gs_dict = self.gs_dict_seq
        tp = 0
        fp = 0
        fn = 0
        for key in sys_dict.keys():
            if key in gs_dict.keys() and self.relax_cond(key, sys_dict, gs_dict):
                tp = tp + 1
            else:
                fp = fp + 1
        for key in gs_dict.keys():
            if key not in sys_dict.keys() or \
                    (key in sys_dict.keys() and not self.relax_cond(key, sys_dict, gs_dict)):
                fn = fn + 1
        self.print_out(tp, fp, fn, "instance", "relax")
        # strict
        tp = 0
        fp = 0
        fn = 0
        for key in sys_dict.keys():
            if key in gs_dict.keys() and self.strict_cond(key, sys_dict, gs_dict):
                tp = tp + 1
            else:
                fp = fp + 1
        for key in gs_dict.keys():
            if (key not in sys_dict.keys())\
                    or (key in sys_dict.keys() and not self.strict_cond(key, sys_dict, gs_dict)):
                fn = fn + 1
        self.print_out(tp, fp, fn, "instance", "strict")
        # data format, instance
        tp = 0
        fp = 0
        fn = 0
        for key in sys_dict.keys():
            if type(sys_dict[key][1]) == str and len(sys_dict[key][1]) != 0:
                self.noAddressType = False
            if key in gs_dict.keys() and self.format_cond(key, sys_dict, gs_dict):
                tp = tp + 1
            else:
                fp = fp + 1
        for key in gs_dict.keys():
            if key not in sys_dict.keys() or \
                    (key in sys_dict.keys() and not self.format_cond(key, sys_dict, gs_dict)):
                fn = fn + 1
        self.print_out(tp, fp, fn, self.evaluation_type, "strict")
        self.noAddressType = True

    def relax_cond(self, key, sys_dict, gs_dict):
        return abs(sys_dict[key][2]-gs_dict[key][2]) <= 2

    def strict_cond(self, key, sys_dict, gs_dict):
        return abs(sys_dict[key][2]-gs_dict[key][2]) == 0

    def format_cond(self, key, sys_dict, gs_dict):
        return (sys_dict[key][1] == gs_dict[key][1]) and abs(sys_dict[key][2] - gs_dict[key][2]) == 0

    def eval_category_token(self):
        # relax
        sys_dict = self.sys_dict_token
        gs_dict = self.gs_dict_token
        tp = 0
        fp = 0
        fn = 0
        for key in sys_dict.keys():
            if key in gs_dict.keys() and self.strict_cond(key, sys_dict, gs_dict):
                tp = tp + 1
            else:
                fp = fp + 1
        for key in gs_dict.keys():
            if key not in sys_dict.keys() or \
                    (key in sys_dict.keys() and not self.strict_cond(key, sys_dict, gs_dict)):
                fn = fn + 1
        self.print_out(tp, fp, fn, "token", "strict")

    def print_out(self, tp, fp, fn, type_up, type_lower):
        if (type_up == "date" or type_up == "person") or \
         (type_up == "address" and self.noAddressType is True):
            precision = float('nan')
            recall = float('nan')
            F1 = float('nan')
        else:
            # precision (P): TP / (TP + FP)
            # Recall (R): TP / (TP + FN)
            # F1 score: 2 * ((P * R) / (P + R))
            if tp + fp == 0:
                precision = 0
            else:
                precision = round(tp / (tp + fp), 2)
            if tp + fn == 0:
                recall = 0
            else:
                recall = round(tp / (tp + fn), 2)
            if precision + recall == 0:
                F1 = 0
            else:
                F1 = round(2 * ((precision * recall) / (precision + recall)), 2)
        # print("F1 {}".format(F1))
        # print(type_up,type_lower)
        # print("tp: {},fp: {},fn: {}".format(tp,fp,fn))
        str_fmt = "{:<25}{:<15}{:<15}{:<20}"

        print(str_fmt.format(type_up, "F1", "Precision", "Recall"))

        print("{:-<25}{:-<15}{:-<15}{:-<20}".format("", "", "", ""))

        print(str_fmt.format(type_lower, F1,
                             precision,
                             recall))

        print("\n")
        eval_dict = {"F1": F1, "precision": precision, "recall": recall}
        # loc_map = dict()
        # type_map = dict()
        if type_up != self.evaluation_type:
            for key in eval_dict.keys():
                loc_map = {"metric": key,
                           "value": eval_dict[key],
                           "type": type_up,
                           "mode": type_lower}
                self.loc_list.append(loc_map)
        else:
            for key in eval_dict.keys():
                type_map = {"metric": key,
                            "value": eval_dict[key]}
                self.type_list.append(type_map)


class DateEvaluation(Evaluation):
    evaluation_type = "date"
    annotation = "dateFormat"
    col = "date_annotations"


class PersonNameEvaluation(Evaluation):
    evaluation_type = "person"
    annotation = "personType"
    col = "person_name_annotations"


class PhysicalAddressEvaluation(Evaluation):
    evaluation_type = "address"
    annotation = "addressType"
    col = "physical_location_annotations"
