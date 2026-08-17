# Validation Checklist

Run this checklist after every XML edit, before claiming the bot is ready.

## 1. XML Well-Formedness

- [ ] File is valid XML (no parse errors)
- [ ] All tags are properly opened and closed
- [ ] All attribute values are quoted
- [ ] No unescaped special characters (`&`, `<`, `>`)
- [ ] No duplicate `id` attributes within the file

**Test:**
```bash
python -c "import xml.etree.ElementTree as ET; ET.parse('FILE.xml'); print('PASS')"
```

## 2. Root Element

- [ ] Root is `<xml>` with correct namespaces
- [ ] `is_dbot="true"` attribute present
- [ ] `collection="false"` attribute present

## 3. Variables Section

- [ ] `<variables>` section exists before any blocks
- [ ] Every variable used in the file is declared
- [ ] Every declared variable is used at least once
- [ ] No duplicate variable names
- [ ] Variable `id` attributes match between declaration and usage

**Test:**
```bash
# Extract declared IDs and used IDs, find mismatches
python -c "
import re, sys
xml = open('FILE.xml').read()
declared = set(re.findall(r'<variable id=\"([^\"]+)\">', xml))
used = set(re.findall(r'name=\"VAR\"\s+id=\"([^\"]+)\"', xml))
missing = used - declared
unused = declared - used
if missing: print(f'MISSING DECLARATIONS: {missing}')
if unused: print(f'UNUSED VARIABLES: {unused}')
if not missing and not unused: print('PASS')
"
```

## 4. Trade Definition

- [ ] `trade_definition` block exists
- [ ] Has `TRADE_OPTIONS` statement
- [ ] Contains all 6 chain blocks in order:
  1. `trade_definition_market`
  2. `trade_definition_tradetype`
  3. `trade_definition_contracttype`
  4. `trade_definition_candleinterval`
  5. `trade_definition_restartbuysell`
  6. `trade_definition_restartonerror`
- [ ] All chain blocks connected via `<next>`
- [ ] `trade_definition` has `deletable="false"`
- [ ] Chain blocks have `deletable="false"` and `movable="false"`
- [ ] `MARKET_LIST` is a valid market name
- [ ] `SYMBOL_LIST` is a valid symbol for the chosen market
- [ ] `TRADETYPECAT_LIST` matches `TRADETYPE_LIST`
- [ ] `CANDLEINTERVAL_LIST` is a valid interval

## 5. Trade Options (SUBMARKET)

- [ ] `SUBMARKET` statement exists in trade_definition
- [ ] Contains `trade_definition_tradeoptions` block (if using duration/amount)
- [ ] Duration and amount values are reasonable

## 6. Before Purchase Block

- [ ] `before_purchase` block exists at top level
- [ ] Has `BEFOREPURCHASE_STACK` statement
- [ ] Contains signal logic that leads to a `purchase` block
- [ ] All variables referenced are declared
- [ ] All block `id` attributes are unique

## 7. After Purchase Block

- [ ] `after_purchase` block exists at top level
- [ ] Has `AFTERPURCHASE_STACK` statement
- [ ] Updates `Total_Profit` using contract payout
- [ ] Handles win/loss (checks `contract Profit` or `contract Code`)
- [ ] Contains `trade_again` block (bot must be able to continue)
- [ ] Stop conditions checked before `trade_again`:
  - [ ] Target profit check
  - [ ] Stop loss check
  - [ ] Daily loss limit check

## 8. Martingale Logic (if applicable)

- [ ] `Loss_Count` incremented on loss
- [ ] `Loss_Count` reset to 0 on win
- [ ] `Current_Stake` multiplied by `Martingale_Multiplier` on loss
- [ ] `Current_Stake` reset to `Initial_Stake` on win
- [ ] `Loss_Count` compared against `Max_Martingale_Level`
- [ ] Stake does not exceed logical maximum

## 9. Block Connection Integrity

- [ ] No orphaned blocks (every block is inside a statement, value, or next)
- [ ] Every `controls_if` with `else="1"` has a `<statement name="ELSE">`
- [ ] Every `controls_if` with `elseif="N"` has IF0..IFN and DO0..DON
- [ ] `mutation` element present on every `controls_if` with elif/else
- [ ] `trade_again` is reachable from all code paths in after_purchase

## 10. Common Pitfalls

- [ ] No empty `<statement>` tags
- [ ] No whitespace-only `<field name="NUM">` values
- [ ] No duplicate block IDs
- [ ] `notify` blocks have `NOTIFICATION_TYPE` and `NOTIFICATION_SOUND` fields
- [ ] `text` blocks inside `notify` have `TEXT` field with non-empty value

---

## Automated Validation Script

Save as `validate_bot.py`:

```python
#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re
import sys

def validate(filepath):
    errors = []
    
    # 1. Parse XML
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"FAIL: XML parse error: {e}")
        return False
    
    # 2. Check root
    if root.tag != 'xml':
        errors.append("Root element must be <xml>")
    if root.get('is_dbot') != 'true':
        errors.append("Missing is_dbot='true' attribute")
    
    # 3. Check variables
    xml_text = open(filepath).read()
    declared = set(re.findall(r'<variable id="([^"]+)">', xml_text))
    used = set(re.findall(r'name="VAR"\s+id="([^"]+)"', xml_text))
    missing = used - declared
    if missing:
        errors.append(f"Variables used but not declared: {missing}")
    
    # 4. Check trade definition
    has_trade_def = 'trade_definition" id=' in xml_text
    has_market = 'trade_definition_market' in xml_text
    has_tradetype = 'trade_definition_tradetype' in xml_text
    has_contracttype = 'trade_definition_contracttype' in xml_text
    has_candleinterval = 'trade_definition_candleinterval' in xml_text
    has_restartbuysell = 'trade_definition_restartbuysell' in xml_text
    has_restartonerror = 'trade_definition_restartonerror' in xml_text
    
    if not has_trade_def:
        errors.append("Missing trade_definition block")
    if not all([has_market, has_tradetype, has_contracttype, has_candleinterval, has_restartbuysell, has_restartonerror]):
        errors.append("Incomplete trade definition chain")
    
    # 5. Check top-level blocks
    has_before = 'before_purchase' in xml_text
    has_after = 'after_purchase' in xml_text
    if not has_before:
        errors.append("Missing before_purchase block")
    if not has_after:
        errors.append("Missing after_purchase block")
    
    # 6. Check for trade_again
    has_trade_again = 'trade_again' in xml_text
    if not has_trade_again:
        errors.append("Missing trade_again block")
    
    # Report
    if errors:
        print(f"FAIL: {filepath}")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"PASS: {filepath}")
        return True

if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else ['*.xml']
    import glob
    all_files = []
    for f in files:
        all_files.extend(glob.glob(f))
    
    passed = 0
    failed = 0
    for f in all_files:
        if validate(f):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
```

**Usage:**
```bash
python validate_bot.py *.xml
python validate_bot.py specific-bot.xml
```
