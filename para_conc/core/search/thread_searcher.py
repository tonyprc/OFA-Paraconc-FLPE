#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Core concordancing thread
# Copyright (c) 2024 Tony Chang (42716403@qq.com)

import os, sys, time, json, pickle, re, copy
from PySide6.QtCore import Signal, Slot, QThread
from para_conc.core.search.search import SearchScope, SearchRequest, SearchResult, SearchResultItem, MatchResult, SearchMode
from para_conc.core.lemma_map import LEMMA_MAP

class SrcThread(QThread):
    result_signal = Signal(dict)
    pbar_signal = Signal([int, int]) 
    msg_m_signal = Signal(str)       
    output_window_signal = Signal([str, str, str])
    refresh_signal = Signal(list)    
    def __init__(self, corpora, req, scope):  
        super(SrcThread, self).__init__()
        self.en_lemma = LEMMA_MAP
        self.corpora = corpora
        self.req = req
        self.scope = scope
                
    def __del__(self):
        pass   
   
    def run (self):
        result = SearchResult()
        result.num_list = []
        result.lang_list = []
        result.sent_list = []
        idx_num = 1
        hit_words = 0
        hit_sents = 0               
        j = len(self.corpora)        
        self.pbar_signal.emit(0,j)
        time.sleep(2)
        T1 = time.perf_counter()        
        src_lang = 'zh'
        query, query_2 = self._build_reverse_query(self.req, self.req.mode)
        if self.detect_lang(self.req.q) == 'en':
            src_lang = 'en'
            query, query_2 = self._build_query(self.req, self.req.mode)
        if self.req.mode == SearchMode.REGEX:
            if self.scope.value == 1:
                self.msg_m_signal.emit(f"{j}份语料检索中，请稍候....")
                for f_num, (corp_path, corpus_id) in enumerate(self.corpora, start=1):
                    corpus = self.open_dat_file(corp_path)
                    ref_corpus = ""
                    if corpus.genre_en not in ["educational philosophy", "governance of china"]:
                        if src_lang == "zh":
                            self.msg_m_signal.emit(f"{corpus.title_zh}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_zh_tag(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        else:
                            self.msg_m_signal.emit(f"{corpus.title_en}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_en_tag(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        result.num_list.extend(num_list)
                        result.lang_list.extend(lang_list)
                        result.sent_list.extend(sent_list)
                        idx_num = idx_n
                        hit_words = hit_wds
                        hit_sents = hit_sts
                    else:
                        if corpus.genre_en in ["educational philosophy"]:
                            for corp in [corpus.info, corpus.contents]:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{corp.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{corp.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts                            
                            for art in corpus.preface.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts                                
                            for art in corpus.chapters.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts 
                            for art in corpus.annex.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts
                        if corpus.genre_en in ["governance of china"]:
                            for corp in [corpus.info, corpus.contents]:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{corp.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{corp.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts                            
                            for theme in corpus.themes:
                                for art in theme.articles:
                                    if src_lang == "zh":
                                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    else:
                                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    result.num_list.extend(num_list)
                                    result.lang_list.extend(lang_list)
                                    result.sent_list.extend(sent_list)
                                    idx_num = idx_n
                                    hit_words = hit_wds
                                    hit_sents = hit_sts
                            if corpus.annex:
                                for art in corpus.annex.articles:
                                    if src_lang == "zh":
                                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    else:
                                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    result.num_list.extend(num_list)
                                    result.lang_list.extend(lang_list)
                                    result.sent_list.extend(sent_list)
                                    idx_num = idx_n
                                    hit_words = hit_wds
                                    hit_sents = hit_sts 
                    self.pbar_signal.emit(f_num,j)
            if self.scope.value == 2:
                new_corpora = self.corpora[0]
                index_list = self.corpora[1]
                f_num = len(index_list)
                self.msg_m_signal.emit(f"{f_num}份语料检索中，请稍候....")
                for family in index_list:
                    if len(family.keys())== 1:
                        corp_root = family['0']
                        for corp in new_corpora:
                            if corp_root in corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corpus.type_en == "article":
                                    if src_lang == "zh":
                                        self.msg_m_signal.emit(f"{corpus.title_zh}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_zh_tag(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                    else:
                                        self.msg_m_signal.emit(f"{corpus.title_en}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_en_tag(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                    result.num_list.extend(num_list)
                                    result.lang_list.extend(lang_list)
                                    result.sent_list.extend(sent_list)
                                    idx_num = idx_n
                                    hit_words = hit_wds
                                    hit_sents = hit_sts
                                else:
                                    if corpus.genre_en in ["governance of china"]:
                                        for cp in [corpus.info, corpus.contents]:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{cp.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{cp.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for theme in corpus.themes:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                        if corpus.annex:
                                            for art in corpus.annex.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts 
                                    if corpus.genre_en in ["educational philosophy"]:
                                        for cp in [corpus.info, corpus.contents]:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{cp.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{cp.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for art in corpus.preface.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for art in corpus.chapters.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        if corpus.annex:
                                            for art in corpus.annex.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                    elif len(family.keys())== 2:
                        corp_root = family['0']
                        corp_child = family['1']
                        if corp_root not in ["UXEP", "GOC"]:
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    if corp_child == corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh_tag(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en_tag(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                        break
                        elif corp_root == "UXEP":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_child == "概况":
                                        art = corpus.info
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                        break
                                    if corp_child == "目录":
                                        art = corpus.contents
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                        break
                                    if corp_child == "导言":
                                        for art in corpus.preface.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        break
                                    if corp_child == "章节":
                                        for art in corpus.chapters.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        break
                                    if corp_child == "附录":
                                        for art in corpus.annex.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        break                                       
                        elif corp_root == "GOC":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    if corp_child == corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        for art in [corpus.info, corpus.contents]:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for theme in corpus.themes:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                        if corpus.annex:
                                            for art in corpus.annex.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                        break                                                
                        else:
                            pass                            
                    elif len(family.keys())== 3:
                        corp_root = family['0'] 
                        corp_pa = family['1']   
                        corp_id = family['2']   
                        if corp_root == "UXEP":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    art_num = corp_id.split("-")[0]
                                    if corp_pa == "章节":                                        
                                        for art in corpus.chapters.articles:                                            
                                            if art.num == art_num:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                                break
                                    if corp_pa == "附录": 
                                        for art in corpus.annex.articles:
                                            if art.num == art_num:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                                break
                                    break
                        if corp_root == "GOC":
                            for corp in new_corpora:
                                if corp_pa == corp[1]:                                    
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_id == "概况":                                        
                                        art = corpus.info
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                    if corp_id == "目录":
                                        art = corpus.contents
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                    if corp_id == "主题":
                                        for theme in corpus.themes:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                    if corp_id == "附录":
                                        for art in corpus.annex.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                    break
                    elif len(family.keys())== 4:
                        corp_root = family['0']   
                        corp_gpa = family['1']  
                        corp_pa = family['2']      
                        corp_id = family['3']      
                        corp_num = corp_id.split("-")[0]
                        for corp in new_corpora:
                            if corp_gpa == corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corp_pa == "主题":
                                    for theme in corpus.themes:
                                        if corp_num == theme.num:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                            break
                                if corp_pa == "附录":
                                    for art in corpus.annex.articles:
                                        if art.num == corp_num:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                            break
                                break                        
                    elif len(family.keys())== 5:
                        corp_root = family['0']   
                        corp_ggpa = family['1']       
                        corp_gpa = family['2']     
                        corp_pa = family['3']      
                        corp_id = family['4']        
                        theme_num = corp_pa.split("-")[0]
                        art_num = corp_id.split("-")[0]
                        for corp in new_corpora:
                            if corp_ggpa == corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corp_gpa == "主题":
                                    for theme in corpus.themes:
                                        if theme_num == theme.num:
                                            for art in theme.articles:
                                                if art_num  == art.num:
                                                    if src_lang == "zh":
                                                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                                  self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                    else:
                                                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                                  self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                    result.num_list.extend(num_list)
                                                    result.lang_list.extend(lang_list)
                                                    result.sent_list.extend(sent_list)
                                                    idx_num = idx_n
                                                    hit_words = hit_wds
                                                    hit_sents = hit_sts
                                                    break
                                        break
                            break                                    
                    else:
                        pass
                    self.pbar_signal.emit(f_num,j)  
            if self.scope.value == 3: 
                self.msg_m_signal.emit(f"1份语料检索中，请稍候....")
                corpus = self.corpora[0]
                art = self.corpora[1]
                ref_corpus = ""
                f_num = 1
                if not art:
                    if src_lang == "zh":
                        self.msg_m_signal.emit(f"{corpus.title_zh}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_zh_tag(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                    else:
                        self.msg_m_signal.emit(f"{corpus.title_en}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_en_tag(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                    result.num_list.extend(num_list)
                    result.lang_list.extend(lang_list)
                    result.sent_list.extend(sent_list)
                    idx_num = idx_n
                    hit_words = hit_wds
                    hit_sents = hit_sts
                else:
                    if src_lang == "zh":
                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                    else:
                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                    result.num_list.extend(num_list)
                    result.lang_list.extend(lang_list)
                    result.sent_list.extend(sent_list)
                    idx_num = idx_n
                    hit_words = hit_wds
                    hit_sents = hit_sts
                self.pbar_signal.emit(f_num,j)
            if self.scope.value == 4:
                self.msg_m_signal.emit(f"{j}份语料检索中，请稍候....")
                for f_num, (corp_path, corp_id) in enumerate(self.corpora, start=1):
                    corpus = self.open_dat_file(corp_path)
                    ref_corpus = ""
                    if corpus.genre_en not in ["educational philosophy", 'governance of china']:
                        if src_lang == "zh":
                            self.msg_m_signal.emit(f"{corpus.title_zh}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_zh_tag(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        else:
                            self.msg_m_signal.emit(f"{corpus.title_en}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_en_tag(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        result.num_list.extend(num_list)
                        result.lang_list.extend(lang_list)
                        result.sent_list.extend(sent_list)
                        idx_num = idx_n
                        hit_words = hit_wds
                        hit_sents = hit_sts
                    elif corpus.genre_en in ["educational philosophy"]:
                        for art in [corpus.info, corpus.contents]:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                        for art in corpus.preface.articles:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                        for art in corpus.chapters.articles:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                        for art in corpus.annex.articles:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                    elif corpus.genre_en in ["governance of china"]:
                        for corp in [corpus.info, corpus.contents]:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{corp.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh_tag(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{corp.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en_tag(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts                            
                        for theme in corpus.themes:
                            for art in theme.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts
                        if corpus.annex:
                            for art in corpus.annex.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en_tag(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts
                    else: pass
                    # endregion
                    self.pbar_signal.emit(f_num,j)
        else:
            if self.scope.value == 1:
                self.msg_m_signal.emit(f"{j}份语料检索中，请稍候....")
                for f_num, (corp_path, corpus_id) in enumerate(self.corpora, start=1):
                    corpus = self.open_dat_file(corp_path)
                    ref_corpus = ""
                    if corpus.genre_en not in ["educational philosophy", "governance of china"]:
                        if src_lang == "zh":
                            self.msg_m_signal.emit(f"{corpus.title_zh}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_zh(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        else:
                            self.msg_m_signal.emit(f"{corpus.title_en}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_en(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        result.num_list.extend(num_list)
                        result.lang_list.extend(lang_list)
                        result.sent_list.extend(sent_list)
                        idx_num = idx_n
                        hit_words = hit_wds
                        hit_sents = hit_sts
                    else:
                        if corpus.genre_en in ["educational philosophy"]:
                            for corp in [corpus.info, corpus.contents]:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{corp.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{corp.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts                            
                            for art in corpus.preface.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts                                
                            for art in corpus.chapters.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts 
                            for art in corpus.annex.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts
                        if corpus.genre_en in ["governance of china"]:
                            for corp in [corpus.info, corpus.contents]:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{corp.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{corp.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts                            
                            for theme in corpus.themes:
                                for art in theme.articles:
                                    if src_lang == "zh":
                                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    else:
                                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    result.num_list.extend(num_list)
                                    result.lang_list.extend(lang_list)
                                    result.sent_list.extend(sent_list)
                                    idx_num = idx_n
                                    hit_words = hit_wds
                                    hit_sents = hit_sts
                            if corpus.annex:
                                for art in corpus.annex.articles:
                                    if src_lang == "zh":
                                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    else:
                                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                    result.num_list.extend(num_list)
                                    result.lang_list.extend(lang_list)
                                    result.sent_list.extend(sent_list)
                                    idx_num = idx_n
                                    hit_words = hit_wds
                                    hit_sents = hit_sts 
                    self.pbar_signal.emit(f_num,j)
            if self.scope.value == 2:
                new_corpora = self.corpora[0]
                index_list = self.corpora[1]
                f_num = len(index_list)
                self.msg_m_signal.emit(f"{f_num}份语料检索中，请稍候....")
                for family in index_list:
                    if len(family.keys())== 1:
                        corp_root = family['0']
                        for corp in new_corpora:
                            if corp_root in corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corpus.type_en == "article":
                                    if src_lang == "zh":
                                        self.msg_m_signal.emit(f"{corpus.title_zh}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_zh(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                    else:
                                        self.msg_m_signal.emit(f"{corpus.title_en}")
                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                  self.para_concording_en(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                    result.num_list.extend(num_list)
                                    result.lang_list.extend(lang_list)
                                    result.sent_list.extend(sent_list)
                                    idx_num = idx_n
                                    hit_words = hit_wds
                                    hit_sents = hit_sts
                                else:
                                    if corpus.genre_en in ["governance of china"]:
                                        for cp in [corpus.info, corpus.contents]:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{cp.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{cp.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for theme in corpus.themes:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                        if corpus.annex:
                                            for art in corpus.annex.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts 
                                    if corpus.genre_en in ["educational philosophy"]:
                                        for cp in [corpus.info, corpus.contents]:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{cp.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{cp.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(cp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for art in corpus.preface.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for art in corpus.chapters.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        if corpus.annex:
                                            for art in corpus.annex.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                    elif len(family.keys())== 2:
                        corp_root = family['0']
                        corp_child = family['1']
                        if corp_root not in ["UXEP", "GOC"]:
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    if corp_child == corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en(corpus, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                        break
                        elif corp_root == "UXEP":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_child == "概况":
                                        art = corpus.info
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                        break
                                    if corp_child == "目录":
                                        art = corpus.contents
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                        break
                                    if corp_child == "导言":
                                        for art in corpus.preface.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        break
                                    if corp_child == "章节":
                                        for art in corpus.chapters.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        break
                                    if corp_child == "附录":
                                        for art in corpus.annex.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        break                                       
                        elif corp_root == "GOC":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    if corp_child == corp[1]:
                                        corpus = self.open_dat_file(corp[0])
                                        for art in [corpus.info, corpus.contents]:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                        for theme in corpus.themes:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                        if corpus.annex:
                                            for art in corpus.annex.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                        break                                                
                        else:
                            pass                            
                    elif len(family.keys())== 3:
                        corp_root = family['0'] 
                        corp_pa = family['1']  
                        corp_id = family['2']  
                        if corp_root == "UXEP":
                            for corp in new_corpora:
                                if corp_root in corp[1]:
                                    corpus = self.open_dat_file(corp[0])
                                    art_num = corp_id.split("-")[0]
                                    if corp_pa == "章节":                                        
                                        for art in corpus.chapters.articles:                                            
                                            if art.num == art_num:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                                break
                                    if corp_pa == "附录": 
                                        for art in corpus.annex.articles:
                                            if art.num == art_num:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                                break
                                    break
                        if corp_root == "GOC":
                            for corp in new_corpora:
                                if corp_pa == corp[1]:                                    
                                    corpus = self.open_dat_file(corp[0])
                                    if corp_id == "概况":                                        
                                        art = corpus.info
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                    if corp_id == "目录":
                                        art = corpus.contents
                                        if src_lang == "zh":
                                            self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        else:
                                            self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                      self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                        result.num_list.extend(num_list)
                                        result.lang_list.extend(lang_list)
                                        result.sent_list.extend(sent_list)
                                        idx_num = idx_n
                                        hit_words = hit_wds
                                        hit_sents = hit_sts
                                    if corp_id == "主题":
                                        for theme in corpus.themes:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                    if corp_id == "附录":
                                        for art in corpus.annex.articles:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                    break
                    elif len(family.keys())== 4:
                        corp_root = family['0'] 
                        corp_gpa = family['1']  
                        corp_pa = family['2']       
                        corp_id = family['3']        
                        corp_num = corp_id.split("-")[0]
                        for corp in new_corpora:
                            if corp_gpa == corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corp_pa == "主题":
                                    for theme in corpus.themes:
                                        if corp_num == theme.num:
                                            for art in theme.articles:
                                                if src_lang == "zh":
                                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                else:
                                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                result.num_list.extend(num_list)
                                                result.lang_list.extend(lang_list)
                                                result.sent_list.extend(sent_list)
                                                idx_num = idx_n
                                                hit_words = hit_wds
                                                hit_sents = hit_sts
                                            break
                                if corp_pa == "附录":
                                    for art in corpus.annex.articles:
                                        if art.num == corp_num:
                                            if src_lang == "zh":
                                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            else:
                                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                            result.num_list.extend(num_list)
                                            result.lang_list.extend(lang_list)
                                            result.sent_list.extend(sent_list)
                                            idx_num = idx_n
                                            hit_words = hit_wds
                                            hit_sents = hit_sts
                                            break
                                break                        
                    elif len(family.keys())== 5:
                        corp_root = family['0']  
                        corp_ggpa = family['1']        
                        corp_gpa = family['2']       
                        corp_pa = family['3']      
                        corp_id = family['4']     
                        theme_num = corp_pa.split("-")[0]
                        art_num = corp_id.split("-")[0]
                        for corp in new_corpora:
                            if corp_ggpa == corp[1]:
                                corpus = self.open_dat_file(corp[0])
                                if corp_gpa == "主题":
                                    for theme in corpus.themes:
                                        if theme_num == theme.num:
                                            for art in theme.articles:
                                                if art_num  == art.num:
                                                    if src_lang == "zh":
                                                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                                  self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                    else:
                                                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                                                  self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                                    result.num_list.extend(num_list)
                                                    result.lang_list.extend(lang_list)
                                                    result.sent_list.extend(sent_list)
                                                    idx_num = idx_n
                                                    hit_words = hit_wds
                                                    hit_sents = hit_sts
                                                    break
                                        break
                            break                                    
                    else:
                        pass
                    self.pbar_signal.emit(f_num,j)                                        
            if self.scope.value == 3:
                self.msg_m_signal.emit(f"1份语料检索中，请稍候....")
                corpus = self.corpora[0]
                art = self.corpora[1]
                ref_corpus = ""
                f_num = 1
                if not art:
                    if src_lang == "zh":
                        self.msg_m_signal.emit(f"{corpus.title_zh}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_zh(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                    else:
                        self.msg_m_signal.emit(f"{corpus.title_en}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_en(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                    result.num_list.extend(num_list)
                    result.lang_list.extend(lang_list)
                    result.sent_list.extend(sent_list)
                    idx_num = idx_n
                    hit_words = hit_wds
                    hit_sents = hit_sts
                else:
                    if src_lang == "zh":
                        self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                    else:
                        self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                        num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                  self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                    result.num_list.extend(num_list)
                    result.lang_list.extend(lang_list)
                    result.sent_list.extend(sent_list)
                    idx_num = idx_n
                    hit_words = hit_wds
                    hit_sents = hit_sts
                self.pbar_signal.emit(f_num,j)
            if self.scope.value == 4:
                self.msg_m_signal.emit(f"{j}份语料检索中，请稍候....")
                for f_num, (corp_path, corp_id) in enumerate(self.corpora, start=1):
                    corpus = self.open_dat_file(corp_path)
                    ref_corpus = ""
                    if corpus.genre_en not in ["educational philosophy", 'governance of china']:
                        if src_lang == "zh":
                            self.msg_m_signal.emit(f"{corpus.title_zh}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_zh(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        else:
                            self.msg_m_signal.emit(f"{corpus.title_en}")
                            num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                      self.para_concording_en(corpus, ref_corpus, self.req, query, query_2, idx_num, hit_sents, hit_words)
                        result.num_list.extend(num_list)
                        result.lang_list.extend(lang_list)
                        result.sent_list.extend(sent_list)
                        idx_num = idx_n
                        hit_words = hit_wds
                        hit_sents = hit_sts
                    elif corpus.genre_en in ["educational philosophy"]:
                        for art in [corpus.info, corpus.contents]:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                        for art in corpus.preface.articles:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                        for art in corpus.chapters.articles:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                        for art in corpus.annex.articles:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts
                    elif corpus.genre_en in ["governance of china"]:
                        for corp in [corpus.info, corpus.contents]:
                            if src_lang == "zh":
                                self.msg_m_signal.emit(f"{corpus.title_zh}-{corp.title_zh}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_zh(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            else:
                                self.msg_m_signal.emit(f"{corpus.title_en}-{corp.title_en}")
                                num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                          self.para_concording_en(corp, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                            result.num_list.extend(num_list)
                            result.lang_list.extend(lang_list)
                            result.sent_list.extend(sent_list)
                            idx_num = idx_n
                            hit_words = hit_wds
                            hit_sents = hit_sts                            
                        for theme in corpus.themes:
                            for art in theme.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts
                        if corpus.annex:
                            for art in corpus.annex.articles:
                                if src_lang == "zh":
                                    self.msg_m_signal.emit(f"{corpus.title_zh}-{art.title_zh}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_zh(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                else:
                                    self.msg_m_signal.emit(f"{corpus.title_en}-{art.title_en}")
                                    num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n = \
                                              self.para_concording_en(art, corpus, self.req, query, query_2, idx_num, hit_sents, hit_words, "book")
                                result.num_list.extend(num_list)
                                result.lang_list.extend(lang_list)
                                result.sent_list.extend(sent_list)
                                idx_num = idx_n
                                hit_words = hit_wds
                                hit_sents = hit_sts
                    else: pass
                    # endregion
                    self.pbar_signal.emit(f_num,j)

        result.hit_words = hit_words
        result.hit_pairs = hit_sents
        result_dict = {}
        result_dict['obj'] = result
        self.result_signal.emit(result_dict)
        T2 = time.perf_counter()
        time_used = T2 - T1
        self.pbar_signal.emit(-1,10)
        self.msg_m_signal.emit(f"本次检索共用时{time_used:.2f}秒")

    def open_dat_file(self, dat_file):
        dat_read = ''
        with open(dat_file, 'rb') as f:
            dat_read = pickle.load(f)
        return dat_read

    def _build_query(self, q, mode: SearchMode):
        result = '' 
        result_sl = "" 
        if mode == SearchMode.NORMAL:
            result = re.compile(r'\b' + q.q + r'\b') 
            if q.q_sl:
                result_sl = re.compile("|".join(q.q_sl)) 
        if mode == SearchMode.REGEX:
            result = re.compile(r"{}".format(q.q)) 
        if mode == SearchMode.EXTENDED:
            result = self.en_regex_wrapper(q.q)
            if q.q_sl:
                result_sl = re.compile("|".join(q.q_sl))
        return result, result_sl

    def _build_reverse_query(self, q, mode: SearchMode):
        result = ''
        result_tl = ''
        if mode == SearchMode.NORMAL:
            result = q.q
            if q.q_tl:
                result_tl = re.compile(r'\b(' + "|"+ "|".join(q.q_tl) + r')\b')
        if mode == SearchMode.REGEX:
            result = re.compile(r"{}".format(q.q))            
        if mode == SearchMode.EXTENDED:
            result = q.q
            if q.q_tl: # ['the Chinese Dream', 'Chinese Dream']
                result_tl = self.en_regex_wrapper(q.q_tl)
        return result, result_tl
    
    def detect_lang(self, text):
        target_lang = 'en'
        if "/" in text:
            target_lang = 'zh'
        for word in text:
            if '\u4e00' <= word <= '\u9fa5' or '\u3400' <= word <= '\u4DB5':
                target_lang = 'zh'
                break        
        return target_lang

    def phrase_lemma_organizer(self, phrase):
        ph_words = [x for x in phrase.split() if x] 
        ph_list = []      
        for word in ph_words:
            word_string = ""
            head_word = word.title() 
            word_lemmas = self.en_lemma.get(head_word, [])
            if word_lemmas:
                word_string = head_word + "|" + "|".join(word_lemmas)
            else:
                head_word = word.lower() 
                word_lemmas = self.en_lemma.get(head_word, [])
                if word_lemmas:
                    word_string = head_word + "|" + "|".join(word_lemmas) 
                else:
                    for k, v_list in self.en_lemma.items(): 
                        if head_word in v_list:
                            word_string = k + "|" + "|".join(v_list) 
                        elif head_word.title() in v_list:
                            word_string = k + "|" + "|".join(v_list) 
                        else:
                            pass 
            if not word_string: 
                word_string = word
            ph_list.append(r"(?:"+word_string+r")") 
        ph_regex =r"\b(?:" + "\s".join(ph_list) + r")\b" 
        return ph_regex
   
    def en_regex_wrapper(self, word_list):        
        if isinstance(word_list, list): 
            final_list = []
            for word in word_list:
                word_regex = self.phrase_lemma_organizer(word)
                final_list.append(word_regex)
                final_regex = re.compile(r"\b(?:"+"|".join(final_list)+r")\b", re.I) 
        elif isinstance(word_list, str): 
            word_regex = self.phrase_lemma_organizer(word_list) 
            final_regex = re.compile(word_regex, re.I)
        else:
            final_regex = ""
        return final_regex

    def get_notes(self, sent, mode, note_corpus, lang = 'en'):
        notes = []
        if lang == 'en':
            if mode == 3:
                note_regex = re.compile(r"(\[\d+\]_XZ|\[[a-z]\]_XZ|\*_SYM)")
                try:
                    corp = note_corpus.notes.notes_en
                except:
                    try:
                        corp = note_corpus.notes_en
                    except:
                        try:
                            corp = note_corpus.note_en
                        except:
                            corp = ""
            else:
                note_regex = re.compile(r"(\[\d+\]|\[[a-z]\]|\*)")
                try:
                    corp = note_corpus.notes.notes_en
                except:
                    try:
                        corp = note_corpus.notes_en
                    except:
                        try:
                            corp = note_corpus.note_en
                        except:
                            corp = ""
        else:
            if mode == 3:
                note_regex = re.compile(r"(〔\d+〕/xz|〔[a-z]〕/xz|\*/w)")
                try:
                    corp = note_corpus.notes.notes_zh
                except:
                    try:
                        corp = note_corpus.notes_zh
                    except:
                        try:
                            corp = note_corpus.note_zh
                        except:
                            corp = ""
            else:
                note_regex = re.compile(r"(〔\d+〕|〔[a-z]〕|\*)")
                try:
                    corp = note_corpus.notes.notes_zh
                except:
                    try:
                        corp = note_corpus.notes_zh
                    except:
                        try:
                            corp = note_corpus.note_zh
                        except:
                            corp = ""
        m = re.finditer(note_regex, sent)
        if m and corp:            
            for note_id in m:
                note_id_found = copy.deepcopy(note_id.group())
                for note in corp:                    
                    if note_id_found == note.index:
                        if mode == 3:
                            notes.append(note.index + " " +note.note_tag)
                        else:
                            notes.append(note.index + " " +note.note)
        return notes

    def get_extra (self, idx_num, req, sent, sents_zh, sents_en, hi_sent, hi_sent_2, note_corpus, corpus, ref_corpus, title_zh, title_en, lang, genre="article"):
        num_list = []
        lang_list = []
        sent_list = []
        notes_en = self.get_notes(sent.en, req.mode, note_corpus, 'en')
        notes_zh = self.get_notes(sent.zh, req.mode, note_corpus, 'zh')
        if lang == 'en':
            if req.dsp_ct:
                if hi_sent_2:
                    sents_zh[int(sent.num)-1]="<font color = 'green'>"+hi_sent_2+"</font>"
                else:
                    sents_zh[int(sent.num)-1]="<font color = 'green'>"+sent.zh+"</font>"
                sents_en[int(sent.num)-1]="<font color = 'green'>"+hi_sent+"</font>"
                zh_set = "".join(sents_zh)
                zh_set = zh_set.replace("[PS]", "<br>")
                en_set = " ".join(sents_en)
                en_set = en_set.replace("[PS]", "<br>")
                if req.dsp_sc:
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                      
                            else:
                                sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                        else:
                            print("error: no ref_corpus!")
                    else:
                        sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh) + "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh)+ "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                    sent_list.append(zh_set+sc_sl)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                            else:
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                        else:
                            print("error: no ref_corpus!")
                    else:
                        sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) +" (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set+sc_tl)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
                else:
                    sent_list.append(zh_set)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
            elif req.dsp_sc:
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                      
                        else:
                            sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"                      
                    else:
                        print("error: no ref_corpus!") 
                else:
                    sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh) + "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh)+ "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                if hi_sent_2:
                    sent_list.append(hi_sent_2+sc_sl)
                else:
                    sent_list.append(sent.zh+sc_sl)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                        else:
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                    else:
                        print("error: no ref_corpus!")
                else:
                    sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) + " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                num_list.append(idx_num)
                lang_list.append("译文")
                sent_list.append(hi_sent+sc_tl)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))
            else:
                if hi_sent_2:
                    sent_list.append(hi_sent_2)
                else:
                    sent_list.append(sent.zh)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                num_list.append(idx_num)
                lang_list.append("译文")
                sent_list.append(hi_sent)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))
        else:
            if req.dsp_ct:
                sents_zh[int(sent.num)-1]="<font color = 'green'>"+hi_sent+"</font>"
                if hi_sent_2:
                    sents_en[int(sent.num)-1]="<font color = 'green'>"+hi_sent_2+"</font>"
                else:
                    sents_en[int(sent.num)-1]="<font color = 'green'>"+sent.en+"</font>"
                zh_set = "".join(sents_zh)
                zh_set = zh_set.replace("[PS]", "<br>")
                en_set = " ".join(sents_en)
                en_set = en_set.replace("[PS]", "<br>")
                if req.dsp_sc:                    
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                     
                            else:
                                sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                        else:
                            print("error: no ref_corpus!")
                    else:
                        sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh)+ "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh) + "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                    sent_list.append(zh_set+sc_sl)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                            else:
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                        else:
                            print("error: no ref_corpus!")
                    else:
                        sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) + " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set+sc_tl)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
                else:
                    sent_list.append(zh_set)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
            elif req.dsp_sc:
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                        
                        else:
                            sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                    else:
                        print("error: no ref_corpus!")
                else:
                    sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh) + "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh) + "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                sent_list.append(hi_sent+sc_sl)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                        else:
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) + " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                    else:
                        print("error: no ref_corpus!")
                else:
                    sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                num_list.append(idx_num)
                lang_list.append("译文")
                if hi_sent_2:
                    sent_list.append(hi_sent_2+sc_tl)
                else:
                    sent_list.append(sent.en+sc_tl)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))
            else:
                sent_list.append(hi_sent)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                num_list.append(idx_num)
                lang_list.append("译文")                
                if hi_sent_2:
                    sent_list.append(hi_sent_2)
                else:
                    sent_list.append(sent.en)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))            
            
        return num_list, lang_list, sent_list

    def get_tag_extra (self, idx_num, req, sent, sents_zh_tag, sents_en_tag, hi_sent, hi_sent_2, corpus, ref_corpus, title_zh, title_en, lang, genre="article"):
        num_list = []
        lang_list = []
        sent_list = []
        notes_en = self.get_notes(sent.en_tag, req.mode, corpus) 
        notes_zh = self.get_notes(sent.zh_tag, req.mode, corpus, 'zh') 
        if lang == 'en':
            if req.dsp_ct:
                if hi_sent_2:
                    sents_zh_tag[int(sent.num)-1]="<font color = 'green'>"+hi_sent_2+"</font>"
                else:
                    sents_zh_tag[int(sent.num)-1]="<font color = 'green'>"+sent.zh_tag+"</font>"
                sents_en_tag[int(sent.num)-1]="<font color = 'green'>"+hi_sent+"</font>"
                zh_set = "".join(sents_zh_tag)
                zh_set = zh_set.replace("[PS]", "<br>")
                en_set = " ".join(sents_en_tag)
                en_set = en_set.replace("[PS]", "<br>")
                if req.dsp_sc:
                    if genre == "book":                        
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                        
                            else:
                                sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                        else:
                            print("error: no ref_corpus!")                                     
                    else:
                        sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh) + "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh) + "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                    sent_list.append(zh_set+sc_sl)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                            else:
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                        else:
                            print("error: no ref_corpus!")
                    else:
                        sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en) + ") Genre: " +re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set+sc_tl)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
                else:
                    sent_list.append(zh_set)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
            elif req.dsp_sc:
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                        
                        else:
                            sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                    else:
                        print("error: no ref_corpus!") 
                else:
                    sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh)+ "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh) + "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                if hi_sent_2:
                    sent_list.append(hi_sent_2+sc_sl)
                else:
                    sent_list.append(sent.zh_tag+sc_sl)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                        else:
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                    else:
                        print("error: no ref_corpus!")
                else:
                    sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) + " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                num_list.append(idx_num)
                lang_list.append("译文")
                sent_list.append(hi_sent+sc_tl)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))
            else:
                if hi_sent_2:
                    sent_list.append(hi_sent_2)
                else:
                    sent_list.append(sent.zh_tag)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                num_list.append(idx_num)
                lang_list.append("译文")
                sent_list.append(hi_sent)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))

        else:
            if req.dsp_ct:
                sents_zh_tag[int(sent.num)-1]="<font color = 'green'>"+hi_sent+"</font>"
                if hi_sent_2:
                    sents_en_tag[int(sent.num)-1]="<font color = 'green'>"+hi_sent_2+"</font>"
                else:
                    sents_en_tag[int(sent.num)-1]="<font color = 'green'>"+sent.en_tag+"</font>"
                zh_set = "".join(sents_zh_tag)
                zh_set = zh_set.replace("[PS]", "<br>")
                en_set = " ".join(sents_en_tag)
                en_set = en_set.replace("[PS]", "<br>")
                if req.dsp_sc:
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                        
                            else:
                                sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                        else:
                            print("error: no ref_corpus!") 
                    else:
                        sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh) + "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh) + "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                    sent_list.append(zh_set+sc_sl)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    if genre == "book":
                        if ref_corpus:
                            if ref_corpus.genre_en != "governance of china":
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                            else:
                                sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                        else:
                            print("error: no ref_corpus!")
                    else:
                        sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) + " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())+ "</font>"
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set+sc_tl)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
                else:
                    sent_list.append(zh_set)
                    if req.dsp_nt:
                        if notes_zh:
                            num_list.append(idx_num)
                            lang_list.append("原注")
                            sent_list.append("<br>".join(notes_zh))
                    num_list.append(idx_num)
                    lang_list.append("译文")
                    sent_list.append(en_set)
                    if req.dsp_nt:
                        if notes_en:
                            num_list.append(idx_num)
                            lang_list.append("译注")
                            sent_list.append("<br>".join(notes_en))
            elif req.dsp_sc:
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_sl = "<br><font color = 'grey'>语源：《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.genre_zh)+ "•" + title_zh +"》</font>"                                        
                        else:
                            sc_sl = "<br><font color = 'grey'>语源："+ "《"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.title_zh) + "》，"+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_zh)+re.sub(r"\[[A-Z]+?\]", "", ref_corpus.edition_zh)+"，"+re.sub(r"\[[A-Z]+?\]", "", title_zh) +"</font>"
                    else:
                        print("error: no ref_corpus!") 
                else:
                    sc_sl = "<br><font color = 'grey'>语源："+ re.sub(r"\[[A-Z]+?\]", "", corpus.genre_zh)+ "，《"+re.sub(r"\[[A-Z]+?\]", "", title_zh) + "》，" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_zh)  + "</font>"                                        
                sent_list.append(hi_sent+sc_sl)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                if genre == "book":
                    if ref_corpus:
                        if ref_corpus.genre_en != "governance of china":
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.genre_en.title() + "</font>"
                        else:
                            sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en)+ " from "+ ref_corpus.title_en.title()+ " (" + re.sub(r"\[[A-Z]+?\]", "", ref_corpus.volume_en)+ ")</font>"
                    else:
                        print("error: no ref_corpus!")
                else:
                    sc_tl = "<br> <font color = 'grey'>SOURCE: " + re.sub(r"\[[A-Z]+?\]", "", title_en) + " (" + re.sub(r"\[[A-Z]+?\]", "", corpus.date_en)+ ") Genre: " + re.sub(r"\[[A-Z]+?\]", "", corpus.genre_en.title())  + "</font>"
                num_list.append(idx_num)
                lang_list.append("译文")
                if hi_sent_2:
                    sent_list.append(hi_sent_2+sc_tl)
                else:
                    sent_list.append(sent.en_tag+sc_tl)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))
            else:
                sent_list.append(hi_sent)
                if req.dsp_nt:
                    if notes_zh:
                        num_list.append(idx_num)
                        lang_list.append("原注")
                        sent_list.append("<br>".join(notes_zh))
                num_list.append(idx_num)
                lang_list.append("译文")                
                if hi_sent_2:
                    sent_list.append(hi_sent_2)
                else:
                    sent_list.append(sent.en_tag)
                if req.dsp_nt:
                    if notes_en:
                        num_list.append(idx_num)
                        lang_list.append("译注")
                        sent_list.append("<br>".join(notes_en))            
            
        return num_list, lang_list, sent_list    

    def para_concording_zh(self, corpus, ref_corpus, req, query, query_2, idx_num, hit_sents, hit_words, type="article"):
        num_list = []
        lang_list = []
        sent_list = []
        hit_sts = hit_sents
        hit_wds = hit_words
        idx_n = idx_num
        for para in corpus.paras:
            sents_en = [re.sub(r"(\[P\]|\|)","", sent.en) for sent in para.sents]
            sents_zh = [re.sub(r"(\[P\]|\|)","", sent.zh) for sent in para.sents]                    
            for sent in para.sents:
                sent.en = re.sub(r"(\[P.*?\]|\|)","", sent.en)
                sent.zh = re.sub(r"(\[P.*?\]|\|)","", sent.zh)
                m = re.findall(query, sent.zh)
                if m:
                    hit_sts += 1
                    hit_wds += len(m)
                    num_list.append(idx_n)                            
                    lang_list.append("原文")
                    hi_sent = sent.zh
                    key = set(m)
                    for k in key:
                        hi_sent = re.sub(k, "<font color = 'red'><b>"+k+"</b></font>", hi_sent)
                    hi_sent_2 = ""
                    if query_2:
                        m_2 = re.findall(query_2, sent.en)
                        if m_2:
                            hi_sent_2 = re.sub(query_2, "<font color = 'blue'><b>"+r"\g<0>"+"</b></font>", sent.en)
                    n_l, l_l, s_l = self.get_extra(idx_n, req, sent, sents_zh, sents_en, hi_sent, hi_sent_2, corpus, corpus, ref_corpus, corpus.title_zh, corpus.title_en, "zh", type)
                    num_list.extend(n_l)
                    lang_list.extend(l_l)
                    sent_list.extend(s_l)
                    idx_n += 1
        return num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n

    def para_concording_en(self, corpus, ref_corpus, req, query, query_2, idx_num, hit_sents, hit_words, type="article"):
        num_list = []
        lang_list = []
        sent_list = []
        hit_sts = hit_sents
        hit_wds = hit_words
        idx_n = idx_num
        for para in corpus.paras:
            sents_en = [re.sub(r"(\[P\]|\|)","", sent.en) for sent in para.sents]
            sents_zh = [re.sub(r"(\[P\]|\|)","", sent.zh) for sent in para.sents]                    
            for sent in para.sents:
                sent.en = re.sub(r"(\[P.*?\]|\|)","", sent.en)
                sent.zh = re.sub(r"(\[P.*?\]|\|)","", sent.zh)
                m = re.findall(query, sent.en)
                if m:
                    hit_sts += 1
                    hit_wds += len(m)
                    num_list.append(idx_n)                            
                    lang_list.append("原文")
                    hi_sent = sent.en
                    key = set(m)
                    for k in key:
                        hi_sent = re.sub(k, "<font color = 'red'><b>"+k+"</b></font>", hi_sent)
                    hi_sent_2 = ""
                    if query_2:
                        m_2 = re.findall(query_2, sent.zh)
                        if m_2:
                            hi_sent_2 = re.sub(query_2, "<font color = 'blue'><b>"+r"\g<0>"+"</b></font>", sent.zh)
                    n_l, l_l, s_l = self.get_extra(idx_n, req, sent, sents_zh, sents_en, hi_sent, hi_sent_2, corpus, corpus, ref_corpus, corpus.title_zh, corpus.title_en, "en", type)
                    num_list.extend(n_l)
                    lang_list.extend(l_l)
                    sent_list.extend(s_l)
                    idx_n += 1
        return num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n    

    def para_concording_zh_tag(self, corpus, ref_corpus, req, query, query_2, idx_num, hit_sents, hit_words, type="article"):
        num_list = []
        lang_list = []
        sent_list = []
        hit_sts = hit_sents
        hit_wds = hit_words
        idx_n = idx_num
        for para in corpus.paras:
            sents_en_tag = [re.sub(r"(\[P\]_XM\s*|\|_XN\s*)","", sent.en_tag) for sent in para.sents]
            sents_zh_tag = [re.sub(r"(\[P\]/xm\s*|\|/xm\s*)","", sent.zh_tag) for sent in para.sents]
            for sent in para.sents:
                sent.en_tag = re.sub(r"(\[P.*?\]_XM\s*|\|_XN\s*)","", sent.en_tag)
                sent.zh_tag = re.sub(r"(\[P.*?\]/xm\s*|\|/xn\s*)","", sent.zh_tag)          
                m = re.findall(query, sent.zh_tag)
                if m:
                    hit_sts += 1
                    hit_wds += len(m)
                    num_list.append(idx_n)                            
                    lang_list.append("原文")
                    hi_sent = sent.zh_tag
                    key = set(m)
                    for k in key:
                        hi_sent = re.sub(k, "<font color = 'red'><b>"+k+"</b></font>", sent.zh_tag)
                    hi_sent_2 = ""
                    if query_2:
                        m_2 = re.findall(query_2, sent.en_tag)
                        if m_2:
                            hi_sent_2 = re.sub(query_2, "<font color = 'blue'><b>"+r"\g<0>"+"</b></font>", sent.en_tag)
                    n_l, l_l, s_l = self.get_tag_extra(idx_n, req, sent, sents_zh_tag, sents_en_tag, hi_sent, hi_sent_2, corpus, ref_corpus, corpus.title_zh, corpus.title_en, "zh", type)
                    num_list.extend(n_l)
                    lang_list.extend(l_l)
                    sent_list.extend(s_l)
                    idx_n += 1
        return num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n

    def para_concording_en_tag(self, corpus, ref_corpus, req, query, query_2, idx_num, hit_sents, hit_words, type="article"):
        num_list = []
        lang_list = []
        sent_list = []
        hit_sts = hit_sents
        hit_wds = hit_words
        idx_n = idx_num
        for para in corpus.paras:
            sents_en_tag = [re.sub(r"(\[P\]_XM\s*|\|_XN\s*)","", sent.en_tag) for sent in para.sents]
            sents_zh_tag = [re.sub(r"(\[P\]/xm\s*|\|/xm\s*)","", sent.zh_tag) for sent in para.sents]
            for sent in para.sents:
                sent.en_tag = re.sub(r"(\[P.*?\]_XM\s*|\|_XN\s*)","", sent.en_tag)
                sent.zh_tag = re.sub(r"(\[P.*?\]/xm\s*|\|/xn\s*)","", sent.zh_tag)          
                m = re.findall(query, sent.en_tag)
                if m:
                    hit_sts += 1
                    hit_wds += len(m)
                    num_list.append(idx_n)                            
                    lang_list.append("原文")
                    hi_sent = sent.en_tag
                    key = set(m)
                    for k in key:
                        hi_sent = re.sub(k, "<font color = 'red'><b>"+k+"</b></font>", sent.en_tag)
                    hi_sent_2 = ""
                    if query_2:
                        m_2 = re.findall(query_2, sent.zh_tag)
                        if m_2:
                            hi_sent_2 = re.sub(query_2, "<font color = 'blue'><b>"+r"\g<0>"+"</b></font>", sent.zh_tag)
                    n_l, l_l, s_l = self.get_tag_extra(idx_n, req, sent, sents_zh_tag, sents_en_tag, hi_sent, hi_sent_2, corpus, ref_corpus, corpus.title_zh, corpus.title_en, "en", type)
                    num_list.extend(n_l)
                    lang_list.extend(l_l)
                    sent_list.extend(s_l)
                    idx_n += 1                    
        return num_list, lang_list, sent_list, hit_sts, hit_wds, idx_n
