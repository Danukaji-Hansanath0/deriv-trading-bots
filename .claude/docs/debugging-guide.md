# Debugging Guide

## Systematic Debugging Workflow

### Step 1: Identify the Symptom

| Symptom | Likely Cause |
|---------|--------------|
| Bot won't import | XML parse error (malformed tags, unclosed elements) |
| Bot imports but won't start | Missing trade_definition block or broken chain |
| Bot starts but no trades | Signal logic never triggers purchase |
| Bot trades wrong market | Wrong SYMBOL_LIST or TRADETYPECAT_LIST |
| Bot crashes mid-run | Uninitialized variable, division by zero |
| Bot ignores stop conditions | Stop check block not connected to trade chain |
| Martingale not working | Loss_Count not incrementing or reset logic wrong |

### Step 2: Check XML Well-Formedness

```bash
python -c "import xml.etree.ElementTree as ET; ET.parse('bot.xml'); print('XML is valid')"
```

Common parse errors:
- **Unclosed tag:** `<block type="...">` without matching `</block>`
- **Mismatched quotes:** `<field name="OP">GT</field` (missing `>`)
- **Ampersand in text:** `AT&T` should be `AT&amp;T`
- **Nested incorrectly:** block A opens, block B opens, block A closes before B

### Step 3: Check Trade Definition Chain

The trade_definition chain must be unbroken. Verify:

1. `trade_definition` block exists
2. Contains `TRADE_OPTIONS` statement
3. Inside it: market → tradetype → contracttype → candleinterval → restartbuysell → restartonerror
4. Each connected via `<next>` element
5. All 6 blocks present and in order

**Quick check:**
```bash
grep -c "trade_definition_market" bot.xml
grep -c "trade_definition_tradetype" bot.xml
grep -c "trade_definition_contracttype" bot.xml
grep -c "trade_definition_candleinterval" bot.xml
grep -c "trade_definition_restartbuysell" bot.xml
grep -c "trade_definition_restartonerror" bot.xml
```

Each should return exactly `1`.

### Step 4: Check Variables

**Common variable errors:**

1. **Variable used but not declared:**
   - Search for `<field name="VAR" id="X">` — the `id` must exist in `<variables>`
   - The display name after `</field>` must match the `<variable id="X">Name</variable>` text

2. **Variable declared but never used:**
   - Not fatal but wastes clarity — remove unused variables

3. **Duplicate variable names:**
   - Two `<variable>` with the same text — causes name collision

4. **Mismatched IDs:**
   ```bash
   # Extract declared variable IDs
   grep '<variable id=' bot.xml | sed 's/.*id="\([^"]*\)".*/\1/' | sort > /tmp/declared.txt
   
   # Extract used variable IDs
   grep 'name="VAR" id=' bot.xml | sed 's/.*id="\([^"]*\)".*/\1/' | sort > /tmp/used.txt
   
   # Find used but not declared
   comm -23 /tmp/used.txt /tmp/declared.txt
   ```

### Step 5: Check Block Connections

**Orphaned blocks:** blocks that aren't connected to any statement or value:

```bash
# Find blocks that aren't inside a <statement> or <value>
# (Manual inspection required — look for <block> at unexpected indentation)
```

**Missing connections:**
- Every `controls_if` with `else="1"` must have a `<statement name="ELSE">`
- Every `controls_if` with `elseif="N"` must have `IF0` through `IFN` and `DO0` through `DON`
- `trade_again` must be reachable from the after_purchase logic path

### Step 6: Check Field Values

Incorrect field values cause silent failures:

| Block Type | Field | Valid Values |
|------------|-------|--------------|
| `trade_definition_market` | `MARKET_LIST` | `synthetic_index`, `forex`, `indices`, `commodities`, `stocks` |
| `trade_definition_tradetype` | `TRADETYPECAT_LIST` | `callput`, `accumulator`, `multiplier`, `turbos`, `ticks` |
| `trade_definition_contracttype` | `TYPE_LIST` | `both`, `call`, `put`, `ACCU` |
| `trade_definition_candleinterval` | `CANDLEINTERVAL_LIST` | `60`, `120`, `300`, `900`, `1800`, `3600` |
| `logic_compare` | `OP` | `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE` |
| `math_arithmetic` | `OP` | `ADD`, `MINUS`, `MULTIPLY`, `DIVIDE`, `POWER` |
| `logic_operation` | `OP` | `AND`, `OR` |

### Step 7: Check for Common XML Bugs

1. **Whitespace in NUM fields:**
   ```xml
   <!-- BAD -->
   <field name="NUM"> 10 </field>
   <!-- GOOD -->
   <field name="NUM">10</field>
   ```

2. **Empty statements:**
   ```xml
   <!-- BAD - empty statement causes error -->
   <statement name="DO0"></statement>
   ```

3. **Double-nested trade_definition:**
   ```xml
   <!-- BAD - trade_definition inside another trade_definition -->
   ```

4. **Missing mutation element:**
   ```xml
   <!-- controls_if with elseif or else MUST have mutation -->
   <block type="controls_if">
     <mutation else="1"></mutation>  <!-- REQUIRED -->
   ```

---

## Python Script Debugging

The project includes `fix_bots.py` and `fix_martingale.py` for bulk XML modifications.

### Running fix_bots.py

```bash
python fix_bots.py
```

**What it does:**
1. Adds `Max_Martingale_Level`, `Martingale_Multiplier`, `Daily_Loss_Limit` variables if missing
2. Adds initialization blocks for those variables after `Stop_Loss`
3. Adds stop condition checks (target profit, stop loss, daily loss) before `trade_again`

### Debugging Script Issues

If the script fails on a file:
- Check if the file has a `Stop_Loss` variable initialization (required anchor point)
- Check if `trade_again` block exists (required for stop condition insertion)
- Check if the XML is well-formed first

---

## Quick Fix Patterns

### Fix Missing Variable Declaration

Find the `<variables>` section and add:
```xml
<variable id="YOUR_ID">Variable_Name</variable>
```

### Fix Orphaned Block

Wrap the orphaned block in the correct statement:
```xml
<block type="after_purchase" id="...">
  <statement name="AFTERPURCHASE_STACK">
    <!-- Move orphaned block here -->
  </statement>
</block>
```

### Fix Broken Chain

Reconnect broken `<next>` links:
```xml
<block type="variables_set" id="block1">
  <!-- ... -->
  <next>
    <block type="variables_set" id="block2">  <!-- This was disconnected -->
      <!-- ... -->
    </block>
  </next>
</block>
```

### Fix Missing Else Branch

Add the else statement to a controls_if:
```xml
<block type="controls_if" id="if_block">
  <mutation else="1"></mutation>
  <!-- existing IF0 and DO0 -->
  <statement name="ELSE">
    <block type="trade_again" id="trade_final"></block>
  </statement>
</block>
```
