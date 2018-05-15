""" Transformation creating merge mandelbrot jobs
"""
import json

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.TransformationSystem.Client.Transformation import Transformation
#from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient

def submitTS():
  
  # get arguments
  '''infile = args[0]
  f = open( infile, 'r' )
  infileList = []
  for line in f:
    infile = line.strip()
    if line != "\n":
      infileList.append( infile )'''
 
  job = Job()
  job.setName('merge mandelbrot')
  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  job.setExecutable('./mandel4ts/merge_data.py')
 
  outputPath = '/vo.cta.in2p3.fr/user/a/arrabito/mandelbrot/testMD/images/merged'
  outputPattern = 'data_merged*txt'
  outputSE = 'DESY-ZN-USER'
  outputMetadata = json.dumps( {"application":"mandelbrot","image_type":"merged","owner":"arrabito"} )

  job.setExecutable( './mandel4ts/dirac-add-files.py', arguments = "%s '%s' %s '%s'" % (outputPath, outputPattern, outputSE, outputMetadata ) )
  
  t = Transformation()
  #tc = TransformationClient()

  t.setType( "DataReprocessing" ) 
  t.setDescription( "Merge mandelbrot images production" )
  t.setLongDescription( "Merge mandelbrot images production" )
  t.setGroupSize( 10 ) 
  t.setBody ( job.workflow.toXML() )

  inputMetaquery = json.dumps( {"application":"mandelbrot","image_type":"raw","owner":"arrabito"} )
  t.setFileMask(inputMetaquery) # catalog query is defined here

  res = t.addTransformation()  # Transformation is created here

  if not res['OK']:
    print(res['Message'])
    DIRAC.exit( -1 )

  t.setStatus( "Active" )
  t.setAgentType( "Automatic" )
  transID = t.getTransformationID()
  #tc.addFilesToTransformation(transID['Value'],infileList) # files are added here
  
  return res


#########################################################
if __name__ == '__main__':

  #args = Script.getPositionalArgs()
  #if ( len( args ) != 1):
    #Script.showHelp()
  try:
    res = submitTS()
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
