import struct
import numpy as np
from Orange.data import FileFormat
from orangecontrib.spectroscopy.io.util import SpectralFileFormat


class BlockReader:
    def __init__(self, data, start=0):
        self.data = data
        self.start = start
    

    def peek(self, step, format=None, expect_tuple=False):
        block = self.data[self.start : self.start + step]
        return BlockReader.format(block, format, expect_tuple=expect_tuple)
    

    def read(self, step, format=None, expect_tuple=False):
        block = self.peek(step, format=format, expect_tuple=expect_tuple)
        self.step(step)
        return block
    

    def step(self, step):
        self.start += step

    
    def atEnd(self, step=0):
        return self.start >= self.size - step
    

    @property
    def size(self):
        return len(self.data)
    

    @staticmethod
    def readData(data, start, step, format=None, expect_tuple=False):
        block = data[start : start + step]
        return BlockReader.format(block, format, expect_tuple=expect_tuple)
    

    @staticmethod
    def format(data, format, expect_tuple=False):
        DECODE_FORMATS = [
            "utf-8",
        ]

        if format == None:
            return data
        
        if format in DECODE_FORMATS:
            assert(not expect_tuple)

            return BlockReader._decode(data, format)
        
        unpacked = BlockReader._unpack(data, format)
        
        if expect_tuple:
            return unpacked
        
        return BlockReader._asSingular(unpacked)
    

    @staticmethod
    def _decode(data, format):
        return data.decode(format)


    @staticmethod
    def _unpack(data, format):
        return struct.unpack(format, data)
    

    @staticmethod
    def _asSingular(unpacked):
        assert(len(unpacked) == 1)

        return unpacked[0]





class PerkinElmer:
    @staticmethod
    def varIdDecode(data, var_id, format, step, expect_tuple=False):
        _var_id = BlockReader.readData(data, 0, 2, "<H", False)

        if var_id == _var_id:
            return BlockReader.readData(data, 2, step, format=format, expect_tuple=expect_tuple)
        
        raise struct.error(f"Expected {var_id}, but got {_var_id}.")
    

    @staticmethod
    def createMeta(values, attrs, meta=dict()):
        for attr_name, attr_index in attrs:
            try:
                meta[attr_name] = values[attr_index]
            except IndexError:
                meta[attr_name] = None

        return meta


    @staticmethod
    def decode5100(data):
        
        name_size = BlockReader.readData(data, 0, 2, format="<h", expect_tuple=False)
        name = BlockReader.readData(data, 2, name_size, format="utf-8")

        header_format = '<ddddddddddiiihBhBhBhB'
        header_size = 104

        values = BlockReader.readData(data, name_size + 2, header_size, format=header_format, expect_tuple=True)

        meta = PerkinElmer.createMeta(
            values,
            [
                ("x_delta", 0),
                ("y_delta", 1),
                ("z_delta", 2),
                ("z_start", 3),
                ("z_end", 4),
                ("z_4d_start", 5),
                ("z_4d_end", 6),
                ("x_init", 7),
                ("y_init", 8),
                ("z_init", 9),
                ("n_x", 10),
                ("n_y", 11),
                ("n_z", 12),
                ("text1", 14),
                ("text2", 16),
                ("resolution", 17),
                ("text3", 18),
                ("transmission", 19),
                ("text4", 20),
            ],
            meta={"name": name,}
        )
        
        return meta


    @staticmethod
    def decode5104(data):
        values = []

        block_reader = BlockReader(data)

        while not block_reader.atEnd(2):
            tag = block_reader.read(2)

            if tag == b'#u':
                value_size = block_reader.read(2, format="<h", expect_tuple=False)
                values.append(block_reader.read(value_size, format="utf-8"))
                block_reader.step(6)
            
            elif tag == b'$u':
                values.append(block_reader.read(2, format="<h", expect_tuple=False))
                block_reader.step(6)
            
            elif tag == b',u':
                values.append(block_reader.read(2, format="<h", expect_tuple=False))
            
            else:
                block_reader.step(-1)

        meta = PerkinElmer.createMeta(
            values,
            [
                ("analyst", 0),
                ("date", 2),
                ("image_name", 4),
                ("instrument_model", 5),
                ("instrument_serial_number", 6),
                ("instrument_software_version", 7),
                ("accumulations", 9),
                ("detector", 11),
                ("source", 12),
                ("beam_splitter", 13),
                ("apodization", 15),
                ("spectrum_type", 16),
                ("beam_type", 17),
                ("phase_correction", 20),
                ("ir_accessory", 26),
                ("igram_type", 28),
                ("scan_direction", 29),
                ("background_scans", 32),
                ("ir_laser_wave_number_unit", 67),
            ],
        )
        
        return meta


    @staticmethod
    def decode5105(data):
        return np.frombuffer(data, dtype=np.float32)


    @staticmethod
    def decode25739(data):
        var_size = PerkinElmer.varIdDecode(data, 29987, "<H", 2, expect_tuple=False)
        file_path = BlockReader.readData(data, 4, var_size, format="utf-8")
        
        return {'file_path': file_path}


    @staticmethod
    def decode35698(data):
        min_wavelength, max_wavelength = PerkinElmer.varIdDecode(data, 29981, "<dd", 16, expect_tuple=True)
        
        return {'min_wavelength': min_wavelength, 'max_wavelength': max_wavelength}


    @staticmethod
    def decode35699(data):
        min_abs, max_abs = PerkinElmer.varIdDecode(data, 29981, "<dd", 16, expect_tuple=True)

        return {'min_absolute': min_abs, 'max_absolute': max_abs}


    @staticmethod
    def decode35700(data):
        wavelength_step = PerkinElmer.varIdDecode(data, 29979, "<d", 8, expect_tuple=False)

        return {'wavelength_step': wavelength_step}


    @staticmethod
    def decode35701(data):
        n_points = PerkinElmer.varIdDecode(data, 29995, "<I", 4, expect_tuple=False)

        return {'n_points': n_points}


    @staticmethod
    def decode35708(data):
        var_size = PerkinElmer.varIdDecode(data, 29974, "<I", 4, expect_tuple=False)

        return np.frombuffer(BlockReader.readData(data, 6, var_size, format=None), dtype=np.float64)

    


