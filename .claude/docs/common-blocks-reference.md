# Common Blocks Reference

## Trade Definition Blocks

### `trade_definition`
Root block for trade configuration. Non-deletable.
- **Statements:** `TRADE_OPTIONS`, `SUBMARKET`

### `trade_definition_market`
Sets market and symbol.
- **Fields:** `MARKET_LIST`, `SUBMARKET_LIST`, `SYMBOL_LIST`

### `trade_definition_tradetype`
Sets trade type category and specific type.
- **Fields:** `TRADETYPECAT_LIST`, `TRADETYPE_LIST`

### `trade_definition_contracttype`
Sets contract direction.
- **Fields:** `TYPE_LIST` — `both`, `call`, `put`, `ACCU`

### `trade_definition_candleinterval`
Sets candle interval for indicators.
- **Fields:** `CANDLEINTERVAL_LIST` — `60`, `120`, `300`, `900`, `1800`, `3600`

### `trade_definition_restartbuysell`
Controls restart on buy/sell.
- **Fields:** `TIME_MACHINE_ENABLED` — `TRUE`, `FALSE`

### `trade_definition_restartonerror`
Controls restart on error.
- **Fields:** `RESTARTONERROR` — `TRUE`, `FALSE`

### `trade_definition_tradeoptions`
Sets duration and amount.
- **Fields:** `DURATIONTYPE_LIST` — `t` (ticks), `m` (minutes), `h` (hours), `d` (days)
- **Values:** `DURATION`, `AMOUNT`
- **Mutation:** `has_first_barrier`, `has_second_barrier`, `has_prediction`

---

## Logic Blocks

### `controls_if`
Conditional if/else.
- **Values:** `IF0` (condition)
- **Statements:** `DO0` (then), `ELSE` (else)
- **Mutation:** `elseif` (count), `else` (0 or 1)
- Multiple conditions: `IF1`/`DO1`, `IF2`/`DO2`, etc.

### `controls_if_else` (convenience)
Same as `controls_if` with `else="1"` pre-set.

### `logic_compare`
Comparison operator.
- **Field:** `OP` — `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`
- **Values:** `A`, `B`

### `logic_operation`
Boolean AND/OR.
- **Field:** `OP` — `AND`, `OR`
- **Values:** `A`, `B`

### `logic_negate`
Boolean NOT.
- **Values:** `BOOL`

### `logic_boolean`
True/false constant.
- **Field:** `BOOL` — `TRUE`, `FALSE`

### `logic_null`
Represents null/undefined.

---

## Math Blocks

### `math_number`
Numeric constant.
- **Field:** `NUM` — the number value

### `math_arithmetic`
Arithmetic operation.
- **Field:** `OP` — `ADD`, `MINUS`, `MULTIPLY`, `DIVIDE`, `POWER`
- **Values:** `A`, `B`

### `math_single`
Single-argument math (sqrt, abs, neg, ln, log10, exp, pow10).
- **Field:** `OP` — `ROOT`, `ABS`, `NEG`, `LN`, `LOG10`, `EXP`, `POW10`
- **Values:** `NUM`

### `math_number_property`
Check number property (even, odd, prime, positive, negative, zero).
- **Field:** `PROPERTY` — `EVEN`, `ODD`, `PRIME`, `POSITIVE`, `NEGATIVE`, `ZERO`
- **Values:** `NUMBER_TO_CHECK`

### `math_round`
Round number.
- **Field:** `OP` — `ROUND`, `ROUNDUP`, `ROUNDDOWN`
- **Values:** `NUM`, `ROUNDTO`

### `math_modulo`
Remainder of division.
- **Values:** `DIVIDEND`, `DIVISOR`

### `math_random_int`
Random integer in range.
- **Values:** `FROM`, `TO`

