### What is this utility for? 

The utility was designed to convert the normal maps used in the game  [Transformers: Fall of Cybertron](https://en.wikipedia.org/wiki/Transformers:_Fall_of_Cybertron)  from its original format to the Mikk format, which is easier to work with and is supported by many 3D modeling software and more.


![alt text](https://github.com/mrglaster/normal-maps-converter/blob/main/readme_images/demo.png)

### How to use it?

1) Install [Python 3.X](https://www.python.org/downloads/)
2) Install required libraries with command

```pip install -r requirements.txt```

or

```
pip install blend_modes==2.1.0 colortrans==1.0.0 numpy==1.24.0 Pillow==9.4.0
```

3) The utility supports two modes of operation: first, we feed norm_x and norm_y textures as input, optionally write where the file will be saved (as a default setting, this is the results folder in the project folder).

Exaple:

```
normals_processor.py -xnormal RB_AirRaid_Chest_TEXSET_Color_NormX.tga -ynormal RB_AirRaid_Chest_TEXSET_Masks_NormY.tga
```

Second option, we specify the path to the folder where the norm_x and norm_y texture pairs are stored. For the program to work correctly, X and Y must have the same base names, only postfixes must differ. So, that the program correctly determines the pair, the textures must have the following naming format: ```mySuperTextureName_NormX.png``` and ```mySuperTexture_NormY.png```
As the default postfixes utility uses ```_Color_NormX```  and ```_Masks_NormY```. You can change them [if necessary] by command line arguments ```-xnpostfix```  and ```-ynpostfix```

Example: 

```
normals_processor.py -texfolder C:\Users\mrglaster\Desktop\test -xnpostfix _NormX -ynpostfix _NormY
```

### Command Line Arguments 

| Full Argunent Name<br> | Short Argument Name<br> | Type | Default Value<br>   | Description                                                                               |
| ---------------------- | ----------------------- | ---- | ------------------- | ----------------------------------------------------------------------------------------- |
| \--x_normals_file      | \-xnormal               | str  | None                | Path to X normals file                                                                    |
| \--y_normals_file<br>  | \-ynormal               | str  | None                | Path to Y normals file                                                                    |
| \--textures_folder     | \-texfolder             | str  | None                | Path to folder containing X and Y normals files                                           |
| \--x_normals_postfix   | \-xnpostfix             | str  | _Color_NormX        | Postfix for X normals. It will be used if  'you work with multiple textures in one folder |
| \--y_normals_postfix   | \-ynpostfix             | str  | _Masks_NormY        | Postfix for Y normals. It will be used if  'you work with multiple textures in one folder |
| \--output_file         | \-ofile                 | str  | results//result.png | Name of the output file                                                                   |
| \--output_folder       | \-ofolder               | str  | results             | Name of the folder in which results will be 'saved                                        |
