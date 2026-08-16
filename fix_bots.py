#!/usr/bin/env python3
import re
import glob

def add_money_management_variables(xml_content):
    has_max_mart = 'Max_Martingale_Level' in xml_content
    has_mart_mult = 'Martingale_Multiplier' in xml_content
    has_daily_loss = 'Daily_Loss_Limit' in xml_content
    
    if has_max_mart and has_mart_mult and has_daily_loss:
        return xml_content
    
    var_match = re.search(r'<variables>(.*?)</variables>', xml_content, re.DOTALL)
    if not var_match:
        print("ERROR: Could not find variables section")
        return xml_content
    
    vars_section = var_match.group(1)
    
    if not has_max_mart:
        vars_section += '\n    <variable id="Max_Martingale_Level">Max_Martingale_Level</variable>'
    if not has_mart_mult:
        vars_section += '\n    <variable id="Martingale_Multiplier">Martingale_Multiplier</variable>'
    if not has_daily_loss:
        vars_section += '\n    <variable id="Daily_Loss_Limit">Daily_Loss_Limit</variable>'
    
    new_xml = xml_content[:var_match.start()] + f'<variables>{vars_section}</variables>' + xml_content[var_match.end():]
    return new_xml

def add_initialization_blocks(xml_content):
    if 'set_max_martingale' in xml_content or 'Max_Martingale_Level</field>' in xml_content:
        return xml_content
    
    stop_loss_pattern = r'(<block type="variables_set"[^>]*>\s*<field name="VAR"[^>]*>Stop_Loss</field>.*?</block>)'
    match = re.search(stop_loss_pattern, xml_content, re.DOTALL)
    
    if not match:
        print("ERROR: Could not find Stop_Loss initialization")
        return xml_content
    
    init_blocks = '''
                            <next>
                              <block type="variables_set" id="set_max_martingale">
                                <field name="VAR" id="Max_Martingale_Level">Max_Martingale_Level</field>
                                <value name="VALUE">
                                  <block type="math_number" id="max_mart_num">
                                    <field name="NUM">5</field>
                                  </block>
                                </value>
                                <next>
                                  <block type="variables_set" id="set_mart_multiplier">
                                    <field name="VAR" id="Martingale_Multiplier">Martingale_Multiplier</field>
                                    <value name="VALUE">
                                      <block type="math_number" id="mart_mult_num">
                                        <field name="NUM">2.1</field>
                                      </block>
                                    </value>
                                    <next>
                                      <block type="variables_set" id="set_daily_loss">
                                        <field name="VAR" id="Daily_Loss_Limit">Daily_Loss_Limit</field>
                                        <value name="VALUE">
                                          <block type="math_number" id="daily_loss_num">
                                            <field name="NUM">200</field>
                                          </block>
                                        </value>
                                        <next>
'''
    insert_pos = match.end()
    new_xml = xml_content[:insert_pos] + init_blocks + xml_content[insert_pos:]
    return new_xml

