"""Inventory Windows SAPI voices for Japanese availability."""
try:
    import pyttsx3
    e = pyttsx3.init()
    voices = e.getProperty('voices')
    print(f'Available SAPI voices: {len(voices)}')
    ja_voices = []
    for v in voices:
        name = v.name or ''
        vid = v.id or ''
        is_ja = 'jap' in name.lower() or 'jap' in vid.lower() or 'haruka' in name.lower() or 'ayumi' in name.lower() or 'ichiro' in name.lower()
        marker = '  JA  ' if is_ja else '      '
        print(f'{marker}{name[:50]:50} | {vid[-50:]}')
        if is_ja:
            ja_voices.append(v)
    print(f'\nJapanese SAPI voices: {len(ja_voices)}')
except Exception as exc:
    print(f'pyttsx3 error: {type(exc).__name__}: {exc}')
