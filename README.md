# Wikipedia文本

##### 步骤

1. 下载wiki dump地址：<https://dumps.wikimedia.org/backup-index-bydb.html>
2. 生成term-to-concept的索引：java -DentityExpansionLimit=2147480000 -DtotalEntitySizeLimit=2147480000 -Djdk.xml.totalEntitySizeLimit=2147480000 -Xmx16g -jar esa-1.0-SNAPSHOT.jar
3. 繁体转简体、分词、停用词
4. tfidf特征构建索引

### wiki概念分析

使用JWPL操作wiki数据，<https://dkpro.github.io/dkpro-jwpl/JWPL_Core/>

1. 利用de.tudarmstadt.ukp.wikipedia.datamachine-1.1.0.jar解析dump数据生成txt文件，倒入数据库。
2. 利用txt文件分析测试用例。

**第一步：**

参考<https://www.cs.bgu.ac.il/~elhadad/nlp12/jwpl/wikification.html>，下载categorylinks.sql.gz、pagelinks.sql.gz、pages-articles.xml.bz2三个文件

执行 java -Dfile.encoding=utf8 -Xmx4g -cp de.tudarmstadt.ukp.wikipedia.datamachine-0.9.1-jar-with-dependencies.jar de.tudarmstadt.ukp.wikipedia.datamachine.domain.JWPLDataMachine chinese 化妆品 消歧页 wiki_zh/ 生成txt文件

\1. 在Category.txt中化妆品对应的ID如下：

**204544** **204544** 化妝品

\2. 在category_outlinks.txt中找到化妆品的父子概念，它的两个父概念分别是：

**764039** **764039** 化妝

**493378** **493378** 個人護理用品

\3. 子概念分别是：

**204544** 69157

**204544** 493380

**204544** 587933



其中，**940078**的外链如下：

**940078** **940078** 化妝品公司 -> **5426371** **5426371** 各国化妆品公司 -> **5426378** **5426378** 英国化妆品公司

\4. 接下来在category_pages.txt找到概念对应的页面id

**5426378** 494284 联合利华

**5426378** 622851 美體小舖

根据联合利华的page id 494284在Page.txt中找到对应的联合利华wiki页面内容。

##### **抽取结果：**

{"化妆品": [{"香水": [{"芳香疗法": ["精油"]}, "精油", {"香水成分": ["精油"]}]}, "美发品", "香港化妆品店", {"化妆品品牌": ["欧莱雅品牌"]}, {"化妆品公司": ["个人护理公司", {"各国化妆品公司": ["德国化妆品公司", {"法国化妆品公司": [{"莱雅": ["欧莱雅品牌", "欧莱雅人物"]}]}, {"日本化妆品公司": ["资生堂"]}, "韩国化妆品公司", "加拿大化妆品公司", "美国化妆品公司", "中国化妆品公司", "英国化妆品公司", "西班牙化妆品公司", "荷兰化妆品公司"]}]}, {"化妆品化学品": ["PH调节剂", {"蜡": [{"蜡烛": [{"灯笼": [{"灯艺师": ["台湾灯艺师"]}]}]}]}, {"香水成分": ["精油"]}, "氧化铁颜料", "防晒剂", {"保湿剂": [{"亲水性保湿剂": [{"多元醇": ["糖醇", {"二醇": [{"二酚": [{"邻苯二酚": ["儿茶酚胺"]}, "间苯二酚", "二羟基苯甲酸", "对苯二酚"]}]}, {"环多醇": ["肌醇"]}]}]}, "天然保湿因子", "高分子型保湿剂"]}, "仿晒剂"]}, "护肤品", "化妆品广告歌曲", "眼部化妆品", "面部化妆品", "唇部化妆品", "芳香化妆品"]}

##### 参考：

1. 论文：<http://www.cs.technion.ac.il/~gabr/papers/ijcai-2007-sim.pdf>

2. 代码：<https://github.com/pvoosten/explicit-semantic-analysis>

3. wiki文本处理：<https://blog.csdn.net/wangyangzhizhou/article/details/78348949>，<https://blog.csdn.net/jdbc/article/details/59483767>

4. <https://github.com/attardi/wikiextractor> 抽取wiki的概念和文章

5. https://radimrehurek.com/gensim/scripts/segment_wiki.html