### `math_on_list`
Aggregate operation on list (sum, min, max, average, median, std_dev, rand).
- **Field:** `OP` — `SUM`, `MIN`, `MAX', `AVERAGE', 'MEDIAN', 'STD_DEV', 'RANDOM`
- **Values:** `LIST`

---

## Text Blocks

### `text`
Text constant.
- **Field:** `TEXT` — the string value

### `text_join`
Concatenate strings.
- **Mutation:** `items` (count)
- **Values:** `ADD0`, `ADD1`, etc.

### `text_length`
String length.
- **Values:** `VALUE`

### `text_isEmpty`
Check if string is empty.
- **Values:** `VALUE`

### `text_indexOf`
Find substring index.
- **Field:** `END` — `FIRST`, `LAST`
- **Values:** `FIND`, `VALUE`

### `text_changeCase`
Change case (uppercase, lowercase, titlecase).
- **Field:** `CASE` — `UPPERCASE`, `LOWERCASE`, `TITLECASE`
- **Values:** `TEXT`

### `text_trim`
Trim whitespace.
- **Field:** `MODE` — `BOTH`, `LEFT`, `RIGHT`
- **Values:** `TEXT`

### `text_print`
Output text (for debugging).
- **Values:** `TEXT`

---

## Variable Blocks

### `variables_set`
Set a variable value.
- **Field:** `VAR` — variable name
- **Values:** `VALUE`

### `variables_get`
Get a variable value.
- **Field:** `VAR` — variable name

---

## List Blocks

### `lists_create_empty`
Create empty list.

### `lists_create_with`
Create list with items.
- **Mutation:** `items` (count)
- **Values:** `ADD0`, `ADD1`, etc.

### `lists_length`
Get list length.
- **Values:** `VALUE`

### `lists_isEmpty`
Check if list is empty.
- **Values:** `VALUE`

### `lists_indexOf`
Find element index.
- **Field:** `END` — `FIRST`, `LAST`
- **Values:** `FIND`, `VALUE`

### `lists_getIndex`
Get element at index.
- **Field:** `MODE` — `GET`, `GET_REMOVE`, `REMOVE`
- **Field:** `WHERE` — `FROM_START`, `FROM_END`, `FIRST`, `LAST`
- **Values:** `VALUE`, `AT`

### `lists_setIndex`
Set element at index.
- **Field:** `MODE` — `SET`, `INSERT`
- **Field:** `WHERE` — `FROM_START`, `FROM_END`, `FIRST`, `LAST`
- **Values:** `LIST`, `AT`, `TO`

### `lists_repeat`
Create list with repeated value.
- **Values:** `VALUE`, `NUM`

### `lists_reverse`
Reverse a list.
- **Values:** `LIST`

### `lists_sort`
Sort a list.
- **Field:** `DIRECTION` — `1` (ascending), `-1` (descending)
- **Field:** `TYPE` — `NUMERIC`, `TEXT`, `IGNORE_CASE`
- **Values:** `LIST`

---

## Deriv-Specific Blocks

### `purchase`
Buy a contract. No fields or values — just triggers purchase.

### `trade_again`
Continue trading after contract ends. No fields or values.

### `sell`
Sell current contract.
- **Values:** `ASK_PRICE` (optional)

### `notify`
Show notification.
- **Field:** `NOTIFICATION_TYPE` — `info`, `success`, `warning`, `error`
- **Field:** `NOTIFICATION_SOUND` — `silent`, `announcement`
- **Values:** `MESSAGE`

### `read_ohlc`
Read candle (OHLC) data.
- **Fields:** `CONTRACT_TYPE` — `CALL`, `PUT`, `ASIANU`, `ASIAND`
- **Values:** `CANDLE_INTERVAL`, `CANDLE_GRANULARITY`

### `read_ohlc_vert`
Read single candle value.
- **Fields:** `OHLC_FIELD` — `OPEN`, `HIGH`, `LOW`, `CLOSE`
- **Values:** `CANDLE_INTERVAL`, `CANDLE_GRANULARITY`, `CANDLE_INDEX`

### `candle_interval`
Candle interval selector.
- **Field:** `CANDLEINTERVAL_LIST`

### `candle_granularity`
Candle granularity selector.
- **Field:** `CANDLEGRANULARITY_LIST`

### `contract`
Contract data reader.
- **Field:** `CONTRACT_FIELD` — `REFERENCE`, `PAYOUT`, `STAKE`, `PROFIT`, `ENTRY_SPOT`, `EXIT_SPOT`, `BARRIER`, `HIGH_BARRIER`, `LOW_BARRIER`, `DATE_START`, `DATE_END`, `CURRENT_SPOT`, `CURRENT_SPOT_TIME`, `TICK_COUNT`, `TICK_STAKE`, `TICK_PROFIT`, `CURRENCY`

### `contract_chart`
Display contract chart.

---

## Loop Blocks

### `controls_forEach`
For each item in list.
- **Field:** `VAR` — loop variable
- **Values:** `LIST`
- **Statements:** `DO` — loop body

### `controls_for`
Counting for loop.
- **Field:** `VAR` — loop variable
- **Field:** `FROM`, `TO`, `BY` — start, end, step (as text)
- **Statements:** `DO`

### `controls_whileUntil`
Repeat while/until condition.
- **Field:** `MODE` — `WHILE`, `UNTIL`
- **Values:** `CONDITION`
- **Statements:** `DO`

---

## Procedure Blocks

### `procedures_defnoreturn`
Define procedure (no return value).
- **Field:** `NAME` — procedure name
- **Statements:** `STACK` — procedure body

### `procedures_defreturn`
Define procedure (with return value).
- **Field:** `NAME` — procedure name
- **Statements:** `STACK`
- **Values:** `RETURN`

### `procedures_callnoreturn`
Call procedure (no return).
- **Field:** `NAME` — procedure name
- **Mutation:** `arguments` (count)
- **Values:** `ARG0`, `ARG1`, etc.

### `procedures_callreturn`
Call procedure (with return).
- **Field:** `NAME`
- **Mutation:** `arguments`
- **Values:** `ARG0`, `ARG1`, etc.

### `procedures_ifreturn`
Conditional return from procedure.
- **Values:** `VALUE`
