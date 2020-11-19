# Industrial-Group-Project
**Software analysis code for the PHYS 355 Industrial Group Project with TFP.**

The aim of the project is to characterise defects in PEM fuel cell materials produced by TFP. In particular, the presence of visually unappealing lines in the gas diffusion layers (GDL) of fuel cells has plagued particular carbon-based nonwovens manufactured by TFP. Such defects do not appear to hinder the technical performance of the GDL, yet impair the customer perception of product quality. This has called for a quantitative testing method to be devised, providing both a quantifiable determination of line severity, and a clear procedure through which future improvements can be assessed.

Various methods are explored to devise an automated and efficient testing process for batch samples. Analysis of such data is most easily achieved through automated software analysis, which can be found in its entirety on this repository. The bulk of the analysis software is written and managed by Melissa Chung, Tom Fell and Michael Revell.

To begin with, three data collection methods will be used. The first two will produce images of the samples, which the team aims to analyse using various image processing and manipulation techniques. Such techniques include line and edge detection, Hough transforms and gradient calculations. The third method will produce an array of values indicating the relative light intensity detected through the sample, which may be used to identify and measure relative maxima and minima.
