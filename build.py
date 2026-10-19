# Monta guiapega.com.br: copy do rascunho SuperNanny 16/10 + tracking da v3 com pixel NOVO.
import re, pathlib
R = pathlib.Path(__file__).parent
src = (R.parent/'supernanny/rascunhos/2026-10-16-guia-copy-meta/index.html').read_text(encoding='utf-8')
v3 = (R.parent/'guiadapega/guia-v3/index.html').read_text(encoding='utf-8')
PX = '1646156103576897'

pixel = v3[v3.index('<!-- Meta Pixel'):v3.index('<!-- End Meta Pixel -->')+len('<!-- End Meta Pixel -->')]
pixel = pixel.replace('2192980584647606', PX).replace(' domain=.manualdorecemnascido.com.br;', '')
pixel = pixel.replace('(Guia da Pega - 2 pixels)', '(guiapega.com.br - pixel novo 16/10)')
assert pixel.count(PX) >= 3, pixel.count(PX)

# Clarity adiado: carrega na 1a interacao ou apos 3,5s (nao disputa banda com a 1a dobra)
clarity = '''<script>(function(){var go=function(){if(window.__cl)return;window.__cl=1;(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","xq5004c7qg");};['scroll','pointerdown','keydown','touchstart'].forEach(function(e){addEventListener(e,go,{once:true,passive:true})});setTimeout(go,3500);})();</script>'''

out = src
out = out.replace('<!-- [rascunho] Clarity removido -->', clarity)
out = out.replace('<!-- [rascunho] GTM removido -->\n', '')
out = re.sub(r'<!-- \[rascunho\] PIXEL removido[^>]*-->', lambda m: pixel, out)
beacon = v3[v3.index('<!-- funil-secao (Sherlock)'):]
beacon = beacon[:beacon.index('</script>')+len('</script>')]
out = re.sub(r'<!-- \[rascunho\] beacon do medidor removido[^>]*-->', lambda m: beacon, out)
out = out.replace('https://guiadapega.com.br/guia-v3/assets/', 'assets/')
assert 'guiadapega.com.br' not in out and '[rascunho]' not in out

# fontes sem bloquear a renderizacao
fonts = re.search(r'<link href="(https://fonts.googleapis.com/css2[^"]+)" rel="stylesheet">', out)
out = out.replace(fonts.group(0), f'<link rel="preload" as="style" href="{fonts.group(1)}" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="{fonts.group(1)}"></noscript>')

# depoimentos: falas reais do site antigo (guia-v3) com tapa leve pra tirar termo de saude (aprovado Bruno 19/10)
DEPO = {
    'Bruna · ': 'Me diziam que sofrer no começo era normal e que eu tinha que aguentar. Aprendi a oferecer o peito de um jeito que o Theo pega com facilidade, e hoje amamento tranquila, sem medo da próxima mamada.',
    'Mariana · ': 'A Aurora mamava o tempo todo e nunca parecia satisfeita. Quando aprendi a facilitar a pega, ela passou a tirar muito mais leite em cada mamada e hoje sai do peito tranquila e cheia.',
    'Pati · ': 'Eu já chegava em cada mamada sem aguentar mais. Poucos dias depois de mudar a forma de oferecer o peito, tudo mudou. Agora o Davi mama e eu curto o momento.',
}
for nome, txt in DEPO.items():
    i = out.index(nome); a = out.index('<p>', i) + 3; b = out.index('</p>', a)
    out = out[:a] + txt + out[b:]

# headline + botao (opcao 1 "nao desistir", aprovada Bruno 19/10)
h1a = out.index('<h1>'); h1b = out.index('</h1>', h1a)
out = out[:h1a] + '<h1>Pensando em desistir de amamentar? Existe um jeito de facilitar a pega do seu bebê, e a mamada fica leve <em>já na próxima vez</em>.' + out[h1b:]
assert out.count('Quero amamentar tranquila') == 3
out = out.replace('Quero amamentar tranquila', 'Quero continuar amamentando')
visivel = re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', out)).lower()
for w in (' dor ', 'fissura', 'machuc', 'carne viva', 'cicatriz', 'peso', 'engord', 'consultora', 'enfermeira'):
    assert w not in visivel, (w, visivel[max(0,visivel.find(w)-120):visivel.find(w)+60])

og = '<meta name="facebook-domain-verification" content="fwouj6eyndilhopnl0eb0e4cw2yixt" />\n<link rel="canonical" href="https://guiapega.com.br/">\n<meta property="og:title" content="Guia da Pega | por Dayane Dos Anjos">\n<meta property="og:image" content="https://guiapega.com.br/assets/hero.webp">\n<meta property="og:url" content="https://guiapega.com.br/">\n'
out = out.replace('<title>', og + '<title>', 1)
(R/'index.html').write_text(out, encoding='utf-8')
print('ok', len(out))
