# king_pics_feat_py
Using matrix factorization to extract images' features.(PCA &amp; NMF)

* 代码架构
* 原理解析
  * 王者荣耀
  * 爬虫
  * PCA
  * NMF
  
## 代码架构
 * crawl_pictures.py  爬取王者荣耀英雄和装备头像
 * pca_feats.py  通过PCA进行提取所有王者荣耀头像的特征成分
 * nmf_feats.py  通过NMF提取王者荣耀头像的特征成分
 
## 原理解析
  * 王者荣耀 <br>
  [王者荣耀](http://pvp.qq.com/web201605/herolist.shtml)的英雄和装备图片见官网。
  * 爬虫 <br>
      本实验为了获取王者荣耀所有英雄头像和装备图像，使用爬虫爬取官网上给出的图片。由于爬取图像的时候需要给图像一个标签，比如爬取花木兰的头像时，要知道她是“战士”和“刺客”类型的英雄，所以要模拟官网点击每个英雄类型，使用selenium+chrome模拟登陆，使用bs4解析网页源代码，获得图像名称和图像URL，然后下载即可。 <br>
      Selenium+Chrome的使用和配置可以参考[博客](https://www.jianshu.com/p/4b84a7d7e567)。
  * PCA <br>
      PCA，主成分分析，Principal Component Analysis，是一种无监督降维的方法。其实现可以通过矩阵的奇异值分解来完成，<a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;U\Sigma&space;V^T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;U\Sigma&space;V^T" title="X = U\Sigma V^T" /></a>
  * Iterated Function Systems <br>
      
