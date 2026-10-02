import base64, re, html, json, sys
from urllib.parse import quote
from pathlib import Path

# ------------------------------------------------------------------
# Contatos do restaurante
# Vazio = site em demonstração: o site mostra (99) 99999-9999, esconde o
# Instagram, os botões do WhatsApp mostram uma prévia da mensagem e o
# Google não indexa a página.
# Depois da venda, preencha e rode de novo:
#   WHATSAPP = '11930056723'
#   INSTAGRAM = 'cearagrillrestaurante'
# ------------------------------------------------------------------
WHATSAPP = ''
INSTAGRAM = ''

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'build'))
from menu_data import CATEGORIAS  # noqa: E402

tpl = (ROOT / 'src/template.html').read_text(encoding='utf-8')
esc = lambda s: html.escape(s, quote=True)


def data_uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode((ROOT / path).read_bytes()).decode()


def brl(valor):
    return 'R$ ' + f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


PLUS = ('<span class="plus" aria-hidden="true"><svg class="ico mais"><use href="#i-plus"/></svg>'
        '<svg class="ico ok"><use href="#i-check"/></svg></span>')


def botao(nome_pedido, rotulo, preco, tamanho=''):
    partes = []
    if rotulo:
        partes.append(f'<span class="size">{esc(rotulo)}</span>')
    partes.append(f'<span class="mi-price">{brl(preco)}</span>')
    detalhe = f', {tamanho.lower()}' if tamanho else ''
    aria = f'Adicionar {nome_pedido}{detalhe} ao pedido: {brl(preco)}'
    attrs = f'data-nome="{esc(nome_pedido)}" data-preco="{preco}"'
    if tamanho:
        attrs += f' data-tamanho="{esc(tamanho)}"'
    return f'<button class="add" type="button" {attrs} aria-label="{esc(aria)}">{"".join(partes)}{PLUS}</button>'


MARQUEE = ['Feijoada completa', 'Picanha', 'Contra filé à parmegiana', 'Rabada', 'Cuscuz com queijo',
           'Costelinha assada', 'Filé de tilápia', 'Marmitas do dia', 'Fazemos entregas']


def render_marquee():
    sep = '<svg viewBox="0 0 64 64"><use href="#i-forks"/></svg>'
    grupo = ''.join(f'<span>{esc(n)}</span>{sep}' for n in MARQUEE)
    return '\n'.join(f'      <div class="mq-group">{grupo}</div>' for _ in range(2))


def render_menu():
    out = ['<div class="tabs" role="tablist" aria-label="Categorias do cardápio">']
    for i, cat in enumerate(CATEGORIAS):
        sel = 'true' if i == 0 else 'false'
        tab_index = '' if i == 0 else ' tabindex="-1"'
        out.append(f'  <button class="tab" type="button" role="tab" id="tab-{cat["id"]}" aria-controls="cat-{cat["id"]}" aria-selected="{sel}"{tab_index}>{esc(cat["titulo"])}</button>')
    out.append('  <span class="tab-ink" aria-hidden="true"></span>')
    out.append('</div>')

    for cat in CATEGORIAS:
        out.append(f'<div class="menu-cat" id="cat-{cat["id"]}">')
        out.append(f'  <h3 class="menu-cat-title">{esc(cat["titulo"])}</h3>')
        out.append('  <ul class="menu-list">')
        for nome, desc, opcoes in cat['itens']:
            botoes = []
            for rotulo, preco, nome_pedido in opcoes:
                if nome_pedido:  # variação com nome próprio (ex.: churrasco ou asinha)
                    botoes.append(botao(nome_pedido, rotulo, preco))
                else:  # tamanho único ou médio/grande
                    botoes.append(botao(nome, rotulo, preco, tamanho=rotulo or ''))
            multi = ' is-multi' if len(opcoes) > 1 else ''
            out.append('    <li class="mi">')
            out.append(f'      <h4 class="mi-name">{esc(nome)}</h4>')
            if desc:
                out.append(f'      <p class="mi-desc">{esc(desc)}</p>')
            out.append(f'      <div class="mi-buy{multi}">{"".join(botoes)}</div>')
            out.append('    </li>')
        if cat.get('salgados'):
            s = cat['salgados']
            chips = ''.join(
                f'<button class="add" type="button" data-nome="{esc(n)}" data-preco="{s["preco"]}" '
                f'aria-label="{esc(f"Adicionar {n} ao pedido: {brl(s["preco"])}")}"><span class="add-chip">{esc(n)}</span>{PLUS}</button>'
                for n in s['nomes'])
            out.append('    <li class="mi mi-salgados">')
            out.append('      <h4 class="mi-name">Salgados</h4>')
            out.append(f'      <p class="mi-desc">{brl(s["preco"])} cada. Toque para adicionar.</p>')
            out.append(f'      <div class="mi-chips">{chips}</div>')
            out.append('    </li>')
        out.append('  </ul>')
        out.append('</div>')
    return '\n'.join('      ' + linha for linha in out)


