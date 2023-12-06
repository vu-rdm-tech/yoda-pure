## Issues, questions 


### `ids`
_type attribute must be a token from the classification scheme /dk/atira/pure/dataset/datasetsources/dataset_
- Alle ids behalve DOI? Hier de interne id van Yoda gebruiken (ben de naam even kwijt).
### `persons`
- Is er een plek voor de ROR?
- Als `contactPerson` gebruik ik nu de eerste Yoda `creator`, dat lijkt mij ok.
#### `id` 
- Hoe refereer je aan Orcids en andere IDs in de XML? Er is een id veld, dat zegt: _ID of the developer, this must be unique for each internal person_ dat is wat cryptisch.
Voorlopig maar `"person<n>"` als id
- De XML lijkt er vanuit te gaan dat je, iig voor internen, de Pure id invult, maar die weten we niet. 
Gaat de import proberen te matchen, of moeten we op voorhand een query via de API doen om de `person`s te vinden?
#### `role`
_token from the classification scheme /dk/atira/pure/dataset/roles/dataset_
- Ik weet niet wat die tokens zijn. Waarschijnlijk wel te mappen voor `creator` en `contributor`

### `managingOrganisation`
_The managing organisation of the dataset, this must always be an internal organisation_
- Is verplicht, ik denk dat dit de afdeling van de `contactPerson` kan zijn. Dit weten we niet bij import tenzij we eerst query doen.

### `visibility`
_The visibility of the dataset_
- Dit lijkt het veld waarmee je aangeeft of de metadata in de frontend getoond mag worden. Default `public`. 
`confidential` als dit in een nog te verzinnen metadataveld aangegeven is.

### `license`
_token from the classification scheme /dk/atira/pure/dataset/documentlicenses_ 
- Yoda spelt de uit, bijv. `Creative Commons Attribution 4.0 International Public License`. Hier moet een mapping komen maar ik weet niet wat de tokens zijn.

### `openAccess`
_token from the classification scheme /dk/atira/pure/core/openaccesspermission_
- Geen idee wat Pure hier voor waardes verwacht. 

### `links`
_The links to the dataset_
- Hier de Yoda url van de dataset inzetten voor niet gepubliceerde sets? Bijv. https://portal.yoda.vu.nl/vault/?dir=%2Fvault-beta-es-aerocarb%2Fresearch-beta-es-aerocarb%5B1671795277%5D

## TO DO
### `relatedPublications` e.a.
- Een aantal van deze relaties kunnen wel gemapped worden
```
    # relatedProjects
    # relatedEquipments
    # relatedStudentThesis
    # relatedPublications
    # relatedActivities
    # relatedDatasets
```

### `DOI`
- De `yoda-metadata.json` bevat de DOI niet, die zal uit de iRODS metadata moeten komen. Die heb ik nu niet.

### `availableDate`
_The date on which the dataset was published._
- Voor `unpublished`, date of Vault dataset creation. Voor `published`, date of publishing. Beide waardes staan niet in de `yoda-metadata.json`.

### Yoda `Funding_Reference`
- Lijkt interessante info voor Pure maar ik zie niet waar ik die kwijt kan.

### pretty print
- Voor de leesbaarheid van de XML is een prettify handig, maar die van `Beautifulsoup` voegt line ends toe waardoor de XML niet meer valideert.
### valideren
- Handig als het script zelf de XML valideert. 