#!/bin/bash
set -e

# Downloads datasets and references from:
# https://github.com/liseda-lab/complex-OM-benchmark
#
# Conference dataset is sourced from popconference/popconference-0-v1.
# Change CONFERENCE_VERSION below to use a different population level (0, 20, 40, 60, 80, 100).

BASE_URL="https://raw.githubusercontent.com/liseda-lab/complex-OM-benchmark/main"
CONFERENCE_VERSION="popconference-0-v1"

LFS_BATCH_URL="https://github.com/liseda-lab/complex-OM-benchmark.git/info/lfs/objects/batch"

download() {
    local url="$1"
    local dest="$2"
    local tmp
    tmp=$(mktemp)

    wget -q -O "$tmp" "$url"

    if grep -q "version https://git-lfs.github.com/spec/v1" "$tmp" 2>/dev/null; then
        local oid size lfs_href
        oid=$(grep "^oid sha256:" "$tmp" | sed 's/oid sha256://')
        size=$(grep "^size " "$tmp" | sed 's/size //')
        lfs_href=$(curl -s -X POST \
            -H "Content-Type: application/vnd.git-lfs+json" \
            -H "Accept: application/vnd.git-lfs+json" \
            -d "{\"operation\":\"download\",\"transfers\":[\"basic\"],\"objects\":[{\"oid\":\"$oid\",\"size\":$size}]}" \
            "$LFS_BATCH_URL" \
            | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['objects'][0]['actions']['download']['href'])")
        wget -q --show-progress -O "$dest" "$lfs_href"
        rm -f "$tmp"
    else
        mv "$tmp" "$dest"
    fi
}

# ── Directory structure ────────────────────────────────────────────────────────

mkdir -p datasets/conference
mkdir -p datasets/enslaved
mkdir -p datasets/geolink
mkdir -p datasets/hydrography
mkdir -p datasets/taxon

mkdir -p references/conference
mkdir -p references/enslaved
mkdir -p references/geolink
mkdir -p references/hydrography
mkdir -p references/taxon

CONF_SRC="$BASE_URL/popconference/$CONFERENCE_VERSION"

# ── Datasets ───────────────────────────────────────────────────────────────────

echo "=============================="
echo " Downloading DATASETS"
echo "=============================="

echo "[datasets/conference]  (source: popconference/$CONFERENCE_VERSION)"
download "$CONF_SRC/cmt-confOf/source.rdf"       datasets/conference/cmt.owl
download "$CONF_SRC/cmt-confOf/target.rdf"        datasets/conference/confOf.owl
download "$CONF_SRC/cmt-conference/target.rdf"    datasets/conference/conference.owl
download "$CONF_SRC/cmt-edas/target.rdf"          datasets/conference/edas.owl
download "$CONF_SRC/cmt-ekaw/target.rdf"          datasets/conference/ekaw.owl

echo "[datasets/enslaved]"
download "$BASE_URL/popenslaved/enslaved-wikidata/source.rdf"  datasets/enslaved/enslaved.owl
download "$BASE_URL/popenslaved/enslaved-wikidata/target.rdf"  datasets/enslaved/wikidata.owl

echo "[datasets/geolink]"
download "$BASE_URL/geolink/gbo-gmo/source.rdf"   datasets/geolink/gbo.owl
download "$BASE_URL/geolink/gbo-gmo/target.rdf"   datasets/geolink/gmo.owl

echo "[datasets/hydrography]"
download "$BASE_URL/hydrography/cree-swo/source.rdf"              datasets/hydrography/cree.owl
download "$BASE_URL/hydrography/cree-swo/target.rdf"              datasets/hydrography/swo.owl
download "$BASE_URL/hydrography/hydro3-swo/source.rdf"            datasets/hydrography/hydro3.owl
download "$BASE_URL/hydrography/hydrOntology_native-swo/source.rdf"  datasets/hydrography/hydrOntology.owl

echo "[datasets/taxon]"
download "$BASE_URL/taxon/taxon-agrovoc/source.owl"  datasets/taxon/taxon.owl
download "$BASE_URL/taxon/taxon-agrovoc/target.owl"  datasets/taxon/agrovoc.owl
download "$BASE_URL/taxon/taxon-dbpedia/target.owl"  datasets/taxon/dbpedia.owl
download "$BASE_URL/taxon/taxon-taxref/target.owl"   datasets/taxon/taxref.owl

# ── References ─────────────────────────────────────────────────────────────────

echo ""
echo "=============================="
echo " Downloading REFERENCES"
echo "=============================="

echo "[references/conference]  (source: popconference/$CONFERENCE_VERSION)"
CONF_PAIRS=(
    cmt-confOf
    cmt-conference
    cmt-edas
    cmt-ekaw
    #confOf-cmt
    #confOf-conference
    confOf-edas
    confOf-ekaw
    #conference-cmt
    #conference-confOf
    conference-edas
    conference-ekaw
    #edas-cmt
    #edas-confOf
    #edas-conference
    edas-ekaw
    #ekaw-cmt
    #ekaw-confOf
    #ekaw-conference
    #ekaw-edas
)
for pair in "${CONF_PAIRS[@]}"; do
    download "$CONF_SRC/$pair/reference.rdf" "references/conference/$pair.edoal"
done

echo "[references/enslaved]"
download "$BASE_URL/popenslaved/enslaved-wikidata/reference.rdf"  references/enslaved/enslaved-wikidata.edoal

echo "[references/geolink]"
download "$BASE_URL/geolink/gbo-gmo/reference.rdf"  references/geolink/gbo-gmo.edoal

echo "[references/hydrography]"
download "$BASE_URL/hydrography/cree-swo/reference.rdf"                     references/hydrography/cree-swo.edoal
download "$BASE_URL/hydrography/hydro3-swo/reference.rdf"                   references/hydrography/hydro3-swo.edoal
download "$BASE_URL/hydrography/hydrOntology_native-swo/reference.rdf"      references/hydrography/hydrOntology-swo.edoal
download "$BASE_URL/hydrography/hydrOntology_translated-swo/reference.rdf"  references/hydrography/hydrOntology_translated-swo.edoal

echo "[references/taxon]"
download "$BASE_URL/taxon/taxon-agrovoc/reference.edoal"  references/taxon/taxon-agrovoc.edoal
download "$BASE_URL/taxon/taxon-dbpedia/reference.edoal"  references/taxon/taxon-dbpedia.edoal
download "$BASE_URL/taxon/taxon-taxref/reference.edoal"   references/taxon/taxon-taxref.edoal

echo ""
echo "=============================="
echo " Download complete!"
echo "=============================="
echo ""
echo "Folder structure:"
find datasets references -type f | sort
