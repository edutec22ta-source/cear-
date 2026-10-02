# Restaurante Ceará Grill

Site de página única do **Restaurante Ceará Grill**, na Av. Guarapiranga, 2598 – Guarapiranga, São Paulo/SP.

A feijoada fica em destaque logo na abertura. O site traz o cardápio real com preços e monta o pedido para enviar pelo WhatsApp (11) 93005-6723.

## O que tem no site

- Abertura com a feijoada, vapor animado em tempo real (WebGL), brasas subindo e parallax com o mouse
- Cardápio com abas (Pratos especiais, Marmitas do dia e Café da manhã com salgados)
- Pedido montado no próprio site: o cliente toca no preço, ajusta as quantidades e envia tudo pelo WhatsApp com o total estimado
- Faixa com pratos rodando, seções que aparecem ao rolar e microinterações
- Funciona no celular, respeita a opção "reduzir movimento" e mostra o cardápio inteiro mesmo sem JavaScript

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `index.html` | O site pronto, num arquivo só e com as imagens embutidas. É esse que vai para o ar. |
| `src/template.html` | Código-fonte da página (HTML, CSS e JavaScript) |
| `src/vapor.js` | Efeito de vapor da feijoada (shader WebGL) |
| `build/menu_data.py` | Cardápio: nomes, descrições e preços |
| `build/build.py` | Gera o `index.html` juntando a página, o cardápio e as imagens |
| `assets/` | Logo, foto da feijoada e favicon usados na geração |

## Como mudar o cardápio ou o texto

1. Para preços e pratos, edite `build/menu_data.py`. Para o resto, edite `src/template.html`.
2. Rode `python3 build/build.py` (só precisa de Python 3, sem instalar nada).
3. Envie o `index.html` novo.

O número do WhatsApp e o Instagram ficam no começo do `build/build.py`.

## Como publicar

- **GitHub Pages:** em Settings → Pages, escolha a branch `main` e a pasta raiz. No plano grátis, o repositório precisa ser público.
- **Vercel ou Netlify:** importe o repositório como site estático. Não precisa de comando de build.

## Confirmar com o restaurante antes de publicar

- Se o (11) 93005-6723 é WhatsApp e se o Instagram é mesmo @cearagrill_
- Horário de funcionamento e dias e valor da feijoada (não estão nos flyers)
- "Filé de peixe panga frito": no flyer está escrito "Panca"
- Se "Costelinha assada, frango assado, linguiça assada e calabresa" é uma escolha entre as carnes ou um prato com todas
- A foto da feijoada é ilustrativa, então vale trocar por uma foto real quando houver

---

Site feito por Protocol.
