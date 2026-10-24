"""Shared runtime and static-preview appearance parameters."""
import json
from pathlib import Path

CONFIG = json.loads(Path(__file__).with_suffix('.json').read_text(encoding='utf-8'))

def css():
    mode = CONFIG['modes'][CONFIG['default_mode']]
    return ('.label{background:rgba(43,43,43,' + str(mode['panel_alpha']) + ');'
            'text-shadow:-1px 0 rgba(0,0,0,.9),1px 0 rgba(0,0,0,.9),'
            '0 -1px rgba(0,0,0,.9),0 1px rgba(0,0,0,.9)}'
            '.label.note{background:rgba(43,43,43,' + str(mode['note_alpha']) + ')}')

def csharp():
    def values(key):
        return ','.join(str(float(mode[key]))+'f' for mode in CONFIG['modes'])
    return ('namespace LakeviewChinese { internal static class Appearance { '
            'internal const int DefaultMode = '+str(CONFIG['default_mode'])+'; '
            'internal const string PreferenceKey = '+json.dumps(CONFIG['preference_key'])+'; '
            'internal const float OutlineAlpha = '+str(CONFIG['outline_alpha'])+'f; '
            'internal static readonly float[] PanelAlpha = new float[]{'+values('panel_alpha')+'}; '
            'internal static readonly float[] NoteAlpha = new float[]{'+values('note_alpha')+'}; '
            '} }')
