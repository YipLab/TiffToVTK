from pyevtk.hl import imageToVTK
#import dicom
import fnmatch
import os
import sys
import numpy as np
#import tifffile 
import glob as gb 
import operator
from scipy.ndimage import zoom
import javabridge as jv
import bioformats as bf
import matplotlib.pyplot as pp
jv.start_vm(class_path=bf.JARS)
pp.ion()


def ReadStackSize(NameTif):
    rdr = bf.ImageReader(NameTif, perform_init=True)
    Meta = bf.get_omexml_metadata(NameTif)
    md = bf.omexml.OMEXML(Meta)
    pixels = md.image().Pixels
    TempStack = False
    VolumeStack = False
    Xsize_f, Ysize_f = pixels.SizeX, pixels.SizeY
    if (pixels.SizeT > 1):
        TempStack = True    
        StackLength = pixels.SizeT
    elif (pixels.SizeZ > 1):
        VolumeStack = True
        StackLength = pixels.SizeZ
    else: 
        print(FilesOnFold)
        sys.exit("\n\n Selected file is not a Stack \n\n")

    return rdr,TempStack,StackLength,Xsize_f, Ysize_f;

def ReadImageSlice(rdrImg,Slice,TempStack):
    if TempStack:
        img = rdrImg.read(t=Slice,rescale=False)
    else:
        img = rdrImg.read(z=Slice,rescale=False)
    
    return img;

def GenVTK(XCrop, YCrop, XYScale):
    Names=sorted(gb.glob('*.tif'))
    for kat in Names:
        print(kat)
        Idx = 0
        rdr1, TempStack1, Zsize, Xsize, Ysize = ReadStackSize(kat)#rdr,TempStack,StackLength  #Zsize=ReadStackSize()
        XPart, YPart = Xsize*XCrop/100, Ysize*YCrop/100
        Vol=np.zeros([XPart-1, YPart-1, Zsize])
        for katSlc in np.arange(Zsize):
            Pix=ReadImageSlice(rdr1,katSlc,TempStack1)
            ##pp.matshow(Pix)
            ##raw_input("press enter")
            ##pp.close()
            Pix=zoom(Pix, XYScale*0.01)
            Vol[:,:,Idx]=Pix[1:XPart,1:YPart]
            #print(Idx)
            #pp.matshow(Pix[1:XPart,1:YPart])
            #raw_input("press enter")
            #pp.close()
            Idx+=1
        FoldOut=kat[0:-4]
        imageToVTK("VTK_"+FoldOut, cellData = {"Fluorescence Signal" : Vol} )
        print("VTK_"+FoldOut)
    return Vol;


    #patata
    #imageToVTK("./VTKimage", cellData = {"Scattering" : Vol} )
 #TempFileprefix


os.chdir(sys.argv[1])
#FoldTempFile=sys.argv[1]
TempFileprefix='VTK'
NameMatch='*_OCT'
matches = []
foldNum = []
XKeep = raw_input('enter percentage to keep along the X direction:')
YKeep = raw_input('enter percentage to keep along the Y direction:')
XYScale = raw_input('enter percentage to scale XY plane:')
XKeep=int(XKeep)
YKeep = int(YKeep)
XYScale = int(XYScale)
##patata
VolOut=GenVTK(XKeep,YKeep,XYScale)
 
