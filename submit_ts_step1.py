""" Transformation launching Mandelbrot jobs
"""

import json

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Core.Workflow.Parameter import Parameter
from DIRAC.TransformationSystem.Client.Transformation import Transformation

def submitTS():

  job = Job()
  job.setName('mandelbrot raw')
  job.setOutputSandbox( ['*log'] )

  job.workflow.addParameter( Parameter( "JOB_ID", "000000", "string", "", "", True, False, "Initialize JOB_ID" ) )   
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  job.setExecutable('./mandel4ts/mandelbrot.py',arguments="-P 0.0005 -M 1000 -L @{JOB_ID} -N 200")

  outputPath = '/vo.france-grilles.fr/user/l/larrabito/mandelbrot/images/raw'
  outputPattern = 'data_*txt'
  outputSE = 'DIRAC-USER'
  metadata = json.dumps( {"application":"mandelbrot","image_type":"raw","owner":"larrabito"} )
  job.setExecutable( './mandel4ts/dirac-add-files.py', arguments = "%s '%s' %s '%s'" % (outputPath, outputPattern, outputSE, metadata ) )

  t = Transformation()

  t.setType( "MCSimulation" ) 
  t.setDescription( "Mandelbrot images production" )
  t.setLongDescription( "Mandelbrot images production" )  # mandatory
  t.setBody ( job.workflow.toXML() )

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
