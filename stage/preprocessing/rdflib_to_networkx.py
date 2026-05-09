from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from rdflib import OWL, RDF, RDFS, SKOS, BNode, Graph, Literal, URIRef, XSD

import networkx as nx

# ---------- Helpers ----------
def _qname_or_str(g: Graph, node) -> str:
    """Try qname; se fail, returns str(node)."""
    try:
        return g.qname(node)
    except Exception:
        return str(node)

def _label(g: Graph, node) -> str:
    """Get rdfs:label/skos:prefLabel; fallback p/ qname/str."""
    for p in (RDFS.label, SKOS.prefLabel):
        for lbl in g.objects(node, p):
            return str(lbl)
    return _qname_or_str(g, node)

def _in_allowed_ns(node, allowed_ns: Optional[Iterable[str]]) -> bool:
    if allowed_ns is None:
        return True
    if isinstance(node, (URIRef,)):
        s = str(node)
        return any(s.startswith(ns) for ns in allowed_ns)
    # Permite blank nodes quando filtrando por namespace (úteis em restrictions)
    return not isinstance(node, BNode)

def _in_relations_to_remove(relation: str, relations_to_remove: List[str]) -> bool:
    if relations_to_remove:
        for rel in relations_to_remove:
            if rel in relation:
                return True
    return False

def _add_node(G: nx.MultiDiGraph, node, **attrs):
    if node not in G:
        G.add_node(node, **attrs)
    else:
        # merge rótulos (não sobrescreve se já existe)
        for k, v in attrs.items():
            if k not in G.nodes[node] or G.nodes[node][k] in (None, "", []):
                G.nodes[node][k] = v

def _add_unique_edge(G, u, v, **attrs):
    # percorre todas as arestas existentes entre u e v
    for _, _, data in G.edges(u, v, default={}):
        if data == attrs:
            return  # já existe, não adiciona
    G.add_edge(u, v, **attrs)

# ---------- Coleta de tipos ----------
def _collect_sets(g: Graph, allowed_ns: Optional[Iterable[str]]) -> Tuple[Set, Set, Set]:
    classes, obj_props, data_props = set(), set(), set()

    for c in g.subjects(RDF.type, OWL.Class):
        if _in_allowed_ns(c, allowed_ns):
            classes.add(c)
    for c in g.subjects(RDF.type, RDFS.Class):
        if _in_allowed_ns(c, allowed_ns):
            classes.add(c)

    for p in g.subjects(RDF.type, OWL.ObjectProperty):
        if _in_allowed_ns(p, allowed_ns):
            obj_props.add(p)
    for p in g.subjects(RDF.type, OWL.DatatypeProperty):
        if _in_allowed_ns(p, allowed_ns):
            data_props.add(p)
    # Algumas ontologias usam rdf:Property genérico; registramos, mas
    # só rotulamos como objeto/dado quando virmos Literals nas asserções.
    return classes, obj_props, data_props

# ---------- Parsing de Restriction ----------
_RESTRICTION_FILLERS = [
    OWL.someValuesFrom,
    OWL.allValuesFrom,
    OWL.hasValue,
    OWL.minQualifiedCardinality,
    OWL.maxQualifiedCardinality,
    OWL.qualifiedCardinality,
    OWL.minCardinality,
    OWL.maxCardinality,
    OWL.cardinality,
]

def _parse_restrictions(g: Graph, cls, restriction_bnode) -> Dict[str, Any]:
    """Extrai dados principais de um owl:Restriction."""
    data: Dict[str, Any] = {"kind": "restriction"}
    on_prop = next(g.objects(restriction_bnode, OWL.onProperty), None)
    if on_prop:
        data["onProperty"] = on_prop
        data["onProperty_label"] = _label(g, on_prop)
    for f in _RESTRICTION_FILLERS:
        val = next(g.objects(restriction_bnode, f), None)
        if val is not None:
            data["filler_predicate"] = f
            data["filler_predicate_qname"] = _qname_or_str(g, f)
            # value pode ser classe, tipo de dado, literal ou número de cardinalidade
            data["filler_value"] = val
            data["filler_value_label"] = (
                str(val) if isinstance(val, Literal) else _label(g, val)
            )
            break
    return data


