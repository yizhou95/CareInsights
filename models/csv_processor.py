import csv
import pymysql

def connect_to_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="visualization",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
#Processes a CSV file by determining the appropriate table-specific insertion method.
#Parameters:   file_name (str): The name of the CSV file.
# csv_data (DataFrame): The data from the CSV file to be inserted into the database.
def process_csv_file(file_name,csv_data):
    # A dictionary mapping file names to their corresponding database insertion methods.
    table_methods={
        "patients.csv": insert_into_patients_table,
        "providers.csv": insert_into_providers_table,
        "organizations.csv": insert_into_organizations_table,
        "payers.csv": insert_into_payers_table,
        "payer_transitions.csv": insert_into_payer_transitions_table,
        "encounters.csv": insert_into_encounters_table,
        "supplies.csv": insert_into_supplies_table,
        "procedures.csv":insert_into_procedures_table,
        "observations.csv": insert_into_observations_table,
        "medications.csv": insert_into_medications_table,
        "immunizations.csv": insert_into_immunizations_table,
        "conditions.csv": insert_into_conditions_table,
        "claims_transactions.csv": insert_into_claims_transactions_table,
        "claims.csv": insert_into_claims_table,
        "careplans.csv": insert_into_careplans_table,
        "allergies.csv": insert_into_allergies_table,
    }
    # Check if the file name is in the dictionary.
    if file_name in table_methods:
        # Call the corresponding insertion method with the provided data.
        table_methods[file_name](csv_data)
    else:
        # Print a message if no method is defined for the file.
        print(f"No method defined for {file_name}.Skipping.")

