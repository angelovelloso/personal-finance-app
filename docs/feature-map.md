## Mapa de funcionalidades

```mermaid
flowchart TD
    classDef group fill:#bde0fe,font-size:0.9rem, font-family:Manrope, font-weight: bold, color: #003049;
    classDef item fill:#ffc8dd, font-size:0.9rem, font-family:Manrope, color: #003049;

    i("importers")
    e("exporter")
    f("features")
    class e,i,f group;

    e1("entry")
    e2("category")
    e3("accounts")

    ex1("csv")

    v1("Filter Entries")
    v2("Set Categories")
    v3("Create transfer")
    v4("Delete")

    i1("BB-CC")
    i2("...importers")

    class e1,e2,e3,v1,v2,v3,v4,i1,i2,ex1 item;

    e2 --> e1;
    e3 --> e1;

    e1 --> e;
    e1 --> f;

    e --> ex1;

    i --> e3;
    
    i1 --> i;
    i2 --> i;

    f --> v1;
    f --> v2;
    f --> v3;
    f --> v4;
```

## My to-do list

- Objective: end-to-end Classification to Conta.BB / Cartao.SICOOB
- Audit and complete BB entries for JAN, FEV and MAR

- Import improvements:
  - Avoid duplicate imports (decided to warn -> how to check? what is duplicated?)

- On category changes: change signal according category

- Parser improvements / technical debt:
  - #### OBS: The minimum is made, focus on persist NOW!
  - Parser UI is loading classes directly, must pass through api (discover how!!)

- Create other importers
  - C6 Credit Card (CSV parser) - Invert value signal (positive/negative)
  - Inter Credit Card (PDF parser?)
  - Generic CSV (for manual entries?)

## Decided not to-do (at least now!)
- Change the way transfer was record. 
  - Create "Tranfer"/model table: id_transfer, id_debt_entry, id_crt_entry
    Each transfer will have it own ID!
  Annotation: It is needed or I can made some kind of "check" at the end?

- Implement delete action (delete by database until there)