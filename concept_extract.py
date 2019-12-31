#!--coding:utf8--

import time
import sys
from bottle import route, run, request, template
import logging
from extract_hierachical_concept import ExtractConcept

ec = ExtractConcept()

@route("/concept_extractor")
def is_a_question():
    question = request.query["concept"].decode("utf8")
    return ec.gen_hier_concepts(question)
'''

@route("/get_sentiment", method = 'get')
def is_a_question():
    return template('login')

@route("/get_sentiment", method = 'post')
def is_a_question():
    #question = request.query["sentence"] 
    t = time.time()
    question = request.forms.get('q')
    feedback = request.forms.get('feedback_yes')
    if question:
        result = word_filter_object.do_filter(question.decode('utf-8'))
        #print (question+"\t"+result).encode('utf-8')
	logging.debug(result+'\t' +str(time.time() - t))
	result = result.replace('\n','<br>') 
        return template('{{!name}}', name=result), template('feedback')
    if feedback:
        return template('login')
    else:
	logging.debug(u"分类错误")
        return template('login')
'''


if __name__ == "__main__":
    print("get sentiment service is starting...")
    run(host='ip', port=9900, debug=False)
