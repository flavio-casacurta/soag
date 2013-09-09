
      *----------------------------------------------------------------*
       2600-GRAVAR-DADOS-SAIDA         SECTION.
      *----------------------------------------------------------------*
           MOVE '2600-GRAVAR-DADOS-SAIDA'  TO WRK-PARAGRAFO.
           MOVE @APPLIDW@SIGLAPGMI-S-NREG-QTDE TO WRK-NREG-QTDE.
           MOVE @APPLIDW@SIGLAPGMI-S-NREG-QTDE TO @APPLIDW@SIGLAPGMS-NREG-QTDE.
           PERFORM VARYING WRK-IDX FROM 1 BY 1
             UNTIL WRK-IDX GREATER WRK-NREG-QTDE
@DADOSSAIDA
           END-PERFORM.
           MOVE @APPLIDW@SIGLAPGMS-HEADER TO @APPLID1200-HEADER.
           MOVE @APPLIDW@SIGLAPGMS-REGISTRO TO @APPLID1200-REGISTRO.
           PERFORM 90400-CRIAR-GAM.
      *----------------------------------------------------------------*
       2600-99-EXIT. EXIT.
      *----------------------------------------------------------------*
