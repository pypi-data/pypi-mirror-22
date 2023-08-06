import gzip
import json
import tarfile
from collections import OrderedDict
from copy import deepcopy
from io import BytesIO

import six
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError as JsonSchemaError

from ...exceptions import ValidationError
from ...schema import DEFAULT_FILE_MODE
from ...utils import evaluate_vars, merge_config


class BaseBackend(object):
    """
    Base Backend class
    """
    schema = None
    FILE_SECTION_DELIMITER = '# ---------- files ---------- #'
    intermediate_data = None

    def __init__(self, config, templates=[], context={}):
        """
        :param config: ``dict`` containing valid **NetJSON DeviceConfiguration**
        :param templates: ``list`` containing **NetJSON** dictionaries that will be
                          used as a base for the main config, defaults to empty list
        :param context: ``dict`` containing configuration variables
        :raises TypeError: raised if ``config`` is not of type ``dict`` or if
                           ``templates`` is not of type ``list``
        """
        # perform deepcopy to avoid modifying the original config argument
        config = deepcopy(self._load(config))
        self.config = self._merge_config(config, templates)
        self.config = self._evaluate_vars(self.config, context)

    def _load(self, config):
        """
        Loads config from string or dict
        """
        if isinstance(config, six.string_types):
            try:
                config = json.loads(config)
            except ValueError:
                pass
        if not isinstance(config, dict):
            raise TypeError('config block must be an istance '
                            'of dict or a valid NetJSON string')
        return config

    def _merge_config(self, config, templates):
        """
        Merges config with templates
        """
        # type check
        if not isinstance(templates, list):
            raise TypeError('templates argument must be an instance of list')
        # merge any present template with main configuration
        base_config = {}

        for template in templates:
            template = self._load(template)
            base_config = merge_config(base_config, template)
        if base_config:
            return merge_config(base_config, config)
        return config

    def _evaluate_vars(self, config, context):
        """
        Evaluates configuration variables
        """
        # return immediately if context is empty
        if not context:
            return config
        # only if variables are found perform evaluation
        return evaluate_vars(config, context)

    def _render_files(self):
        """
        Renders additional files specified in ``self.config['files']``
        """
        output = ''
        # render files
        files = self.config.get('files', [])
        # add delimiter
        if files:
            output += '\n{0}\n\n'.format(self.FILE_SECTION_DELIMITER)
        for f in files:
            mode = f.get('mode', DEFAULT_FILE_MODE)
            # add file to output
            file_output = '# path: {0}\n'\
                          '# mode: {1}\n\n'\
                          '{2}\n\n'.format(f['path'], mode, f['contents'])
            output += file_output
        return output

    def validate(self):
        try:
            validate(self.config, self.schema, format_checker=FormatChecker())
        except JsonSchemaError as e:
            raise ValidationError(e)

    def render(self, files=True):
        """
        Converts the configuration dictionary into the corresponding configuration format

        :param files: whether to include "additional files" in the output or not;
                      defaults to ``True``
        :returns: string with output
        """
        self.validate()
        # convert NetJSON config to intermediate data structure
        if self.intermediate_data is None:
            self.to_intermediate()
        # render intermediate data structure into native configuration
        renderer = self.renderer(self)
        output = renderer.render()
        # remove reference to renderer instance (not needed anymore)
        del renderer
        # are we required to include
        # additional files?
        if files:
            # render additional files
            files_output = self._render_files()
            if files_output:
                # max 2 new lines
                output += files_output.replace('\n\n\n', '\n\n')
        # return the configuration
        return output

    def json(self, validate=True, *args, **kwargs):
        """
        returns a string formatted as **NetJSON DeviceConfiguration**;
        performs validation before returning output;

        ``*args`` and ``*kwargs`` will be passed to ``json.dumps``;

        :returns: string
        """
        if validate:
            self.validate()
        # automatically adds NetJSON type
        config = deepcopy(self.config)
        config.update({'type': 'DeviceConfiguration'})
        return json.dumps(config, *args, **kwargs)

    def generate(self):
        """
        Returns a ``BytesIO`` instance representing an in-memory tar.gz archive
        containing the native router configuration.

        :returns: in-memory tar.gz archive, instance of ``BytesIO``
        """
        tar_bytes = BytesIO()
        tar = tarfile.open(fileobj=tar_bytes, mode='w')
        self._generate_contents(tar)
        self._process_files(tar)
        tar.close()
        tar_bytes.seek(0)  # set pointer to beginning of stream
        # `mtime` parameter of gzip file must be 0, otherwise any checksum operation
        # would return a different digest even when content is the same.
        # to achieve this we must use the python `gzip` library because the `tarfile`
        # library does not seem to offer the possibility to modify the gzip `mtime`.
        gzip_bytes = BytesIO()
        gz = gzip.GzipFile(fileobj=gzip_bytes, mode='wb', mtime=0)
        gz.write(tar_bytes.getvalue())
        gz.close()
        gzip_bytes.seek(0)  # set pointer to beginning of stream
        return gzip_bytes

    def _generate_contents(self, tar):
        raise NotImplementedError()

    def write(self, name, path='./'):
        """
        Like ``generate`` but writes to disk.

        :param name: file name, the tar.gz extension will be added automatically
        :param path: directory where the file will be written to, defaults to ``./``
        :returns: None
        """
        byte_object = self.generate()
        file_name = '{0}.tar.gz'.format(name)
        if not path.endswith('/'):
            path += '/'
        f = open('{0}{1}'.format(path, file_name), 'wb')
        f.write(byte_object.getvalue())
        f.close()

    def _process_files(self, tar):
        """
        Adds files specified in self.config['files'] to tarfile instance.

        :param tar: tarfile instance
        :returns: None
        """
        # insert additional files
        for file_item in self.config.get('files', []):
            path = file_item['path']
            # remove leading slashes from path
            if path.startswith('/'):
                path = path[1:]
            self._add_file(tar=tar,
                           name=path,
                           contents=file_item['contents'],
                           mode=file_item.get('mode', DEFAULT_FILE_MODE))

    def _add_file(self, tar, name, contents, mode=DEFAULT_FILE_MODE):
        """
        Adds a single file in tarfile instance.

        :param tar: tarfile instance
        :param name: string representing filename or path
        :param contents: string representing file contents
        :param mode: string representing file mode, defaults to 644
        :returns: None
        """
        byte_contents = BytesIO(contents.encode('utf8'))
        info = tarfile.TarInfo(name=name)
        info.size = len(contents)
        # mtime must be 0 or any checksum operation
        # will return a different digest even when content is the same
        info.mtime = 0
        info.type = tarfile.REGTYPE
        info.mode = int(mode, 8)  # permissions converted to decimal notation
        tar.addfile(tarinfo=info, fileobj=byte_contents)

    def to_intermediate(self):
        """
        Converts the NetJSON configuration dictionary (self.config)
        to the intermediate data structure (self.intermediate_data) that will
        be then used by the renderer class to generate the router configuration
        """
        self.validate()
        data = OrderedDict()
        for converter_class in self.converters:
            # skip unnecessary loop cycles
            if not converter_class.should_run(self.config):
                continue
            converter = converter_class(self)
            for item in converter.to_intermediate():
                key, value = item
                if value:
                    data.setdefault(key, [])
                    data[key] += value
        self.intermediate_data = data
