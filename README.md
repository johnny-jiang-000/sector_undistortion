# sector_undistortion
目前想到的方法是用GLSL写一个vertex shader来对图像做扇形remap。像素点mapping可以放到shader里面pixel by pixel计算或者是单独算好map（sector.cpp就是只算map，38400x21600大小的map在ryzen 3700x @16线程下只要1.5秒左右）然后shader读取。
- clutter支持添加GLSL到渲染层。。。
