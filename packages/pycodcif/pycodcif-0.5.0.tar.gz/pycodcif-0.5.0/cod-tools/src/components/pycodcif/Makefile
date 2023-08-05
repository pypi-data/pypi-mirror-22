#---*- Makefile -*-------------------------------------------------------------
#$Author: antanas $
#$Revision: 4632 $
#$Date: 2016-05-02 16:15:40 +0300 (Mon, 02 May 2016) $
#$URL: svn://www.crystallography.net/cod-tools/trunk/makefiles/Makefile-backbone $
#------------------------------------------------------------------------------

MAKECONF_FILES = ${filter-out %~, ${wildcard Makeconf*}}

ifneq ("${MAKECONF_FILES}","")
include ${MAKECONF_FILES}
endif

all:

clean:

cleanAll distclean: clean

MAKELOCAL_FILES = ${filter-out %~, ${wildcard Makelocal*}}

ifneq ("${MAKELOCAL_FILES}","")
include ${MAKELOCAL_FILES}
endif
