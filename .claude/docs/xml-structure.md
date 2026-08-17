# Blockly XML Structure for Deriv DBot

## Root Element

Every Deriv bot XML file starts with:

```xml
<xml xmlns="https://developers.google.com/blockly/xml"
     xmlns:html="http://www.w3.org/1999/xhtml"
     is_dbot="true"
     collection="false">
```

**Required attributes:**
- `xmlns="https://developers.google.com/blockly/xml"` — Blockly namespace
- `is_dbot="true"` — marks this as a Deriv DBot file
- `collection="false"` — standard for single-bot files

---

## Variables Section

Declared immediately after root `<xml>`, before any blocks:

```xml
<variables>
  <variable id="cV~-Alq}UZ+O~dGM!1Fk">Initial_Stake</variable>
  <variable id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</variable>
</variables>
```

**Rules:**
- Each `<variable>` has an `id` (unique, Blockly-generated) and text content (display name)
- Variable IDs are typically random-looking strings like `cV~-Alq}UZ+O~dGM!1Fk`
- Some bots use readable IDs like `Max_Martingale_Level` — both work
- Every variable used in `<field name="VAR">` blocks must be declared here

---

## Block Structure

### Block Element

```xml
<block type="block_type_name" id="unique_id" x="0" y="0">
```

**Required attributes:**
- `type` — the Blockly block type (e.g., `trade_definition`, `controls_if`, `variables_set`)
- `id` — unique identifier within the file

**Optional attributes:**
- `x`, `y` — canvas position (cosmetic, ignored by bot engine)
- `deletable="false"` — prevents deletion in the editor (used on trade_definition)
- `movable="false"` — prevents dragging (used on definition chain blocks)

### Statement Connections

Statements are named slots that hold chains of blocks:

```xml
<block type="trade_definition" id="main">
  <statement name="TRADE_OPTIONS">
    <block type="trade_definition_market" id="market">
      <!-- ... -->
    </block>
  </statement>
  <statement name="SUBMARKET">
    <block type="variables_set" id="init_vars">
      <!-- ... -->
    </block>
  </statement>
</block>
```

**Key statement names:**
| Statement Name | Used By | Purpose |
|----------------|---------|---------|
| `TRADE_OPTIONS` | `trade_definition` | Market/type chain |
| `SUBMARKET` | `trade_definition` | Variable init + trade options |
| `INITIALIZATION` | `trade_definition` (alt) | Variable init (some bots) |
| `BEFOREPURCHASE_STACK` | `before_purchase` | Pre-trade logic |
| `AFTERPURCHASE_STACK` | `after_purchase` | Post-trade logic |
| `DO0`, `DO1`, etc. | `controls_if` | If/else branches |
| `ELSE` | `controls_if` | Else branch |

### Value Connections

Values are input slots for expressions (return a value):

```xml
<block type="logic_compare" id="compare">
  <field name="OP">GT</field>
  <value name="A">
    <block type="variables_get" id="get_profit">
      <field name="VAR" id="profit_id">Total_Profit</field>
    </block>
  </value>
  <value name="B">
    <block type="math_number" id="target_num">
      <field name="NUM">100</field>
    </block>
  </value>
</block>
```

### Next Connection

Chains blocks vertically (like a sequence):

```xml
<block type="variables_set" id="set1">
  <field name="VAR" id="var_id">Variable</field>
  <value name="VALUE">...</value>
  <next>
    <block type="variables_set" id="set2">
      <!-- next block in sequence -->
    </block>
  </next>
</block>
```

### Shadow Blocks

Shadow blocks are default values that users can override:

```xml
<value name="DURATION">
  <shadow type="math_number" id="duration_shadow">
    <field name="NUM">2</field>
  </shadow>
</value>
```

---

## Trade Definition Chain

The trade definition is a strict chain of 6 blocks, always in this order:

```
trade_definition
  └─ TRADE_OPTIONS statement
       └─ trade_definition_market
            └─ trade_definition_tradetype
                 └─ trade_definition_contracttype
                      └─ trade_definition_candleinterval
                           └─ trade_definition_restartbuysell
                                └─ trade_definition_restartonerror
```

Each block feeds into the next via `<next>`. The chain must be complete and unbroken.

### Market Values

| Field | Options |
|-------|---------|
| `MARKET_LIST` | `synthetic_index`, `forex`, `indices`, `commodities`, `stocks` |
| `SUBMARKET_LIST` | `random_index`, `volatility_index`, `boom_crash`, etc. |
| `SYMBOL_LIST` | `R_10`, `R_25`, `R_50`, `R_75`, `R_100`, `1HZ100V`, etc. |

### Trade Type Values

| Field | Options |
|-------|---------|
| `TRADETYPECAT_LIST` | `callput`, `accumulator`, `multiplier`, `turbos`, `ticks` |
| `TRADETYPE_LIST` | `callput`, `callputequal`, `accumulator`, `multiplier`, etc. |
| `TYPE_LIST` | `both`, `call`, `put`, `ACCU`, etc. |

### Candle Interval

| Value | Meaning |
|-------|---------|
| `60` | 1 minute |
| `120` | 2 minutes |
| `300` | 5 minutes |
| `900` | 15 minutes |
| `1800` | 30 minutes |
| `3600` | 1 hour |

---

## Top-Level Block Types

These blocks sit directly under `<xml>`, not nested inside other blocks:

| Block Type | Purpose | Statement Name |
|------------|---------|----------------|
| `trade_definition` | Market + type config | `TRADE_OPTIONS`, `SUBMARKET` |
| `before_purchase` | Pre-trade signal logic | `BEFOREPURCHASE_STACK` |
| `after_purchase` | Post-trade management | `AFTERPURCHASE_STACK` |
| `durationslider` | (Deprecated) Duration control | — |

---

## Common Patterns

### Variable Assignment Chain

```xml
<block type="variables_set" id="s1">
  <field name="VAR" id="var1_id">Initial_Stake</field>
  <value name="VALUE">
    <block type="math_number" id="n1">
      <field name="NUM">10</field>
    </block>
  </value>
  <next>
    <block type="variables_set" id="s2">
      <field name="VAR" id="var2_id">Current_Stake</field>
      <value name="VALUE">
        <block type="variables_get" id="g1">
          <field name="VAR" id="var1_id">Initial_Stake</field>
        </block>
      </value>
      <next>...</next>
    </block>
  </next>
</block>
```

### If-Else Logic

```xml
<block type="controls_if" id="if1">
  <mutation else="1"></mutation>
  <value name="IF0">
    <block type="logic_compare" id="cmp1">
      <field name="OP">GT</field>
      <value name="A">...</value>
      <value name="B">...</value>
    </block>
  </value>
  <statement name="DO0">
    <!-- true branch -->
  </statement>
  <statement name="ELSE">
    <!-- false branch -->
  </statement>
</block>
```

### Elif Chain

```xml
<mutation elseif="2" else="1"></mutation>
<!-- Creates IF0/DO0, IF1/DO1, IF2/DO2, ELSE -->
```
