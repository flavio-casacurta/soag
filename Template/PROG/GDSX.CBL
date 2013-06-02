
      *----------------------------------------------------------------*
       2400-GRAVAR-DADOS-SAIDA         SECTION.
      *----------------------------------------------------------------*
           MOVE '2400-GRAVAR-DADOS-SAIDA' TO WRK-PARAGRAFO.
@DADOSSAIDA
           MOVE @APPLIDW@SIGLAPGMS-HEADER TO @APPLID1200-HEADER.
           MOVE @APPLIDW@SIGLAPGMS-REGISTRO TO @APPLID1200-REGISTRO.
           PERFORM 90400-CRIAR-GAM.
      *----------------------------------------------------------------*
       2400-99-EXIT. EXIT.
      *----------------------------------------------------------------*