# Inserts patient data from a CSV string into the `patients` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_patients_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 25:  # Ensure there are 25 columns in the row
                    query = """
                        INSERT INTO patients (
                            id, birthdate, deathdate, SSN, drivers, passport, prefix, first, last, suffix,
                            maiden, marital, race, ethnicity, gender, birthplace, address, city, state, country, zip,
                            lat, lon, healthcare_expenses, healthcare_coverage
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            birthdate = VALUES(birthdate),
                            deathdate = VALUES(deathdate),
                            SSN = VALUES(SSN),
                            drivers = VALUES(drivers),
                            passport = VALUES(passport),
                            prefix = VALUES(prefix),
                            first = VALUES(first),
                            last = VALUES(last),
                            suffix = VALUES(suffix),
                            maiden = VALUES(maiden),
                            marital = VALUES(marital),
                            race = VALUES(race),
                            ethnicity = VALUES(ethnicity),
                            gender = VALUES(gender),
                            birthplace = VALUES(birthplace),
                            address = VALUES(address),
                            city = VALUES(city),
                            state = VALUES(state),
                            country = VALUES(country),
                            zip = VALUES(zip),
                            lat = VALUES(lat),
                            lon = VALUES(lon),
                            healthcare_expenses = VALUES(healthcare_expenses),
                            healthcare_coverage = VALUES(healthcare_coverage)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into patients table.")
    except Exception as e:
        print(f"Error inserting into patients table: {e}")
    finally:
        conn.close()

# Inserts providers data from a CSV string into the `providers` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_providers_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 12:
                    query = """
                        INSERT INTO providers (
                            id, organization, name, gender, speciality, address, city, state, zip, lat, lon, utilization
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            organization = VALUES(organization),
                            name = VALUES(name),
                            gender = VALUES(gender),
                            speciality = VALUES(speciality),
                            address = VALUES(address),
                            city = VALUES(city),
                            state = VALUES(state),
                            zip = VALUES(zip),
                            lat = VALUES(lat),
                            lon = VALUES(lon),
                            utilization = VALUES(utilization)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into providers table.")
    except Exception as e:
        print(f"Error inserting into providers table: {e}")
    finally:
        conn.close()

# Inserts organizations data from a CSV string into the `organizations` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_organizations_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            # Parse CSV content
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 11:  # Ensure the row has 11 columns
                    query = """
                        INSERT INTO organizations (
                            id, name, address, city, state, zip, lat, lon, phone, revenue, utilization
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            address = VALUES(address),
                            city = VALUES(city),
                            state = VALUES(state),
                            zip = VALUES(zip),
                            lat = VALUES(lat),
                            lon = VALUES(lon),
                            phone = VALUES(phone),
                            revenue = VALUES(revenue),
                            utilization = VALUES(utilization)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")

            conn.commit()  # Commit the transaction
        print("Data successfully inserted into organizations table.")
    except Exception as e:
        print(f"Error inserting into organizations table: {e}")
    finally:
        conn.close()

# Inserts payers data from a CSV string into the `payers` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_payers_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 21:  # Ensure the correct number of columns
                    query = """
                        INSERT INTO payers (
                            id, name, address, city, state_headquartered, zip, phone, 
                            amount_covered, amount_uncovered, revenue, 
                            covered_encounters, uncovered_encounters, 
                            covered_medications, uncovered_medications, 
                            covered_procedures, uncovered_procedures, 
                            covered_immunizations, uncovered_immunizations, 
                            unique_customers, qols_avg, member_months
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, 
                                %s, %s, 
                                %s, %s, 
                                %s, %s, 
                                %s, %s, 
                                %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            address = VALUES(address),
                            city = VALUES(city),
                            state_headquartered = VALUES(state_headquartered),
                            zip = VALUES(zip),
                            phone = VALUES(phone),
                            amount_covered = VALUES(amount_covered),
                            amount_uncovered = VALUES(amount_uncovered),
                            revenue = VALUES(revenue),
                            covered_encounters = VALUES(covered_encounters),
                            uncovered_encounters = VALUES(uncovered_encounters),
                            covered_medications = VALUES(covered_medications),
                            uncovered_medications = VALUES(uncovered_medications),
                            covered_procedures = VALUES(covered_procedures),
                            uncovered_procedures = VALUES(uncovered_procedures),
                            covered_immunizations = VALUES(covered_immunizations),
                            uncovered_immunizations = VALUES(uncovered_immunizations),
                            unique_customers = VALUES(unique_customers),
                            qols_avg = VALUES(qols_avg),
                            member_months = VALUES(member_months)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into payers table.")
    except Exception as e:
        print(f"Error inserting into payers table: {e}")
    finally:
        conn.close()

# Inserts payer_transitions data from a CSV string into the `payer_transitions` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_payer_transitions_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 8:  # Ensure the correct number of columns
                    query = """
                        INSERT INTO payer_transitions (
                            patient, memberid, start_year, end_year, payer, 
                            secondary_payer, ownership, ownername
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            start_year = VALUES(start_year),
                            end_year = VALUES(end_year),
                            payer = VALUES(payer),
                            secondary_payer = VALUES(secondary_payer),
                            ownership = VALUES(ownership),
                            ownername = VALUES(ownername)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into payer_transactions table.")
    except Exception as e:
        print(f"Error inserting into payer_transactions table: {e}")
    finally:
        conn.close()

# Inserts encounters data from a CSV string into the `encounters` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_encounters_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 15:  # Ensure the correct number of columns
                    query = """
                        INSERT INTO encounters (
                            id, start, stop, patient, organization, provider, payer,
                            encounterclass, code, description, base_encounter_cost,
                            total_claim_cost, payer_coverage, reasoncode, reasondescription
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            start = VALUES(start),
                            stop = VALUES(stop),
                            patient = VALUES(patient),
                            organization = VALUES(organization),
                            provider = VALUES(provider),
                            payer = VALUES(payer),
                            encounterclass = VALUES(encounterclass),
                            code = VALUES(code),
                            description = VALUES(description),
                            base_encounter_cost = VALUES(base_encounter_cost),
                            total_claim_cost = VALUES(total_claim_cost),
                            payer_coverage = VALUES(payer_coverage),
                            reasoncode = VALUES(reasoncode),
                            reasondescription = VALUES(reasondescription)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into encounters table.")
    except Exception as e:
        print(f"Error inserting into encounters table: {e}")
    finally:
        conn.close()

# Inserts supplies data from a CSV string into the `supplies` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_supplies_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 6:  # Ensure the correct number of columns
                    query = """
                        INSERT INTO supplies (
                            date, patient, encounter, code, description, quantity
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            patient = VALUES(patient),
                            encounter = VALUES(encounter),
                            code = VALUES(code),
                            description = VALUES(description),
                            quantity = VALUES(quantity)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into supplies table.")
    except Exception as e:
        print(f"Error inserting into supplies table: {e}")
    finally:
        conn.close()

# Inserts procedures data from a CSV string into the `procedures` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_procedures_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 9:  # Ensure the correct number of columns
                    query = """
                        INSERT INTO procedures (
                            start, stop, patient, encounter, code, description, base_cost, reasoncode, reasondescription
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            patient = VALUES(patient),
                            encounter = VALUES(encounter),
                            code = VALUES(code),
                            description = VALUES(description),
                            base_cost = VALUES(base_cost),
                            reasoncode = VALUES(reasoncode),
                            reasondescription = VALUES(reasondescription)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into procedures table.")
    except Exception as e:
        print(f"Error inserting into procedures table: {e}")
    finally:
        conn.close()

# Inserts observations data from a CSV string into the `observations` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_observations_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 9:  # Ensure the correct number of columns
                    query = """
                        INSERT INTO observations (
                            date, patient, encounter, category, code, description, value, units, type
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            patient = VALUES(patient),
                            encounter = VALUES(encounter),
                            category = VALUES(category),
                            code = VALUES(code),
                            description = VALUES(description),
                            value = VALUES(value),
                            units = VALUES(units),
                            type = VALUES(type)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into observations table.")
    except Exception as e:
        print(f"Error inserting into observations table: {e}")
    finally:
        conn.close()

# Inserts medications data from a CSV string into the `medications` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_medications_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                # Ensure row has 13 columns (excluding the auto-increment ID)
                if len(row) == 13:
                    query = """
                        INSERT INTO medications (
                            start, stop, patient, payer, encounter, code, description, 
                            base_cost, payer_coverage, dispenses, totalcost, reasoncode, reasondescription
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            start = VALUES(start),
                            stop = VALUES(stop),
                            patient = VALUES(patient),
                            payer = VALUES(payer),
                            encounter = VALUES(encounter),
                            code = VALUES(code),
                            description = VALUES(description),
                            base_cost = VALUES(base_cost),
                            payer_coverage = VALUES(payer_coverage),
                            dispenses = VALUES(dispenses),
                            totalcost = VALUES(totalcost),
                            reasoncode = VALUES(reasoncode),
                            reasondescription = VALUES(reasondescription)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into medications table.")
    except Exception as e:
        print(f"Error inserting into medications table: {e}")
    finally:
        conn.close()

# Inserts immunizations data from a CSV string into the `immunizations` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_immunizations_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                # Ensure row has 6 columns (excluding the auto-increment ID)
                if len(row) == 6:
                    query = """
                        INSERT INTO immunizations (
                            date, patient, encounter, code, description, base_cost
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            date = VALUES(date),
                            patient = VALUES(patient),
                            encounter = VALUES(encounter),
                            code = VALUES(code),
                            description = VALUES(description),
                            base_cost = VALUES(base_cost)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into immunizations table.")
    except Exception as e:
        print(f"Error inserting into immunizations table: {e}")
    finally:
        conn.close()

# Inserts conditions data from a CSV string into the `conditions` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_conditions_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                # Ensure row has 6 columns (excluding the auto-increment ID)
                if len(row) == 6:
                    query = """
                        INSERT INTO conditions (
                            start, stop, patient, encounter, code, description
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            start = VALUES(start),
                            stop = VALUES(stop),
                            patient = VALUES(patient),
                            encounter = VALUES(encounter),
                            code = VALUES(code),
                            description = VALUES(description)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")
            conn.commit()
        print("Data successfully inserted into conditions table.")
    except Exception as e:
        print(f"Error inserting into conditions table: {e}")
    finally:
        conn.close()

# Inserts claims transactions data from a CSV string into the `claims-transactions` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_claims_transactions_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 24:  # Ensure the correct number of columns (24 based on your schema)
                    query = """
                        INSERT INTO claims_transactions (
                            ID, CLAIMID, CHARGEID, PATIENTID, TYPE, AMOUNT, METHOD, FROMDATE, TODATE, PLACEOFSERVICE, 
                            PROCEDURECODE, DEPARTMENTID, NOTES, UNITAMOUNT, TRANSFEROUTID, TRANSFERTYPE, PAYMENTS, 
                            TRANSFERS, OUTSTANDING, APPOINTMENTID, LINENOTE, PATIENTINSURANCEID, PROVIDERID, SUPERVISINGPROVIDERID
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            CLAIMID = VALUES(CLAIMID), CHARGEID = VALUES(CHARGEID), PATIENTID = VALUES(PATIENTID), 
                            TYPE = VALUES(TYPE), AMOUNT = VALUES(AMOUNT), METHOD = VALUES(METHOD), FROMDATE = VALUES(FROMDATE), 
                            TODATE = VALUES(TODATE), PLACEOFSERVICE = VALUES(PLACEOFSERVICE), PROCEDURECODE = VALUES(PROCEDURECODE),
                            DEPARTMENTID = VALUES(DEPARTMENTID), NOTES = VALUES(NOTES), UNITAMOUNT = VALUES(UNITAMOUNT), 
                            TRANSFEROUTID = VALUES(TRANSFEROUTID), TRANSFERTYPE = VALUES(TRANSFERTYPE), PAYMENTS = VALUES(PAYMENTS), 
                            TRANSFERS = VALUES(TRANSFERS), OUTSTANDING = VALUES(OUTSTANDING), APPOINTMENTID = VALUES(APPOINTMENTID), 
                            LINENOTE = VALUES(LINENOTE), PATIENTINSURANCEID = VALUES(PATIENTINSURANCEID), PROVIDERID = VALUES(PROVIDERID), 
                            SUPERVISINGPROVIDERID = VALUES(SUPERVISINGPROVIDERID)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")

            conn.commit()  # Commit the changes to the database
        print("Data successfully inserted into claims_transactions table.")
    except Exception as e:
        print(f"Error inserting into claims_transactions table: {e}")
    finally:
        conn.close()  # Close the database connection


# Inserts claims data from a CSV string into the `claims` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_claims_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 24:
                    query = """
                        INSERT INTO claims (
                            Id, PATIENTID, PROVIDERID, PRIMARYPATIENTINSURANCEID, SECONDARYPATIENTINSURANCEID, 
                            DEPARTMENTID, PATIENTDEPARTMENTID, DIAGNOSIS1, DIAGNOSIS2, APPOINTMENTID, CURRENTILLNESSDATE, 
                            SERVICEDATE, SUPERVISINGPROVIDERID, STATUS1, STATUS2, STATUSP, OUTSTANDING1, OUTSTANDING2, 
                            OUTSTANDINGP, LASTBILLEDDATE1, LASTBILLEDDATE2, LASTBILLEDDATEP, HEALTHCARECLAIMTYPEID1, 
                            HEALTHCARECLAIMTYPEID2
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            PATIENTID = VALUES(PATIENTID), PROVIDERID = VALUES(PROVIDERID), 
                            PRIMARYPATIENTINSURANCEID = VALUES(PRIMARYPATIENTINSURANCEID), 
                            SECONDARYPATIENTINSURANCEID = VALUES(SECONDARYPATIENTINSURANCEID), 
                            DEPARTMENTID = VALUES(DEPARTMENTID), PATIENTDEPARTMENTID = VALUES(PATIENTDEPARTMENTID), 
                            DIAGNOSIS1 = VALUES(DIAGNOSIS1), DIAGNOSIS2 = VALUES(DIAGNOSIS2), 
                            APPOINTMENTID = VALUES(APPOINTMENTID), CURRENTILLNESSDATE = VALUES(CURRENTILLNESSDATE), 
                            SERVICEDATE = VALUES(SERVICEDATE), SUPERVISINGPROVIDERID = VALUES(SUPERVISINGPROVIDERID), 
                            STATUS1 = VALUES(STATUS1), STATUS2 = VALUES(STATUS2), STATUSP = VALUES(STATUSP), 
                            OUTSTANDING1 = VALUES(OUTSTANDING1), OUTSTANDING2 = VALUES(OUTSTANDING2), 
                            OUTSTANDINGP = VALUES(OUTSTANDINGP), LASTBILLEDDATE1 = VALUES(LASTBILLEDDATE1), 
                            LASTBILLEDDATE2 = VALUES(LASTBILLEDDATE2), LASTBILLEDDATEP = VALUES(LASTBILLEDDATEP), 
                            HEALTHCARECLAIMTYPEID1 = VALUES(HEALTHCARECLAIMTYPEID1), 
                            HEALTHCARECLAIMTYPEID2 = VALUES(HEALTHCARECLAIMTYPEID2)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")

            conn.commit()  # Commit the changes to the database
        print("Data successfully inserted into claims table.")
    except Exception as e:
        print(f"Error inserting into claims table: {e}")
    finally:
        conn.close()  # Close the database connection

# Inserts care plans data from a CSV string into the `careplans` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_careplans_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 9:  # Ensure the correct number of columns (9 based on your schema)
                    query = """
                        INSERT INTO careplans (
                            Id, START, STOP, PATIENT, ENCOUNTER, CODE, DESCRIPTION, REASONCODE, REASONDESCRIPTION
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            START = VALUES(START), STOP = VALUES(STOP), PATIENT = VALUES(PATIENT),
                            ENCOUNTER = VALUES(ENCOUNTER), CODE = VALUES(CODE), DESCRIPTION = VALUES(DESCRIPTION),
                            REASONCODE = VALUES(REASONCODE), REASONDESCRIPTION = VALUES(REASONDESCRIPTION)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")

            conn.commit()  # Commit the changes to the database
        print("Data successfully inserted into careplans table.")
    except Exception as e:
        print(f"Error inserting into careplans table: {e}")
    finally:
        conn.close()  # Close the database connection

# Inserts allergies data from a CSV string into the `allergies` table in the database.
# If a record already exists (based on primary key or unique constraint), it updates the existing record.
def insert_into_allergies_table(csv_data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            reader = csv.reader(csv_data.splitlines())
            header = next(reader)  # Skip the header row

            for row in reader:
                if len(row) == 13:
                    query = """
                        INSERT INTO allergies (
                            START, STOP, PATIENT, ENCOUNTER, CODE, SYSTEM1, DESCRIPTION, TYPE, CATEGORY, 
                            DESCRIPTION1, SEVERITY1, DESCRIPTION2, SEVERITY2
                        ) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            START = VALUES(START), STOP = VALUES(STOP), PATIENT = VALUES(PATIENT),
                            ENCOUNTER = VALUES(ENCOUNTER), CODE = VALUES(CODE), SYSTEM1 = VALUES(SYSTEM1),
                            DESCRIPTION = VALUES(DESCRIPTION), TYPE = VALUES(TYPE), CATEGORY = VALUES(CATEGORY),
                            DESCRIPTION1 = VALUES(DESCRIPTION1), SEVERITY1 = VALUES(SEVERITY1),
                            DESCRIPTION2 = VALUES(DESCRIPTION2), SEVERITY2 = VALUES(SEVERITY2)
                    """
                    cursor.execute(query, row)  # Pass the row as a tuple of values
                else:
                    print(f"Skipping row due to incorrect column count: {row}")

            conn.commit()  # Commit the changes to the database
        print("Data successfully inserted into allergies table.")
    except Exception as e:
        print(f"Error inserting into allergies table: {e}")
    finally:
        conn.close()  # Close the database connection

# def check_claim_exists(cursor, claim_id):
#     cursor.execute("SELECT COUNT(1) FROM claims WHERE Id = %s", (claim_id,))
#     return cursor.fetchone()[0] > 0
#
#
# def check_patient_exists(cursor, patient_id):
#     cursor.execute("SELECT COUNT(1) FROM patients WHERE Id = %s", (patient_id,))
#     return cursor.fetchone()[0] > 0
#
#
# def check_provider_exists(cursor, provider_id):
#     cursor.execute("SELECT COUNT(1) FROM providers WHERE Id = %s", (provider_id,))
#     return cursor.fetchone()[0] > 0