class SPReader(FileFormat, SpectralFileFormat):

    EXTENSIONS = (".sp",)
    DESCRIPTION = "Perkin Elmer File"


    def read_spectra(self):
        f = open(self.filename, "rb")
        data = f.read()
        f.close()

        block_reader = BlockReader(data)

        meta = {
            "signature" : block_reader.read(4, format="utf-8"),
            "description" : block_reader.read(40, format="utf-8"),
        }

        func_decode = {
            25739: PerkinElmer.decode25739,
            35698: PerkinElmer.decode35698,
            35699: PerkinElmer.decode35699,
            35700: PerkinElmer.decode35700,
            35701: PerkinElmer.decode35701,
            35708: PerkinElmer.decode35708,
        }

        stops = []
        spectrum = []

        block_id, block_size = block_reader.read(6, format="<Hi", expect_tuple=True)

        stops.append(block_reader.start + block_size)

        while block_id != 122 and not block_reader.atEnd(2):
            next_block_id = block_reader.peek(2)

            if next_block_id[1] == 117:
                block_reader.start = stops[-1]
                stops = stops[:-1]

                while block_reader.start >= stops[-1]:
                    stops = stops[:-1]
            
            else:
                block_id, block_size = block_reader.read(6, format="<Hi", expect_tuple=True)
                stops.append(block_reader.start + block_size)

        meta.update(PerkinElmer.decode5104(block_reader.read(block_size)))

        block_reader.start = stops[1]

        while not block_reader.atEnd():
            block_id, block_size = block_reader.read(6, format="<Hi", expect_tuple=True)

            if block_id in func_decode.keys():
                decoded = func_decode[block_id](block_reader.peek(block_size))

                if isinstance(decoded, dict):
                    meta.update(decoded)
                
                else:
                    spectrum = decoded

            block_reader.start += block_size

        wavelength = np.linspace(meta['min_wavelength'], meta['max_wavelength'], meta['n_points'])
        
        return np.array(wavelength), np.array(spectrum)[None,...], None




class FSMReader(FileFormat, SpectralFileFormat):

    EXTENSIONS = (".fsm",)
    DESCRIPTION = "Perkin Elmer File"


    def read_spectra(self):
        f = open(self.filename, "rb")
        data = f.read()
        f.close()

        block_reader = BlockReader(data)

        meta = {
            "signature" : block_reader.read(4, format="utf-8"),
            "description" : block_reader.read(40, format="utf-8"),
        }

        func_decode = {
            5100: PerkinElmer.decode5100,
            5104: PerkinElmer.decode5104,
            5105: PerkinElmer.decode5105,
        }

        spectrum = []

        while not block_reader.atEnd(6):
            block_id, block_size = block_reader.read(6, format="<Hi", expect_tuple=True)

            data_extracted = func_decode[block_id](block_reader.read(block_size))

            if isinstance(data_extracted, dict):
                meta.update(data_extracted)
            else:
                spectrum.append(data_extracted)

        spectrum = np.squeeze(spectrum)
        wavelength = np.arange(meta['z_start'], meta['z_end'] + meta['z_delta'], meta['z_delta'])

        return np.array(wavelength), spectrum, None
