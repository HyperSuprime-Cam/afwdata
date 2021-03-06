#!/usr/bin/env python

"""Convert from multi-file to multi-extension.
"""

from astropy.io import fits
import sys
import os

suffix = "_%s.fits"


def main(names):
    baseNames = []
    for name in names:
        if name.endswith(suffix % "img"):
            baseNames.append(name[0:len(name) - len(suffix % "img")])
        elif not name.endswith("fits") and os.path.exists(name + suffix % "img"):
            baseNames.append(name)
    for baseName in baseNames:
        imgName = baseName + suffix % "img"
        mskName = baseName + suffix % "msk"
        varName = baseName + suffix % "var"
        miName = baseName + ".fits"
        if os.path.exists(imgName) and os.path.exists(mskName) and os.path.exists(varName):
            print("Converting '%s_(img|mask|var).fits' to '%s.fits'" % (baseName, baseName))
            imgFits = fits.open(imgName, do_not_scale_image_data=True)
            mskFits = fits.open(mskName, do_not_scale_image_data=True)
            varFits = fits.open(varName, do_not_scale_image_data=True)
            assert(len(imgFits) == 1)
            assert(len(mskFits) == 1)
            assert(len(varFits) == 1)
            imgHdu = fits.ImageHDU(data=imgFits[0].data, header=imgFits[0].header)
            imgHdu.header["EXTTYPE"] = "IMAGE"
            mskHdu = fits.ImageHDU(data=mskFits[0].data, header=mskFits[0].header)
            mskHdu.header["EXTTYPE"] = "MASK"
            varHdu = fits.ImageHDU(data=varFits[0].data, header=varFits[0].header)
            varHdu.header["EXTTYPE"] = "VARIANCE"
            miFits = fits.HDUList([fits.PrimaryHDU(), imgHdu, mskHdu, varHdu])
            if os.path.exists(miName):
                os.remove(miName)
            miFits.writeto(miName)
            imgFits.close()
            mskFits.close()
            varFits.close()
            os.remove(imgName)
            os.remove(mskName)
            os.remove(varName)
        else:
            print("Images with base name '%s' not found; skipping." % baseName)


if __name__ == "__main__":
    main(sys.argv[1:])
