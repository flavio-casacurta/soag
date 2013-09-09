      *----------------------------------------------------------------*
      *  WORKING COMUM A TODOS OS MODULOS COORDENADORES                *
      *----------------------------------------------------------------*
       01  WRK-CONTROLES-AUXILIARES.
           03      WRK-MODULO               PIC  X(08) VALUE SPACES.
           03      WRK-LENGTH               PIC S9(05) COMP-3 VALUE +0.
           03      WRK-IDX                  PIC S9(09) COMP VALUE +0.
           03      WRK-ABCODE               PIC  X(04) VALUE SPACES.
           03      WRK-CURRENT-TIMESTAMP    PIC  X(26).
      *----------------------------------------------------------------*
      *            COMMAREA DE GESTOR DAS AREAS DE MEMORIA
      *----------------------------------------------------------------*
       01  WRK-COPY-GAM.
           COPY 'I#FRWK04'.
      *----------------------------------------------------------------*
      *            BLOCO DE INFORMACOES DA SESSAO
      *----------------------------------------------------------------*
       01  WRK-AREA-FRWKWAAA.
           COPY FRWKWAAA.
       01  WRK-AREA-FRWKEL83.
           COPY I#FRWK83.
      *----------------------------------------------------------------*
       01  WRK-AREA-GAM.
           COPY IMAGW12W.
