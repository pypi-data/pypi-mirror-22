/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2012-01-21 15:27:56 +0200 (Sat, 21 Jan 2012) $ 
**$Revision: 1898 $
**$URL: svn://www.crystallography.net/cod-tools/trunk/src/components/codcif/yy.c $
\*---------------------------------------------------------------------------*/

/* exports: */
#include <yy.h>

/* uses: */
#include <stdio.h>
#include <stdarg.h>

void yyerrorf( const char *message, ... )
{
    static char buffer[200];
    va_list ap;
    va_start(ap, message);
 
#ifdef _GNU_SOURCE
    vsnprintf( buffer, sizeof(buffer), message, ap );
#else
    vsprintf( buffer, message, ap );
#endif

    yyerror( buffer );
    va_end(ap);
}

void yyverrorf( const char *message, va_list ap )
{
    static char buffer[200];
 
#ifdef _GNU_SOURCE
    vsnprintf( buffer, sizeof(buffer), message, ap );
#else
    vsprintf( buffer, message, ap );
#endif

    yyerror( buffer );
    va_end(ap);
}
