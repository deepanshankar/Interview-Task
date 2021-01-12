# importing libraries
import json
import pandas as pd
import os
import enum
import re
import logging

logs_dir = "../logs/"
logs_file = os.path.join(logs_dir,"summary.log")
if not os.path.exists(logs_dir):  # create logs directory if not present
    os.mkdir(logs_dir)


logging.basicConfig(filename=logs_file, filemode="w", level=logging.DEBUG)    # logger's configuration

# defining global variables and output file path
if __name__ == "__main__":
    definition = {}
    error_codes = {}
    output_dir = "../parsed"
    output_report_file = os.path.join(output_dir, "report.csv")
    output_summary_file = os.path.join(output_dir, "summary.txt")


class DataType(enum.Enum):
    """
    Enum class representing the data types
    """
    digits = 0
    word_characters = 1
    others = 2


def read_input_files():
    """
    Reads all input files and parsed to be stored in global objects

    :return: definitions, error codes and inputs
    """
    with open("../standard_definition.json", "r") as def_file:
        definition = json.load(def_file)

    with open("../error_codes.json", "r") as error_file:
        error_codes = json.load(error_file)

    with open("../input_file.txt", "r") as input_file:
        inputs = input_file.readlines()

    return definition, error_codes, inputs


definition, error_codes, inputs = read_input_files()      # reading input files


def get_sub_sections(section):
    """
    Fetches sub-sections for the respective sections

    :param section: section from input
    :return: sub-sections if present and None if not available
    """
    for key in definition:
        if key["key"] == section:
            return key["sub_sections"]  # returns respective sub-sections

    return None  # return None if key doesn't match the input data


def get_input_data_type(value):
    """
    Finds the matching data type for the inputs

    :param value: each sub-section from input
    :return: the data type
    """
    pattern_char = re.compile("^[a-zA-Z ]+$")    # pattern to check for words_characters, which includes space

    pattern_digit = re.compile("^[0-9]+$")       # pattern to check for numbers

    if pattern_digit.match(value):
        d_type = DataType.digits.name
    elif pattern_char.match(value):
        d_type = DataType.word_characters.name
    else:
        d_type = DataType.others.name

    return d_type


def calculate_error_code(value, exp_data_type, exp_max_length, given_data_type, given_length):
    """
    To fetch error codes based on conditions given

    :param value: input value
    :param exp_data_type: expected data type
    :param exp_max_length: expected max length
    :param given_data_type: input's data type
    :param given_length: input's length
    :return: calculated error code
    """
    data_type_match = (exp_data_type == given_data_type)

    length_match = exp_max_length >= given_length

    if not data_type_match and not length_match:
        return "E04"
    elif data_type_match and length_match:
        return "E01"
    elif data_type_match:
        return "E03"
    elif length_match:
        return "E02"

    return None


def get_summary(summary, error_key, exp_max_length, exp_data_type, section, sub_section):
    """
    To append refactored message template from error code to cumulative summary content

    :param summary: cumulative summary content
    :param error_key: calculated error code
    :param exp_max_length: expected max length
    :param exp_data_type: expected data type
    :param section: section from input
    :param sub_section: sub-section of the input
    :return: appended summary string
    """
    message_template = ""

    for code in error_codes:
        if code["code"] == error_key:
            message_template = code["message_template"]

    message = message_template.replace("LXY", sub_section).replace("LX", section)
    summary = summary + message.format(data_type=exp_data_type, max_length=exp_max_length) + "\n"

    return summary


def add_row_to_df(df, section, sub_section, given_data_type, exp_data_type, given_length, exp_max_length, error_key):
    """
    Adds rows to the data frame

    :param df: cumulative dataframe
    :param section: section from input
    :param sub_section: sub-section from input
    :param given_data_type: input's data type
    :param exp_data_type: expected data type
    :param given_length: input's length
    :param exp_max_length: expected max length
    :param error_key: error code
    :return: appended data frame
    """

    row = {"Section": section, "Sub-Section": sub_section, "Given DataType": given_data_type,
           "Expected DataType": exp_data_type, "Given Length": given_length,
           "Expected MaxLength": exp_max_length, "Error Code": error_key}

    logging.info("Row is added to data frame %s", row)
    df = df.append(row, ignore_index=True)

    return df


def write_to_file(df, summary):
    """
    Writes summary and report to the files

    :param df: data frame with report
    :param summary: summary content
    :return: None
    """
    if not os.path.exists(output_dir):      # create directory if not present
        os.mkdir(output_dir)

    logging.info("Summary \n\n%s", summary)
    logging.info("Report DataFrame \n\n%s", df)

    try:
        df.to_csv(output_report_file, index=False, header=True)
        with open(output_summary_file, "w") as output_file:
            output_file.write(summary)
    except Exception as e:
        logging.error("Error occurred while writing parsed code into files : ", e)


def process_input(input_data, is_testcase):
    """
    Method to fetch input data line by line and process data to store in output files

    :param input_data: data from input file
    :param is_testcase: check for calling from UnitTest.py or main method
    :return: data frame, when called from unit test cases and None, if called from main method
    """

    columns = ["Section", "Sub-Section", "Given DataType", "Expected DataType", "Given Length",
               "Expected MaxLength", "Error Code"]

    df = pd.DataFrame(columns=columns)     # initializing empty dataframe with columns
    summary = ""                           # initializing summary to be empty

    for line in input_data:
        line = line.replace("\n", '')
        logging.info("input data : %s", line)
        data = line.split("&")
        section = data[0]
        sub_sections = get_sub_sections(section)

        if sub_sections:                               # check if sub-section present in definition, else prompt to user
            for index in range(len(sub_sections)):     # loop for every sub-sections from definition
                sub_section_key = sub_sections[index]["key"]
                exp_data_type = sub_sections[index]["data_type"]
                exp_max_length = sub_sections[index]["max_length"]
                given_data_type, given_length = "", ""

                if len(data) > index + 1:              # check for missing input for sub-sections
                    value = data[index + 1]
                    given_data_type = get_input_data_type(value)
                    given_length = len(value)
                    error_key = calculate_error_code(value, exp_data_type, exp_max_length, given_data_type,
                                                     given_length)
                else:
                    error_key = "E05"

                summary = get_summary(summary, error_key, exp_max_length, exp_data_type, section, sub_section_key)

                df = add_row_to_df(df, section, sub_section_key, given_data_type, exp_data_type,
                                   given_length, exp_max_length, error_key)
        else:
            logging.warning("Section {key} not found".format(key=section))

        summary = summary + "\n"        # add a new line to distinguish every input

    if not is_testcase:                 # check for method call from test case or main method
        write_to_file(df, summary)
    else:
        return df


if __name__ == "__main__":
    process_input(inputs, False)        # method call to start processing
    print("Inputs are parsed and report is stored in respective files. Check for logs/summary.log for more details")
