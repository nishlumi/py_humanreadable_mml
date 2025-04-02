"""
py_humanreadable_mml
"""
def custom_mml_to_mml(custom_mml):
    """Full custom MML to Original MML
    
    * `drmfsac -> cdefgab`
    * `_ -> <`
    * `^ -> >`
    * `d- -> c8` if `L16`
    * `d-- -> c4` if `L16`
    * `d/ -> c32` if `L16`
    * `p -> r`
    * `b -> -`
    * Other symbols are same as the original
    """
    mml = ""
    index = 0
    octave_shift = 0
    base_duration = 4 # デフォルトの基本音長 (4分音符)

    note_map = {'d': 'c', 'r': 'd', 'm': 'e', 'f': 'f', 's': 'g', 'a': 'a', 'si': 'b', 'c' : 'b', 'p': 'r'}

    def get_octave(octave_shift):
        return "<" * -octave_shift + ">" * octave_shift

    def get_duration_mml(duration_value):
        if duration_value == 4:
            return ""
        elif duration_value > 0:
            #return str(int(4 / duration_value))
            return str(duration_value)
        return ""

    while index < len(custom_mml):
        char = custom_mml.lower()[index]
        
        #print(char)

        # MMLコマンドを処理
        if char in ['t', '@', 'o', 'v', 'l']:
            command = ""
            command += custom_mml.lower()[index]
            index += 1
            while index < len(custom_mml) and custom_mml.lower()[index].isalnum():
                command += custom_mml.lower()[index]
                index += 1
            mml += command
            duration_str = ""
            #while index < len(custom_mml) and (custom_mml.lower()[index].isdigit() or custom_mml.lower()[index] == '/'):
            #    duration_str += custom_mml.lower()[index]
            #    index += 1
            #mml += duration_str
            if command.lower() == 'l' and duration_str:
                try:
                    if '/' in duration_str:
                        num, den = map(int, duration_str.split('/'))
                        base_duration = den / num
                    else:
                        base_duration = int(duration_str)
                except ValueError:
                    pass  # パースに失敗したらデフォルト値を維持
            continue

        # 「si」の処理
        if index + 1 < len(custom_mml) and custom_mml.lower()[index:index+2] == 'si':
            mml_note = note_map.get('si')
            octave_str = get_octave(octave_shift)
            mml += octave_str + mml_note
            index += 2
            current_duration = base_duration

            while index < len(custom_mml) and custom_mml.lower()[index] in ['#', '+', 'b']:
                if custom_mml.lower()[index] == 'b':
                    mml = mml[:-len(mml_duration) if mml_duration else len(octave_str) + 1] + mml_note + '-' + mml_duration
                else:
                    mml += '#'
                index += 1
            octave_shift = 0
            
            hyphen_count = 0
            while index < len(custom_mml) and custom_mml.lower()[index] == '-':
                hyphen_count += 1
                current_duration //= 2
                if current_duration == 0:
                    current_duration = max(current_duration, 1)
                index += 1
            
            while index < len(custom_mml) and custom_mml.lower()[index] == "/":
                current_duration *= 2
                index += 1

            mml_duration = get_duration_mml(current_duration)
            if mml_duration == "0":
                mml_duration = "32" # 極端に短い場合はPyxelで扱える最小に近い値に
            mml += mml_duration

            continue

        if char in note_map:
            mml_note = note_map.get(char)
            octave_str = get_octave(octave_shift)
            mml += octave_str + mml_note
            index += 1
            current_duration = base_duration

            while index < len(custom_mml) and custom_mml.lower()[index] in ['#', '+', 'b']:
                if custom_mml.lower()[index] == 'b':
                    #mml = mml[:-len(mml_duration) if mml_duration else len(octave_str) + 1] + mml_note + '-' + mml_duration
                    mml += "-"
                else:
                    mml += '#'
                index += 1
            octave_shift = 0
            
            hyphen_count = 0
            while index < len(custom_mml) and custom_mml.lower()[index] == '-':
                hyphen_count += 1
                current_duration //= 2
                if current_duration == 0:
                    current_duration = max(current_duration, 1)
                #print(char, "base_duration=", base_duration, " | current_duration = ",current_duration)
                index += 1
            while index < len(custom_mml) and custom_mml.lower()[index] == "/":
                current_duration *= 2
                #print(char, "base_duration=", base_duration, " | current_duration = ",current_duration)
                index += 1

            mml_duration = get_duration_mml(current_duration)
            if mml_duration == "0":
                mml_duration = "32" # 極端に短い場合はPyxelで扱える最小に近い値に
            #print("mml_duration=", mml_duration)
            mml += mml_duration


        elif char == '^':
            octave_shift += 1
            index += 1
        elif char == '_':
            octave_shift -= 1
            index += 1
        else:
            mml += char
            index += 1

    return mml

def midcustom_mml_to_mml(custom_mml):
    """Middle custom MML to Original MML
    
    * `drmfsac -> cdefgab`
    * `_ -> <`
    * `^ -> >`
    * `p -> r`
    * Other symbols are same as the original
    """
    mml = ""
    index = 0
    note_map = {'d': 'c', 'r': 'd', 'm': 'e', 'f': 'f', 's': 'g', 'a': 'a', 'si': 'b', 'c' : 'b', 'p': 'r'}

    while index < len(custom_mml):
        char = custom_mml.lower()[index]
        
        if char in note_map:
            mml_note = note_map.get(char)
            index += 1
            mml += mml_note
        elif char == '^':
            mml += ">"
            index += 1
        elif char == "_":
            mml += "<"
            index += 1
        else:
            mml += char
            index += 1
    return mml