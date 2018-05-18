#!/usr/bin/env python
"""
  Transformation removing intermediate mandelbrot images
"""

import json

from DIRAC.Core.Base import Script
Script.parseCommandLine()
import DIRAC
from DIRAC.TransformationSystem.Client.Transformation import Transformation

def submitTS():

  ########################################
  # Modify here with your dirac username 
  owner = 'user02'
  ########################################

  ########################################
  # Transformation definition
  ########################################
  t = Transformation( )

  t.setTransformationName( owner+'_step4' )
  t.setType("Removal")
  t.setDescription("Remove intermediate mandelbrot images")
  t.setLongDescription( "Remove intermediate mandelbrot images" ) 
  # set the request to be executed
  t.setBody ( "Removal;RemoveFile" ) # Mandatory (the default is a ReplicateAndRegister operation)

  # define input data by metadata query
  inputMetaquery = json.dumps( {"application":"mandelbrot","image_format":"ascii","owner":owner} )
  t.setFileMask(inputMetaquery) 

  ########################################
  # Transformation submission
  ########################################
  res = t.addTransformation()  
  if not res['OK']:
    print(res['Message'])
    DIRAC.exit( -1 )

  t.setStatus("Active")
  t.setAgentType("Automatic")
  
  return res

if __name__ == '__main__':

  try:
    res = submitTS()
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
    


