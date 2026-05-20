---
name: drug-discovery
description: Pharmaceutical research assistant — search bioactive compounds on ChEMBL, calculate drug-likeness (Lipinski Ro5, QED, TPSA), look up drug interactions via OpenFDA, and interpret ADMET profiles
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks about drug molecules, bioactive compounds, or pharmaceutical research
  - User wants to assess drug-likeness of a molecule (Lipinski Ro5, Veber rules, QED)
  - User asks about drug-drug interactions or adverse events for a medication
  - User needs target-disease associations or gene-disease literature
  - User wants molecular property analysis, ADMET profiling, or lead optimization
related_skills:
  - fitness-nutrition
  - searxng-search
---

# Drug Discovery & Pharmaceutical Research

## Description

Pharmaceutical research assistant for drug discovery workflows. Search bioactive compounds on ChEMBL, calculate drug-likeness (Lipinski Rule of Five, QED, TPSA, synthetic accessibility), look up drug-drug interactions via OpenFDA, interpret ADMET profiles, and assist with lead optimization. Uses free, public APIs — no authentication required.

## Prerequisites

- Python 3.8+ (stdlib only: `json`, `urllib.parse`, `sys`)
- `curl` for API calls
- Internet access for ChEMBL, PubChem, OpenFDA, and OpenTargets APIs

## Steps

### 1. Bioactive compound search (ChEMBL)

ChEMBL is the world's largest open bioactivity database. No API key required.

**Search targets by name (e.g., "EGFR", "COX-2", "ACE"):**

```bash
TARGET="EGFR"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$TARGET")
curl -s "https://www.ebi.ac.uk/chembl/api/data/target/search?q=${ENCODED}&format=json" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
targets=data.get('targets',[])[:5]
for t in targets:
    print(f\"ChEMBL ID : {t.get('target_chembl_id')}\")
    print(f\"Name      : {t.get('pref_name')}\")
    print(f\"Type      : {t.get('target_type')}\")
    print()
"
```

**Get bioactivity data for a ChEMBL target ID:**

```bash
TARGET_ID="CHEMBL203"
curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id=${TARGET_ID}&pchembl_value__gte=6&limit=10&format=json" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
acts=data.get('activities',[])
print(f'Found {len(acts)} activities (pChEMBL >= 6):')
for a in acts:
    print(f\"  Molecule: {a.get('molecule_chembl_id')}  |  {a.get('standard_type')}: {a.get('standard_value')} {a.get('standard_units')}  |  pChEMBL: {a.get('pchembl_value')}\")
"
```

**Look up a specific molecule by ChEMBL ID:**

```bash
MOL_ID="CHEMBL25"  # aspirin
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule/${MOL_ID}?format=json" \
  | python3 -c "
import json,sys
m=json.load(sys.stdin)
props=m.get('molecule_properties',{}) or {}
print(f\"Name       : {m.get('pref_name','N/A')}\")
print(f\"SMILES     : {m.get('molecule_structures',{}).get('canonical_smiles','N/A') if m.get('molecule_structures') else 'N/A'}\")
print(f\"MW         : {props.get('full_mwt','N/A')} Da\")
print(f\"LogP       : {props.get('alogp','N/A')}\")
print(f\"HBD        : {props.get('hbd','N/A')}\")
print(f\"HBA        : {props.get('hba','N/A')}\")
print(f\"TPSA       : {props.get('psa','N/A')} Å²\")
print(f\"Ro5 violations: {props.get('num_ro5_violations','N/A')}\")
print(f\"QED        : {props.get('qed_weighted','N/A')}\")
"
```

### 2. Drug-likeness calculation (Lipinski Ro5 + Veber)

Assess any molecule against established oral bioavailability rules using PubChem's free property API — no RDKit required.

```bash
COMPOUND="aspirin"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,TPSA,InChIKey/JSON" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
props=data['PropertyTable']['Properties'][0]
mw   = float(props.get('MolecularWeight', 0))
logp = float(props.get('XLogP', 0))
hbd  = int(props.get('HBondDonorCount', 0))
hba  = int(props.get('HBondAcceptorCount', 0))
rot  = int(props.get('RotatableBondCount', 0))
tpsa = float(props.get('TPSA', 0))
print('=== Lipinski Rule of Five (Ro5) ===')
print(f'  MW   {mw:.1f} Da    {\"✓\" if mw<=500 else \"✗ VIOLATION (>500)\"}')
print(f'  LogP {logp:.2f}       {\"✓\" if logp<=5 else \"✗ VIOLATION (>5)\"}')
print(f'  HBD  {hbd}           {\"✓\" if hbd<=5 else \"✗ VIOLATION (>5)\"}')
print(f'  HBA  {hba}           {\"✓\" if hba<=10 else \"✗ VIOLATION (>10)\"}')
viol = sum([mw>500, logp>5, hbd>5, hba>10])
print(f'  Violations: {viol}/4  {\"→ Likely orally bioavailable\" if viol<=1 else \"→ Poor oral bioavailability predicted\"}')
print()
print('=== Veber Oral Bioavailability Rules ===')
print(f'  TPSA         {tpsa:.1f} Å²   {\"✓\" if tpsa<=140 else \"✗ VIOLATION (>140)\"}')
print(f'  Rot. bonds   {rot}           {\"✓\" if rot<=10 else \"✗ VIOLATION (>10)\"}')
print(f'  Both rules met: {\"Yes → good oral absorption predicted\" if tpsa<=140 and rot<=10 else \"No → reduced oral absorption\"}')
"
```