def so_digitos(texto):
    d = re.sub(r'\D', '', texto)
    if d.startswith('55') and len(d) in (12, 13):
        d = d[2:]
    return d


def formatar_telefone(d):
    if len(d) == 11:
        return f'({d[:2]}) {d[2:7]}-{d[7:]}'
    if len(d) == 10:
        return f'({d[:2]}) {d[2:6]}-{d[6:]}'
    raise SystemExit(f'WHATSAPP inválido: {WHATSAPP!r} (use DDD + número, ex.: 11930056723)')


DDD_NUMERO = so_digitos(WHATSAPP)
DEMO = not DDD_NUMERO
WA_NUMBER = '' if DEMO else '55' + DDD_NUMERO
PHONE_DISPLAY = '(99) 99999-9999' if DEMO else formatar_telefone(DDD_NUMERO)
INSTA = INSTAGRAM.strip().lstrip('@').strip('/')
INSTAGRAM_URL = f'https://www.instagram.com/{INSTA}/' if INSTA else ''

ld = {
    '@context': 'https://schema.org',
    '@type': 'Restaurant',
    'name': 'Restaurante Ceará Grill',
    'servesCuisine': ['Brasileira', 'Churrasco'],
    'priceRange': 'R$ 5 a R$ 47',
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': 'Av. Guarapiranga, 2598',
        'addressLocality': 'São Paulo',
        'addressRegion': 'SP',
        'postalCode': '04911-005',
        'addressCountry': 'BR',
    },
}
if not DEMO:
    ld['telephone'] = f'+55 {DDD_NUMERO[:2]} {PHONE_DISPLAY.split(" ", 1)[1]}'
if INSTAGRAM_URL:
    ld['sameAs'] = [INSTAGRAM_URL]

values = {
    'LOGO': data_uri('assets/logo-320.webp', 'image/webp'),
    'FEIJOADA': data_uri('assets/feijoada.webp', 'image/webp'),
    'FAVICON': data_uri('assets/favicon-64.png', 'image/png'),
    'WA_NUMBER': WA_NUMBER,
    'PHONE_DISPLAY': PHONE_DISPLAY,
    'INSTAGRAM_URL': INSTAGRAM_URL,
    'INSTAGRAM_HANDLE': f'@{INSTA}',
    'JSON_LD': json.dumps(ld, ensure_ascii=False, indent=2).replace('</', '<\\/'),
    'GMAPS': esc('https://www.google.com/maps/search/?api=1&query=' + quote('Restaurante Ceará Grill, Av. Guarapiranga, 2598, São Paulo - SP, 04911-005', safe='')),
    'WAZE': esc('https://waze.com/ul?q=' + quote('Av. Guarapiranga, 2598, São Paulo - SP', safe='') + '&navigate=yes'),
    'MENU': render_menu(),
    'MARQUEE': render_marquee(),
    'VAPOR_JS': (ROOT / 'src/vapor.js').read_text(encoding='utf-8'),
}


def wa_link(m):
    texto = m.group(1)
    if DEMO:  # sem número: o link leva ao pedido e o JS mostra a prévia da mensagem
        return f'href="#pedido" data-wa="{esc(texto)}"'
    return f'href="https://wa.me/{WA_NUMBER}?text={quote(texto, safe="")}" target="_blank" rel="noopener"'


# Trechos que só aparecem em um dos modos: {{#DEMO}}...{{/DEMO}} e {{#INSTAGRAM}}...{{/INSTAGRAM}}
blocos = {'DEMO': DEMO, 'INSTAGRAM': bool(INSTA)}
out = re.sub(r'^[ \t]*\{\{#(\w+)\}\}[ \t]*\n(.*?)^[ \t]*\{\{/\1\}\}[ \t]*\n',
             lambda m: m.group(2) if blocos[m.group(1)] else '', tpl, flags=re.M | re.S)

total_wa = out.count('{{WA|')
out, trocados = re.subn(r'href="\{\{WA\|([^}]*)\}\}" target="_blank" rel="noopener"', wa_link, out)
assert trocados == total_wa, f'{total_wa - trocados} link(s) do WhatsApp fora do padrão'
for k, v in values.items():
    out = out.replace('{{' + k + '}}', v)

left = re.findall(r'\{\{[^}]+\}\}', out)
assert not left, left
dest = ROOT / 'index.html'
dest.write_text(out, encoding='utf-8')
modo = 'demonstração' if DEMO else f'WhatsApp {PHONE_DISPLAY}'
print('ok:', dest.name, round(dest.stat().st_size / 1024), 'KB |', modo, '| Instagram:', f'@{INSTA}' if INSTA else 'oculto')
