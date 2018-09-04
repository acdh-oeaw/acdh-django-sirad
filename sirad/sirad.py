import re
import lxml.etree as ET
import pandas as pd
from jinja2 import Template

from . code_templates import *

FIELD_TYPE_MAP = {
    "INTEGER": "IntegerField",
    "SMALLINT": "IntegerField",
    "CHARACTER VARYING": "CharField",
    "TIMESTAMP": "DateTimeField",
    "DOUBLE PRECISION": "FloatField",
    "BOOLEAN": "NullBooleanField"
}


def harmonize_field_types(string):
    try:
        match = re.findall('\d+', string)[0]
    except IndexError:
        match = False
    if match:
        if int(match) > 250:
            return "TextField"
        else:
            return "CharField"
    else:
        return FIELD_TYPE_MAP[string]


def make_class_names(string):
    joined = "".join([x.title() for x in string.lower().split('_')])
    if len(joined) > 3 and joined.endswith('s'):
        return joined[:-1]
    else:
        return joined


class SiradReader():

    """ a class to process sirad metadata file """

    def __init__(self, xml_file):
        self.nsmap = {
            'sirad': "http://www.bar.admin.ch/xmlns/siard/2.0/metadata.xsd"
        }
        self.tree = ET.parse(xml_file)
        self.DJANGO_APP_FILES = {
            "admin.py": ADMIN_PY,
            "urls.py": URLS_PY,
            "filters.py": FILTERS_PY,
            "forms.py": FORMS_PY,
            "tables.py": TABLES_PY,
            "views.py": VIEWS_PY,
            "models.py": MODELS_PY
        }

    def get_columns(self):
        return self.tree.xpath('.//sirad:tables//sirad:columns/sirad:column', namespaces=self.nsmap)

    def get_field_dict(self, column):
        field_dict = {}
        field_dict['table_name'] = column.xpath(
            './/ancestor::sirad:table/sirad:name/text()',
            namespaces=self.nsmap
        )[0]
        field_dict['table_rows'] = int(
            column.xpath(
                './/ancestor::sirad:table/sirad:rows/text()',
                namespaces=self.nsmap
            )[0]
        )
        field_dict['folder_name'] = column.xpath(
            './/ancestor::sirad:table/sirad:folder/text()',
            namespaces=self.nsmap
        )[0]
        field_dict['field_name'] = column.xpath('./sirad:name/text()', namespaces=self.nsmap)[0]
        field_dict['field_type'] = column.xpath('./sirad:type/text()', namespaces=self.nsmap)[0]
        field_dict['field_nullable'] = column.xpath(
            './sirad:nullable/text()', namespaces=self.nsmap)[0]

        return field_dict

    def tables_df(self):
        df = pd.DataFrame([self.get_field_dict(x) for x in self.get_columns()])
        df['fields_per_table'] = df.groupby('table_name')['table_name'].transform('count')
        df['model_name'] = df.apply(lambda row: make_class_names(row['table_name']), axis=1)
        df['model_field_name'] = df.apply(lambda row: row['field_name'].lower(), axis=1)
        df['model_field_type'] = df.apply(
            lambda row: harmonize_field_types(row['field_type']), axis=1
        )
        return df

    def get_unique_values(self, column_name='table_name'):
        df = self.tables_df()
        return df[column_name].unique()

    def rows_grouped_by(self, column_name='model_name'):
        return self.tables_df().groupby(column_name)

    def datamodel_as_dicts(self):
        classes = []
        for name, group in self.rows_grouped_by('model_name'):
            class_dict = {}
            class_dict['model_name'] = name
            class_dict['fields'] = []
            for i, row in group.iterrows():
                field = {}
                field['model_field_name'] = row['model_field_name']
                field['model_field_type'] = row['model_field_type']
                class_dict['fields'].append(field)
            classes.append(class_dict)
        return classes

    def serialize_data_model(self, app_name="my_sirad_app", file_name='output_model.py'):
        t = Template(MODELS_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_views(self, app_name="my_sirad_app", file_name='output_views.py'):
        t = Template(VIEWS_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_tables(self, app_name="my_sirad_app", file_name='output_tables.py'):
        t = Template(TABLES_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_forms(self, app_name="my_sirad_app", file_name='output_forms.py'):
        t = Template(FORMS_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_filters(self, app_name="my_sirad_app", file_name='output_filters.py'):
        t = Template(FILTERS_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_urls(self, app_name="my_sirad_app", file_name='output_urls.py'):
        t = Template(URLS_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_admin(self, app_name="my_sirad_app", file_name='output_admin.py'):
        t = Template(ADMIN_PY)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def serialize_file(
        self, app_name="my_sirad_app", file_name='output_file.py', template=MODELS_PY
    ):
        t = Template(template)
        output = t.render(
            data=self.datamodel_as_dicts(),
            app_name=app_name
        )
        with open(file_name, "w") as text_file:
            print(output, file=text_file)
        return output

    def generate_app_files(self, app_name='my_sirad_app', prefix=None):
        for key, value in self.DJANGO_APP_FILES.items():
            if prefix:
                filename = "{}_{}".format(prefix, key)
            else:
                filename = key
            yield self.serialize_file(app_name="my_sirad_app", file_name=key, template=value)
