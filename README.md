# Genetic Algorithm for Graph Partitioning

>> ## **1. Graph partitioning (Phân hoạch đồ thị) là gì?**
> 
>> ### **1.1 Giới thiệu bài toán**

Cho một đồ thị vô hướng $G = (V, E)$ với $V$ là tập hợp các đỉnh có $n$ phần tử và $E$ là tập hợp các cạnh giữa các đỉnh. Yêu cầu chia đồ thị thành hai tập hợp đỉnh $v1$ và $v2$ sao cho số cạnh nối giữa các đỉnh thuộc hai tập hợp khác nhau là nhỏ nhất và kích thước của hai tập hợp bằng nhau.

![](https://i.ibb.co/sPVJWcF/graph-partitioning.png)

> ### **1.2 Mục đích của phân hoạch đồ thị**
>> Phân tích bài toán đồ thị quy mô lớn thành các bài toán con nhỏ hơn có thể giải quyết độc lập và song song.

>> Tốc độ xử lý nhanh hơn. 

>
> ## **2. Thiết kế decision (quyết định)**
>> ### 2.1 Parameters (tham số)
> Thiết kế chương trình gồm 5 tham số.
> 
> * **POP_SIZE**
>     * Kích thước quần thể ban đầu.
>     * Type : INT
>     * Range : [1, INF)
>     
> * **NUM_NODES**
>     * Số đỉnh trong đồ thị được tạo ra ngẫu nhiên.
>     * Nó phải là số **chẵn**.
>     * Type : INT
>     * Range : [2, INF)
>
> * **CONNECT_PROB**
>     * Xác xuất kết nối giữa hai đỉnh bằng cạnh.
>     * Type : FLOAT
>     * Range : [0., 1.)
>     
> * **MUT_PROB**
>     * Xác suất thực hiện đột biến.
>     * Type : FLOAT
>     * Range : [0., 1.)
>     
> * **STOPPING_COUNT**
>     * Tiêu chí dừng lại
>     * Nếu không có sự cải thiện nào trong STOPPING_COUNT lần, thì chương trình sẽ bị kết thúc.
>     * Type : INT
>     * Range : (1, INF)
>
> * **K_IND**
>     * Số lượng cá thể được lựa chọn cho cạnh tranh.
>     * Type : INT
>     * Range : [1, NUM_NODES)
> -----    
>> ### 2.2 Stopping criteria (tiêu chí dừng)
> * Nếu không có cải tiến trong 10 lần, chương trình sẽ bị kết thúc.
> * Số lần mà chương trình chấp nhận không có cải tiến có thể điều chỉnh với tham số **STOPPING_COUNT**.
> -----
>> ### 2.3 Fitness function (Hàm đánh giá) 
> * Giá trị fitness của mỗi cá thể sẽ được tính bằng phương trình dưới đây.
> 

 $$F_i = \frac{(C_w – C_y) + (C_w – C_b)}{3}
$$
> * Trong đó:\
> $C_w$: Kích thước cắt của giải pháp tệ nhất trong quần thể.\
> $C_b$: Kích thước cắt của giải pháp tốt nhất trong quần thể.\
> $C_y$: Kích thước cắt của giải pháp $i$, đó là kích thước cắt của cá nhân đang được đánh giá.
> * Kích thước cắt là số lượng cạnh giữa các phân vùng của đồ thị. Kích thước cắt nhỏ hơn cho thấy một phân vùng tốt hơn.
> * Hàm fitness được sử dụng hướng dẫn thuật toán tối ưu hóa để tìm kiếm một giải pháp tốt hơn. Các cá thể có giá trị fitness cao hơn có khả năng được lựa chọn để tiếp tục lai tạo và đột biến, trong khi các cá thể có giá trị fitness thấp hơn có khả năng bị loại bỏ hơn. Mục tiêu cuối cùng là tìm ra cá thể có giá trị fitness tốt nhất, đại diện cho phân vùng tốt nhất của đồ thị theo tiêu chí đã cho.

> 
> -----
>> ### 2.4 Selection operator (toán tử chọn lọc)
> * **Tournament selection (chọn lọc cạnh tranh)**
>     * Chọn ngẫu nhiên $k$ cá thể từ quần thể và chọn cá thể tốt nhất trong số chúng.
>     * -	Số ngẫu nhiên k có thể điều chỉnh với tham số **K_IND**.
>     
>     ![image](./images/tournament_selection.png)
>     
> -----
>> ### 2.5 Crossover operator (Toán tử lai ghép) 
> * **Multi-point crossover**
>   * Từ chọn lọc cạnh tranh, hai nhiễm sắc thể được chọn làm cha mẹ.
>   * 5 điểm cắt được chọn ngẫu nhiên để thực hiện lai ghép.
>   * Hai con cái 1 và 2 sẽ được tạo ra theo cách khác nhau (được mô tả như hình ảnh dưới đây).
>   * Nếu các phân vùng của con cái mới không có kích thước bằng nhau thì bị loại bỏ.
>     ![image](./images/multi_crossover.PNG)

>
> * **Single point crossover (Lai ghép 1 điểm )**
>   * Từ việc lựa chọn cạnh tranh, hai nhiễm sắc thể được chọn làm cha mẹ.
>   * Điểm lai ghép được chọn ngẫu nhiên.
>   * Nếu các phân vùng của cá thể con mới không có cùng kích thước, cá thể con đó sẽ bị loại bỏ.

>
> -----
>> ### 2.6 Mutation operator (Toán tử đột biến)
> *	Thay thế một node trong đồ thị bằng 1 loại khác phù hợp.
> *	Node được chọn ngẫu nhiên từ phân vùng 0 sẽ được trao đổi với node được chọn ngẫu nhiên từ phân vùng 1.

>![image](./images/mutation.png)
>
> -----
>> ### Generational selection strategy (chiến lược lựa chọn thế hệ)
> * **Elitism**
>     * Giữ lại M cá thể tốt nhất từ thế hệ cha mẹ để giữ cho chất lượng tổng thể của quần thể không giảm.
>     ![image](./images/elitism.PNG)
>     
> ## **3. Thực thi chương trình**.
> ```
> cd src
> python3 main.py
> ```
>> ### Yêu cầu
> ```
> networkx
> numpy
> ```
>> **Installation**
>> ```
>> pip3 install networkx
>> pip3 install numpy
>> ```
> ## **4. Điều chỉnh tham số học**.
> Định nghĩa các tham số là biến toàn cục trong tệp main.py .
> ```
> POP_SIZE = 300 
> NUM_NODES = 100
> CONNECT_PROB = 0.1
> MUT_PROB = 0.3
> STOPPING_COUNT = 10
> K_IND = int(POP_SIZE * 0.1)
> ```
> Ta có thể điều chỉnh các tham số bằng cách sửa đổi giá trị của chúng.
> 
> ## **5. Tài liệu tham khảo**.
>> ### Genetic algorithm and graph partitioning
>> (Paper link: https://ieeexplore.ieee.org/abstract/document/508322)

> 
