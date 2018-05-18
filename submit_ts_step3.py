""" Transformation creating the job building the final mandelbrot image
"""
import json
import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
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
  job.setName('build mandelbrot')
  job.setOutputSandbox( ['*log'] )

  ## define the job workflow in 3 steps
  # job step1: setup software  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')
  # job step2: run mandelbrot build image
  job.setExecutable('./mandel4ts/build_merged_img.py')

  outputPath = os.path.join('/vo.france-grilles.fr/user',owner[0],owner,'mandelbrot/images3/final')
  outputPattern = 'merged_image.bmp'
  outputSE = 'DIRAC-USER'
  outputMetadata = json.dumps( {"application":"mandelbrot","image_format":"bmp", "image_width":7680, "image_height":4200, "owner":owner} )

  # job step3: upload data and set metadata
  job.setExecutable( './mandel4ts/dirac-add-files.py', arguments = "%s '%s' %s '%s'" % (outputPath, outputPattern, outputSE, outputMetadata ) )
  
  ########################################
  # Transformation definition
  ########################################
  t = Transformation()

  t.setTransformationName( owner+'_step3' )
  t.setType( "DataReprocessing" ) 
  t.setDescription( "Merge mandelbrot images production" )
  t.setLongDescription( "Merge mandelbrot images production" )
  t.setGroupSize( 3 ) # group input files
  # set the job workflow to the transformation
  t.setBody ( job.workflow.toXML() )

  # define input data by metadata query
  inputMetaquery = json.dumps( {"application":"mandelbrot","image_format":"ascii", "image_width":7680, "image_height":1400, "owner":owner} )
  t.setFileMask(inputMetaquery) 

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