### 3. Drug interaction & safety lookup (OpenFDA)

**Drug interactions from FDA labels:**

```bash
DRUG="warfarin"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
curl -s "https://api.fda.gov/drug/label.json?search=drug_interactions:\"${ENCODED}\"&limit=3" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
results=data.get('results',[])
if not results: print('No interaction data found in FDA labels.'); sys.exit()
for r in results[:2]:
    brand=r.get('openfda',{}).get('brand_name',['Unknown'])[0]
    generic=r.get('openfda',{}).get('generic_name',['Unknown'])[0]
    interactions=r.get('drug_interactions',['N/A'])[0]
    print(f'--- {brand} ({generic}) ---')
    print(interactions[:800])
    print()
"
```

**Top adverse events for a drug:**

```bash
DRUG="warfarin"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
curl -s "https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:\"${ENCODED}\"&count=patient.reaction.reactionmeddrapt.exact&limit=10" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
results=data.get('results',[])
if not results: print('No adverse event data found.'); sys.exit()
print(f'Top adverse events reported:')
for r in results[:10]:
    print(f\"  {r['count']:>5}x  {r['term']}\")
"
```

### 4. PubChem compound search

```bash
COMPOUND="aspirin"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
CID=$(curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/cids/TXT" | head -1 | tr -d '[:space:]')
echo "PubChem CID: $CID"
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${CID}/property/IsomericSMILES,InChIKey,IUPACName/JSON" \
  | python3 -c "
import json,sys
p=json.load(sys.stdin)['PropertyTable']['Properties'][0]
print(f\"IUPAC Name : {p.get('IUPACName','N/A')}\")
print(f\"SMILES     : {p.get('IsomericSMILES','N/A')}\")
print(f\"InChIKey   : {p.get('InChIKey','N/A')}\")
"
```

### 5. Target & disease literature (OpenTargets)

```bash
GENE="EGFR"
curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"{ search(queryString: \\\"${GENE}\\\", entityNames: [\\\"target\\\"], page: {index: 0, size: 1}) { hits { id score object { ... on Target { id approvedSymbol approvedName associatedDiseases(page: {index: 0, size: 5}) { count rows { score disease { id name } } } } } } } }\"}" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
hits=data.get('data',{}).get('search',{}).get('hits',[])
if not hits: print('Target not found.'); sys.exit()
obj=hits[0]['object']
print(f\"Target: {obj.get('approvedSymbol')} — {obj.get('approvedName')}\")
assoc=obj.get('associatedDiseases',{})
print(f\"Associated with {assoc.get('count',0)} diseases. Top associations:\")
for row in assoc.get('rows',[]):
    print(f\"  Score {row['score']:.3f}  |  {row['disease']['name']}\")
"
```

## Reasoning Guidelines

When analyzing drug-likeness or molecular properties:

1. State raw values first — MW, LogP, HBD, HBA, TPSA, RotBonds
2. Apply rule sets — Ro5 (Lipinski), Veber, Ghose filter where relevant
3. Flag liabilities — metabolic hotspots, hERG risk, high TPSA for CNS penetration
4. Suggest optimizations — bioisosteric replacements, prodrug strategies, ring truncation
5. Cite the source API — ChEMBL, PubChem, OpenFDA, or OpenTargets

For ADMET questions, reason through Absorption, Distribution, Metabolism, Excretion, Toxicity systematically. See `references/ADMET_REFERENCE.md` for detailed guidance.

## Pitfalls

1. **ChEMBL rate limits** — Add `sleep 1` between batch requests to avoid being rate-limited. ChEMBL is a shared public resource.
2. **FDA adverse events are reported, not causal** — OpenFDA data reflects reported events, not necessarily proven causal relationships. Always state this caveat and recommend consulting a licensed pharmacist or physician for clinical decisions.
3. **PubChem property values may vary by source** — XLogP, MW, and other properties may differ between PubChem and ChEMBL for the same compound. Always cite which source you used.
4. **WHOIS/GDPR does not apply here but FDA labels may be incomplete** — Not all drugs have comprehensive interaction data in OpenFDA labels. If a query returns no results, it may mean the data is missing, not that no interactions exist.
5. **ChEMBL search uses `term` parameter** — The exercise search endpoint uses `term`, not `query`. Using the wrong parameter name returns empty results with no error.

## Verification

1. **ChEMBL target search works**: Run the target search for "EGFR" and confirm it returns ChEMBL IDs and target names
2. **Drug-likeness calculation works**: Run the Lipinski Ro5 calculation for "aspirin" and confirm it returns MW, LogP, HBD, HBA with pass/fail assessments
3. **OpenFDA interaction lookup works**: Run the drug interaction search for "warfarin" and confirm it returns interaction text from FDA labels

## Cross-References

- **fitness-nutrition** — Health and fitness tracking complementary to pharmacology queries
- **searxng-search** — General web research for pharmaceutical news and publications