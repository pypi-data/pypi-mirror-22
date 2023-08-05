/*---------------------------------------------------------------------------*\
** $Author: saulius $
** $Date: 2011-03-08 20:45:40 +0200 (Tue, 08 Mar 2011) $ 
** $Revision: 1590 $
** $URL: svn://www.crystallography.net/cod-tools/trunk/src/externals/cexceptions/stdiox.h $
\*---------------------------------------------------------------------------*/

#ifndef _STDIOX_H
#define _STDIOX_H

#include <stdio.h>
#include <cexceptions.h>

extern void *stdiox_subsystem;

typedef enum {
  STDIOX_OK = 0,
  STDIOX_FILE_OPEN_ERROR,
  STDIOX_FILE_CLOSE_ERROR,

  STDIOX_ERROR_last
} STDIOX_ERROR;

FILE *fopenx( const char *filename, const char *mode, cexception_t *ex );
void fclosex( FILE *file, cexception_t *ex );

#endif
