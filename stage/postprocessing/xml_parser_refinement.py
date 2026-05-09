from lxml import etree

NS = {
    "edoal": "http://ns.inria.org/edoal/1.0/#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}

class XMLParserRefinement:
    def __init__(self, edoal_string):
        self.edoal_string = edoal_string

    def parse(self):
        return etree.fromstring(self.edoal_string.encode())

    def refine(self, root, verbalize_dict, source_or_target):
        for key, value in verbalize_dict.items():
            self.replace_all_with_iri(root, "//edoal:Class", key, value, source_or_target)
            self.replace_all_with_iri(root, "//edoal:Relation", key, value, source_or_target)

    def replace_all_with_iri(self, root, tag, key, value, source_or_target):
        for cls in root.xpath(tag, namespaces=NS):
            if self.get_source_or_target(cls) == source_or_target:
                self.replace_with_iri(cls, key, value)

    def get_source_or_target(self, classes):
        parent = classes.getparent()
        while True:
            if "entity1" in parent.tag:
                return "source"
            if "entity2" in parent.tag:
                return "target"
            parent = parent.getparent()

    def replace_with_iri(self, classes, key, value):
        about_attribute = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
        resource_attribute = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"
        about = classes.get(about_attribute)
        resource = classes.get(resource_attribute)
        if about:
            self.replace(classes, about_attribute, key, value, about)
        elif resource:
            self.replace(classes, resource_attribute, key, value, resource)

    def replace(self, classes, attribute, key, value, iri):
        iri_label = ''
        if '#' in iri:
            iri_label = iri.split('#')[-1]
        elif '/' in iri:
            iri_label = iri.split('/')[-1]

        if value == iri or value == iri_label:
            classes.set(
                attribute,
                key
            )