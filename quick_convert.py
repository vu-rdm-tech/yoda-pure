import json
from bs4 import BeautifulSoup
import os
import glob
from datetime import datetime
import lxml
import pretty

INTERNAL_AFFILIATION_NAME = 'Vrije Universiteit Amsterdam'


def convert_to_dataset_xml(data, root):
    # title - Title
    root.append(get_title(data))
    
    # translatedTitles - NA
    
    # description - Description
    root.append(get_description(data))
    
    # ids - TODO
    
    # additionalDescriptions - NA
    
    # temporalCoverage - Covered_Period
    if 'Start_Date' in data['Covered_Period']:
        root.append(get_tempporalCoverage(data))
        
    # productionDate - Collected
    if 'Start_Date' in data['Collected']:
        root.append(get_productionDate(data))
        
    # geographicalCoverages - Covered_Geolocation_Place (multiple)
    if 'Covered_Geolocation_Place' in data:	
        root.append(get_geographicalCoverages(data))
    
    # persons - Creator (multiple) and Contributor (multiple)
    root.append(get_persons(data)) # TODO orcids

    # organisations - NA, or always VU?? (The internal organisations related to the dataset)
    
    
    # managingOrganisation - NA (The managing organisation of the dataset, this must always be an internal organisation)
    # If the organisation is an internal organisation in Pure, then the lookupId attribute must be used.
    root.append(get_managing_organisation(data)) # TODO
    
    
    # DOI - This is not in the metadata.json, but needs to be read from the irods metadata
    
    # physicalDatas - NA (refers to physical objects)
    
    # availableDate - This is not in the metadata.json, but needs to be read from the irods metadata
    root.append(get_availableDate(data))
    
    # publisher - Always set to 'Vrije Universiteit Amsterdam'
    root.append(get_publisher())
    
    # openAccess - Data_Access_Restriction (token from the classification scheme /dk/atira/pure/core/openaccesspermission)
    root.append(get_classification(data)) # needs a mapping but I don't know what the expected values are
    
    # embargoPeriod - Embargo_End_Date (The embargo period for the dataset if access option is embargoed, value is in number of months)
    if 'Embargo_End_Date' in data:
        root.append(get_embargoPeriod(data))
    
    # constraints - NA (The legal and ethical constraints on the use of the dataset)
        
    # keywords - Keyword (Tag in 1.8) and Discipline? (Keywords of the dataset)
    root.append(get_keywords(data))
    
    # links - ? relations ? (The links to the dataset)
    
    # license - license (The license of the dataset)
    root.append(get_license(data)) # TO DO needs to match '[^\p{C}\{Z}]]'

    # documents - NA
    
    # relatedProjects
    # relatedEquipments
    # relatedStudentThesis
    # relatedPublications
    # relatedActivities
    # relatedDatasets
    
    # visibility - Published/Unpublished? 
    
    # workflow - NA (Used to set the workflow state of the dataset (Workflow states: entryInProgress, forValidation, validated NOTE workflow is disabled by default, therefore it must be enabled in Pure if values are present in this tag)

def get_managing_organisation(data):
    tag = soup.new_tag('v1:managingOrganisation')
    tag['lookupId'] = 'VU' # TODO lookupId
    return tag

def get_availableDate(data):
    tag = soup.new_tag('v1:availableDate')
    yeartag = soup.new_tag('v3:year')
    yeartag.string = '2023' # TODO get date from irods metadata
    tag.append(yeartag)
    return tag


def get_license(data):	
    tag = soup.new_tag('v1:license')
    tag.string = data['License'] # TODO needs to match Pure token
    return tag


