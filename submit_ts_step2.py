""" Transformation creating merge mandelbrot jobs
"""
import json

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.TransformationSystem.Client.Transformation import Transformation

def submitTS():

  job = Job()
  job.setName('merge mandelbrot')
  job.setOutputSandbox( ['*log'] )
  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  job.setExecutable('./mandel4ts/merge_data.py')
 
  outputPath = '/vo.france-grilles.fr/user/l/larrabito/mandelbrot/images/merged'
  outputPattern = 'data_merged*txt'
  outputSE = 'DIRAC-USER'
  outputMetadata = json.dumps( {"application":"mandelbrot","image_type":"merged","owner":"larrabito"} )

  job.setExecutable( './mandel4ts/dirac-add-files.py', arguments = "%s '%s' %s '%s'" % (outputPath, outputPattern, outputSE, outputMetadata ) )
  
  t = Transformation()
  
  t.setType( "DataReprocessing" ) 
  t.setDescription( "Merge mandelbrot images production" )
  t.setLongDescription( "Merge mandelbrot images production" )
  t.setGroupSize( 7 ) 
  t.setBody ( job.workflow.toXML() )

  inputMetaquery = json.dumps( {"application":"mandelbrot","image_type":"raw","owner":"larrabito"} )
  t.setFileMask(inputMetaquery) # catalog query is defined here

  res = t.addTransformation()  # Transformation is created here

  if not res['OK']:
    print(res['Message'])
    DIRAC.exit( -1 )

  t.setStatus( "Active" )
  t.setAgentType( "Automatic" )
  
  return res


#########################################################
if __name__ == '__main__':

  try:
    res = submitTS()
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
