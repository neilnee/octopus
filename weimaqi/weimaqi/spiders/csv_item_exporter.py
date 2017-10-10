from scrapy.exporters import CsvItemExporter
from scrapy.conf import settings


class WeimaqiCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT_SETTING', [])
        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export

        super(WeimaqiCsvItemExporter, self).__init__(*args, **kwargs)
