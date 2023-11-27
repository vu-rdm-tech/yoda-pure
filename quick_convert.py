import json
from bs4 import BeautifulSoup
import os
import glob
from datetime import datetime



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
    root.append(get_persons(data)) # TODO

    # organisations - NA (The internal organisations related to the dataset)
    
    # managingOrganisation - NA (The managing organisation of the dataset, this must always be an internal organisation)
        
    # DOI - This is not in the metadata.json, but needs to be read from the irods metadata
    
    # physicalDatas - NA
    
    # availableDate - This is not in the metadata.json, but needs to be read from the irods metadata
    
    # publisher - Always set to 'Vrije Universiteit Amsterdam'
    root.append(get_publisher())
    
    # openAccess - Data_Access_Restriction (token from the classification scheme /dk/atira/pure/core/openaccesspermission)
    root.append(get_classification(data))
    
    # embargoPeriod - Embargo_End_Date (The embargo period for the dataset if access option is embargoed, value is in number of months)
    if 'Embargo_End_Date' in data:
        root.append(get_embargoPeriod(data))
    
    # constraints - NA (The legal and ethical constraints on the use of the dataset)
    
    # keywords - Keyword (Tag in 1.8) and Discipline? (Keywords of the dataset)
    root.append(get_keywords(data))
    
    # links - ? relations ? (The links to the dataset)
    
    # license - license (The license of the dataset)

    # documents - NA
    
    # relatedProjects
    # relatedEquipments
    # relatedStudentThesis
    # relatedPublications
    # relatedActivities
    # relatedDatasets
    
    # visibility - Published/Unpublished?
    
    # workflow - NA (Used to set the workflow state of the dataset (Workflow states: entryInProgress, forValidation, validated NOTE workflow is disabled by default, therefore it must be enabled in Pure if values are present in this tag)


def get_tempporalCoverage(data):
    startdate = datetime.strptime(data['Covered_Period']['Start_Date'], '%Y-%m-%d')
    enddate = datetime.strptime(data['Covered_Period']['End_Date'], '%Y-%m-%d')
    xmlstr = f"""<v1:temporalCoverage>
        <v3:from>
            <v3:year>
                {startdate.year}
            </v3:year>
            <v3:month>
                {startdate.month}
            </v3:month>
            <v3:day>
                {startdate.day}
            </v3:day>
        </v3:from>
        <v3:to>
            <v3:year>
                {enddate.year}
            </v3:year>
            <v3:month>
                {enddate.month}
            </v3:month>
            <v3:day>
                {enddate.day}
            </v3:day>
        </v3:to>
        </v1:temporalCoverage>"""
    return BeautifulSoup(xmlstr, features="xml")


def get_productionDate(data):
    startdate = datetime.strptime(data['Collected']['Start_Date'], '%Y-%m-%d')
    enddate = datetime.strptime(data['Collected']['End_Date'], '%Y-%m-%d')
    xmlstr = f"""<v1:productionDate>
        <v3:from>
            <v3:year>
                {startdate.year}
            </v3:year>
            <v3:month>
                {startdate.month}
            </v3:month>
            <v3:day>
                {startdate.day}
            </v3:day>
        </v3:from>
        <v3:to>
            <v3:year>
                {enddate.year}
            </v3:year>
            <v3:month>
                {enddate.month}
            </v3:month>
            <v3:day>
                {enddate.day}
            </v3:day>
        </v3:to>
        </v1:productionDate>"""
    return BeautifulSoup(xmlstr, features="xml")


def get_geographicalCoverages(data):
    tag = soup.new_tag('v1:geographicalCoverages')
    for place in data['Covered_Geolocation_Place']:
        subtag = soup.new_tag('v1:geographicalCoverage')
        subtag.string = place
        tag.append(subtag)
    return tag


def get_title(data):
    tag = soup.new_tag('v1:title')
    tag.string = data['Title']
    return tag


def get_description(data):
    tag = soup.new_tag('v1:description')
    tag.string = data['Description']
    return tag


def get_persons(data):
    tag = soup.new_tag('v1:persons')
    # TODO - Creator and Contributor
    return tag


def get_publisher():
    tag = soup.new_tag('v1:publisher')
    tag.string = 'Vrije Universiteit Amsterdam'
    return tag


def get_classification(data):
    tag = soup.new_tag('v1:openAccess')
    # needs a mapping
    tag.string = data['Data_Access_Restriction']
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
        
        # Perform your desired operations on the JSON data here
        # For example, convert to XML using BeautifulSoup
        
        # Example code to convert JSON to XML using BeautifulSoup
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
            xml.write(str(pretty_xml))
        n += 1