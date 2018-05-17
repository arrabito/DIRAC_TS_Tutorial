#!/usr/bin/env python
"""
  Transformation removing intermediate mandelbrot images
"""

import json

from DIRAC.Core.Base import Script
Script.parseCommandLine()
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [option|cfgfile] ... [File List] ...' % Script.scriptName,
                                     'Arguments:',
                                     '  List of Files to remove'] ) )
import DIRAC
from DIRAC.TransformationSystem.Client.Transformation import Transformation

def submitTS():

  t = Transformation( )

  t.setType("Removal")
  t.setPlugin("Standard") # Not needed. The default is 'Standard'
  t.setDescription("Remove intermediate mandelbrot images")
  t.setLongDescription( "Remove intermediate mandelbrot images" ) # Mandatory
  #t.setGroupSize( 1 )  # Here you specify how many files should be grouped within the same request, e.g. 100
  t.setBody ( "Removal;RemoveFile" ) # Mandatory (the default is a ReplicateAndRegister operation)

  inputMetaquery = json.dumps( {"application":"mandelbrot","image_type":{"in":["raw","merged"]},"owner":"larrabito"} )
  t.setFileMask(inputMetaquery) # catalog query is defined here
  
  res = t.addTransformation()  # Transformation is created here
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
    


