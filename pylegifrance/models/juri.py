#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 10:44:53 2024

@author: raphael
"""

from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel, Field

from pylegifrance.models.constants import TypeRecherche


class DecisionsAttaquees(str, Enum):
    """Liste pour le filtre DECISION_ATTAQUEE"""

    COMMISSION_INDEMNISATION_VICTIMES_INFRACTIONS = (
        "COMMISSION_INDEMNISATION_VICTIMES_INFRACTIONS"
    )
    CONSEIL_PRUDHOMME = "CONSEIL_PRUDHOMME"
    COUR_APPEL = "COUR_APPEL"
    COUR_ASSISES = "COUR_ASSISES"
    COUR_CASSATION = "COUR_CASSATION"
    COUR_JUSTICE_REPUBLIQUE = "COUR_JUSTICE_REPUBLIQUE"
    COUR_NATIONAL_INCAPACITE_TARIFICATION = "COUR_NATIONAL_INCAPACITE_TARIFICATION"
    TRIBUNAL_AFFAIRES_SECURITE_SOCIALE = "TRIBUNAL_AFFAIRES_SECURITE_SOCIALE"
    TRIBUNAL_COMMERCE = "TRIBUNAL_COMMERCE"
    TRIBUNAL_CONTENTIEUX_INCAPACITE = "TRIBUNAL_CONTENTIEUX_INCAPACITE"
    TRIBUNAL_CORRECTIONNEL = "TRIBUNAL_CORRECTIONNEL"
    TRIBUNAL_FORCES_ARMEES = "TRIBUNAL_FORCES_ARMEES"
    TRIBUNAL_GRANDE_INSTANCE = "TRIBUNAL_GRANDE_INSTANCE"
    TRIBUNAL_INSTANCE = "TRIBUNAL_INSTANCE"
    TRIBUNAL_MARITIME_COMMERCIAL = "TRIBUNAL_MARITIME_COMMERCIAL"
    TRIBUNAL_PARITAIRE_BAUX_RURAUX = "TRIBUNAL_PARITAIRE_BAUX_RURAUX"
    TRIBUNAL_POLICE = "TRIBUNAL_POLICE"
    TRIBUNAL_PREMIERE_INSTANCE = "TRIBUNAL_PREMIERE_INSTANCE"
    TRIBUNAL_SUPERIEURS_APPEL = "TRIBUNAL_SUPERIEURS_APPEL"


class Ressort(str, Enum):
    """Liste pour le filtre APPEL_SIEGE_APPEL"""

    GRENOBLE = "GRENOBLE"
    TOULOUSE = "TOULOUSE"
    PAU = "PAU"
    AMIENS = "AMIENS"
    BASSE_TERRE = "BASSE-TERRE"
    ROUEN = "ROUEN"
    MONTPELLIER = "MONTPELLIER"
    NIMES = "NIMES"
    LYON = "LYON"
    COLMAR = "COLMAR"
    AIX_PROVENCE = "AIX-PROVENCE"
    AGEN = "AGEN"
    ST_DENIS_REUNION = "ST-DENIS-REUNION"
    BESANCON = "BESANCON"
    CAEN = "CAEN"
    NANCY = "NANCY"
    ANGERS = "ANGERS"
    BORDEAUX = "BORDEAUX"
    BASTIA = "BASTIA"
    ORLEANS = "ORLEANS"
    DIJON = "DIJON"
    CAYENNE = "CAYENNE"
    PARIS = "PARIS"
    CHAMBERY = "CHAMBERY"
    NOUMEA = "NOUMEA"
    VERSAILLES = "VERSAILLES"
    DOUAI = "DOUAI"
    RIOM = "RIOM"
    BOURGES = "BOURGES"
    PAPEETE = "PAPEETE"
    REIMS = "REIMS"
    POITIERS = "POITIERS"
    METZ = "METZ"
    LIMOGES = "LIMOGES"
    FORT_DE_FRANCE = "FORT-DE-FRANCE"
    RENNES = "RENNES"


class Formations(str, Enum):
    AVIS = "AVIS"
    ORDONNANCE_PREMIER_PRESIDENT = "ORDONNANCE_PREMIER_PRESIDENT"
    COMMISSION_REEXAMEN = "COMMISSION_REEXAMEN"
    COUR_REVISION = "COUR_REVISION"
    COMMISSION_REVISION = "COMMISSION_REVISION"
    COMMISSION_REPARATION_DETENTION = "COMMISSION_REPARATION_DETENTION"
    TRIBUNAL_CONFLIT = "TRIBUNAL_CONFLIT"
    CHAMBRE_CIVILE_1 = "CHAMBRE_CIVILE_1"
    CHAMBRE_CIVILE_3 = "CHAMBRE_CIVILE_3"
    CHAMBRE_CRIMINELLE = " CHAMBRE_CRIMINELLE"
    CHAMBRE_MIXTE = "CHAMBRE_MIXTE"
    CHAMBRE_COMMERCIALE = "CHAMBRE_COMMERCIALE"
    ASSEMBLEE_PLENIERE = "ASSEMBLEE_PLENIERE"
    CHAMBRES_REUNIES = "CHAMBRES_REUNIES"


class JuridictionJudiciaire(str, Enum):
    """liste pour filtre juridication judiciaire"""

    cour_de_cassation = "Cour de cassation"
    juridictions_appel = "Juridictions d'appel"
    juridictions_1er_degre = "Juridictions du premier degré"


class NatureDecision(str, Enum):
    avis = "avis"
    ordonnance = "ordonnance"
    arret = "arret"
    autres_decisions = "autres_decisions"


class ChampsJURI(str, Enum):
    ALL = "ALL"
    TITLE = "TITLE"
    ABSTRATS = "ABSTRATS"
    TEXTE = "TEXTE"
    RESUMES = "RESUMES"
    NUM_AFFAIRE = "NUM_AFFAIRE"


# Facettes autorisées pour CODE, LODA ...


class FacettesJURI(str, Enum):
    """Les filtres de JURI sont référencés dans le document "description-des-tris-et-filtres-de-l-pi.xlsx
    La liste ci-dessous n'en reprends qu'une partie. A ce stade, les filtres ne marchent pas
    pour le fond JURI'cassPubliBulletin'
    """

    CASSATION_TYPE_PUBLICATION_BULLETIN = "CASSATION_TYPE_PUBLICATION_BULLETIN"
    CASSATION_FORMATION = "CASSATION_FORMATION"
    JURIDICTION_JUDICIAIRE = "JURIDICTION_JUDICIAIRE"
    APPEL_SIEGE_APPEL = "APPEL_SIEGE_APPEL"
    CASSATION_NATURE_DECISION = "CASSATION_NATURE_DECISION"
    PDC_CHECKBOX_RESTREINDRE_ARRET = "PDC_CHECKBOX_RESTREINDRE_ARRET"
    PREMIER_DEGRE_TYPE_JURIDICTION = "PREMIER_DEGRE_TYPE_JURIDICTION"
    CASSATION_DECISION_ATTAQUEE = (
        "CASSATION_DECISION_ATTAQUEE"  # cf. valeurs = Juridictions
    )


# Filtres spécifiques à jURI


class JuridictionJudiciaireFiltre(BaseModel):
    facette: FacettesJURI = FacettesJURI.JURIDICTION_JUDICIAIRE
    valeurs: List[JuridictionJudiciaire]  # doit sûrement être une liste


class Publication(str, Enum):
    T = "T"
    F = "F"


class PublicationBulletinFiltre(BaseModel):
    facette: str = FacettesJURI.CASSATION_TYPE_PUBLICATION_BULLETIN
    valeurs: List[Publication] = Field(
        default=["T"]
    )  # Soit 'T' publié au bulletin soit 'F'


class FormationFiltre(BaseModel):
    pass


class CourAppelFiltre(BaseModel):
    facette: str = FacettesJURI.APPEL_SIEGE_APPEL
    valeurs: List[Ressort]


class DecisionAttaqueeFiltre(BaseModel):
    facette: FacettesJURI = FacettesJURI.CASSATION_DECISION_ATTAQUEE
    valeurs: List[DecisionsAttaquees]


class RestreindrePlanClassement(BaseModel):
    facette: FacettesJURI = FacettesJURI.PDC_CHECKBOX_RESTREINDRE_ARRET


class SortJURI(str, Enum):
    PERTINENCE = "PERTINENCE"
    DATE_DESC = "DATE_DESC"
    DATE_ASC = "DATE_ASC"


class TexteLien(BaseModel):
    cidTexte: str = Field(..., description="Identifiant du texte")
    datePubliTexte: Optional[str] = Field(
        None, description="Date de publication du texte", example="YYYY-MM-DD"
    )
    dateSignaTexte: Optional[str] = Field(
        None, description="Date de signature du texte", example="YYYY-MM-DD"
    )
    id: str = Field(..., description="Identifiant unique du lien")
    natureTexte: str = Field(..., description="Nature du texte")
    norTexte: str = Field(..., description="Numéro NOR du texte")
    num: str = Field(..., description="Numéro du texte")
    numTexte: str = Field(
        ...,
        description="Numéro du texte dans une autre nomenclature ou système de référencement",
    )
    sens: str = Field(
        ..., description="Sens du lien, par exemple 'source'", example="source"
    )
    typeLien: str = Field(
        ..., description="Type de lien, par exemple 'CITATION'", example="CITATION"
    )
    title: Optional[Union[int, str, None]] = Field(
        ..., description="Titre du texte lié, peut inclure des références législatives"
    )


class DecisionAttaquee(BaseModel):
    formation: Optional[Union[int, str, None]] = None
    date: Optional[Union[str, int]] = None


class Decision(BaseModel):
    id: str = None
    idEli: Optional[str] = None
    idEliAlias: Optional[str] = None
    origine: str = None
    nature: Optional[Union[int, str, None]] = None
    cid: Optional[str] = None
    num: Optional[str] = None
    numeroBo: Optional[str] = None
    numParution: Optional[str] = None
    juridiction: str = None
    natureJuridiction: str = None
    solution: Optional[Union[int, str, None]] = None
    numeroAffaire: List[str]
    numsequence: Optional[str] = None
    nor: Optional[str] = None
    natureQualifiee: Optional[str] = None
    natureDelib: Optional[str] = None
    datePubli: Optional[str] = None
    datePubliComputed: Optional[str] = None
    dateTexte: Optional[Union[str, int]] = None
    dateTexteComputed: Optional[Union[int, str, None]]
    dateDerniereModif: Optional[str] = None
    originePubli: Optional[Union[str, int]] = None
    publicationRecueil: str = None
    formation: Optional[Union[int, str, None]] = None
    provenance: str = None
    decisionAttaquee: DecisionAttaquee
    siegeAppel: Optional[str] = None
    president: Optional[str] = None
    avocatGl: Optional[str] = None
    avocats: Optional[Union[str, List]] = None
    rapporteur: Optional[Union[str, int]]
    commissaire: Optional[str] = None
    ecli: Optional[str] = None
    version: Optional[str] = None
    titre: str = None
    titreLong: str = None
    titreJo: Optional[str] = None
    lienJo: Optional[str] = None
    numTexteJo: Optional[str] = None
    idTexteJo: Optional[str] = None
    numJo: Optional[str] = None
    dateJo: Optional[str] = None
    idConteneur: Optional[str] = None
    urlCC: Optional[str] = None
    etat: Optional[str] = None
    dateDebut: Optional[str] = None
    dateFin: Optional[str] = None
    autorite: Optional[str] = None
    ministere: Optional[str] = None
    emetteur: Optional[str] = None
    appliGeo: Optional[str] = None
    codesNomenclatures: List[str] = []
    renvoi: Optional[str] = None
    visas: Optional[str] = None
    visasHtml: Optional[str] = None
    signataires: Optional[str] = None
    signatairesHtml: Optional[str] = None
    signataireKali: Optional[str] = None
    travauxPreparatoires: Optional[str] = None
    travauxPreparatoiresHtml: Optional[str] = None
    nota: Optional[str] = None
    notaHtml: Optional[str] = None
    texte: str = None
    texteHtml: str = None
    sommaire: List[dict] = []
    titrages: List[str] = []
    titragesKey: Optional[Union[List, None]] = []
    natureNumero: Optional[str] = None
    dateVersement: Optional[str] = None
    citationJp: Optional[str] = None
    citationJpHtml: Optional[str] = None
    liens: List[TexteLien] = []
    annePublicationBulletin: Optional[Union[int, str, None]]
    numeroPublicationBulletin: Optional[Union[int, str, None]]
    typePublicationBulletin: str
    notice: Optional[str] = None
    noticeHtml: Optional[str] = None
    inap: Optional[bool] = None
    typeTexte: Optional[str] = None
    motsCles: List[str] = []
    appellations: List[str] = []
    dossiersLegislatifs: List[str] = []
    relevantDate: Optional[Union[int, str, None]]
    typeDecision: Optional[str] = None
    typeControleNormes: Optional[str] = None
    numLoiDef: Optional[str] = None
    dateLoiDef: Optional[str] = None
    titreLoiDef: Optional[str] = None
    juridictionJudiciaire: str
    conditionDiffere: Optional[str] = None
    conteneurs: List[str] = []
    refInjection: str = None
    idTechInjection: str = None
    resume: Optional[str] = None
    resumeHtml: Optional[str] = None
    rectificatif: Optional[str] = None
    observations: Optional[str] = None
    ancienId: Optional[Union[int, str, None]]
    demandeur: Optional[str] = None
    pagePdf: Optional[str] = None
    infosRestructurationBranche: Optional[str] = None
    infosRestructurationBrancheHtml: Optional[str] = None
    descriptionFusion: Optional[str] = None
    descriptionFusionHtml: Optional[str] = None
    infosComplementaires: Optional[str] = None
    infosComplementairesHtml: Optional[str] = None
    notaSectionsAafficher: Optional[str] = None
    embedding: List[float] = None
    """
    def create_embeddings(self ,model="text-embedding-ada-002") -> List[float]:

        Crée des embeddings à partir d'un texte en utilisant l'API d'OpenAI.

        client = OpenAI()

        response = client.embeddings.create(
            input=[self.sommaire[0]['abstrats']],
            model=model
        )
        self.embedding = response.data[0].embedding
  """


# Dictionnaire des champs à inclure lors de la sérialisation
INCLUDE_SER = {
    "decisionAttaquee",
    "formation",
    "id",
    "juridiction",
    "nature",
    "num",
    "numeroPublicatonBulletin",
    "originePubli",
    "solution",
    "texte",
    "textHtml",
    "sommaire",
    "titre",
    "titreLong",
    "typePublicationBulletin",
}


class SearchJURI(BaseModel):
    search: str = Field("", description="Le texte ou les mots-clés à rechercher.")
    # publication_bulletin: List[Publication] = Field(default=[Publication.T, Publication.F], description="Si la décision a été publiée au bulletin")
    publication_bulletin: Optional[List[Publication]] = Field(
        default=None, description="Si la décision a été publiée au bulletin"
    )

    sort: SortJURI = Field(default=SortJURI.PERTINENCE)
    champ: ChampsJURI = Field(default=ChampsJURI.ALL)
    type_recherche: TypeRecherche = Field(
        default=TypeRecherche.TOUS_LES_MOTS_DANS_UN_CHAMP
    )
    page_size: int = Field(default=5)
    page_number: int = Field(default=1)
    type_pagination: str = Field(default="ARTICLE")
    formatter: bool = Field(
        default=True,
        description="Si True, n'extrait que certains champs spécifiques (cf. keys) ou par défaut (fichier de configuration)",
    )
    fetch_all: bool = Field(
        default=False, description="Si True rapatrie tous les résultats trouvés"
    )
    juri_keys: Optional[List[str]] = Field(
        default=None,
        description="Clés d'extraction des informations d'une décision de justice",
    )
    juridiction_judiciaire: Optional[List[str]] = Field(default=None)

    @classmethod
    def describe(cls) -> str:
        lines = [f"Description du modèle {cls.__name__}", ""]
        for name, field in cls.model_fields.items():
            description = field.description or "Aucune description."
            field_type = field.annotation

            lines.append(f"- Champ : {name}")
            lines.append(
                f"  Type : {field_type.__name__ if hasattr(field_type, '__name__') else str(field_type)}"
            )
            lines.append(f"  Description : {description}")

            import inspect

            if inspect.isclass(field_type) and issubclass(field_type, Enum):
                enum_vals = ", ".join(e.value for e in field_type)
                lines.append(f"  Valeurs possibles : {enum_vals}")

            lines.append("")

        return "\n".join(lines).strip()
