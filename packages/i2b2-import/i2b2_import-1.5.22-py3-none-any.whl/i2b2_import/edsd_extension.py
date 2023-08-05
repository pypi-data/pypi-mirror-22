import logging

from re import split
from os.path import join
from os.path import basename

from . import utils


DATASET = 'edsd'
ACQUISITION_SETTINGS = ['Manufacturer', 'ManufacturerModelName', 'MagneticFieldStrength']
ACQUISITION_CONCEPT_PREFIX = join("/", DATASET, "Imaging Data/Acquisition Settings")


def txt2i2b2(file_path, i2b2_conn):
    info = _extract_info(file_path)
    patient_ide = _patient_ide_from_path(file_path)
    visit_ide = patient_ide + '_V' + info['StudyID'] if len(info['StudyID']) > 1 else 'V0' + info['StudyID']

    patient_sex = None
    patient_age = None
    acq_date = None
    birthdate = None

    try:
        patient_sex = info['PatientSex']
    except KeyError:
        logging.info("PatientSex not found in %s for patient %s", file_path, patient_ide)
    try:
        patient_age = utils.compute_age_years(int(info['PatientAge'][:-1]), info['PatientAge'][-1])
    except KeyError:
        logging.info("PatientAge not found in %s for patient %s", file_path, patient_ide)
    try:
        acq_date = utils.datetime_from_dcm_date(info['AcquisitionDate'])
    except KeyError:
        logging.info("AcquisitionDate not found in %s for patient %s", file_path, patient_ide)
    try:
        birthdate = utils.datetime_from_dcm_date(info['PatientBirthdate'])
    except KeyError:
        logging.info("PatientBirthdate not found in %s for patient %s", file_path, patient_ide)

    encounter_num = i2b2_conn.get_encounter_num(visit_ide, DATASET, DATASET, patient_ide, DATASET)
    patient_num = i2b2_conn.get_patient_num(patient_ide, DATASET, DATASET)

    i2b2_conn.save_visit(encounter_num, patient_num, patient_age, acq_date)
    i2b2_conn.save_patient(patient_num, patient_sex, birth_date=birthdate)

    visit = i2b2_conn.get_visit(encounter_num, patient_num)

    concept_path = join(ACQUISITION_CONCEPT_PREFIX, "name")
    concept_cd = DATASET + ':protocol_name'
    i2b2_conn.save_concept(concept_path, concept_cd)

    try:
        start_date = visit.start_date
        if not start_date:
            raise AttributeError
    except AttributeError:
        start_date = utils.DEFAULT_DATE
    i2b2_conn.save_observation(encounter_num, concept_cd, DATASET, start_date, patient_num, 'T',
                               info['SeriesDescription'], None)

    for concept in ACQUISITION_SETTINGS:
        concept_cd = DATASET + ':' + concept
        concept_path = join(ACQUISITION_CONCEPT_PREFIX, concept)
        i2b2_conn.save_concept(concept_path, concept_cd)

        try:
            val = info[concept]
            valtype_cd = utils.find_type(val)
            if valtype_cd == 'N':
                tval_char = 'E'
                nval_num = float(val)
            else:
                tval_char = val
                nval_num = None
            try:
                start_date = visit.start_date
                if not start_date:
                    raise AttributeError
            except AttributeError:
                start_date = utils.DEFAULT_DATE
            i2b2_conn.save_observation(encounter_num, concept_cd, DATASET, start_date, patient_num, valtype_cd,
                                       tval_char, nval_num)
        except KeyError:
            logging.info("%s not found in %s for patient %s", concept, file_path, patient_ide)


def _patient_ide_from_path(file_path):
    path_info = split(r'[+.]+', basename(file_path))
    prefix = path_info[0] + '+'
    site = path_info[2]
    sid_per_site = path_info[3]
    proto = path_info[4]
    return prefix + site + proto + sid_per_site


def _extract_info(file_path):
    f = open(file_path, 'r')
    d = {}
    for line in f.readlines():
        line = line.strip()
        line = line.split('//')
        if len(line) == 3:
            if not line[1].isspace():
                key = ''.join(split(r'[ ]+', line[1].strip())[1:])
                value = ' '.join(split(r'[ ]+', line[2].strip())).split("\\")
                d.update({key: value if len(value) > 1 else value[0]})
    f.close()
    return d
