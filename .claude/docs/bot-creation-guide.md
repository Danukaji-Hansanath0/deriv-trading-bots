# Bot Creation Guide

## Step-by-Step: Creating a New Deriv DBot

### Step 1: Choose a Strategy Template

Pick the closest existing bot from the project:

| Strategy | File | Best For |
|----------|------|----------|
| Trend following | `ma-cross-trend.xml` | Markets with clear direction |
| Mean reversion | `bb-band-reversion.xml` | Ranging markets |
| Momentum | `macd-hist-momentum.xml` | Strong trend entries |
| Reversal | `rsi-reversal.xml` | Overbought/oversold entries |
| Multi-indicator | `macd-rsi-bb-aggressive-v3.xml` | High-confidence signals |
| Pullback | `trend-pullback-combo.xml` | Trend + pullback entries |

### Step 2: Copy and Rename

```bash
cp "ma-cross-trend.xml" "my-new-strategy.xml"
```

### Step 3: Modify Trade Definition

The trade definition block controls market, type, and candle settings:

```xml
<block type="trade_definition" id="..." deletable="false" x="0" y="0">
  <statement name="TRADE_OPTIONS">
    <block type="trade_definition_market" id="...">
      <field name="MARKET_LIST">synthetic_index</field>
      <field name="SUBMARKET_LIST">random_index</field>
      <field name="SYMBOL_LIST">R_25</field>        <!-- Change symbol here -->
```

**Common symbols:**
- `R_10` — Lowest volatility, fastest ticks
- `R_25` — Low volatility (recommended for testing)
- `R_50` — Medium volatility
- `R_75` — High volatility
- `R_100` — Highest volatility
- `1HZ100V` — Volatility 100 (1s)

### Step 4: Update Variables

In the `<variables>` section, add or remove variables as needed:

```xml
<variables>
  <!-- Core money management (always keep these) -->
  <variable id="...">Initial_Stake</variable>
  <variable id="...">Current_Stake</variable>
  <variable id="...">Total_Profit</variable>
  <variable id="...">Target_Profit</variable>
  <variable id="...">Stop_Loss</variable>
  <variable id="...">Loss_Count</variable>
  <variable id="Max_Martingale_Level">Max_Martingale_Level</variable>
  <variable id="Martingale_Multiplier">Martingale_Multiplier</variable>
  <variable id="Daily_Loss_Limit">Daily_Loss_Limit</variable>

  <!-- Strategy-specific variables -->
  <variable id="...">closes</variable>       <!-- Price history -->
  <variable id="...">bbUpper</variable>      <!-- Bollinger upper band -->
  <variable id="...">bbLower</variable>      <!-- Bollinger lower band -->
  <variable id="...">maFast</variable>       <!-- Fast MA value -->
  <variable id="...">maSlow</variable>       <!-- Slow MA value -->
</variables>
```

### Step 5: Modify Indicator Logic

Update the `before_purchase` block with your signal logic. Common patterns:

**Bollinger Bands:**
```xml
<!-- Calculate BB: read closes array, compute upper/lower bands -->
<!-- Signal: price touches lower band → CALL, touches upper band → PUT -->
```

**Moving Average Crossover:**
```xml
<!-- Read candle close values into variables -->
<!-- Calculate fast MA and slow MA -->
<!-- Signal: fast > slow → CALL, fast < slow → PUT -->
```

**MACD:**
```xml
<!-- Read closes, calculate EMA12, EMA26, MACD line, signal line -->
<!-- Signal: MACD crosses above signal → CALL, below → PUT -->
```

**RSI:**
```xml
<!-- Read closes, calculate RSI (14-period) -->
<!-- Signal: RSI < 30 → CALL, RSI > 70 → PUT -->
```

### Step 6: Update After-Purchase Logic

The `after_purchase` block manages trade outcomes:

```xml
<block type="after_purchase" id="..." x="0" y="800">
  <statement name="AFTERPURCHASE_STACK">
    <!-- 1. Update Total_Profit -->
    <!-- 2. Check win/loss -->
    <!-- 3. Apply martingale or reset stake -->
    <!-- 4. Check stop conditions (target, stop loss, daily limit) -->
    <!-- 5. trade_again or stop -->
  </statement>
</block>
```

### Step 7: Validate

Run through the validation checklist: `.claude/docs/validation-checklist.md`

---

## Money Management Template

Every bot should include this initialization chain in the `SUBMARKET` statement:

