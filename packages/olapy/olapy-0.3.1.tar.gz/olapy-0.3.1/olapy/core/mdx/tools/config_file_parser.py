from __future__ import absolute_import, division, print_function

import os

from lxml import etree

from .models import Cube, Dimension, Facts


class ConfigParser:
    """
    Parse olapy config files
    """

    def __init__(self, cube_path, file_name='cubes-config.xml'):
        """
        
        :param cube_path: path to cube (csv folders)
        :param file_name: config file name (DEFAULT = cubes-config.xml)
        """
        self.cube_path = cube_path
        self.file_name = file_name

    def config_file_exist(self):
        """
        check whether the config file exists or not 
        :return: True | False
        """
        return os.path.isfile(os.path.join(self.cube_path, self.file_name))

    def xmla_authentication(self):
        """
        check if excel need authentication to access cubes or not. (xmla_authentication tag in the config file)
        :return: True | False
        """

        with open(os.path.join(self.cube_path, self.file_name)) as config_file:

            parser = etree.XMLParser()
            tree = etree.parse(config_file, parser)

            try:
                return tree.xpath('/cubes/xmla_authentication')[
                    0].text == 'True'
            except:
                return False

    def get_cubes_names(self):
        """
        get all cubes names in the config file
        
        :return: dict of cube name as key and cube source as value (csv or postgres) (right now only postgres is supported)
        """

        with open(os.path.join(self.cube_path, self.file_name)) as config_file:

            parser = etree.XMLParser()
            tree = etree.parse(config_file, parser)

            try:
                return {
                    cube.find('name').text: cube.find('source').text
                    for cube in tree.xpath('/cubes/cube')
                }
            except:
                raise ('missed name or source tags')

    def construct_cubes(self):
        """
        construct cube (with it dimensions) and facts from  the config file
        :return: list of Cubes instance
        """

        if self.config_file_exist():
            try:
                with open(os.path.join(self.cube_path,
                                       self.file_name)) as config_file:

                    parser = etree.XMLParser()
                    tree = etree.parse(config_file, parser)

                    facts = [
                        Facts(
                            table_name=xml_facts.find('table_name').text,
                            keys={
                                key.text: key.attrib['ref']
                                for key in xml_facts.findall(
                                    'keys/column_name')
                            },
                            measures=[
                                mes.text
                                for mes in xml_facts.findall('measures/name')
                            ]) for xml_facts in tree.xpath('/cubes/cube/facts')
                    ]

                    dimensions = [
                        Dimension(
                            name=xml_dimension.find('name').text,
                            displayName=xml_dimension.find('displayName').text,
                            columns=[
                                column_name.text
                                for column_name in xml_dimension.findall(
                                    'columns/name')
                            ])
                        for xml_dimension in tree.xpath(
                            '/cubes/cube/dimensions/dimension')
                    ]

                return [
                    Cube(
                        name=xml_cube.find('name').text,
                        source=xml_cube.find('source').text,
                        facts=facts,
                        dimensions=dimensions)
                    for xml_cube in tree.xpath('/cubes/cube')
                ]
            except:
                raise ('Bad configuration in the configuration file')
        else:
            raise ("Config file don't exist")