def rdflib_to_networkx(
        g: Graph,
        *,
        include_instances: bool = False,
        include_assertions: bool = False,
        include_restrictions: bool = False,
        allowed_namespaces: Optional[Iterable[str]] = None,
        relations_to_remove: Optional[Iterable[str]] = None,
    ) -> nx.MultiDiGraph:
        """
        Converte um rdflib.Graph em nx.MultiDiGraph.
        Nós têm attrs: kind ∈ {class, objectProperty, datatypeProperty, individual, literal, other},
        label, iri.
        Arestas têm attrs: relation (e.g., subClassOf, domain, range, type, assertion, equivalent, disjoint, restriction),
        e metadados (ex.: prop para assertions).
        """
        G = nx.MultiDiGraph()
        classes, obj_props, data_props = _collect_sets(g, allowed_namespaces)

        # --- Registrar classes e propriedades ---
        for c in classes:
            if not _in_allowed_ns(c, allowed_namespaces):
                continue
            _add_node(G, c, kind="class", label=_label(g, c), iri=str(c))
            _add_unique_edge(G, c, OWL.Class, relation=RDF.type)

        for p in obj_props:
            _add_node(G, p, kind="objectProperty", label=_label(g, p), iri=str(p))
            _add_unique_edge(G, p, OWL.ObjectProperty, relation=RDF.type)
        for p in data_props:
            _add_node(G, p, kind="datatypeProperty", label=_label(g, p), iri=str(p))
            _add_unique_edge(G, p, OWL.DatatypeProperty, relation=RDF.type)

        # --- Hierarquia de classes ---
        if not _in_relations_to_remove(str(RDFS.subClassOf), relations_to_remove):
            for s, o in g.subject_objects(RDFS.subClassOf):
                if not (_in_allowed_ns(s, allowed_namespaces) and _in_allowed_ns(o, allowed_namespaces)):
                    continue
                # o pode ser Restriction (bnode)
                if isinstance(o, BNode) and include_restrictions and (s, RDF.type, OWL.Class) in g:
                    if (o, RDF.type, OWL.Restriction) in g:
                        data = _parse_restrictions(g, s, o)
                        _add_node(G, s, kind="class", label=_label(g, s), iri=str(s))
                        # reificamos o restriction como um nó também (facilita visualização e consulta)
                        restr_node = o  # mantemos o próprio BNode
                        _add_node(G, restr_node, kind="restriction", label=data.get("filler_predicate_qname", "Restriction"))
                        _add_unique_edge(G, s, restr_node, relation=OWL.Restriction, **data)
                        #G.add_edge(s, restr_node, relation=OWL.Restriction, **data)
                        continue
                # subClassOf normal
                _add_node(G, s, kind="class", label=_label(g, s), iri=str(s))
                if isinstance(o, (URIRef, BNode)):
                    _add_node(G, o, kind="class", label=_label(g, o), iri=str(o))
                    _add_unique_edge(G, s, o, relation=RDFS.subClassOf)
                    #G.add_edge(s, o, relation=RDFS.subClassOf)

        # --- Equivalência / Disjunção de classes ---
        if not _in_relations_to_remove(str(OWL.equivalentClass), relations_to_remove):
            for s, o in g.subject_objects(OWL.equivalentClass):
                if _in_allowed_ns(s, allowed_namespaces) and _in_allowed_ns(o, allowed_namespaces):
                    _add_node(G, s, kind="class", label=_label(g, s), iri=str(s))
                    _add_node(G, o, kind="class", label=_label(g, o), iri=str(o))
                    _add_unique_edge(G, s, o, relation=OWL.equivalentClass)
                    _add_unique_edge(G, o, s, relation=OWL.equivalentClass)
                    # G.add_edge(s, o, relation=OWL.equivalentClass)
                    # G.add_edge(o, s, relation=OWL.equivalentClass)

        if not _in_relations_to_remove(str(OWL.disjointWith), relations_to_remove):
            for s, o in g.subject_objects(OWL.disjointWith):
                if _in_allowed_ns(s, allowed_namespaces) and _in_allowed_ns(o, allowed_namespaces):
                    _add_node(G, s, kind="class", label=_label(g, s), iri=str(s))
                    _add_node(G, o, kind="class", label=_label(g, o), iri=str(o))
                    _add_unique_edge(G, s, o, relation=OWL.disjointWith)
                    _add_unique_edge(G, o, s, relation=OWL.disjointWith)
                    # G.add_edge(s, o, relation=OWL.disjointWith)
                    # G.add_edge(o, s, relation=OWL.disjointWith)

        # --- Hierarquia de propriedades ---
        if not _in_relations_to_remove(str(RDFS.subPropertyOf), relations_to_remove):
            for s, o in g.subject_objects(RDFS.subPropertyOf):
                if _in_allowed_ns(s, allowed_namespaces) and _in_allowed_ns(o, allowed_namespaces):
                    # pode ser obj ou data; se ainda não conhecido, registramos como 'otherProperty'
                    if s not in G:
                        _add_node(G, s, kind="otherProperty", label=_label(g, s), iri=str(s))
                    if o not in G:
                        _add_node(G, o, kind="otherProperty", label=_label(g, o), iri=str(o))
                    _add_unique_edge(G, s, o, relation=RDFS.subPropertyOf)
                    # G.add_edge(s, o, relation=RDFS.subPropertyOf)

        # --- Domain / Range ---
        if not _in_relations_to_remove(str(RDFS.domain), relations_to_remove):
            for p, c in g.subject_objects(RDFS.domain):
                if _in_allowed_ns(p, allowed_namespaces) and _in_allowed_ns(c, allowed_namespaces):
                    if p not in G:
                        # pode não estar tipado; inferimos tipo pelo uso
                        _add_node(G, p, kind="otherProperty", label=_label(g, p), iri=str(p))
                    _add_node(G, c, kind="class", label=_label(g, c), iri=str(c))
                    _add_unique_edge(G, p, c, relation=RDFS.domain)
                    # G.add_edge(p, c, relation=RDFS.domain)
        if not _in_relations_to_remove(str(RDFS.range), relations_to_remove):
            for p, c in g.subject_objects(RDFS.range):
                if _in_allowed_ns(p, allowed_namespaces) and _in_allowed_ns(c, allowed_namespaces):
                    if p not in G:
                        _add_node(G, p, kind="otherProperty", label=_label(g, p), iri=str(p))
                    # range pode ser classe (obj prop) ou datatipo (XSD…)
                    node_kind = "class"
                    if isinstance(c, URIRef) and str(c).startswith(str(XSD)):
                        node_kind = "datatype"
                    _add_node(G, c, kind=node_kind, label=_label(g, c), iri=str(c))
                    _add_unique_edge(G, p, c, relation=RDFS.range)
                    #G.add_edge(p, c, relation=RDFS.range)

        # --- Propriedades equivalentes ---
        if not _in_relations_to_remove(str(OWL.equivalentProperty), relations_to_remove):
            for s, o in g.subject_objects(OWL.equivalentProperty):
                if _in_allowed_ns(s, allowed_namespaces) and _in_allowed_ns(o, allowed_namespaces):
                    if s not in G:
                        _add_node(G, s, kind="otherProperty", label=_label(g, s), iri=str(s))
                    if o not in G:
                        _add_node(G, o, kind="otherProperty", label=_label(g, o), iri=str(o))
                    _add_unique_edge(G, s, o, relation=OWL.equivalentProperty)
                    _add_unique_edge(G, o, s, relation=OWL.equivalentProperty)
                    # G.add_edge(s, o, relation=OWL.equivalentProperty)
                    # G.add_edge(o, s, relation=OWL.equivalentProperty)

        # --- Indivíduos e tipagem ---
        if include_instances:
            for s, o in g.subject_objects(RDF.type) and _in_relations_to_remove(str(RDF.type), relations_to_remove):
                if not _in_allowed_ns(s, allowed_namespaces):
                    continue
                # ignorar declarações de classe/propriedade aqui
                # if o in (OWL.Class, RDFS.Class, OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property):
                #     continue
                _add_node(G, s, kind="individual", label=_label(g, s), iri=str(s))
                if _in_allowed_ns(o, allowed_namespaces):
                    _add_node(G, o, kind="class", label=_label(g, o), iri=str(o))
                    _add_unique_edge(G, s, o, relation=RDF.type)
                    # G.add_edge(s, o, relation=RDF.type)

        # --- Asserções (triples) s p o ---
        if include_assertions:
            # Heurística: se o objeto for Literal => data property; se for URIRef/BNode => possivelmente object property
            for s, p, o in g:
                # pula triples de esquema já cobertos acima
                if p in (RDF.type, RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range,
                        OWL.equivalentClass, OWL.disjointWith, OWL.equivalentProperty):
                    continue
                if not _in_allowed_ns(s, allowed_namespaces) or not _in_allowed_ns(p, allowed_namespaces):
                    continue

                if isinstance(o, Literal):
                    _add_node(G, s, kind="individual", label=_label(g, s), iri=str(s))
                    _add_node(G, p, kind="datatypeProperty" if p in data_props else "otherProperty",
                            label=_label(g, p), iri=str(p))
                    lit_node = (s, p, o)  # cria um id estável p/ o literal ligado ao (s,p)
                    _add_node(G, lit_node, kind="literal", value=str(o), datatype=str(o.datatype) if o.datatype else None)
                    _add_unique_edge(G, s, lit_node, relation="dataAssertion", prop=p, prop_label=_label(g, p))
                    #G.add_edge(s, lit_node, relation="dataAssertion", prop=p, prop_label=_label(g, p))
                else:
                    # objeto é recurso; trate como object property assertion
                    if not _in_allowed_ns(o, allowed_namespaces):
                        continue
                    _add_node(G, s, kind="individual", label=_label(g, s), iri=str(s))
                    _add_node(G, o, kind="individual" if (o, RDF.type, None) in g else "other",
                            label=_label(g, o), iri=str(o))
                    _add_node(G, p, kind="objectProperty" if p in obj_props else "otherProperty",
                            label=_label(g, p), iri=str(p))
                    _add_unique_edge(G, s, o, relation="objectAssertion", prop=p, prop_label=(g, p))
                    #G.add_edge(s, o, relation="objectAssertion", prop=p, prop_label=_label(g, p))
        nodes_to_remove = [
            OWL.Class,
            OWL.ObjectProperty,
            OWL.DatatypeProperty,
            OWL.Thing,
            XSD.string,
            XSD.anyURI,
            XSD.date,
            XSD.time
        ]
        for n in G.nodes():
            if isinstance(n, BNode):
                nodes_to_remove.append(n)
        G.remove_nodes_from(nodes_to_remove)
        return G