# recherche_LODA

```python
def recherche_LODA(
    text_id: str = "",
    search: str = None,
    champ: str = "NUM_ARTICLE",
    type_recherche: str = "EXACTE",
    fond: str = "LODA_DATE",
    nature: List = ["LOI", "ORDONNANCE", "DECRET", "ARRETE"],
    date_signature: List = None,
    formatter: bool = False,
    page_number: int = 1,
    page_size: int = 10,
    *args,
)
```

Recherche dans les lois, ordonnances, décrets et arrêtés.