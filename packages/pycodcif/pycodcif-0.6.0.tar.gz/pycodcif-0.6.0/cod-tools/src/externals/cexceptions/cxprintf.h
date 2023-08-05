/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2011-03-08 20:45:40 +0200 (Tue, 08 Mar 2011) $ 
**$Revision: 1590 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/externals/cexceptions/cxprintf.h $
\*---------------------------------------------------------------------------*/

#ifndef __CEX_REPORT_H
#define __CEX_REPORT_H

#include <stdarg.h>

const char* cxprintf( const char * format, ... );
const char* vcxprintf( const char * format, va_list args );

#endif