```xml
<!-- Initial_Stake -->
<block type="variables_set" id="init_stake">
  <field name="VAR" id="...">Initial_Stake</field>
  <value name="VALUE">
    <block type="math_number" id="..."><field name="NUM">10</field></block>
  </value>
  <next>
    <!-- Current_Stake = Initial_Stake -->
    <block type="variables_set" id="init_current">
      <field name="VAR" id="...">Current_Stake</field>
      <value name="VALUE">
        <block type="variables_get" id="...">
          <field name="VAR" id="...">Initial_Stake</field>
        </block>
      </value>
      <next>
        <!-- Target_Profit -->
        <block type="variables_set" id="init_target">
          <field name="VAR" id="...">Target_Profit</field>
          <value name="VALUE">
            <block type="math_number" id="..."><field name="NUM">350</field></block>
          </value>
          <next>
            <!-- Stop_Loss -->
            <block type="variables_set" id="init_sl">
              <field name="VAR" id="...">Stop_Loss</field>
              <value name="VALUE">
                <block type="math_number" id="..."><field name="NUM">100</field></block>
              </value>
              <next>
                <!-- Max_Martingale_Level -->
                <block type="variables_set" id="set_max_martingale">
                  <field name="VAR" id="Max_Martingale_Level">Max_Martingale_Level</field>
                  <value name="VALUE">
                    <block type="math_number" id="max_mart_num"><field name="NUM">5</field></block>
                  </value>
                  <next>
                    <!-- Martingale_Multiplier -->
                    <block type="variables_set" id="set_mart_multiplier">
                      <field name="VAR" id="Martingale_Multiplier">Martingale_Multiplier</field>
                      <value name="VALUE">
                        <block type="math_number" id="mart_mult_num"><field name="NUM">2.1</field></block>
                      </value>
                      <next>
                        <!-- Daily_Loss_Limit -->
                        <block type="variables_set" id="set_daily_loss">
                          <field name="VAR" id="Daily_Loss_Limit">Daily_Loss_Limit</field>
                          <value name="VALUE">
                            <block type="math_number" id="daily_loss_num"><field name="NUM">200</field></block>
                          </value>
                        </block>
                      </next>
                    </block>
                  </next>
                </block>
              </next>
            </block>
          </next>
        </block>
      </next>
    </block>
  </next>
</block>
```

---

## Stop Conditions Template

Add this before `trade_again` in the `after_purchase` block:

```xml
<block type="controls_if" id="check_stop_conditions">
  <mutation elseif="2" else="1"></mutation>
  <!-- IF: Total_Profit >= Target_Profit -->
  <value name="IF0">
    <block type="logic_operation" id="check_target_or_stoploss">
      <field name="OP">OR</field>
      <value name="A">
        <block type="logic_compare" id="check_target">
          <field name="OP">GTE</field>
          <value name="A">
            <block type="variables_get" id="get_tp">
              <field name="VAR" id="...">Total_Profit</field>
            </block>
          </value>
          <value name="B">
            <block type="variables_get" id="get_tp_var">
              <field name="VAR" id="...">Target_Profit</field>
            </block>
          </value>
        </block>
      </value>
      <value name="B">
        <block type="logic_compare" id="check_sl">
          <field name="OP">LTE</field>
          <value name="A">
            <block type="variables_get" id="get_sl_check">
              <field name="VAR" id="...">Total_Profit</field>
            </block>
          </value>
          <value name="B">
            <block type="math_arithmetic" id="negate_sl">
              <field name="OP">MULTIPLY</field>
              <value name="A">
                <shadow type="math_number"><field name="NUM">-1</field></shadow>
              </value>
              <value name="B">
                <block type="variables_get" id="get_sl_var">
                  <field name="VAR" id="...">Stop_Loss</field>
                </block>
              </value>
            </block>
          </value>
        </block>
      </value>
    </block>
  </value>
  <statement name="DO0">
    <block type="notify" id="notify_stop">
      <field name="NOTIFICATION_TYPE">error</field>
      <field name="NOTIFICATION_SOUND">silent</field>
      <value name="MESSAGE">
        <block type="text" id="stop_msg">
          <field name="TEXT">Stop condition reached</field>
        </block>
      </value>
    </block>
  </statement>
  <!-- ELIF: Daily_Loss_Limit breached -->
  <value name="IF1">
    <block type="logic_compare" id="check_daily">
      <field name="OP">LTE</field>
      <value name="A">
        <block type="variables_get" id="get_profit_daily">
          <field name="VAR" id="...">Total_Profit</field>
        </block>
      </value>
      <value name="B">
        <block type="math_arithmetic" id="negate_daily">
          <field name="OP">MULTIPLY</field>
          <value name="A">
            <shadow type="math_number"><field name="NUM">-1</field></shadow>
          </value>
          <value name="B">
            <block type="variables_get" id="get_daily_var">
              <field name="VAR" id="Daily_Loss_Limit">Daily_Loss_Limit</field>
            </block>
          </value>
        </block>
      </value>
    </block>
  </value>
  <statement name="DO1">
    <block type="notify" id="notify_daily">
      <field name="NOTIFICATION_TYPE">error</field>
      <field name="NOTIFICATION_SOUND">silent</field>
      <value name="MESSAGE">
        <block type="text" id="daily_msg">
          <field name="TEXT">Daily loss limit reached</field>
        </block>
      </value>
    </block>
  </statement>
  <!-- ELSE: trade again -->
  <statement name="ELSE">
    <block type="trade_again" id="trade_again_final"></block>
  </statement>
</block>
```
