# Ontology to SMW
_**Querying an ontology in order to bring it to import to SMW**_

In virtual environment install requirements `pip install -r requirements.txt`

python script: `python ./main.py ` 



SPARQL Query for Ontology properties `query_properties.rq`:

```sparql
PREFIX dc: <http://dublincore.org/specifications/dublin-core/dcmi-terms/2012-06-14/>
PREFIX ns: <http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX bfo: <http://purl.obolibrary.org/obo/bfo/2019-08-26/bfo.owl#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX aeon: <https://github.com/tibonto/aeon#>
PREFIX obda: <https://w3id.org/obda/vocabulary#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT ?subject ?subpropertyof ?domain ?type
WHERE {
    {?subject rdf:type owl:AnnotationProperty}
    UNION {?subject rdf:type owl:ObjectProperty}
    UNION {?subject rdf:type owl:DatatypeProperty}.
    OPTIONAL {
        ?subject rdfs:subPropertyOf ?subpropertyof;
                 rdfs:domain ?domain ;
                 rdf:type ?type.
        }
    FILTER(STRSTARTS(STR(?subject), "https://github.com/tibonto/aeon#")).
}
ORDER BY ?type


```

ARQ command: `$ arq --data=aeon.ttl --query=query_properties.rq `

```
--------------------------------------------------------------------------------------------------------------------
| subject                               | subpropertyof             | domain                | type                 |
====================================================================================================================
| aeon:BFO_0000180                      |                           |                       |                      |
| aeon:CORE_ranking                     |                           |                       |                      |
| aeon:IAO_0000112                      |                           |                       |                      |
| aeon:acceptance_rate                  |                           |                       |                      |
| aeon:accepted_papers                  |                           |                       |                      |
| aeon:accepted_short_papers            |                           |                       |                      |
| aeon:definition                       |                           |                       |                      |
| aeon:event_frequency                  |                           |                       |                      |
| aeon:has_event_type                   |                           |                       |                      |
| aeon:has_external_identifier          |                           |                       |                      |
| aeon:has_fee                          |                           |                       |                      |
| aeon:has_identifier                   |                           |                       |                      |
| aeon:has_part                         |                           |                       |                      |
| aeon:is_about                         |                           |                       |                      |
| aeon:language                         |                           |                       |                      |
| aeon:logo                             |                           |                       |                      |
| aeon:metric                           |                           |                       |                      |
| aeon:metric_value                     |                           |                       |                      |
| aeon:name                             |                           |                       |                      |
| aeon:number_of_attendees              |                           |                       |                      |
| aeon:number_of_tracks                 |                           |                       |                      |
| aeon:occurs_in                        |                           |                       |                      |
| aeon:part_of                          |                           |                       |                      |
| aeon:proceedings_site_count           |                           |                       |                      |
| aeon:series_cite_count                |                           |                       |                      |
| aeon:submitted_papers                 |                           |                       |                      |
| aeon:summary                          |                           |                       |                      |
| aeon:summary_licence                  |                           |                       |                      |
| aeon:procees_translated_name          | aeon:process_name         | obo:BFO_0000015       | owl:DatatypeProperty |
| aeon:process_acronym                  | aeon:process_name         | obo:BFO_0000015       | owl:DatatypeProperty |
| aeon:process_alternative_name         | aeon:process_name         | obo:BFO_0000015       | owl:DatatypeProperty |
| aeon:process_former_name              | aeon:process_name         | obo:BFO_0000015       | owl:DatatypeProperty |
| aeon:process_name                     | aeon:name                 | obo:BFO_0000015       | owl:DatatypeProperty |
| aeon:agent_name                       | aeon:name                 | aeon:Agent            | owl:DatatypeProperty |
| aeon:city                             | aeon:location             | aeon:City             | owl:DatatypeProperty |
| aeon:contact                          | owl:topDataProperty       | aeon:ContactPerson    | owl:DatatypeProperty |
| aeon:contact_email                    | aeon:contact              | aeon:ContactPerson    | owl:DatatypeProperty |
| aeon:contact_person_name              | aeon:contact              | aeon:ContactPerson    | owl:DatatypeProperty |
| aeon:contact_phone                    | aeon:contact              | aeon:ContactPerson    | owl:DatatypeProperty |
| aeon:country                          | aeon:location             | aeon:Country          | owl:DatatypeProperty |
| aeon:abstract_deadline                | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:camera-ready_deadline            | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:deadline                         | owl:topDataProperty       | aeon:Event            | owl:DatatypeProperty |
| aeon:demo_deadline                    | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:duration                         | owl:topDataProperty       | aeon:Event            | owl:DatatypeProperty |
| aeon:end_date                         | aeon:duration             | aeon:Event            | owl:DatatypeProperty |
| aeon:event_status                     | owl:topDataProperty       | aeon:Event            | owl:DatatypeProperty |
| aeon:notofication_deadline            | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:paper_deadline                   | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:poster_deadline                  | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:previous_end_date                | aeon:end_date             | aeon:Event            | owl:DatatypeProperty |
| aeon:previous_start_date              | aeon:start_date           | aeon:Event            | owl:DatatypeProperty |
| aeon:start_date                       | aeon:duration             | aeon:Event            | owl:DatatypeProperty |
| aeon:submission_deadline              | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:tutorial_deadline                | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:workshop_deadline                | aeon:deadline             | aeon:Event            | owl:DatatypeProperty |
| aeon:event_type_other                 | owl:topDataProperty       | aeon:EventType        | owl:DatatypeProperty |
| aeon:event_fee                        | owl:topDataProperty       | aeon:Fee              | owl:DatatypeProperty |
| aeon:event_fee_currency               | aeon:event_fee            | aeon:Fee              | owl:DatatypeProperty |
| aeon:event_fee_value                  | aeon:event_fee            | aeon:Fee              | owl:DatatypeProperty |
| aeon:ID                               | owl:topDataProperty       | aeon:Identifier       | owl:DatatypeProperty |
| aeon:ID_URL                           | aeon:ID                   | aeon:Identifier       | owl:DatatypeProperty |
| aeon:ID_base_URL                      | aeon:ID                   | aeon:Identifier       | owl:DatatypeProperty |
| aeon:landing_page                     | aeon:ID                   | aeon:Identifier       | owl:DatatypeProperty |
| aeon:location                         | owl:topDataProperty       | aeon:Location         | owl:DatatypeProperty |
| aeon:organizational_name              | aeon:agent_name           | aeon:Organisation     | owl:DatatypeProperty |
| aeon:first_name                       | aeon:personal_name        | aeon:Person           | owl:DatatypeProperty |
| aeon:last_name                        | aeon:personal_name        | aeon:Person           | owl:DatatypeProperty |
| aeon:personal_name                    | aeon:agent_name           | aeon:Person           | owl:DatatypeProperty |
| aeon:coordinates                      | aeon:location             | aeon:PhysicalLocation | owl:DatatypeProperty |
| aeon:state                            | aeon:location             | aeon:State            | owl:DatatypeProperty |
| aeon:subject                          | owl:topDataProperty       | aeon:Subject          | owl:DatatypeProperty |
| aeon:venue                            | aeon:location             | aeon:Venue            | owl:DatatypeProperty |
| aeon:venue_URL                        | aeon:venue                | aeon:Venue            | owl:DatatypeProperty |
| aeon:meeting_URL                      | aeon:location             | aeon:VirtualLocation  | owl:DatatypeProperty |
| aeon:has_contact_person               | aeon:has_organizer        | obo:BFO_0000015       | owl:ObjectProperty   |
| aeon:has_internal_identifier          | aeon:has_identifier       | obo:BFO_0000015       | owl:ObjectProperty   |
| aeon:has_organizer                    | owl:topObjectProperty     | obo:BFO_0000015       | owl:ObjectProperty   |
| aeon:has_sponsor                      | owl:topObjectProperty     | obo:BFO_0000015       | owl:ObjectProperty   |
| aeon:has_committee_chair              | aeon:has_committee_member | aeon:Committee        | owl:ObjectProperty   |
| aeon:has_committee_member             | aeon:has_organizer        | aeon:Committee        | owl:ObjectProperty   |
| aeon:collocated_event_of              | aeon:part_of              | aeon:Event            | owl:ObjectProperty   |
| aeon:has_attendee                     | aeon:has_contributor      | aeon:Event            | owl:ObjectProperty   |
| aeon:has_contributor                  | owl:topObjectProperty     | aeon:Event            | owl:ObjectProperty   |
| aeon:has_finance_committee_chair      | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_finance_committee_member     | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_general_committee_chair      | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_general_committee_member     | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_keynote_speaker              | aeon:has_speaker          | aeon:Event            | owl:ObjectProperty   |
| aeon:has_local_committee_chair        | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_local_committee_member       | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_moderator                    | aeon:has_contributor      | aeon:Event            | owl:ObjectProperty   |
| aeon:has_output                       | owl:topObjectProperty     | aeon:Event            | owl:ObjectProperty   |
| aeon:has_programme_committee_chair    | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_programme_committee_member   | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_publication_committee_chair  | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_publication_committee_member | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_publicity_committee_chair    | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_publicity_committee_member   | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_reviewer                     | aeon:has_contributor      | aeon:Event            | owl:ObjectProperty   |
| aeon:has_speaker                      | aeon:has_contributor      | aeon:Event            | owl:ObjectProperty   |
| aeon:has_sponsorship_committee_chair  | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_sponsorship_committee_member | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_steering_committee_chair     | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_steering_committee_member    | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_technical_committee_chair    | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:has_technical_committee_member   | aeon:has_committee_member | aeon:Event            | owl:ObjectProperty   |
| aeon:joint_event_of                   | aeon:part_of              | aeon:Event            | owl:ObjectProperty   |
| aeon:occurs_in_city                   | aeon:occurs_in            | aeon:Event            | owl:ObjectProperty   |
| aeon:occurs_in_country                | aeon:occurs_in            | aeon:Event            | owl:ObjectProperty   |
| aeon:occurs_in_state                  | aeon:occurs_in            | aeon:Event            | owl:ObjectProperty   |
| aeon:occurs_in_venue                  | aeon:occurs_in            | aeon:Event            | owl:ObjectProperty   |
| aeon:occurs_in_virtual_place          | aeon:occurs_in            | aeon:Event            | owl:ObjectProperty   |
| aeon:part_of_series                   | aeon:part_of              | aeon:Event            | owl:ObjectProperty   |
| aeon:umbrella_event_of                | aeon:part_of              | aeon:Event            | owl:ObjectProperty   |
| aeon:has_organization_identifier      | aeon:has_identifier       | aeon:Organisation     | owl:ObjectProperty   |
| aeon:has_person_identifier            | aeon:has_identifier       | aeon:Person           | owl:ObjectProperty   |
--------------------------------------------------------------------------------------------------------------------
```

