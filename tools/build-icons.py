"""يبني شريحة أيقونات SVG من مكتبة Phosphor Icons (النمط العادي + المعبّأ) ويضعها داخل index.html.

الاستخدام:
  npm pack @phosphor-icons/core@2.1.1 && tar xzf phosphor-icons-core-2.1.1.tgz
  python3 tools/build-icons.py package/assets index.html

#ph-NAME للنمط العادي (مثل SF Symbols)، و #phf-NAME للنمط المعبّأ (التبويب النشط ومربعات الإعدادات).
"""
import re
import sys

ICONS = [
    'house', 'calendar-dots', 'chart-bar', 'gear-six', 'sign-in', 'sign-out', 'sun', 'moon',
    'check-circle', 'coffee', 'clock', 'caret-left', 'caret-right', 'caret-down', 'copy',
    'clipboard-text', 'eye', 'eye-slash', 'hourglass-medium', 'timer', 'trend-up',
    'calendar-check', 'airplane-tilt', 'first-aid', 'briefcase', 'cloud-check', 'cloud-slash',
    'warning-circle', 'info', 'trash', 'pencil-simple', 'plus', 'x', 'key', 'link',
    'download-simple', 'upload-simple', 'arrow-clockwise', 'lightning', 'user-circle', 'palette',
    'lightbulb', 'flag', 'sparkle', 'calendar-blank', 'calendar-x', 'calculator',
    'sliders-horizontal', 'shield-check', 'fingerprint', 'hand-palm', 'circle-half', 'laptop',
    'camera', 'lock-simple', 'check', 'text-aa', 'hash', 'map-pin',
]

assets, page = sys.argv[1], sys.argv[2]
symbols = []
for name in ICONS:
    for style, prefix in (('regular', 'ph'), ('fill', 'phf')):
        suffix = '' if style == 'regular' else '-fill'
        svg = open(f'{assets}/{style}/{name}{suffix}.svg', encoding='utf-8').read()
        inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
        symbols.append(f'<symbol id="{prefix}-{name}" viewBox="0 0 256 256">{inner}</symbol>')

sprite = ('<!--ICONS:START--><svg width="0" height="0" style="position:absolute" aria-hidden="true" fill="currentColor"><defs>'
          + ''.join(symbols) + '</defs></svg><!--ICONS:END-->')
html = open(page, encoding='utf-8').read()
html = re.sub(r'<!--ICONS:START-->.*?<!--ICONS:END-->', lambda m: sprite, html, flags=re.S)
open(page, 'w', encoding='utf-8').write(html)
print(f'{len(ICONS)} icons × 2 styles embedded')
