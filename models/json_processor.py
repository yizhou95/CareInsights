import json
from datetime import datetime
import pymysql
import os

def connect_to_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="visualization",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
# def connect_to_db():
#     try:
#         connection = pymysql.connect(
#             host='localhost',
#             database='visualization',
#             user='root',
#             password='123456'
#         )
#
#         if connection.open:
#             print("successfully connected to MySql")
#             return connection
#     except pymysql.MySQLError as e:
#         print(f"Error while connecting to MySql instance:{e}")
#         return None
#

# def load_json_file(file_path):
#     conn = connect_to_db1()  # Assuming this is your method to connect to MySQL
#     try:
#         with conn.cursor() as cursor:
#
#              with open(file_path, 'r', encoding='utf-8') as f:
#                    fhir_data = json.load(f)
#     except Exception as e:
#         print(f"Error when loading json data: {e}")
#     finally:
#         conn.close()
#         return fhir_data


def insert_patient(resource, cursor):
    # Initialize all fields to None
    patient_birthDate = None
    patient_deathDate = None
    patient_SSN = None
    patient_Drivers = None
    patient_Passport = None
    patient_Prefix = None
    patient_First = None
    patient_Last = None
    patient_Suffix = None
    patient_Maiden = None
    patient_Marital = None
    patient_Race = None
    patient_Ethnicity = None
    patient_gender = None
    patient_Birthplace = None
    patient_Address = None
    patient_City = None
    patient_Country = None
    patient_State = None
    patient_Zip = None
    patient_LAT = None
    patient_LON = None
    patient_Healthcare_expenses = None
    patient_healthcare_coverage = None

    # Extract core fields from the resource
    patient_id = resource.get("id")
    patient_birthDate = resource.get("birthDate")
    patient_deathDate = resource.get("deathDate")

    # Extract identifiers (SSN, Drivers, Passport)
    for identifier in resource.get("identifier", []):
        if identifier.get("system") == "http://hl7.org/fhir/sid/us-ssn":
            patient_SSN = identifier.get("value")
        elif identifier.get("system") == "urn:oid:2.16.840.1.113883.4.3.25":
            patient_Drivers = identifier.get("value")
        elif identifier.get("system") == "http://hl7.org/fhir/sid/passport-USA":
            patient_Passport = identifier.get("value")

    # Get name details (First, Last, Prefix, Suffix, Maiden)
    for name in resource.get("name", []):
        if name.get("use") == "official":
            patient_Last = name.get("family")
            patient_First = " ".join(name.get("given", []))  # Join multiple given names
            patient_Prefix = name.get("prefix")
            patient_Suffix = " ".join(name.get("suffix", []))  # Join multiple suffixes if available
        elif name.get("use") == "maiden":
            patient_Maiden = name.get("family")

    # Gender handling
    patient_gender = resource.get("gender")
    if patient_gender == 'female':
        patient_gender = "F"
    elif patient_gender == 'male':
        patient_gender = "M"

    # Extract address, city, state, country, etc.
    for address in resource.get("address", []):
        patient_Address = address.get("line", [])
        patient_City = address.get("city")
        patient_State = address.get("state")
        patient_Zip = address.get("postalCode")
        patient_Country = address.get("country")
        for extension in address.get("extension", []):
            if extension.get("url") == "http://hl7.org/fhir/StructureDefinition/geolocation":
                for geo_extension in extension.get("extension", []):
                    if geo_extension.get("url") == "latitude":
                        patient_LAT = geo_extension.get("valueDecimal")
                    if geo_extension.get("url") == "longitude":
                        patient_LON = geo_extension.get("valueDecimal")

    # Extract race and ethnicity from extensions
    for extension in resource.get("extension", []):
        # Race
        if extension.get("url") == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race":
            for race_extension in extension.get("extension", []):
                if race_extension.get("url") == "ombCategory":
                    patient_Race = race_extension.get("valueCoding", {}).get("display")

        # Ethnicity
        if extension.get("url") == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity":
            for ethnicity_extension in extension.get("extension", []):
                if ethnicity_extension.get("url") == "ombCategory":
                    patient_Ethnicity = ethnicity_extension.get("valueCoding", {}).get("display")

    # Marital status
    maritalStatus = resource.get("maritalStatus")
    if maritalStatus and "coding" in maritalStatus and maritalStatus["coding"]:
        marital_code = maritalStatus["coding"][0].get("code")
        patient_Marital = marital_code if marital_code else 'Unknown'  # Assign a default if code is missing
    else:
        patient_Marital = 'Unknown'  # Handle case where maritalStatus or coding is not provided

    # Birthplace
    for extension in resource.get("extension", []):
        if extension.get("url") == "http://hl7.org/fhir/StructureDefinition/patient-birthPlace":
            birthPlaceAddress = extension.get("valueAddress")
            if birthPlaceAddress:
                city = birthPlaceAddress.get("city", "Unknown")
                state = birthPlaceAddress.get("state", "Unknown")
                country = birthPlaceAddress.get("country", "Unknown")
                # Combine city, state, and country into one string
                patient_Birthplace = f"{city} {state} {country}"

    # Healthcare coverage and expenses (if available)
    patient_Healthcare_expenses = resource.get("healthcareExpenses")
    patient_healthcare_coverage = resource.get("coverage")

    # SQL Insert statement to save all details in MySQL

    cursor.execute("""
        INSERT INTO Patients (
            id, birthDate, deathDate, SSN, Drivers, Passport, Prefix, gender, First, Last, Suffix, Maiden,
            Marital,Race, Ethnicity,Birthplace,Address,City,State,Country,Zip,LAT,LON,Healthcare_expenses,healthcare_coverage
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            birthDate = VALUES(birthDate),
            deathDate = VALUES(deathDate),
            SSN = VALUES(SSN),
            Drivers = VALUES(Drivers),
            Passport = VALUES(Passport),
            Prefix = VALUES(Prefix),
            gender = VALUES(gender),
            First = VALUES(First),
            Last = VALUES(Last),
            Suffix = VALUES(Suffix),
            Maiden = VALUES(Maiden),
            Marital = VALUES(Marital),
            Race=values(Race),
            Ethnicity=values(Ethnicity),
            Birthplace=values(Birthplace),
            Address=values(Address),
            City=values(City),
            State=values(State),
            Country=values(Country),
            Zip=values(Zip),
            LAT=values(LAT),
            LON=values(LON),
            Healthcare_expenses=values(Healthcare_expenses),
            healthcare_coverage=values(healthcare_coverage)

    """, (
        patient_id, patient_birthDate, patient_deathDate, patient_SSN, patient_Drivers, patient_Passport,
        patient_Prefix, patient_gender, patient_First, patient_Last, patient_Suffix, patient_Maiden,
        patient_Marital, patient_Race, patient_Ethnicity, patient_Birthplace, patient_Address, patient_City,
        patient_State,
        patient_Country, patient_Zip, patient_LAT, patient_LON, patient_Healthcare_expenses, patient_healthcare_coverage
    ))

