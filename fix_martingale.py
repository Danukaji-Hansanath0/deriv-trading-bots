#!/usr/bin/env python3
import re
import glob

def fix_martingale_logic(xml_content):
    """Replace simple martingale with proper controlled martingale"""
    
    # Skip if already has proper martingale logic
    if 'check_max_mart_level' in xml_content:
        return xml_content
    
    # Find the after_purchase section and locate the Loss_Count increment block
    # Then replace the following controls_if with proper martingale logic
    
    # Pattern to find the loss handling section
    loss_section_pattern = r'(<block type="variables_set" id="[^"]*">\s*<field name="VAR"[^>]*>GT\+e#pM4g%Q\[dse0aK`n</field>\s*<value name="VALUE">\s*<block type="math_arithmetic" id="[^"]*">\s*<field name="OP">ADD</field>.*?Loss_Count.*?</block>\s*</next>)'
    
    match = re.search(loss_section_pattern, xml_content, re.DOTALL)
    
    if not match:
        # Try alternative pattern for files with different structure
        alt_pattern = r'(Loss_Count</field>\s*</value>\s*</block>\s*<next>\s*<block type="controls_if" id="[^"]*">)'
        alt_match = re.search(alt_pattern, xml_content, re.DOTALL)
        
        if alt_match:
            # Found a controls_if after Loss_Count, need to replace it
            start_pos = alt_match.start(1)
            
            # Find the end of this controls_if block
            remaining = xml_content[start_pos:]
            
            # Count blocks to find the end
            block_count = 0
            end_pos = 0
            in_block = False
            
            for i, char in enumerate(remaining):
                if remaining[i:i+7] == '<block ':
                    block_count += 1
                    in_block = True
                elif remaining[i:i+9] == '</block>':
                    block_count -= 1
                    if block_count == 0 and in_block:
                        end_pos = i + 9
                        break
            
            if end_pos > 0:
                old_block = xml_content[start_pos:start_pos + end_pos]
                
                new_martingale = '''<block type="controls_if" id="martingale_logic_block">
                        <mutation xmlns="http://www.w3.org/1999/xhtml" else="1"></mutation>
                        <value name="IF0">
                          <block type="logic_compare" id="check_max_mart_level">
                            <field name="OP">GTE</field>
                            <value name="A">
                              <block type="variables_get" id="get_loss_count_for_mart">
                                <field name="VAR" id="GT+e#pM4g%Q[dse0aK`n">Loss_Count</field>
                              </block>
                            </value>
                            <value name="B">
                              <block type="variables_get" id="get_max_mart_level_var">
                                <field name="VAR" id="Max_Martingale_Level">Max_Martingale_Level</field>
                              </block>
                            </value>
                          </block>
                        </value>
                        <statement name="DO0">
                          <block type="variables_set" id="reset_after_max_mart">
                            <field name="VAR" id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</field>
                            <value name="VALUE">
                              <block type="variables_get" id="reset_stake_to_initial">
                                <field name="VAR" id="cV~-Alq}UZ+O~dGM!1Fk">Initial_Stake</field>
                              </block>
                            </value>
                            <next>
                              <block type="variables_set" id="reset_loss_count_after_max">
                                <field name="VAR" id="GT+e#pM4g%Q[dse0aK`n">Loss_Count</field>
                                <value name="VALUE">
                                  <block type="math_number" id="zero_loss_count_reset">
                                    <field name="NUM">0</field>
                                  </block>
                                </value>
                              </block>
                            </next>
                          </block>
                        </statement>
                        <statement name="ELSE">
                          <block type="variables_set" id="apply_martingale_mult">
                            <field name="VAR" id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</field>
                            <value name="VALUE">
                              <block type="math_arithmetic" id="multiply_stake_by_multiplier">
                                <field name="OP">MULTIPLY</field>
                                <value name="A">
                                  <block type="variables_get" id="get_current_stake_for_mult">
                                    <field name="VAR" id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</field>
                                  </block>
                                </value>
                                <value name="B">
                                  <block type="variables_get" id="get_martingale_multiplier_var">
                                    <field name="VAR" id="Martingale_Multiplier">Martingale_Multiplier</field>
                                  </block>
                                </value>
                              </block>
                            </value>
                          </block>
                        </statement>
                      </block>'''
                
                new_xml = xml_content[:start_pos] + new_martingale + xml_content[start_pos + end_pos:]
                return new_xml
        
        return xml_content
    
    # Found the primary pattern
    after_loss = match.end(1)
    
    # Now find and replace the next controls_if block
    remaining = xml_content[after_loss:]
    
    # Find the controls_if that handles martingale
    ctrl_if_match = re.search(r'<block type="controls_if" id="[^"]*">', remaining)
    
    if not ctrl_if_match:
        return xml_content
    
    ctrl_start = after_loss + ctrl_if_match.start()
    
    # Find the end of this controls_if block
    remaining_from_ctrl = xml_content[ctrl_start:]
    
    block_count = 0
    end_pos = 0
    for i, char in enumerate(remaining_from_ctrl):
        if remaining_from_ctrl[i:i+7] == '<block ':
            block_count += 1
        elif remaining_from_ctrl[i:i+9] == '</block>':
            block_count -= 1
            if block_count == 0:
                end_pos = i + 9
                break
    
    if end_pos == 0:
        return xml_content
    
    new_martingale = '''<block type="controls_if" id="martingale_logic_block">
                        <mutation xmlns="http://www.w3.org/1999/xhtml" else="1"></mutation>
                        <value name="IF0">
                          <block type="logic_compare" id="check_max_mart_level">
                            <field name="OP">GTE</field>
                            <value name="A">
                              <block type="variables_get" id="get_loss_count_for_mart">
                                <field name="VAR" id="GT+e#pM4g%Q[dse0aK`n">Loss_Count</field>
                              </block>
                            </value>
                            <value name="B">
                              <block type="variables_get" id="get_max_mart_level_var">
                                <field name="VAR" id="Max_Martingale_Level">Max_Martingale_Level</field>
                              </block>
                            </value>
                          </block>
                        </value>
                        <statement name="DO0">
                          <block type="variables_set" id="reset_after_max_mart">
                            <field name="VAR" id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</field>
                            <value name="VALUE">
                              <block type="variables_get" id="reset_stake_to_initial">
                                <field name="VAR" id="cV~-Alq}UZ+O~dGM!1Fk">Initial_Stake</field>
                              </block>
                            </value>
                            <next>
                              <block type="variables_set" id="reset_loss_count_after_max">
                                <field name="VAR" id="GT+e#pM4g%Q[dse0aK`n">Loss_Count</field>
                                <value name="VALUE">
                                  <block type="math_number" id="zero_loss_count_reset">
                                    <field name="NUM">0</field>
                                  </block>
                                </value>
                              </block>
                            </next>
                          </block>
                        </statement>
                        <statement name="ELSE">
                          <block type="variables_set" id="apply_martingale_mult">
                            <field name="VAR" id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</field>
                            <value name="VALUE">
                              <block type="math_arithmetic" id="multiply_stake_by_multiplier">
                                <field name="OP">MULTIPLY</field>
                                <value name="A">
                                  <block type="variables_get" id="get_current_stake_for_mult">
                                    <field name="VAR" id="b{GT|f,n6:nv]_U$%`U2">Current_Stake</field>
                                  </block>
                                </value>
                                <value name="B">
                                  <block type="variables_get" id="get_martingale_multiplier_var">
                                    <field name="VAR" id="Martingale_Multiplier">Martingale_Multiplier</field>
                                  </block>
                                </value>
                              </block>
                            </value>
                          </block>
                        </statement>
                      </block>'''
    
    new_xml = xml_content[:ctrl_start] + new_martingale + xml_content[ctrl_start + end_pos:]
    return new_xml

def process_file(filepath):
    print(f"Fixing martingale in {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    content = fix_martingale_logic(content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Fixed martingale in {filepath}")
        return True
    else:
        print(f"  No changes for {filepath}")
        return False

if __name__ == '__main__':
    xml_files = glob.glob('/workspace/*.xml')
    print(f"Processing {len(xml_files)} files for martingale fix\n")
    
    fixed = 0
    for filepath in xml_files:
        if process_file(filepath):
            fixed += 1
    
    print(f"\nFixed {fixed} files.")
