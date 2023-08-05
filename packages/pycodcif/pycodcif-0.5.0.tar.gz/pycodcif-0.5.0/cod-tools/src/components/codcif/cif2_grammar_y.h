/*---------------------------------------------------------------------------*\
**$Author: andrius $
**$Date: 2017-04-12 13:39:05 +0300 (Wed, 12 Apr 2017) $ 
**$Revision: 5195 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/components/codcif/cif2_grammar_y.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF2_GRAMMAR_Y_H
#define __CIF2_GRAMMAR_Y_H

#include <cif.h>
#include <cif_options.h>
#include <cexceptions.h>

CIF *new_cif_from_cif2_file( FILE *in, char *filename, cif_option_t co,
                             cexception_t *ex );

void cif2_yy_debug_on( void );
void cif2_yy_debug_off( void );

#endif