def insert_encounter(resource, cursor):
    try:
        # Get the Encounter ID
        encounter_id = resource.get("id")
        # print(f"{encounter_id} - Inserting Encounter")

        # Get the period start and end times
        period = resource.get("period", {})
        start = period.get("start", '')
        stop = period.get("end", '')

        # Convert to datetime if necessary
        if start:
            start = datetime.fromisoformat(start.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
        if stop:
            stop = datetime.fromisoformat(stop.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')

        # int(f"Start: {start}, Stop: {stop}")

        # Get the patient reference (subject)
        subject = resource.get("subject", {})
        patient_ref = subject.get("reference", '')
        patient_id = patient_ref.split('|')[-1] if patient_ref else ''
        patient_id = patient_id.split(":")[-1]
        # print(f"Patient ID:{patient_id}")

        # Get the service provider reference (organization)
        service_provider = resource.get("serviceProvider", {})
        service_provider_ref = service_provider.get("reference", '')
        organization_id = service_provider_ref.split('|')[-1] if service_provider_ref else ''
        # print(f"Organization ID: {organization_id}")

        # Get the participant (provider)
        participants = resource.get("participant", [])
        provider_id = ''
        if participants:
            provider = participants[0].get("individual", {})
            provider_ref = provider.get("reference", '')
            provider_id = provider_ref.split('|')[-1] if provider_ref else ''
        # print(f"Provider ID: {provider_id}")

        # Get the encounter class
        encounter_class = resource.get("class", {})
        encounter_class_code = encounter_class.get("code", '')
        # print(f"Encounter Class: {encounter_class_code}")

        # Get the encounter type (code and description)
        encounter_type = resource.get("type", [{}])[0]
        encounter_code = encounter_type.get("coding", [{}])[0].get("code", '')
        encounter_description = encounter_type.get("text", '')
        # print(f"Encounter Code: {encounter_code}, Description: {encounter_description}")

        # Reason for encounter
        reason_codes = resource.get("reasonCode", [])
        reason_code = ''
        reason_description = ''
        if reason_codes:
            reason = reason_codes[0].get("coding", [{}])[0]
            reason_code = reason.get("code", '')
            reason_description = reason.get("display", '')
        # print(f"Reason Code: {reason_code}, Reason Description: {reason_description}")

        # Placeholder for encounter costs and payer coverage
        base_encounter_cost = ''  # Could be fetched or calculated from the data
        total_claim_cost = ''  # Same here
        payer_coverage = ''  # Same here
        # print(f"Base Encounter Cost: {base_encounter_cost}, Total Claim Cost: {total_claim_cost}, Payer Coverage: {payer_coverage}")

        # Insert or update the encounter data in the database
        cursor.execute("""
            INSERT INTO encounters (
                Id, START, STOP, PATIENT, ORGANIZATION, PROVIDER,
                ENCOUNTERCLASS, CODE, DESCRIPTION,
                BASE_ENCOUNTER_COST, TOTAL_CLAIM_COST, PAYER_COVERAGE,
                REASONCODE, REASONDESCRIPTION
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                START = VALUES(START),
                STOP = VALUES(STOP),
                PATIENT = VALUES(PATIENT),
                ORGANIZATION = VALUES(ORGANIZATION),
                PROVIDER = VALUES(PROVIDER),
                ENCOUNTERCLASS = VALUES(ENCOUNTERCLASS),
                CODE = VALUES(CODE),
                DESCRIPTION = VALUES(DESCRIPTION),
                BASE_ENCOUNTER_COST = VALUES(BASE_ENCOUNTER_COST),
                TOTAL_CLAIM_COST = VALUES(TOTAL_CLAIM_COST),
                PAYER_COVERAGE = VALUES(PAYER_COVERAGE),
                REASONCODE = VALUES(REASONCODE),
                REASONDESCRIPTION = VALUES(REASONDESCRIPTION)
        """, (
            encounter_id, start, stop, patient_id, organization_id, provider_id,
            encounter_class_code, encounter_code, encounter_description,
            base_encounter_cost, total_claim_cost, payer_coverage,
            reason_code, reason_description
        ))

    except Exception as e:
        print(f"Error inserting or updating encounter data: {e}")
        # print("Data:", resource)

def insert_condition(resource, cursor):
    try:
        # Get the Condition ID (can be used for Encounter reference)
        condition_id = resource.get("id")
        # print(f"{condition_id} - Inserting Condition")

        # Get the clinical status (active/confirmed, etc.)
        clinical_status = resource.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", '')
        # print(f"Clinical Status: {clinical_status}")

        # Get the verification status (confirmed, etc.)
        verification_status = resource.get("verificationStatus", {}).get("coding", [{}])[0].get("code", '')
        # print(f"Verification Status: {verification_status}")

        # Get the condition category (e.g., diagnosis)
        category = resource.get("category", [{}])[0].get("coding", [{}])[0].get("code", '')
        # print(f"Category: {category}")

        # Get the condition code (code and description)
        condition_code = resource.get("code", {}).get("coding", [{}])[0].get("code", '')
        condition_description = resource.get("code", {}).get("text", '')
        # print(f"Condition Code: {condition_code}, Description: {condition_description}")

        # Get the patient reference (subject)
        subject = resource.get("subject", {})
        patient_ref = subject.get("reference", '')
        patient_id = patient_ref.split('|')[-1] if patient_ref else ''
        patient_id = patient_id.split(":")[-1]
        # print(f"Patient ID: {patient_id}")

        # Get the encounter reference (optional)
        encounter_ref = resource.get("encounter", {}).get("reference", '')
        encounter_id = encounter_ref.split('|')[-1] if encounter_ref else ''
        encounter_id = encounter_id.split(":")[-1]
        # print(f"Encounter ID: {encounter_id}")

        # Get the onset date (if available)
        onset_date = resource.get("onsetDateTime", '')
        if onset_date:
            onset_date = datetime.fromisoformat(onset_date.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
        # print(f"Onset Date: {onset_date}")

        # Get the recorded date
        recorded_date = resource.get("recordedDate", '')
        if recorded_date:
            recorded_date = datetime.fromisoformat(recorded_date.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
        # print(f"Recorded Date: {recorded_date}")

        # Insert or update the condition data in the database
        cursor.execute("""
            INSERT INTO conditions (
                START, STOP, PATIENT, ENCOUNTER, CODE, DESCRIPTION
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                START = VALUES(START),
                STOP = VALUES(STOP),
                PATIENT = VALUES(PATIENT),
                ENCOUNTER = VALUES(ENCOUNTER),
                CODE = VALUES(CODE),
                DESCRIPTION = VALUES(DESCRIPTION)
        """, (
            onset_date, recorded_date, patient_id, encounter_id,
            condition_code, condition_description
        ))


    except Exception as e:
        print(f"Error inserting or updating condition data: {e}")
        # print("Data:", resource)

def insert_claim(resource, cursor):
    try:
        # Get the Claim ID
        claim_id = resource.get("id")
        # print(f"{claim_id} - Inserting Claim")

        # Get the patient reference (subject)
        patient_ref = resource.get("patient", {}).get("reference", '')
        patient_id = patient_ref.split('|')[-1] if patient_ref else ''
        patient_id = patient_id.split(":")[-1]
        # print(f"Patient ID: {patient_id}")

        # Get the provider reference
        provider_ref = resource.get("provider", {}).get("reference", '')
        provider_id = provider_ref.split('|')[-1] if provider_ref else ''
        provider_id = provider_id.split(":")[-1]
        # print(f"Provider ID: {provider_id}")

        # Get the primary insurance (if available)
        primary_insurance = resource.get("insurance", [{}])[0].get("coverage", {}).get("display", '')
        # print(f"Primary Insurance: {primary_insurance}")

        # Get the secondary insurance (if available)
        secondary_insurance = resource.get("insurance", [{}])[1].get("coverage", {}).get("display", '') if len(
            resource.get("insurance", [])) > 1 else ''
        # print(f"Secondary Insurance: {secondary_insurance}")

        # Get the diagnosis codes (if available)
        diagnosis_codes = [
            item.get("productOrService", {}).get("coding", [{}])[0].get("code", '')
            for item in resource.get("item", [])
        ]
        DIAGNOSIS1 = diagnosis_codes[0] if len(diagnosis_codes) > 0 else ''
        DIAGNOSIS2 = diagnosis_codes[1] if len(diagnosis_codes) > 1 else ''

        # print(f"Diagnosis Codes: {DIAGNOSIS2,DIAGNOSIS2}")

        # Get the appointment reference (if available)
        appointment_ref = resource.get("appointment", {}).get("reference", '')
        appointment_id = appointment_ref.split('|')[-1] if appointment_ref else ''
        appointment_id = appointment_id.split(":")[-1]
        # print(f"Appointment ID: {appointment_id}")

        # Get the service date
        service_date = resource.get("billablePeriod", {}).get("start", '')
        if service_date:
            service_date = datetime.fromisoformat(service_date.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
        # print(f"Service Date: {service_date}")

        # Insert or update the claim data in the database
        cursor.execute("""
            INSERT INTO claims (
                ID, PATIENTID, PROVIDERID, PRIMARYPATIENTINSURANCEID, SECONDARYPATIENTINSURANCEID,
                DIAGNOSIS1,DIAGNOSIS2, APPOINTMENTID, SERVICEDATE
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
            ON DUPLICATE KEY UPDATE
                PATIENTID = VALUES(PATIENTID),
                PROVIDERID = VALUES(PROVIDERID),
                PRIMARYPATIENTINSURANCEID = VALUES(PRIMARYPATIENTINSURANCEID),
                SECONDARYPATIENTINSURANCEID = VALUES(SECONDARYPATIENTINSURANCEID),
                DIAGNOSIS1=values(DIAGNOSIS1),
                DIAGNOSIS2=values(DIAGNOSIS2),                
                APPOINTMENTID = VALUES(APPOINTMENTID),
                SERVICEDATE = VALUES(SERVICEDATE)

        """, (
            claim_id, patient_id, provider_id, primary_insurance, secondary_insurance,
            DIAGNOSIS1, DIAGNOSIS2, appointment_id, service_date
        ))

    except Exception as e:
        print(f"Error inserting or updating claim data: {e}")
        # print("Data:", resource)

def process_fhir_resource(fhir_data):
    conn = connect_to_db()  # Assuming this is your method to connect to MySQL
    try:
        with conn.cursor() as cursor:
            for entry in fhir_data.get("entry", []):
                resource = entry.get("resource", {})
                resource_type = resource.get("resourceType")
                if resource_type == "Patient":
                   insert_patient(resource,cursor)
                   #print("processing resource---Patient")
                elif resource_type == "Encounter":
                    insert_encounter(resource, cursor)
                   # print("processing resource---Encounter")
                elif resource_type == "Condition":
                    insert_condition(resource, cursor)
                elif resource_type == "Claim":
                    insert_claim(resource, cursor)
    except Exception as e:
        print(f"Error inserting into database from json: {e}")
    finally:
        conn.commit()
        conn.close()











