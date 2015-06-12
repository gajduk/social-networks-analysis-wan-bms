# Bridging Online and Offline Social Networks: Multiplex Analysis

----

We study a unique dataset that looks at student friendships in real life and on Facebook. 
We consider two types of friendships: strong and weak, which are defined differently for real and Facebook friendships. 
For real friends, 5 contacts per month is considered a strong tie, while less than that but more than 5 contacts in six months is considered a weak tie.
On Facebook where communication is more frequent to friends are considered strongly connected if they communicate at least 5 times a weak.
Any less than that, but still more than 5 times a month and the Facebook friendship is considered as weak.

Based on this four types of network ties we define a multiplex network with 4 layers: strong offline, weak offline, strong online, weak online.

![alt text](https://raw.githubusercontent.com/gajduk/social-networks-analysis-wan-bms/master/results/all%20students/muxViz/bms_frchterman.png)

A visualization of the 4 layers using [MuxViz](http://muxviz.net/).

The resulting multiplex network is analysed using simple graph metrics such as reciprocity and transitivity that are expanded to mutliplex networks. For more details please see the [supporting paper](https://github.com/gajduk/social-networks-analysis-wan-bms/raw/master/suporting%20material/ASL_SOC_NET_PLOS_2.pdf).

![alt text](https://raw.githubusercontent.com/gajduk/social-networks-analysis-wan-bms/master/results/all%20students/by_metric/bms_Three%20Cycles_False.png)

Three cycles metric calculated on 6 layers of the multiplex graph (4 original, 2 aggregated). 