def get_tempporalCoverage(data):
    startdate = datetime.strptime(data['Covered_Period']['Start_Date'], '%Y-%m-%d')
    enddate = datetime.strptime(data['Covered_Period']['End_Date'], '%Y-%m-%d')
    tag = soup.new_tag('v1:temporalCoverage')
    
    fromtag = soup.new_tag('v1:from')
    yeartag = soup.new_tag('v3:year')
    yeartag.string = str(startdate.year)
    fromtag.append(yeartag)
    monthtag = soup.new_tag('v3:month')
    monthtag.string = str(startdate.month)
    fromtag.append(monthtag)
    daytag = soup.new_tag('v3:day')
    daytag.string = str(startdate.day)
    fromtag.append(daytag)
    tag.append(fromtag)
    
    totag = soup.new_tag('v1:to')
    yeartag = soup.new_tag('v3:year')
    yeartag.string = str(enddate.year)
    totag.append(yeartag)
    monthtag = soup.new_tag('v3:month')
    monthtag.string = str(enddate.month)
    totag.append(monthtag)
    daytag = soup.new_tag('v3:day')
    daytag.string = str(enddate.day)
    totag.append(daytag)
    tag.append(totag)
    return tag

def get_productionDate(data):
    startdate = datetime.strptime(data['Collected']['Start_Date'], '%Y-%m-%d')
    enddate = datetime.strptime(data['Collected']['End_Date'], '%Y-%m-%d')
    tag = soup.new_tag('v1:productionDate')
    
    fromtag = soup.new_tag('v1:from')
    yeartag = soup.new_tag('v3:year')
    yeartag.string = str(startdate.year)
    fromtag.append(yeartag)
    monthtag = soup.new_tag('v3:month')
    monthtag.string = str(startdate.month)
    fromtag.append(monthtag)
    daytag = soup.new_tag('v3:day')
    daytag.string = str(startdate.day)
    fromtag.append(daytag)
    tag.append(fromtag)
    
    totag = soup.new_tag('v1:to')
    yeartag = soup.new_tag('v3:year')
    yeartag.string = str(enddate.year)
    totag.append(yeartag)
    monthtag = soup.new_tag('v3:month')
    monthtag.string = str(enddate.month)
    totag.append(monthtag)
    daytag = soup.new_tag('v3:day')
    daytag.string = str(enddate.day)
    totag.append(daytag)
    tag.append(totag)
    return tag

def get_geographicalCoverages(data):
    tag = soup.new_tag('v1:geographicalCoverages')
    n = 0
    for place in data['Covered_Geolocation_Place']:
        subtag = soup.new_tag('v1:geographicalCoverage')
        subtag['id'] = f'place{n}'
        gc = soup.new_tag('v1:geographicalCoverage')
        gc.string = place
        subtag.append(gc)
        tag.append(subtag)
        n += 1
    return tag


def get_title(data):
    tag = soup.new_tag('v1:title')
    tag.string = data['Title']
    return tag


def get_description(data):
    tag = soup.new_tag('v1:description')
    tag.string = data['Description']
    return tag


def get_person(yoda_person, id, is_creator=False, is_contact_person=False):
    internal = False
    affiliation_list = []
    for affiliation in yoda_person['Affiliation']:
        if 'Affiliation_Name' not in affiliation: # default-2
            affiliation_list.append(affiliation)
            if affiliation == INTERNAL_AFFILIATION_NAME: 
                internal = True
        else: # default-3
            affiliation_list.append(affiliation['Affiliation_Name'])
            if affiliation['Affiliation_Name'] == INTERNAL_AFFILIATION_NAME: 
                internal = True
    
    tag = soup.new_tag('v1:person')
    tag['id'] = id
    if is_contact_person:
        tag['contactPerson'] = 'true'
    persontag = soup.new_tag('v1:person')
    tag.append(persontag)

    firstnametag = soup.new_tag('v1:firstName')
    firstnametag.string = yoda_person['Name']['Given_Name']
    persontag.append(firstnametag)
    lastnametag = soup.new_tag('v1:lastName')
    lastnametag.string = yoda_person['Name']['Family_Name']
    persontag.append(lastnametag)
    if not internal:
        persontag['origin'] = 'external'
        organisationstag = soup.new_tag('v1:organisations')
        tag.append(organisationstag)
        for affiliation in affiliation_list:
            organisationtag = soup.new_tag('v1:organisation')
            orgnametag = soup.new_tag('v1:name')
            orgnametag.string = affiliation
            organisationtag.append(orgnametag)
            organisationstag.append(organisationtag)
    roletag = soup.new_tag('v1:role')
    if is_creator:
        roletag.string = 'creator'
    else:
        roletag.string = 'contributor'
    tag.append(roletag)
    return tag


