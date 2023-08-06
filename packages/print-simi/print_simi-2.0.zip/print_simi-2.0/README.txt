print_simi:
输入pdf文档，利用tfidf模型、LSI模型、LDA模型计算文档间的相似性，从大到小排序后分别打印到三个txt文件中。


安装说明： 
1.安装前需要安装python 2.7,gensim 1.0.1,jieba 0.38,pdfminer 20140328。


用法：
print_simi有两个模块：pdf_txt与cal_simi。
（一）pdf_txt:

pdf_to_txt方法接受两个输入参数：保存pdf文档的目录的绝对路径；保存转换好的txt文档的目录的绝对路径。

这个模块将输入的pdf文档名称改为数字（以0开始），并在保存转换好的txt目录下生成转好的txt文件，txt文件名为从0开始的数字。

（二）cal_simi:

similarity_txt方法接受两个输入参数：保存txt文档的目录的绝对路径与主题数目。主题数目根据自己的文档数量与大小自行确定。

这个模块用转好的txt文档，使用tfidf、LSI、LDA模型，两两计算文档间的相似性，并在程序的当前目录下生成tfidf_similarity.txt,lsi_similarity.txt,lda_similarity.txt文件，将相似性打印到txt文件中。