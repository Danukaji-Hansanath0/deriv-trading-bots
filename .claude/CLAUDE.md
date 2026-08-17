# Deriv Trading Bots — AI Assistant Instructions

## Project Overview

This project contains **Deriv DBot Blockly XML trading bots** for the Deriv platform. Bots are authored as Blockly XML files (`.xml`) that define automated trading strategies for synthetic indices (R_25, R_50, R_75, R_100, etc.) and other Deriv markets.

**Primary language:** Blockly XML (Google Blockly dialect with Deriv extensions)
**Support tools:** Python scripts for bulk XML modification

---

## Core Rules

### When Editing XML

1. **Never break the XML hierarchy.** Every `<block>` must have a valid parent and all required child statements.
2. **Preserve block IDs.** Each block has a unique `id` attribute. Never duplicate IDs within a file.
3. **Keep variable references consistent.** If a `<variable id="X">Name</variable>` is declared, all `<field name="VAR" id="X">Name</field>` must match exactly.
4. **Validate before claiming success.** Run the validation checklist (`.claude/docs/validation-checklist.md`) after any edit.
5. **Never add comments to XML** unless the user explicitly requests it.

### When Creating Bots

1. **Always start from a known working template** (see `.claude/docs/bot-creation-guide.md`).
2. **Include money management** — Every bot must have `Initial_Stake`, `Current_Stake`, `Total_Profit`, `Target_Profit`, `Stop_Loss`, and martingale variables.
3. **Include stop conditions** — Target profit, stop loss, and daily loss limit checks before `trade_again`.
4. **Test with R_25 first** — Use the smallest volatility market for initial testing.

### When Debugging

1. **Read the full error first.** Deriv DBot reports specific line/column for XML parse errors.
2. **Check for orphaned blocks** — blocks outside any `<statement>` or `<value>` container.
3. **Check for mismatched variable IDs** — the most common source of silent failures.
4. **See `.claude/docs/debugging-guide.md` for systematic debugging workflow.**

---

## Quick Reference: Bot XML Anatomy

```xml
<xml xmlns="https://developers.google.com/blockly/xml"
     xmlns:html="http://www.w3.org/1999/xhtml"
     is_dbot="true" collection="false">
  <variables>
    <variable id="VAR_ID">Variable_Name</variable>
    <!-- ... -->
  </variables>

  <!-- 1. TRADE DEFINITION (required, non-deletable) -->
  <block type="trade_definition" id="..." x="0" y="0" deletable="false">
    <statement name="TRADE_OPTIONS">
      <!-- market → tradetype → contracttype → candleinterval → restartbuysell → restartonerror -->
    </statement>
    <statement name="SUBMARKET">
      <!-- variable initializations + trade options -->
    </statement>
  </block>

  <!-- 2. BEFORE PURCHASE LOGIC -->
  <block type="before_purchase" id="..." x="0" y="400">
    <statement name="BEFOREPURCHASE_STACK">
      <!-- signal logic, variable updates, purchase call -->
    </statement>
  </block>

  <!-- 3. AFTER PURCHASE LOGIC -->
  <block type="after_purchase" id="..." x="0" y="800">
    <statement name="AFTERPURCHASE_STACK">
      <!-- profit tracking, martingale, stop conditions, trade_again -->
    </statement>
  </block>
</xml>
```

---

## Variable Naming Conventions

| Variable | Purpose | Typical Default |
|----------|---------|-----------------|
| `Initial_Stake` | Starting trade amount | 0.35 — 10 |
| `Current_Stake` | Active trade amount (adjusts with martingale) | = Initial_Stake |
| `Total_Profit` | Running profit/loss total | 0 |
| `Target_Profit` | Profit target to stop bot | 100 — 500 |
| `Stop_Loss` | Max loss before stopping | 50 — 200 |
| `Loss_Count` | Consecutive losses counter | 0 |
| `Max_Martingale_Level` | Max martingale steps | 3 — 7 |
| `Martingale_Multiplier` | Stake multiplier on loss | 1.5 — 3.0 |
| `Daily_Loss_Limit` | Max daily loss | 100 — 500 |

---

## File Naming Convention

- `<strategy-name>.xml` — primary version
- `<strategy-name>_1.xml` — variant/iteration
- `<strategy-name>-live-tested.xml` — confirmed working on live

---

## Reference Docs

| Document | When to Use |
|----------|-------------|
| `.claude/docs/xml-structure.md` | Understanding Blockly XML format |
| `.claude/docs/bot-creation-guide.md` | Building a new bot from scratch |
| `.claude/docs/debugging-guide.md` | Fixing broken or malfunctioning bots |
| `.claude/docs/validation-checklist.md` | Pre-deployment verification |
| `.claude/docs/common-blocks-reference.md` | Looking up block types and fields |
| `.claude/docs/resources.md` | External Deriv docs, tools, APIs |
