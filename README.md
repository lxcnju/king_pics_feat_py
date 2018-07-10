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
      本实验为了获取王者荣耀所有英雄头像和装备图像，使用爬虫爬取官网上给出的图片。由于爬取图像的时候需要给图像一个标签，比如爬取花木兰的头像时，要知道她是“战士”和“刺客”类型的英雄，所以要模拟官网点击每个英雄类型，使用selenium+chrome模拟登陆，使用bs4解析网页源代码，获得图像名称和图像URL，然后下载即可。 共爬取了81张英雄头像和95张装备头像。 <br>
      Selenium+Chrome的使用和配置可以参考[博客](https://www.jianshu.com/p/4b84a7d7e567)。<br>
  * PCA <br>
      PCA，主成分分析，Principal Component Analysis，是一种无监督降维的方法。其实现可以通过矩阵的奇异值分解来完成，<a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;U\Sigma&space;V^T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;U\Sigma&space;V^T" title="X = U\Sigma V^T" /></a>。Sigma是矩阵X的奇异值矩阵，对角元素为正，其余元素为0，所以选择Sigma的前K行前K列，得到一个K\*K的矩阵，然后选择V^T矩阵的前K行，就得到了K\*N的矩阵，N是数据X的维度，即K个特征。记这K\*N的特征矩阵的行向量为F1,F2,...,FK，则对于一个X里面的样本x = a1\*F1 + a2\*F2 + ... + ak\*FK，即每一个样本点都可以用K个特征的线性组合来表示，这也是为什么称K\*N的矩阵为特征矩阵的原因。 <br>
      读取爬取的所有图像，将之标准化为64\*64大小，对于RGB每个通道及其水平反转后的图像，分别变为长度为64\*64=4096维的一个向量当作一个样本点，即一幅图像可以产生6个样本点，所以对于英雄图像，就组成了486\*4096的二维矩阵。每一个英雄头像可以表示为x = a1\*F1 + a2\*F2 + ... + aK\*FK，但是这里的系数a1~aK可能是负数，所以得到的特征图像并不一定是原图像的部分，而是倾向于是一副比较完整的图像。 <br>
      利用PCA进行矩阵分解，得到80\*4096维的矩阵，每一维当作一个特征转为64\*64的图像显示出来，如下图：<br>
      
  * NMF <br>
      NMF，Non-negative Matrix Factorization，即非负矩阵分解，是将矩阵X分解为M和H两个矩阵成绩，且M和H元素都大于零，则根据x = a1\*F1 + a2\*F2 + ... + aK\*FK，每个系数都是正的，这就说明，每个特征图像都是所有英雄头像的部分，经常是一些公共的特殊部位。比如：<br>
      
