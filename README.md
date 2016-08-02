TerrainParam
======================
数値標高モデルから、斜度、傾斜方位、仰角、太陽入射角などの地形パラメータを計算します。  


使い方
------
ターミナルで以下のようなコマンドを入力します。
<pre>
$ terrain.py dem.tif          　  　　斜度と傾斜方位
$ terrain.py dem.tif  direction   　　仰角
$ terrain.py dem.tif  sun_el sun_az 　　太陽入射角 
$ fangle.py dem.tif direction     　　仰角（高速）
$ skyview.py dem.tif num          　　天空視野要素
$ fskyview.py dem.tif num     　　　　 天空視野要素（高速）
</pre>

* 仰角は指定した方位(direction)に対する値をすべての画素に対して計算します。  
* 太陽入射角（の余弦）の計算には太陽高度(sun_el)と太陽方位(sun_az)が必要です。  
* 天空視野要素は計算する方位数(num)が増えると計算時間がかかります。１６方位程度で十分です。   
* 高速用のfangle.pyとfskyview.pyはfortranで計算を行っています。これらを利用するにはFORTRANフォルダに含まれるファイルのコンパイルなどが必要です。fortran.shに必要なコマンドが記載されています。


必要なデータ
----------------
GEOTIFF形式の数値方向モデル(dem.tif)が必要です。KibanDemを用いて作成する事ができます。


利用するライブラリ
--------
Python2.7で動作を確認しています。

1. sys,numpy,osgeoが必要です。
2. 自作のライブラリterrain\_utilにGEOTIFFの読み書き、地形パラメータを計算する関数が含まれています。
3. fangle.pyとfskyview.pyではos,subprocessも必要です。
4. FORTRANコンパイラ(gfortranなど）が必要です。
 
参考文献など
--------
* 飯倉善和：数値標高モデルの投影変換に用いる内挿法の評価、日本リモートセンシング学会誌、21(2)、pp.150-157、2001
* 飯倉善和：数値標高モデルの内挿と高速な地平線計算、GIS-理論と応用、8(2)、pp.1-8、2000


ライセンス
----------
Copyright &copy; 2016 Yoshikazu Iikura  
Distributed under the [MIT License][mit].

[MIT]: http://www.opensource.org/licenses/mit-license.php
