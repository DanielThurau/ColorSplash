## Instructions

1. Via the command line, use conda to activate the correct environment. 

>`$ conda activate colorSplash`

If Visual Studio code does not immediately select the interpreter for running, use the command palette (cmd + shift + p) and select `Python Select Interpreter` and choose `colorSplash: conda`.

I'm going to do the intial color determinartion via this tutorial: https://towardsdatascience.com/color-identification-in-images-machine-learning-application-b26e770c4c71


2. This project uses two languages due to the unsplash SDK relase. Interations with unsplash use nodejs and processing and backend logic is programmed with python.

3. To download images for processing (locally), run :
> `$ node photoRetrieval.js`

this will download images into the `images` folder.

4. To process images into a data structure (locally), run:

> `$ python python processImages.py -o data.json`

5. To use the command line to find images that match a given hex code and distance

> `$ python colorDetection.py -i data.json --hex 008000 --distance 100`

