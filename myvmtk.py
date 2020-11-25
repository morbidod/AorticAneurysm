# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 09:48:09 2020

@author: UTENTE
"""


from vmtk import vmtkscripts
from vmtk import pypes
import numpy as np
import os


base_dir="data"
filename="aorta_x.vtp"
CL_="_cl.vtp"
CL_RS_="_cl_rs.vtp"
CLIPPED_="_clipped.vtp"
CLIPPED_METRICS_="_clipped_metrics.vtp"
CLIPPED_MAPPING_="_clipped_mapping.vtp"
CLIPPED_PATCHING_="_clipped_patching.vtp"
CLIPPED_PATCHING_ID_="_clipped_patching_id.vtp"
CLIPPED_PATCHING_VTI_="_clipped_patching_vti.vti"
CLIPPED_PATCHING_PNG_="_clipped_patching_png.png"
CLIPPED_PATCHING_VTI_ID_="_clipped_patching_vti_id.vti"
CLIPPED_PATCHING_PNG_ID_="_clipped_patching_png_id.png"

base_file = base_dir + "/" + filename
cl_file=base_dir+"/"+filename.split(".")[0]+CL_
cl_rs_file= base_dir+"/"+filename.split(".")[0]+CL_RS_
clipped_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_
clipped_metrics_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_METRICS_
clipped_mapping_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_MAPPING_
clipped_patching_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_PATCHING_
clipped_patching_id_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_PATCHING_ID_
clipped_patching_vti_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_PATCHING_VTI_
clipped_patching_png_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_PATCHING_PNG_

clipped_patching_vti_id_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_PATCHING_VTI_ID_
clipped_patching_png_id_file=base_dir+"/"+filename.split(".")[0]+CLIPPED_PATCHING_PNG_ID_

print("cl file:",cl_file)

#extract centerlines and branch extractor
clArguments = 'vmtkcenterlines -ifile ' + base_file \
              + ' -seedselector pickpoint' \
              + ' --pipe vmtkcenterlineattributes' \
              + ' --pipe vmtkbranchextractor' \
              + ' -ofile ' + cl_file

print("Centerline Arg:",clArguments,"\n\n")
#myPype = pypes.PypeRun(clArguments)

# Bifurcation reference systems
bifArguments= 'vmtkbifurcationreferencesystems' \
             + ' -ifile '+ cl_file \
             + ' -radiusarray MaximumInscribedSphereRadius' \
             + ' -blankingarray Blanking' \
             + ' -groupidsarray GroupIds' \
             + ' -ofile '+ cl_rs_file
print("Arg:",bifArguments,"\n\n")
#myPype = pypes.PypeRun(bifArguments)

#clipping 

clipArguments='vmtkbranchclipper' \
             + ' -ifile ' + base_file \
             + ' -centerlinesfile '+ cl_file \
             + ' -groupidsarray GroupIds ' \
             + ' -radiusarray MaximumInscribedSphereRadius' \
             + ' -blankingarray Blanking' \
             + ' -ofile '+ clipped_file
print("clipArg:",clipArguments,"\n\n")
#myPype = pypes.PypeRun(clipArguments)


# Longitudinal and circumferential metrics
clippedMetricsArguments= 'vmtkbranchmetrics' \
             + ' -ifile ' + clipped_file \
             + ' -centerlinesfile '+ cl_file \
             + ' -abscissasarray Abscissas' \
             + ' -normalsarray ParallelTransportNormals' \
             + ' -groupidsarray GroupIds ' \
             + ' -centerlineidsarray CenterlineIds' \
             + ' -tractidsarray TractIds' \
             + ' -blankingarray Blanking' \
             + ' -radiusarray MaximumInscribedSphereRadius' \
             + ' -ofile '+ clipped_metrics_file
             

print("clippedMetricsArguments:",clippedMetricsArguments,"\n\n")
#myPype = pypes.PypeRun(clippedMetricsArguments) 

# METRICS MAPPING TO BRANCHES AND PATCHING
# Geometry mapping
mappingArguments= 'vmtkbranchmapping' \
             + ' -ifile ' + clipped_metrics_file \
             + ' -centerlinesfile '+ cl_file \
             + ' -referencesystemsfile '+  cl_rs_file \
             + ' -abscissasarray Abscissas' \
             + ' -normalsarray ParallelTransportNormals' \
             + ' -groupidsarray GroupIds' \
             + ' -centerlineidsarray CenterlineIds' \
             + ' -tractidsarray TractIds' \
             + ' -referencesystemsnormalarray Normal' \
             + ' -radiusarray MaximumInscribedSphereRadius' \
             + ' -blankingarray Blanking' \
             + ' -angularmetricarray AngularMetric' \
             + ' -abscissametricarray AbscissaMetric' \
             + ' -ofile '+ clipped_mapping_file            

print("clippledMappingArguments:",mappingArguments,"\n\n")
#myPype = pypes.PypeRun(mappingArguments) 

patchingArguments='vmtkbranchpatching' \
                + ' -ifile ' + clipped_mapping_file \
                +' -groupidsarray GroupIds' \
                +' -longitudinalmappingarray StretchedMapping' \
                +' -circularmappingarray AngularMetric' \
                +' -longitudinalpatchsize 0.005' \
                +' -circularpatches 20' \
                +' -ofile '+ clipped_patching_file \
                +' -patcheddatafile '+ clipped_patching_vti_file

                

print("clippledPatchingArguments:",patchingArguments,"\n\n")
myPype = pypes.PypeRun(patchingArguments) 

#patch extractor of branch 0
branchID=0
gID=str(branchID)
patchingBranchMappingArg= "vmtkbranchclipper " \
                        + "-ifile " + clipped_mapping_file \
                        + " -groupids " +gID \
                        + " -groupidsarray GroupIds" \
                        +" -blankingarray Blanking " \
                        +" -centerlinesfile " +cl_file \
                        +" -radiusarray MaximumInscribedSphereRadius " \
                        +" --pipe vmtkbranchpatching " \
                        +" -circularpatches 12 " \
                        +" -longitudinalpatchsize 0.5 " \
                        +" -longitudinalmappingarray StretchedMapping" \
                        +" -circularmappingarray AngularMetric" \
                        +" -ofile " +clipped_patching_id_file \
                        +" -patcheddatafile " + clipped_patching_vti_id_file

print("patchingBranchMappingArg:",patchingBranchMappingArg,"\n\n")
myPype = pypes.PypeRun(patchingBranchMappingArg)

viewArg="vmtksurfaceviewer -ifile " +clipped_patching_id_file
myPype = pypes.PypeRun(viewArg)

surfaceReader = vmtkscripts.vmtkSurfaceReader()
surfaceReader.InputFileName = clipped_patching_id_file
surfaceReader.Execute()

surfaceNumpyAdaptor = vmtkscripts.vmtkSurfaceToNumpy()
surfaceNumpyAdaptor.Surface = surfaceReader.Surface
surfaceNumpyAdaptor.Execute()

numpySurface = surfaceNumpyAdaptor.ArrayDict

centerlineReader = vmtkscripts.vmtkSurfaceReader()
centerlineReader.InputFileName = cl_file
centerlineReader.Execute()
clNumpyAdaptor = vmtkscripts.vmtkCenterlinesToNumpy()
clNumpyAdaptor.Centerlines = centerlineReader.Surface
clNumpyAdaptor.Execute()
numpyCenterlines = clNumpyAdaptor.ArrayDict