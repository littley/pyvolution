import yaml


class FileManager():
    """
    Use this class to read and write to disk
    """

    def __init__(self):
        pass

    def write(self, data, target):
        """
        Can write anything to file that has a .data() method returning a YAML friendly object
        :param target: the file where this object should be written
        """
        fobj = open(target, "w")
        fobj.write(self.freezeDry(data))
        fobj.close()


    def freezeDry(self, data):
        return yaml.dump(data.data(), default_flow_style=False)

