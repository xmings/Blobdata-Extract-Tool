--
-- SQL*UnLoader: Fast Oracle Text Unloader (GZIP), Release 3.0.1
-- (@) Copyright Lou Fangxin (AnySQL.net) 2004 - 2010, all rights reserved.
--
--  CREATE TABLE wms_cs (
--    DUMMY VARCHAR2(1)
--  );
--
OPTIONS(BINDSIZE=2097152,READSIZE=2097152,ERRORS=-1,ROWS=50000)
LOAD DATA
INFILE 'd:\python\eal\expdatafile.txt' "STR X'0a'"
APPEND INTO TABLE wms_cs
FIELDS TERMINATED BY X'3b3b3b3b' TRAILING NULLCOLS 
(
  "DUMMY" CHAR(1) NULLIF "DUMMY"=BLANKS
)
