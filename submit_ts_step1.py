""" Transformation launching Mandelbrot jobs
"""

import json
import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.TransformationSystem.Client.Transformation import Transformation

def submitTS():

  ########################################
  # Modify here with your dirac username 
  owner = 'user02'
  ########################################

  
  ########################################
  # Job description
  ########################################
  job = Job()
  job.setName('mandelbrot raw')
  job.setOutputSandbox( ['*log'] )
  job.workflow.addParameter( Parameter( "JOB_ID", "000000", "string", "", "", True, False, "Initialize JOB_ID" ) )   

  ## define the job workflow in 3 steps
  # job step1: setup software
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  # job step2: run mandelbrot application
  job.setExecutable('./mandel4ts/mandelbrot.py',arguments="-P 0.0005 -M 1000 -L @{JOB_ID} -N 200")

  outputPath = os.path.join('/vo.france-grilles.fr/user',owner[0],owner,'mandelbrot/images/raw')
  outputPattern = 'data_*txt'
  outputSE = 'DIRAC-USER'
  outputMetadata = json.dumps( {"application":"mandelbrot","image_type":"raw","owner":owner} )

  # job step3: upload data and set metadata
  job.setExecutable( './mandel4ts/dirac-add-files.py', arguments = "%s '%s' %s '%s'" % (outputPath, outputPattern, outputSE, outputMetadata ) )

  ########################################
  # Transformation definition
  ########################################
  t = Transformation()

  t.setTransformationName( owner+'_step1' )
  t.setType( "MCSimulation" ) 
  t.setDescription( "Mandelbrot images production" )
  t.setLongDescription( "Mandelbrot images production" )
  # set the job workflow to the transformation
  t.setBody ( job.workflow.toXML() )

  ########################################
  # Transformation submission
  ########################################
  res = t.addTransformation() 

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
