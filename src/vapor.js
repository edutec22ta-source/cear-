// Vapor realista: shader WebGL com ruído fbm + domain warp, renderizado em baixa resolução
// (o vapor é macio, então a resolução reduzida deixa mais leve e ainda suaviza).
// Uso: const v = criarVapor(canvas, { fontes: [...] }); v.play(); v.pause(); v.render(t)
function criarVapor(canvas, opcoes) {
  const gl = canvas.getContext('webgl', {
    alpha: true, premultipliedAlpha: true, antialias: false, depth: false,
    stencil: false, preserveDrawingBuffer: true, powerPreference: 'low-power'
  });
  if (!gl) return null;

  const vert = `
    attribute vec2 aPos;
    varying vec2 vUv;
    void main() { vUv = aPos * 0.5 + 0.5; gl_Position = vec4(aPos, 0.0, 1.0); }`;

  const frag = `
    #ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
    #else
    precision mediump float;
    #endif
    varying vec2 vUv;
    uniform vec2 uRes;
    uniform float uTime;
    uniform float uFade;
    uniform vec4 uFonte[3];   // x, y (0..1 a partir de baixo), meia largura, altura da coluna
    uniform vec3 uForca;      // intensidade de cada fonte

    vec2 hash2(vec2 p) {
      p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
      return -1.0 + 2.0 * fract(sin(p) * 43758.5453);
    }
    float ruido(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);
      vec2 u = f * f * (3.0 - 2.0 * f);
      float a = dot(hash2(i), f);
      float b = dot(hash2(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
      float c = dot(hash2(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
      float d = dot(hash2(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));
      return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
    }
    float fbm(vec2 p) {
      float s = 0.0;
      float a = 0.5;
      mat2 r = mat2(1.6, 1.2, -1.2, 1.6);
      for (int i = 0; i < 5; i++) { s += a * ruido(p); p = r * p; a *= 0.5; }
      return s;
    }

    float coluna(vec2 P, vec4 f, float A, float t, float semente) {
      vec2 S = vec2(f.x * A, f.y);
      float H = f.w;
      float h = (P.y - S.y) / H;                 // 0 na superfície, 1 no topo da coluna
      if (h < -0.35 || h > 1.2) return 0.0;
      float hp = max(h, 0.0);
      // vento e torção: quanto mais alto, mais o vapor entorta
      float vento = ruido(vec2(semente, hp * 1.4 - t * 0.10)) * 1.25 + 0.22 * sin(t * 0.31 + semente * 2.7);
      float largura = f.z * A * (0.80 + 1.05 * hp);
      float x = (P.x - S.x - vento * hp * hp * H * 0.42) / largura;
      // campo de vapor subindo, com redemoinhos (domain warp)
      vec2 q = vec2(x * 1.15 + semente * 7.3, hp * 2.1 - t * 0.50);
      vec2 w = vec2(fbm(q + vec2(0.0, t * 0.06)), fbm(q + vec2(5.2, 1.3 - t * 0.05)));
      float n = fbm(q * 1.4 + w * 1.9) * 0.5 + 0.5;
      float fios = smoothstep(0.46, 0.80, n);     // fios de vapor
      float veu = smoothstep(0.34, 0.70, n) * 0.36; // véu leve em volta
      float borda = 1.0 - smoothstep(0.30, 1.0, abs(x));
      float base = smoothstep(-0.30, 0.04, h);
      float topo = 1.0 - smoothstep(0.30, 1.0, h);
      float densidade = 1.3 - 0.65 * hp;           // mais denso perto do prato
      return (fios + veu) * borda * base * topo * densidade;
    }

    void main() {
      float A = uRes.x / uRes.y;
      vec2 P = vec2(vUv.x * A, vUv.y);
      float t = uTime;
      float rajada = 0.80 + 0.20 * sin(t * 0.47) * sin(t * 0.19 + 1.3);
      float d = uForca.x * coluna(P, uFonte[0], A, t, 1.0)
              + uForca.y * coluna(P, uFonte[1], A, t * 1.08 + 11.0, 4.0)
              + uForca.z * coluna(P, uFonte[2], A, t * 0.93 + 23.0, 8.0);
      float a = clamp(d * rajada, 0.0, 1.0) * 0.82 * uFade;
      gl_FragColor = vec4(vec3(1.0, 0.965, 0.92) * a, a);
    }`;

  const compilar = (tipo, fonte) => {
    const s = gl.createShader(tipo);
    gl.shaderSource(s, fonte);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  };
  let prog;
  try {
    prog = gl.createProgram();
    gl.attachShader(prog, compilar(gl.VERTEX_SHADER, vert));
    gl.attachShader(prog, compilar(gl.FRAGMENT_SHADER, frag));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  } catch (erro) {
    return null;
  }
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const aPos = gl.getAttribLocation(prog, 'aPos');
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

  const uRes = gl.getUniformLocation(prog, 'uRes');
  const uTime = gl.getUniformLocation(prog, 'uTime');
  const uFade = gl.getUniformLocation(prog, 'uFade');
  const uFonte = gl.getUniformLocation(prog, 'uFonte');
  const uForca = gl.getUniformLocation(prog, 'uForca');

  const fontes = (opcoes.fontes || []).slice(0, 3);
  const dados = new Float32Array(12);
  const forca = [0, 0, 0];
  fontes.forEach((f, i) => { dados.set([f.x, f.y, f.largura, f.altura], i * 4); forca[i] = f.forca ?? 1; });
  gl.uniform4fv(uFonte, dados);
  gl.uniform3fv(uForca, forca);

  const escala = opcoes.escala || 0.5;
  let largura = 2, altura = 2;
  const redimensionar = () => {
    const r = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    largura = Math.max(2, Math.round(r.width * dpr * escala));
    altura = Math.max(2, Math.round(r.height * dpr * escala));
    if (canvas.width !== largura || canvas.height !== altura) {
      canvas.width = largura; canvas.height = altura;
    }
    gl.viewport(0, 0, largura, altura);
  };
  redimensionar();
  if ('ResizeObserver' in window) new ResizeObserver(() => { redimensionar(); if (!rodando) desenhar(ultimoT); }).observe(canvas);

  let rodando = false, raf = 0, inicio = 0, ultimoT = 18, fade = opcoes.fadeInicial ?? 0, comeco = 0;
  const duracaoFade = opcoes.duracaoFade ?? 1.8;   // segundos para o vapor surgir
  const desenhar = (t) => {
    ultimoT = t;
    gl.uniform2f(uRes, largura, altura);
    gl.uniform1f(uTime, t % 900);
    gl.uniform1f(uFade, fade);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
  const quadro = (agora) => {
    if (!inicio) inicio = agora - ultimoT * 1000;
    if (!comeco) comeco = agora - fade * duracaoFade * 1000;
    const t = (agora - inicio) / 1000;
    fade = Math.min(1, (agora - comeco) / (duracaoFade * 1000));
    desenhar(t);
    if (rodando) raf = requestAnimationFrame(quadro);
  };

  return {
    play() { if (rodando) return; rodando = true; inicio = 0; comeco = 0; raf = requestAnimationFrame(quadro); },
    pause() { rodando = false; cancelAnimationFrame(raf); },
    render(t, f = 1) { fade = f; desenhar(t); }
  };
}
