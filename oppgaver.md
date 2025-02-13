# Oppgaver

## a) Applikasjonsnivåprotokoll

### Format
Å bruke ett json format virker som et bra utgangspunkt, siden da kan man sende meldinger i json, så lagre disse i en json-liste. Dette gjør også at man kan bruke ett python dictionary som "database".

### Meldinger

- **Post problem:**
    - Klient $\rightarrow$ Server: `"POST_PROBLEM;{problemtekst};{alternativ1,alternativ2,...}"`
    - Klient $\leftarrow$ Server: `"OK PROBLEM_ID;{id}"`
    - Eksempel:
- **Spør etter problem:**
    - Klient $\rightarrow$ Server: 
    - Klient $\leftarrow$ Server: 
    - Eksempel:  
- **Vis en problemformulering:**
    - Klient $\rightarrow$ Server: 
    - Klient $\leftarrow$ Server: 
    - Eksempel:
- **Vis alternativer:**
    - Klient $\rightarrow$ Server: 
    - Klient $\leftarrow$ Server: 
    - Eksempel:
- **Stem på alternativ:**
    - Klient $\rightarrow$ Server: 
    - Klient $\leftarrow$ Server: 
    - Eksempel: 
- **Vis stemmer på et problem:**
    - Klient $\rightarrow$ Server: 
    - Klient $\leftarrow$ Server: 
    - Eksempel: 

### Respons 

### Tilstandsløs vs tilstandsfull
Applikasjonsprotokollen er tilstandsløs, da alle meldinger inneholder all informasjonen som trengs. 

## b) Bør du bruke TCP eller UDP for denne applikasjonen?
TCP er best egnet da vi trenger pålitelig overføring av data, siden det er viktig at stemmer blir registrert riktig

## Implementer klient-server-applikasjon NVDA i python
Se `server.py` og `client.py`