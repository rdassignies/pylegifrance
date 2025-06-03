# JuriDecision

```python
class JuriDecision:
    def id(self) -> str
    def cid(self) -> Cid
    def eli(self) -> Eli
    def nor(self) -> Nor
    def ecli(self) -> str
    def date(self) -> datetime
    def title(self) -> str
    def long_title(self) -> str
    def text(self) -> str
    def text_html(self) -> str
    def formation(self) -> str
    def numero(self) -> str
    def jurisdiction(self) -> str
    def solution(self) -> str
    def citations(self) -> List[Dict[str, Any]]
    def at(self, date: Union[datetime, str]) -> JuriDecision
    def latest(self) -> JuriDecision
    def versions(self) -> List[JuriDecision]
    def to_dict(self) -> Dict[str, Any]
```

Représente une décision de jurisprudence avec des méthodes pour accéder à ses propriétés et versions.