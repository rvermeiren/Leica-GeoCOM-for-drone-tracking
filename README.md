# Development of a guidance and automatic positioning system for builder drones with a total station

Authors : [Nicolas Sorensen](@nicolassorensen) & [Rémy Vermeiren](@rvermeiren)

Promotor : [Pierre Latteur](https://uclouvain.be/fr/repertoires/pierre.latteur) & [Ramin Sadre](https://uclouvain.be/fr/repertoires/ramin.sadre)

Assistant : [Sebastien Goessens](https://uclouvain.be/fr/repertoires/sebastien.goessens)

[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Repository :

Based on the work of [Maxim Artyom](@art-mx) on this [repository](https://github.com/art-mx/leica_ros_sph)

[Trello](https://trello.com/b/cHMLdS54/m%C3%A9moire)

[Slack](https://tfebuildingwithdrones.slack.com/)

## Run

```
python27.exe measure.py
-v (verbose)
-b (big prism -- default = mini-prism)
-p "#port" (on windows if port is COM4, number is 3)

```




<!--
Plot in 3D from out.txt files:

```
./filter.py out.txt | ./plot.py
```

(ensure numpy and matplotlib are installed and the python scripts executable (chmod 777)) -->
