""" Submit mandelbrot job
"""

from DIRAC.Core.Base import Script
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s first_line factor' % Script.scriptName,
                                     '\ne.g: %s 1'% Script.scriptName,
                                     ] ) )

Script.parseCommandLine()

import DIRAC
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac

def submitWMS( args ):

  first_line = args[0]

  job = Job()
  dirac = Dirac()

  job.setName('mandelbrot')
  
  job.setExecutable('git clone https://github.com/bregeon/mandel4ts.git')

  job.setExecutable('./mandel4ts/mandelbrot.py',arguments="-P 0.0005 -M 1000 -L %s -N 200" % first_line)
                    
  job.setOutputData( ['data_*.bmp','data*.txt'])

  res = dirac.submit(job)

  return res

#########################################################
if __name__ == '__main__':

  args = Script.getPositionalArgs()
  if ( len( args ) != 1 ):
    Script.showHelp()
  try:
    res = submitWMS( args )
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
    else:
      DIRAC.gLogger.notice( 'Submitted job: %s' % res['Value'] )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
