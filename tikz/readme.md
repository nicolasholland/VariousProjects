Tikz Images
===========

There's an online editor [mathcha.io](https://www.mathcha.io/editor) with which
you can write latex code without writing the latex code yourself.
It even allows you to draw diagrams and export them as tikz images.

As a first tiny project with matcha.io we created a sketch of Beijings Forbidden City.

![](https://raw.githubusercontent.com/nicolasholland/VariousProjects/master/tikz/_images/diagram-forbiddencity.png)

You can draw e.g. a straight line or a rectangle in the editor and it will create the corresponding tikz code:

```
%Straight Lines 
\draw [color={rgb, 255:red, 208; green, 2; blue, 27 }  ,draw opacity=1 ]   (278.5,502.11) -- (473.5,502.11) ;


%Shape: Rectangle 
\draw  [color={rgb, 255:red, 245; green, 166; blue, 35 }  ,draw opacity=1 ] (355.5,490.11) -- (397.5,490.11) -- (397.5,511.11) -- (355.5,511.11) -- cycle ;
```