def get_persons(data):
    tag = soup.new_tag('v1:persons')
    # TODO - Creator and Contributor
    # person - NA (The person Pure ID)
    # role - ? (The role of the person in the dataset)
    # organisation - NA (The internal organisations related to the dataset through the internal person)
    # associationStartDate - NA (The date when the person association to the dataset started)
    # associationEndDate - NA (The date when the person association to the dataset ended)
    # id - ? (ID of the developer, this must be unique for each internal person)
    # contactPerson - First Yoda creator (Indicates whether this person is the contact person for the dataset. Only ONE person can be the contact person and it has to be an INTERNAL person. Setting this attribute on multiple persons will result in errors.)
    
    # waar komen de ORCIDS?
    # Kunnen we iets met ROR?
    
    n = 0
    for creator in data['Creator']:
        is_contact_person = False
        if n == 0:
            is_contact_person = True
        persontag = get_person(creator, f'person{n}',is_creator=True, is_contact_person=is_contact_person)
        tag.append(persontag)
        n += 1
    for contributor in data['Contributor']:
        print(contributor)
        if 'Given_Name' in contributor['Name']:
            persontag = get_person(contributor, f'person{n}', is_creator=False)
            tag.append(persontag)
        n += 1
    return tag


def get_publisher():
    tag = soup.new_tag('v1:publisher')
    nametag = soup.new_tag('v1:name')
    nametag.string = 'Vrije Universiteit Amsterdam'
    tag.append(nametag)
    return tag


def get_classification(data):
    tag = soup.new_tag('v1:openAccess')
    # needs a mapping
    tag.string = data['Data_Access_Restriction'].split(' ')[0]
    return tag


def get_embargoPeriod(data):
    tag = soup.new_tag('v1:embargoPeriod')
    enmbargodate = datetime.strptime(data['Embargo_End_Date'], '%Y-%m-%d')
    now = datetime.now()
    print(enmbargodate.year, now.year, enmbargodate.month, now.month)
    tag.string = str((enmbargodate.year - now.year) * 12 + enmbargodate.month - now.month)
    return tag


def get_keywords(data):
    tag = soup.new_tag('v1:keywords')
    if 'Keyword' in data:
        for keyword in data['Keyword']:
            subtag = soup.new_tag('v1:keyword')
            subtag.string = keyword
            tag.append(subtag)
    elif 'Tag' in data:
        for keyword in data['Tag']:
            subtag = soup.new_tag('v1:keyword')
            subtag.string = keyword
            tag.append(subtag)
    return tag




def validate_xml(xml_file):
    
    return True


# Specify the directory path
directory = 'yoda_metadata_files/vu'

# Use glob to find all JSON files in the directory and its subdirectories
json_files = glob.glob(os.path.join(directory, '**/*.json'), recursive=True)

# Process each JSON file
n = 1
for json_file in json_files:
    with open(json_file) as file:
        data = json.load(file)
        
        xml = """
            <v1:datasets xmlns:v1="v1.dataset.pure.atira.dk" xmlns:v3="v3.commons.pure.atira.dk">
                <v1:dataset id="dataset1" type="dataset">
                </v1:dataset>
            </v1:datasets>
        """
        soup = BeautifulSoup(xml, features="xml")
        root = soup.find('v1:dataset')
        convert_to_dataset_xml(data, root)
        
        # Save the XML data to a file
        xml_file = os.path.splitext(json_file)[0] + '.xml'
        pretty_xml = soup.prettify()
        with open(xml_file, 'w') as xml:
            #xml.write(str(pretty_xml))
            xml.write(str(soup))

        n += 1