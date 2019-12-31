# -*- coding:utf-8 -*-

import sys
import codecs
from collections import defaultdict
import json
sys.setrecursionlimit(20000)

class ExtractConcept():
  
  def __init__(self):
    self._path = "output/"
    self._category_id_name_map = self.load_concept1("output_zh/Category.txt", 1, 2) 
    self._category_name_id_map = self.load_concept1("output_zh/Category.txt", 2, 1) 
    self._category_sub_map = self.load_concept("output_zh/category_outlinks.txt", 0, 1)
    self._category_page_map = self.load_concept("output_zh/category_pages.txt", 0, 1) 
    self._page_id_name_map = self.load_concept1("output_zh/Page_title.txt", 1, 2) 
    self._page_re_name_id_map = self.load_concept1("output_zh/page_redirects.txt", 1, 0) 
    self._concepts_id = defaultdict(list)
    self._pages_id= defaultdict(list)


  def load_concept1(self, file_name, key, value):
    concept_dic = dict()
    with codecs.open(file_name, 'r', 'utf-8') as f:
      for line in f:
	line = line.strip()
	line_parts = line.split('\t')
	concept_dic[line_parts[key]] = line_parts[value]
    return concept_dic 
  def load_concept(self, file_name, key, value):
    concept_dic = defaultdict(list)
    with codecs.open(file_name, 'r', 'utf-8') as f:
      for line in f:
	line = line.strip()
	line_parts = line.split('\t')
	concept_dic[line_parts[key]].append(line_parts[value]) 
    return concept_dic 

  def gen_hier_concepts(self, root_concept_name):
    #root_concept_name = sys.argv[1].decode('utf-8')
    '''
    if root_concept_name in self._page_re_name_id_map:
      redirect_concept_id = self._page_re_name_id_map[root_concept_name]
      root_concept_name = self._category_id_name_map[redirect_concept_id]
    '''
    if root_concept_name not in self._category_name_id_map:
      return
    root_concept_id = self._category_name_id_map[root_concept_name]
    concepts_id = defaultdict(list)
    concept_name = self._category_id_name_map[root_concept_id]
    if (root_concept_id in self._category_page_map):
      for page_id in self._category_page_map[root_concept_id]:
	concepts_id[concept_name].append(self._page_id_name_map[page_id])
    for sub_concept_id in self._category_sub_map[root_concept_id]:
      #self._concepts_id.append(sub_concept_id)
      #self._concepts_id[0].append(self._category_id_name_map[sub_concept_id]) #sub_concept_id)
      concepts_id[concept_name].append(self.traverse(sub_concept_id, 0))
    return json.dumps(dict(concepts_id),ensure_ascii=False)

  def traverse(self, concept_id, level):
      if (level == 2):
	return self._category_id_name_map[concept_id]
      if (concept_id not in self._category_sub_map.keys()):
	concept_name = self._category_id_name_map[concept_id]
        if (concept_id in self._category_page_map):
          pages_id = defaultdict(list) 
	  for page_id in self._category_page_map[concept_id]:
	    pages_id[concept_name].append(self._page_id_name_map[page_id])
	  return pages_id
        else:
	  return concept_name
      concepts_id = defaultdict(list)
      concept_name = self._category_id_name_map[concept_id]
      for sub_concept_id in self._category_sub_map[concept_id]:
        #self._concepts_id.append(sub_concept_id)
        #self._concepts_id[level].append(self._category_id_name_map[sub_concept_id])#sub_concept_id)
	concepts_id[concept_name].append(self.traverse(sub_concept_id, level + 1))

      if (concept_id in self._category_page_map):
	for page_id in self._category_page_map[concept_id]:
	  concepts_id[concept_name].append(self._page_id_name_map[page_id])
      return concepts_id

  def output(self):
    print json.dumps(dict(self._concepts_id),ensure_ascii=False)
    #for concept_id in self._concepts_id:
      #print "\t".join(self._concepts_id[concept_id])
      #print concept_id, self._category_id_name_map[concept_id]
        
if __name__ == "__main__":
  ec = ExtractConcept()
  print ec.gen_hier_concepts(u'香水')
  #ec.output()
