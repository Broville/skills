---
name: fitness-nutrition
description: Gym workout planner and nutrition tracker using wger exercise database and USDA FoodData Central, plus offline calculators for BMI, TDEE, 1RM, macros, and body fat
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks about exercises, workouts, gym routines, muscle groups, or workout splits
  - User asks about food macros, calories, protein content, meal planning, or calorie counting
  - User asks about body composition metrics (BMI, body fat, TDEE, caloric surplus/deficit)
  - User asks about one-rep max estimates or training percentages
  - User asks about macro ratios for cutting, bulking, or maintenance
related_skills:
  - drug-discovery
---

# Fitness & Nutrition

## Description

Expert fitness coach and sports nutritionist skill. Two data sources (wger exercise database, USDA FoodData Central) plus offline calculators — everything a gym-goer needs in one place. Search 690+ exercises by muscle, equipment, or category. Look up macros and calories for 380,000+ foods. Compute BMI, TDEE, one-rep max, macro splits, and body fat percentage using pure Python stdlib — no pip installs required.

## Prerequisites

- Python 3.8+ (stdlib only, no pip dependencies)
- `curl` for API calls
- Internet access for wger and USDA APIs (offline calculators work without)

## Data Sources

- **wger** (`https://wger.de/api/v2/`) — Open exercise database, 690+ exercises with muscles, equipment, images. Public endpoints need zero authentication.
- **USDA FoodData Central** (`https://api.nal.usda.gov/fdc/v1/`) — US government nutrition database, 380,000+ foods. Uses `DEMO_KEY` by default (30 req/hour); set `USDA_API_KEY` environment variable for higher limits (free signup at <https://fdc.nal.usda.gov/api-key-signup/>).

## Steps

### 1. Exercise Lookup (wger API)

All wger public endpoints return JSON and require no auth. Always add `format=json` and `language=2` (English) to exercise queries.

**Search exercises by name:**

```bash
QUERY="bench press"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")
curl -s "https://wger.de/api/v2/exercise/search/?term=${ENCODED}&language=english&format=json" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
for s in data.get('suggestions',[])[:10]:
    d=s.get('data',{})
    print(f\"  ID {d.get('id','?'):>4} | {d.get('name','N/A'):<35} | Category: {d.get('category','N/A')}\")
"
```

**Get full exercise details:**

```bash
EXERCISE_ID="1"
curl -s "https://wger.de/api/v2/exerciseinfo/${EXERCISE_ID}/?format=json" \
  | python3 -c "
import json,sys,html,re
data=json.load(sys.stdin)
trans=[t for t in data.get('translations',[]) if t.get('language')==2]
t=trans[0] if trans else data.get('translations',[{}])[0]
desc=re.sub('<[^>]+>','',html.unescape(t.get('description','N/A')))
print(f\"Exercise  : {t.get('name','N/A')}\")
print(f\"Category  : {data.get('category',{}).get('name','N/A')}\")
print(f\"Primary   : {', '.join(m.get('name_en','') for m in data.get('muscles',[])) or 'N/A'}\")
print(f\"Secondary : {', '.join(m.get('name_en','') for m in data.get('muscles_secondary',[])) or 'none'}\")
print(f\"Equipment : {', '.join(e.get('name','') for e in data.get('equipment',[])) or 'bodyweight'}\")
print(f\"How to    : {desc[:500]}\")
"
```

**Filter exercises by muscle, category, or equipment:**

```bash
# Muscles: 1=Biceps, 4=Pectoralis, 10=Quadriceps, 12=Latissimus, 14=Triceps
# Categories: 8=Arms, 9=Legs, 10=Abs, 11=Chest, 12=Back, 13=Shoulders, 15=Cardio
# Equipment: 1=Barbell, 3=Dumbbell, 7=Bodyweight, 10=Kettlebell
FILTER="muscles=4"
curl -s "https://wger.de/api/v2/exercise/?${FILTER}&language=2&status=2&limit=20&format=json" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
print(f'Found {data.get(\"count\",0)} exercises.')
for ex in data.get('results',[]):
    print(f\"  ID {ex['id']:>4} | muscles: {ex.get('muscles',[])} | equipment: {ex.get('equipment',[])}\")
"
```

### 2. Nutrition Lookup (USDA FoodData Central)

```bash
FOOD="chicken breast"
API_KEY="${USDA_API_KEY:-DEMO_KEY}"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$FOOD")
curl -s "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=${API_KEY}&query=${ENCODED}&pageSize=5&dataType=Foundation,SR%20Legacy" \
  | python3 -c "
import json,sys
data=json.load(sys.stdin)
foods=data.get('foods',[])
if not foods: print('No foods found.'); sys.exit()
for f in foods:
    n={x['nutrientName']:x.get('value','?') for x in f.get('foodNutrients',[])}
    cal=n.get('Energy','?'); prot=n.get('Protein','?')
    fat=n.get('Total lipid (fat)','?'); carb=n.get('Carbohydrate, by difference','?')
    print(f\"{f.get('description','N/A')}\")
    print(f\"  Per 100g: {cal} kcal | {prot}g protein | {fat}g fat | {carb}g carbs\")
    print(f\"  FDC ID: {f.get('fdcId','N/A')}\")
    print()
"
```

**Detailed nutrient profile by FDC ID:**

```bash
FDC_ID="175035"
API_KEY="${USDA_API_KEY:-DEMO_KEY}"
curl -s "https://api.nal.usda.gov/fdc/v1/food/${FDC_ID}?api_key=${API_KEY}" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f\"Food: {d.get('description','N/A')}\")
print(f\"{'Nutrient':<40} {'Amount':>8} {'Unit'}\")
print('-'*56)
for x in sorted(d.get('foodNutrients',[]),key=lambda x:x.get('nutrient',{}).get('rank',9999)):
    nut=x.get('nutrient',{}); amt=x.get('amount',0)
    if amt and float(amt)>0:
        print(f\"  {nut.get('name',''):<38} {amt:>8} {nut.get('unitName','')}\")
"
```

### 3. Offline Calculators

Uses helper scripts in `scripts/` for batch operations, or inline for single calculations:

```bash
python3 scripts/body_calc.py bmi <weight_kg> <height_cm>
python3 scripts/body_calc.py tdee <weight_kg> <height_cm> <age> <M|F> <activity 1-5>
python3 scripts/body_calc.py 1rm <weight> <reps>
python3 scripts/body_calc.py macros <tdee_kcal> <cut|maintain|bulk>
python3 scripts/body_calc.py bodyfat <M|F> <neck_cm> <waist_cm> [hip_cm] <height_cm>
```

## Pitfalls

1. **wger returns all languages by default** — Always add `language=2` for English results, otherwise you get exercises in German and other languages.
2. **wger includes unverified user submissions** — Add `status=2` to only get approved exercises; without this filter, low-quality entries appear in results.
3. **USDA DEMO_KEY rate limit is only 30 req/hour** — For batch lookups, add `sleep 2` between requests, or sign up for a free API key (1,000 req/hour) at <https://fdc.nal.usda.gov/api-key-signup/>.
4. **USDA data is per 100g** — Always remind users to scale to their actual portion size; a "serving" in casual speech is rarely exactly 100g.
5. **BMI does not distinguish muscle from fat** — High BMI in muscular people is not necessarily unhealthy; always mention this caveat when reporting BMI.
6. **Body fat formulas are estimates (±3-5%)** — Recommend DEXA scans for precision measurements when accuracy matters.
7. **1RM formulas lose accuracy above 10 reps** — Use sets of 3-5 reps for best one-rep max estimates.
8. **wger search endpoint uses `term` not `query`** — The parameter name is `/exercise/search/?term=...`, not `query=...`.

## Verification

1. **Exercise search returns results**: After running an exercise search query, confirm the output includes exercise names, muscle groups, and equipment fields
2. **Nutrition lookup returns macros**: After a food search, confirm per-100g macros are returned with kcal, protein, fat, and carbs
3. **Calculators produce sane output**: Run `python3 scripts/body_calc.py tdee 75 180 30 M 3` and confirm TDEE is between 2000-3500 kcal for typical adult inputs

## Cross-References

- **drug-discovery** — Pharmaceutical research complementary to health/fitness queries