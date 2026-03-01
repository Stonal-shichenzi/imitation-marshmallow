import json, os, math

class pack():
    class __mcmeta():
        def __init__(self, file_path, resource):
            if os.path.exists(file_path):
                os.remove(file_path)
            self.file = open(file_path, mode="w+")
            self.file.seek(0)
            self.file.write("")
            self.resource = resource
        def versions(self, max: float, min: float):
            self.file.seek(0)
            if not self.file.read():
                self.file.write("{}")
            self.file.seek(0)
            self.written = json.loads(self.file.read())
            if isinstance(min, int) or isinstance(min, float):
                if min < 0:
                    raise TypeError("versions must be unsigned numbers, not {}".format(min.__class__.__name__))
            else:
                raise TypeError("versions must be unsigned numbers, not {}".format(min.__class__.__name__))
            if isinstance(max, int) or isinstance(max, float):
                if max < 0:
                    raise TypeError("versions must be unsigned numbers, not {}".format(max.__class__.__name__))
            else:
                raise TypeError("versions must be unsigned numbers, not {}".format(max.__class__.__name__))
            if min < (65 if self.resource else 82):
                self.written["pack"]["pack_format"] = math.floor(max)
                self.written["pack"]["supported_formats"] = [math.floor(min), math.ceil(max)]
            if max > (64 if self.resource else 81):
                self.written["pack"]["max_format"] = list(map(int, str(max).split(".", maxsplit=1)))
                self.written["pack"]["min_format"] = list(map(int, str(min).split(".", maxsplit=1)))
            self.file.write(json.dumps(self.written))
        def description(self, description: str):
            self.file.seek(0)
            if not self.file.read():
                self.file.write("{}")
            self.written = json.loads(self.file.read())
            self.written["description"] = description
            self.file.seek(0)
            self.file.write(json.dumps(self.written))
        def read_all(self):
            return json.loads(self.file.read())
        # def read(self):
        #     return self.file.read()
        def write_all(self, json_data):
            self.file.seek(0)
            self.file.write(json.dumps(json_data))
        # def write(self, con: str):
        #     self.file.seek(0)
        #     self.file.write(con)
        def __del__(self):
            self.file.close()
    def __init__(self, path: str, pack_name: str, namespace: str, resource = False):
        if os.path.exists(path):
            self.dir = path
            self.name = pack_name
            self.resource = resource
            self.namespace = namespace
            if not os.path.exists("{0}/{1}".format(self.dir, self.name)):
                os.mkdir("{0}/{1}".format(self.dir, self.name))
            os.chdir("{0}/{1}".format(self.dir, self.name))
            self.mcmeta = self.__mcmeta("{0}/{1}/pack.mcmeta".format(self.dir, self.name), resource)
        else:
            raise FileNotFoundError("path '{}' cannot be found".format(path))
    def write_plain(self, path: str, data: str, belong_to_data_pack = True, vanilla = False):
        namespace = ("minecraft" if vanilla else self.namespace)
        if not os.path.exists(("data/{}" if belong_to_data_pack else "assets/{}").format(self.namespace)):
            os.mkdir("{0}/{1}".format(self.dir, self.name))
        main_path = ("data/{0}/{1}" if belong_to_data_pack else "assets/{0}/{1}")
        temporary_file = open(main_path.format(namespace, path), "w", encoding="utf-8")
        temporary_file.write(data)
        temporary_file.close()
    def read_plain(self, path: str, belong_to_data_pack = True, vanilla = False):
        main_path = ("data/{0}/{1}" if belong_to_data_pack else "assets/{0}/{1}")
        namespace = ("minecraft" if vanilla else self.namespace)
        temporary_file = open(main_path.format(namespace, path), "r", encoding="utf-8")
        data = temporary_file.read()
        temporary_file.close()
        return data
    def write_bool(self, path: str, data: bytes, belong_to_data_pack = True, vanilla = False):
        namespace = ("minecraft" if vanilla else self.namespace)
        main_path = ("data/{0}/{1}" if belong_to_data_pack else "assets/{0}/{1}")
        temporary_file = open(main_path.format(namespace, path), "wb")
        temporary_file.write(data)
        temporary_file.close()
    def read_bool(self, path: str, belong_to_data_pack = True, vanilla = False):
        namespace = ("minecraft" if vanilla else self.namespace)
        main_path = ("data/{0}/{1}" if belong_to_data_pack else "assets/{0}/{1}")
        temporary_file = open(main_path.format(namespace, path), "rb")
        data = temporary_file.read()
        temporary_file.close()
        return data
    def write_json(self, path: str, data, belong_to_data_pack = True, vanilla = False):
        self.write_plain(path, json.dumps(data), belong_to_data_pack, vanilla)
    def read_json(self, path: str, belong_to_data_pack = True, vanilla = False):
        return json.loads(self.read_plain(path, belong_to_data_pack, vanilla))
    def write_arg(self, argv: dict):
        arg = argv
        if "belong_to_data_pack" not in arg:
            arg["belong_to_data_pack"] = True
        if "vanilla" not in arg:
            arg["vanilla"] = False
        self.write_plain(arg["path"], arg["data"], arg["belong_to_data_pack"], arg["vanilla"])