def add_stop_conditions(xml_content):
    if 'check_stop_conditions' in xml_content or 'notify_stop_condition' in xml_content:
        return xml_content
    
    trade_again_pattern = r'(<block type="trade_again"[^>]*></block>)'
    match = re.search(trade_again_pattern, xml_content)
    
    if not match:
        return xml_content
    
    stop_check = '''<block type="controls_if" id="check_stop_conditions">
            <mutation xmlns="http://www.w3.org/1999/xhtml" elseif="2" else="1"></mutation>
            <value name="IF0">
              <block type="logic_operation" id="check_target_or_stoploss">
                <field name="OP">OR</field>
                <value name="A">
                  <block type="logic_compare" id="check_target_profit_reached">
                    <field name="OP">GTE</field>
                    <value name="A">
                      <block type="variables_get" id="get_total_profit_for_target">
                        <field name="VAR" id="1]MVFCxN`xPknil1?7u.">Total_Profit</field>
                      </block>
                    </value>
                    <value name="B">
                      <block type="variables_get" id="get_target_profit_var">
                        <field name="VAR" id="rlYcT[__d89=3y]{CW+?">Target_Profit</field>
                      </block>
                    </value>
                  </block>
                </value>
                <value name="B">
                  <block type="logic_compare" id="check_stoploss_reached">
                    <field name="OP">LTE</field>
                    <value name="A">
                      <block type="variables_get" id="get_total_profit_for_stoploss">
                        <field name="VAR" id="1]MVFCxN`xPknil1?7u.">Total_Profit</field>
                      </block>
                    </value>
                    <value name="B">
                      <block type="math_arithmetic" id="negate_stoploss_value">
                        <field name="OP">MULTIPLY</field>
                        <value name="A">
                          <shadow type="math_number" id="neg_mult_shadow_a">
                            <field name="NUM">-1</field>
                          </shadow>
                        </value>
                        <value name="B">
                          <shadow type="math_number" id="neg_mult_shadow_b">
                            <field name="NUM">-1</field>
                          </shadow>
                          <block type="variables_get" id="get_stoploss_var">
                            <field name="VAR" id="73u7zZ}p:I@`SH|oysA+">Stop_Loss</field>
                          </block>
                        </value>
                      </block>
                    </value>
                  </block>
                </value>
              </block>
            </value>
            <statement name="DO0">
              <block type="notify" id="notify_stop_condition">
                <field name="NOTIFICATION_TYPE">error</field>
                <field name="NOTIFICATION_SOUND">silent</field>
                <value name="MESSAGE">
                  <block type="text" id="stop_msg_text">
                    <field name="TEXT">Stop condition reached - stopping bot</field>
                  </block>
                </value>
              </block>
            </statement>
            <value name="IF1">
              <block type="logic_compare" id="check_daily_loss_limit">
                <field name="OP">LTE</field>
                <value name="A">
                  <block type="variables_get" id="get_total_profit_daily_check">
                    <field name="VAR" id="1]MVFCxN`xPknil1?7u.">Total_Profit</field>
                  </block>
                </value>
                <value name="B">
                  <block type="math_arithmetic" id="negate_daily_loss">
                    <field name="OP">MULTIPLY</field>
                    <value name="A">
                      <shadow type="math_number" id="daily_neg_shadow_a">
                        <field name="NUM">-1</field>
                      </shadow>
                    </value>
                    <value name="B">
                      <shadow type="math_number" id="daily_neg_shadow_b">
                        <field name="NUM">-1</field>
                      </shadow>
                      <block type="variables_get" id="get_daily_loss_var">
                        <field name="VAR" id="Daily_Loss_Limit">Daily_Loss_Limit</field>
                      </block>
                    </value>
                  </block>
                </value>
              </block>
            </value>
            <statement name="DO1">
              <block type="notify" id="notify_daily_loss">
                <field name="NOTIFICATION_TYPE">error</field>
                <field name="NOTIFICATION_SOUND">silent</field>
                <value name="MESSAGE">
                  <block type="text" id="daily_loss_msg">
                    <field name="TEXT">Daily loss limit reached - stopping bot</field>
                  </block>
                </value>
              </block>
            </statement>
            <statement name="ELSE">
              <block type="trade_again" id="trade_again_final"></block>
            </statement>
          </block>'''
    
    new_xml = xml_content[:match.start()] + stop_check + xml_content[match.end():]
    return new_xml

def fix_martingale_in_after_purchase(xml_content):
    # Check if file already has proper martingale logic
    if 'check_max_mart_level' in xml_content:
        return xml_content
    
    # Look for the pattern where Loss_Count is used with a simple multiplier
    # Find controls_if blocks that check Loss_Count
    old_pattern = r'(<block type="controls_if" id="[^"]*">\s*<mutation[^>]*elseif="1"[^>]*>.*?<value name="IF0">.*?GT.*?Loss_Count.*?</value>.*?<statement name="DO0">.*?MULTIPLY.*?</statement>.*?<value name="IF1">.*?LTE.*?Loss_Count.*?</value>.*?<statement name="DO1">.*?Initial_Stake.*?</statement>.*?</block>)'
    
    # Simpler approach: just ensure we have the structure right after Loss_Count increment
    # This is complex XML so we'll do targeted replacement
    
    return xml_content

def process_file(filepath):
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    content = add_money_management_variables(content)
    content = add_initialization_blocks(content)
    content = add_stop_conditions(content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Updated {filepath}")
        return True
    else:
        print(f"  No changes needed for {filepath}")
        return False

if __name__ == '__main__':
    xml_files = glob.glob('/workspace/*.xml')
    print(f"Found {len(xml_files)} XML files to process\n")
    
    updated = 0
    for filepath in xml_files:
        if 'rsi-reversal.xml' not in filepath:
            if process_file(filepath):
                updated += 1
    
    print(f"\nCompleted! Updated {updated} files.")
