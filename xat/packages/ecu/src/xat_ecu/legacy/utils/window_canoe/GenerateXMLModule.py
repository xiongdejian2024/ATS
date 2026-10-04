'''
@Filename     : GenerateXMLModule.py
@Time         : 2024/06/21 17:02
@Author       : junxing.pang@jiduauto.com
@Description  : Generate xml module file demo
'''


import os
import re
import winreg
import logging

from xml.dom.minidom import Document


key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Volatile Environment")
username = winreg.QueryValueEx(key, 'USERNAME')

doc = Document()


def add_xml_ele(child_ele_name, parent_ele, child_ele_text=None):
    child_ele = doc.createElement(child_ele_name)
    parent_ele.appendChild(child_ele)
    if child_ele_text:
        child_ele.appendChild(doc.createTextNode(child_ele_text))


def _get_testcase_list(capl_path) -> list[str]:
    """get testcase list from capl file

    :param capl_path: capl file path
    :type capl_path: str
    :return: list of testcase id
    :rtype: list[str]
    """
    with open(capl_path, 'r', encoding='utf-8') as f:
        read = f.read()
    testcasename = re.findall(r"testcase (\w+)", read)
    return testcasename


def generate_xml_file(capl_path: str, filepath: str, filename: str) -> None:
    """Generate capl xml file

    :param capl_path: CAPL file path, just use this file to get testcase id
    :type capl_path: str
    :param filepath: save the xml file path
    :type filepath: str
    :param filename: save the xml file name
    :type filename: str
    """
    testcase_names = _get_testcase_list(capl_path)
    testmodule = doc.createElement('testmodule')
    testmodule.setAttribute('title', 'CANoe Test Module')
    testmodule.setAttribute('version', '1.1')
    testmodule.setAttribute(
        'xmlns', 'http://www.vector-informatik.de/CANoe/TestModule/1.27')
    add_xml_ele(child_ele_name='description', parent_ele=testmodule,
                child_ele_text='For execution of the test module ensure that no macro is running!')
    doc.appendChild(testmodule)

    test_sut_ele = doc.createElement('sut')
    test_info_ele = doc.createElement('info')
    add_xml_ele(child_ele_name='name', parent_ele=test_info_ele,
                child_ele_text='Test Module')
    add_xml_ele(child_ele_name='description', parent_ele=test_info_ele,
                child_ele_text='Function Integration Test Automation')
    test_sut_ele.appendChild(test_info_ele)
    testmodule.appendChild(test_sut_ele)

    test_engineer_ele = doc.createElement('engineer')
    test_info_ele = doc.createElement('info')
    add_xml_ele(child_ele_name='name', parent_ele=test_info_ele,
                child_ele_text=username[0])
    add_xml_ele(child_ele_name='description', parent_ele=test_info_ele,
                child_ele_text='CANoeDemo')
    test_engineer_ele.appendChild(test_info_ele)
    testmodule.appendChild(test_engineer_ele)

    test_testgroup_ele = doc.createElement('testgroup')
    test_testgroup_ele.setAttribute('title', 'PreCondition')
    add_xml_ele(child_ele_name='description', parent_ele=test_testgroup_ele,
                child_ele_text='This test group executed PreCondition.')

    test_capltestcase_ele = doc.createElement('capltestcase')
    test_capltestcase_ele.setAttribute('name', 'PreCondition')
    test_capltestcase_ele.setAttribute('title', 'PreCondition')
    test_capltestcase_ele.setAttribute('ident', 'TC-0000')
    test_testgroup_ele.appendChild(test_capltestcase_ele)
    testmodule.appendChild(test_testgroup_ele)

    test_testgroup_ele = doc.createElement('testgroup')
    test_testgroup_ele.setAttribute('title', 'Main Test')
    add_xml_ele(child_ele_name='description', parent_ele=test_testgroup_ele,
                child_ele_text='This test group verify basic function for UDS.')

    for cnt in range(1, len(testcase_names) - 1):
        test_capltestcase_ele = doc.createElement('capltestcase')
        test_capltestcase_ele.setAttribute('name', testcase_names[cnt])
        test_capltestcase_ele.setAttribute('title', testcase_names[cnt])
        test_capltestcase_ele.setAttribute('ident', 'TC-{:0>4d}'.format(cnt))
        test_testgroup_ele.appendChild(test_capltestcase_ele)
    testmodule.appendChild(test_testgroup_ele)

    test_testgroup_ele = doc.createElement('testgroup')
    test_testgroup_ele.setAttribute('title', 'PostCondition')
    add_xml_ele(child_ele_name='description', parent_ele=test_testgroup_ele,
                child_ele_text='This test group executed PostCondition.')

    test_capltestcase_ele = doc.createElement('capltestcase')
    test_capltestcase_ele.setAttribute('name', 'PostCondition')
    test_capltestcase_ele.setAttribute('title', 'PostCondition')
    test_capltestcase_ele.setAttribute(
        'ident', 'TC-{:0>4d}'.format(len(testcase_names) - 1))
    test_testgroup_ele.appendChild(test_capltestcase_ele)
    testmodule.appendChild(test_testgroup_ele)

    f_name_full = os.path.join(filepath, filename)
    with open(f_name_full, 'w', encoding='utf-8') as f:
        doc.writexml(f, indent='\t', newl='\n',
                     addindent='\t', encoding='utf-8')

    logging.info(f"Generate XML file:{f_name_full} OK")
