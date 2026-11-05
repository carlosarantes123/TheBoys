"""Gera os desenhos do arraste do quadro: o herói (tema claro) e o vilão (tema escuro).

Uso, na raiz do projeto:   python ferramentas/gerar_personagens.py
Saída: src/components/arraste/heroi.svg e src/components/arraste/vilao.svg

Como os personagens são montados:
- proporção heroica calculada, com a cabeça como unidade (H): corpo ~8H, coxa 2H, canela 1,9H,
  braço 1,5H, antebraço 1,25H, mão 0,75H; cada articulação sai de comprimento x direção;
- em cada osso, uma forma de espessura variável (o bíceps engrossa no meio, punho e tornozelo
  afinam), com bordas suavizadas em curvas;
- sombra de desenho animado sempre do lado de baixo (a luz vem de cima) e luz de recorte em cima;
- o vilão tem luz em duas fontes: recorte índigo frio de cima e brasa carmim de baixo;
  barra do sobretudo rasgada em pontas, dobras com sombra em cunha e ventosas nos tentáculos;
- os tentáculos são curvas que afinam até a ponta; a animação (SMIL) interpola variantes com os
  mesmos pontos, e as pontas que agarram a borda do cartão ficam fixas.
Personagens originais da equipe (só o estilo é inspirado em desenho animado de super-herói).
"""

import math
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, 'src', 'components', 'arraste')


# ============================================================ esqueleto e formas

TINTA = '#0a1230'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


# ------------------------------------------------------------- curvas
def catmull(pontos, fechado=True, tensao=0.5):
    """Caminho suave (beziers cúbicas) que passa por todos os pontos."""
    n = len(pontos)
    if n < 3:
        return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pontos)
    d = f'M{f(pontos[0][0])} {f(pontos[0][1])}'
    total = n if fechado else n - 1
    for i in range(total):
        p0 = pontos[(i - 1) % n] if fechado or i > 0 else pontos[0]
        p1 = pontos[i % n]
        p2 = pontos[(i + 1) % n]
        p3 = pontos[(i + 2) % n] if fechado or i + 2 < n else pontos[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * tensao / 3, p1[1] + (p2[1] - p0[1]) * tensao / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tensao / 3, p2[1] - (p3[1] - p1[1]) * tensao / 3)
        d += f' C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}'
    return d + (' Z' if fechado else '')


def spline_aberta(pontos, amostras=12):
    """Amostra uma Catmull-Rom aberta passando pelos pontos (para a linha central dos membros)."""
    res = []
    n = len(pontos)
    for i in range(n - 1):
        p0 = pontos[max(0, i - 1)]
        p1, p2 = pontos[i], pontos[i + 1]
        p3 = pontos[min(n - 1, i + 2)]
        for k in range(amostras if i < n - 2 else amostras + 1):
            t = k / amostras
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            res.append((x, y))
    return res


def normais(pts):
    res = []
    for i in range(len(pts)):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        res.append((-dy / n, dx / n))
    return res


def perfil(t, larguras):
    """Largura em t (0..1) a partir de pontos de controle [(t, largura), ...], com transição suave."""
    for (t0, w0), (t1, w1) in zip(larguras, larguras[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0) if t1 > t0 else 0
            u = u * u * (3 - 2 * u)
            return w0 + (w1 - w0) * u
    return larguras[-1][1]


# ------------------------------------------------------------- membros
class Membro:
    """Forma de espessura variável ao longo de uma linha que passa pelas articulações."""

    def __init__(self, juntas, larguras, amostras=10, ponta_redonda=True):
        self.c = spline_aberta(juntas, amostras)
        self.n = normais(self.c)
        tot = len(self.c) - 1
        self.w = [perfil(i / tot, larguras) / 2 for i in range(len(self.c))]
        self.ponta_redonda = ponta_redonda

    def lados(self, recuo_a=0.0, recuo_b=0.0):
        a = [(x + nx * w * (1 - recuo_a), y + ny * w * (1 - recuo_a)) for (x, y), (nx, ny), w in zip(self.c, self.n, self.w)]
        b = [(x - nx * w * (1 - recuo_b), y - ny * w * (1 - recuo_b)) for (x, y), (nx, ny), w in zip(self.c, self.n, self.w)]
        return a, b

    def _tampa(self, centro, raio, de, ate, passos=5):
        pts = []
        for k in range(1, passos):
            ang = de + (ate - de) * k / passos
            pts.append((centro[0] + math.cos(ang) * raio, centro[1] + math.sin(ang) * raio))
        return pts

    def contorno(self):
        a, b = self.lados()
        pts = list(a)
        if self.ponta_redonda:
            (x, y), (nx, ny), w = self.c[-1], self.n[-1], self.w[-1]
            ang = math.atan2(ny, nx)
            pts += self._tampa((x, y), w, ang, ang - math.pi)
        pts += list(reversed(b))
        (x, y), (nx, ny), w = self.c[0], self.n[0], self.w[0]
        ang = math.atan2(-ny, -nx)
        pts += self._tampa((x, y), w, ang, ang - math.pi)
        return pts

    def lado_sombra(self):
        """+1 se o lado 'a' (normal positiva) aponta para baixo, senão -1."""
        media = sum(ny for _, ny in self.n) / len(self.n)
        return 1 if media > 0 else -1

    def sombra(self, fracao=0.42, de=0.0, ate=1.0):
        """Faixa de sombra no lado de baixo: da borda até `fracao` da largura."""
        lado = self.lado_sombra()
        tot = len(self.c) - 1
        borda, dentro = [], []
        for i, ((x, y), (nx, ny), w) in enumerate(zip(self.c, self.n, self.w)):
            if not de <= i / tot <= ate:
                continue
            borda.append((x + lado * nx * w, y + lado * ny * w))
            dentro.append((x + lado * nx * w * (1 - 2 * fracao), y + lado * ny * w * (1 - 2 * fracao)))
        return borda + list(reversed(dentro))

    def luz(self, de=0.1, ate=0.8, recuo=2.2):
        """Linha de luz de recorte no lado de cima, um pouco para dentro da borda."""
        lado = -self.lado_sombra()
        tot = len(self.c) - 1
        pts = []
        for i, ((x, y), (nx, ny), w) in enumerate(zip(self.c, self.n, self.w)):
            if de <= i / tot <= ate:
                pts.append((x + lado * nx * (w - recuo), y + lado * ny * (w - recuo)))
        return pts


def forma(pontos, cor, contorno=True, largura=2.2, extra=''):
    traco = f' stroke="{TINTA}" stroke-width="{largura}" stroke-linejoin="round"' if contorno else ''
    return f'<path d="{catmull(pontos)}" fill="{cor}"{traco}{extra} />'


def linha(pontos, cor, largura=2, opacidade=1.0):
    return (
        f'<path d="{catmull(pontos, fechado=False)}" fill="none" stroke="{cor}" stroke-width="{largura}" '
        f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacidade}" />'
    )


def membro_svg(m, cor, sombra, luz=None, fracao=0.42, sombra_de=0.0, sombra_ate=1.0):
    partes = [forma(m.contorno(), cor)]
    partes.append(forma(m.sombra(fracao, sombra_de, sombra_ate), sombra, contorno=False))
    if luz:
        partes.append(linha(m.luz(), luz, 1.8, 0.9))
    # contorno de novo por cima da sombra, para a borda ficar limpa
    partes.append(f'<path d="{catmull(m.contorno())}" fill="none" stroke="{TINTA}" stroke-width="2.2" stroke-linejoin="round" />')
    return '\n  '.join(partes)


# ============================================================ tentáculos (curvas afinadas)


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


def amostrar(segs, n):
    pts = []
    for i, s in enumerate(segs):
        for k in range(0 if i == 0 else 1, n + 1):
            pts.append(bezier(*s, k / n))
    return pts


def largura(t, w0, w1, curva=0.85):
    return w1 + (w0 - w1) * (1 - t) ** curva


def afinado(pts, w0, w1, curva=0.85, ponta_redonda=True):
    """Polígono de espessura variável ao longo da curva."""
    ns = normais(pts)
    total = len(pts) - 1
    cima, baixo = [], []
    for i, ((x, y), (nx, ny)) in enumerate(zip(pts, ns)):
        w = largura(i / total, w0, w1, curva) / 2
        cima.append((x + nx * w, y + ny * w))
        baixo.append((x - nx * w, y - ny * w))
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in cima)
    if ponta_redonda:
        r = largura(1, w0, w1, curva) / 2
        x, y = baixo[-1]
        d += f' A{f(r)} {f(r)} 0 0 1 {f(x)} {f(y)}'
    d += ' L' + ' L'.join(f'{f(x)} {f(y)}' for x, y in reversed(baixo))
    r0 = largura(0, w0, w1, curva) / 2
    d += f' A{f(r0)} {f(r0)} 0 0 1 {f(cima[0][0])} {f(cima[0][1])} Z'
    return d


def paralela(pts, desloc, de=0.0, ate=1.0):
    ns = normais(pts)
    n = len(pts) - 1
    sel = [(p, q) for i, (p, q) in enumerate(zip(pts, ns)) if de <= i / n <= ate]
    return 'M' + ' L'.join(f'{f(x + nx * desloc)} {f(y + ny * desloc)}' for (x, y), (nx, ny) in sel)


def ventosas(pts, w0, w1, qtd, de=0.14, ate=0.72):
    ns = normais(pts)
    n = len(pts) - 1
    partes = []
    for j in range(qtd):
        t = de + (ate - de) * j / max(1, qtd - 1)
        i = int(t * n)
        (x, y), (nx, ny) = pts[i], ns[i]
        w = largura(t, w0, w1) / 2
        cx, cy = x - nx * w * 0.58, y - ny * w * 0.58
        r = max(1.0, w * 0.3)
        partes.append(f'M{f(cx - r)} {f(cy)} a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0 a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0')
    return ' '.join(partes)


def deslocar(segs, amp):
    (p0, p1, p2, p3), (q0, q1, q2, q3), *resto = segs
    return [
        (p0, (p1[0], p1[1] + amp), (p2[0], p2[1] - amp * 0.7), (p3[0], p3[1] + amp * 0.35)),
        ((q0[0], q0[1] + amp * 0.35), (q1[0], q1[1] + amp * 0.15), q2, q3),
        *resto,
    ]


def animar_tentaculo(valores, dur, atraso='0s'):
    return (
        f'<animate attributeName="d" dur="{dur}" begin="{atraso}" repeatCount="indefinite" calcMode="spline" '
        f'keyTimes="0;0.25;0.5;0.75;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1;0.45 0 0.55 1" '
        f'values="{";".join(valores)}" />'
    )


TENTACULOS = [([((236, 132), (222, 60), (150, 6), (86, 26)), ((86, 26), (52, 36), (34, 42), (24, 56)), ((24, 56), (14, 68), (20, 82), (32, 76))], 24, 1.2, 9), ([((234, 150), (180, 172), (150, 96), (100, 104)), ((100, 104), (64, 110), (40, 118), (26, 132)), ((26, 132), (16, 142), (22, 156), (34, 150))], 23, 1.2, 11), ([((238, 170), (216, 236), (140, 222), (96, 198)), ((96, 198), (66, 184), (42, 190), (28, 204)), ((28, 204), (18, 214), (24, 228), (36, 222))], 21, 1.2, 10), ([((244, 188), (230, 262), (150, 278), (100, 262)), ((100, 262), (70, 252), (48, 254), (34, 266)), ((34, 266), (24, 274), (28, 288), (40, 282))], 17, 1.1, 12), ([((240, 142), (196, 120), (176, 160), (150, 168)), ((150, 168), (128, 175), (118, 156), (132, 150)), ((132, 150), (142, 146), (146, 158), (138, 160))], 11, 1, 9)]


# ============================================================ herói


H = 34.0

AZUL, AZUL_S, AZUL_LUZ = '#2357e0', '#12318a', '#86a8ff'
AZUL_L, AZUL_LS = '#1a44b8', '#0d2468'
VERM, VERM_S, VERM_LUZ = '#e5202e', '#8f0b16', '#ff8089'
VERM_L, VERM_LS = '#b9141f', '#6e0710'
PELE, PELE_S = '#f2c4a0', '#c4865b'
AMARELO, AMARELO_S = '#ffd21f', '#c99400'
CABELO, CABELO_LUZ = '#1b1530', '#5a4a8f'


# --------------------------------------------------------------- vetores
def rot(v, graus):
    r = math.radians(graus)
    return (v[0] * math.cos(r) - v[1] * math.sin(r), v[0] * math.sin(r) + v[1] * math.cos(r))


def mais(p, v, s=1.0):
    return (p[0] + v[0] * s, p[1] + v[1] * s)


def entre(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# eixo do corpo: da cintura para a cabeça, inclinado 33 graus acima da horizontal
EIXO = rot((1, 0), -33)
FRENTE = rot(EIXO, 90)  # lado do peito (para baixo e para a direita)


def anim_d(valores, dur):
    return (
        f'<animate attributeName="d" dur="{dur}" repeatCount="indefinite" calcMode="spline" '
        f'keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" values="{";".join(valores)}" />'
    )


def mao(punho, cor, sombra, luz):
    """Mão enluvada espalmada no cartão: a base sai do punho e os dedos apontam para cima."""
    larg, alt = 0.66 * H, 1.0 * H
    x0, y1 = punho[0] - 3, punho[1] + 0.22 * H
    y0 = y1 - alt
    x1 = x0 + larg
    dedo = larg / 4
    topo = []
    for k in range(4):
        cx = x0 + dedo * (k + 0.5)
        alto = y0 + (3, 0, 1, 4)[k]
        topo += [(cx - dedo * 0.45, alto + 3.5), (cx, alto), (cx + dedo * 0.45, alto + 3.5)]
    contorno = topo + [(x1 + 0.5, y0 + alt * 0.4), (x1 + 0.5, y1 - 5), (x1 - 3, y1), (x0 + 3, y1), (x0, y1 - 5), (x0, y0 + alt * 0.45)]
    polegar = [(x0 + 1, y0 + alt * 0.72), (x0 - 6, y0 + alt * 0.52), (x0 - 8, y0 + alt * 0.36), (x0 - 4, y0 + alt * 0.32), (x0 + 1, y0 + alt * 0.48)]
    sombra_pts = [(x0 + larg * 0.55, y0 + alt * 0.4), (x1 + 0.5, y0 + alt * 0.4), (x1 + 0.5, y1 - 5), (x1 - 3, y1), (x0 + larg * 0.5, y1)]
    vincos = ''.join(
        f'<path d="M{f(x0 + dedo * k)} {f(y0 + 5)} L{f(x0 + dedo * k)} {f(y0 + alt * 0.36)}" stroke="{TINTA}" stroke-width="1.3" stroke-linecap="round" />'
        for k in (1, 2, 3)
    )
    return (
        forma(polegar, cor, largura=2)
        + forma(contorno, cor, largura=2)
        + forma(sombra_pts, sombra, contorno=False)
        + vincos
        + linha([(x0 + 2, y0 + 6), (x0 + 1.5, y0 + alt * 0.4)], luz, 1.5, 0.9)
        + f'<path d="{catmull(contorno)}" fill="none" stroke="{TINTA}" stroke-width="2" stroke-linejoin="round" />'
    )


def cabeca_svg(centro):
    """Cabeça de perfil olhando para a direita, levemente erguida. Medidas em H."""
    inclina = -8

    def p(x, y):
        v = rot((x * H * 1.08, y * H * 1.08), inclina)
        return (centro[0] + v[0], centro[1] + v[1])

    partes = []
    pele = [p(-0.42, -0.05), p(-0.32, -0.38), p(-0.05, -0.5), p(0.25, -0.44), p(0.4, -0.2), p(0.43, -0.05),
            p(0.53, 0.06), p(0.43, 0.12), p(0.45, 0.2), p(0.42, 0.26), p(0.41, 0.4), p(0.22, 0.48), p(0.0, 0.44), p(-0.18, 0.28)]
    partes.append(forma(pele, PELE))
    partes.append(forma([p(0.41, 0.4), p(0.22, 0.48), p(0.0, 0.44), p(-0.1, 0.32), p(0.18, 0.36), p(0.36, 0.33)], PELE_S, contorno=False))
    partes.append(f'<path d="{catmull(pele)}" fill="none" stroke="{TINTA}" stroke-width="2.1" stroke-linejoin="round" />')
    # orelha
    a, b, c = p(-0.08, -0.02), p(-0.2, 0.06), p(-0.09, 0.18)
    partes.append(f'<path d="M{f(a[0])} {f(a[1])} Q{f(b[0])} {f(b[1])} {f(c[0])} {f(c[1])}" fill="none" stroke="{TINTA}" stroke-width="1.8" stroke-linecap="round" />')
    # cabelo penteado para trás, com duas mechas soltas pelo vento
    cabelo = [p(-0.46, 0.12), p(-0.52, -0.22), p(-0.32, -0.52), p(0.0, -0.62), p(0.3, -0.52), p(0.28, -0.4),
              p(0.06, -0.42), p(-0.16, -0.3), p(-0.26, -0.08), p(-0.3, 0.12)]
    partes.append(forma(cabelo, CABELO, largura=2))
    partes.append(forma([p(-0.42, -0.36), p(-0.9, -0.46), p(-0.5, -0.16)], CABELO, largura=1.8))
    partes.append(forma([p(-0.48, -0.1), p(-0.92, -0.06), p(-0.46, 0.06)], CABELO, largura=1.8))
    partes.append(linha([p(-0.2, -0.46), p(0.1, -0.54)], CABELO_LUZ, 1.8, 0.9))
    # máscara e olho
    mascara = [p(-0.02, -0.22), p(0.2, -0.2), p(0.45, -0.24), p(0.45, -0.07), p(0.2, -0.06), p(0.0, -0.06)]
    partes.append(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in mascara)} Z" fill="{TINTA}" />')
    olho = [p(0.22, -0.16), p(0.39, -0.18), p(0.38, -0.11), p(0.23, -0.1)]
    partes.append(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in olho)} Z" fill="#ffffff" />')
    # boca firme
    m1, m2 = p(0.3, 0.27), p(0.42, 0.25)
    partes.append(f'<path d="M{f(m1[0])} {f(m1[1])} L{f(m2[0])} {f(m2[1])}" stroke="{TINTA}" stroke-width="1.8" stroke-linecap="round" />')
    return '\n  '.join(partes)


def heroi():
    p = []
    ombro = (290, 118)
    quadril = mais(ombro, EIXO, -2.4 * H)
    meio = entre(quadril, ombro, 0.55)

    # --- pernas: quase na linha do corpo, a da frente levemente dobrada
    q_t = mais(quadril, FRENTE, -6)
    joelho_t = mais(q_t, rot(EIXO, -3), -1.85 * H)
    tornozelo_t = mais(joelho_t, rot(EIXO, 3), -1.75 * H)
    ponta_t = mais(tornozelo_t, rot(EIXO, 12), -0.95 * H)
    q_f = mais(quadril, FRENTE, 7)
    joelho_f = mais(q_f, rot(EIXO, 9), -1.85 * H)
    tornozelo_f = mais(joelho_f, rot(EIXO, -12), -1.75 * H)
    ponta_f = mais(tornozelo_f, rot(EIXO, -4), -0.95 * H)

    # --- braços: os dois esticados para a frente, até a borda do cartão
    o_t = mais(ombro, FRENTE, -12)
    cotovelo_t = mais(o_t, rot((1, 0), -6), 1.5 * H)
    punho_t = mais(cotovelo_t, rot((1, 0), -2), 1.25 * H)
    o_f = mais(ombro, FRENTE, 11)
    cotovelo_f = mais(o_f, rot((1, 0), 4), 1.5 * H)
    punho_f = mais(cotovelo_f, rot((1, 0), 0), 1.25 * H)

    # --- cabeça e pescoço
    base_pescoco = mais(mais(ombro, EIXO, 0.25 * H), FRENTE, -3)
    centro_cabeca = mais(mais(base_pescoco, EIXO, 0.8 * H), FRENTE, -3)

    # rastro de velocidade
    cunhas = []
    for (x, y, comp, esp) in [(110, 120, 150, 4), (80, 152, 170, 5), (60, 200, 130, 4), (40, 232, 150, 3)]:
        cunhas.append(f'<path d="M{x} {y - esp / 2} L{x - comp} {y} L{x} {y + esp / 2} Z" fill="{TINTA}" />')
    p.append(f'<g opacity="0.45">{"".join(cunhas)}<animateTransform attributeName="transform" type="translate" values="14 0;-20 0" dur="0.3s" repeatCount="indefinite" /></g>')

    # --- capa: uma faixa longa e curva, presa nos ombros, como nas referências
    preso = mais(ombro, FRENTE, -18)
    def capa_pts(onda):
        x, y = preso
        return [
            (x + 6, y - 4), (x - 50, y - 16 - onda * 0.3), (x - 110, y - 22 - onda), (x - 170, y - 22 - onda * 0.8),
            (x - 222, y - 18 - onda * 1.3), (x - 252, y - 12 - onda * 1.5), (x - 226, y - 2 - onda * 0.9),
            (x - 176, y + 10 + onda * 0.1), (x - 116, y + 24 + onda * 0.3), (x - 60, y + 38), (x - 22, y + 36), (x + 2, y + 18),
        ]
    ca, cb = catmull(capa_pts(0)), catmull(capa_pts(16))
    def sombra_capa(onda):
        x, y = preso
        return [(x - 226, y - 2 - onda * 0.9), (x - 176, y + 10 + onda * 0.1), (x - 116, y + 24 + onda * 0.3), (x - 60, y + 38),
                (x - 22, y + 36), (x - 44, y + 22), (x - 104, y + 10 + onda * 0.2), (x - 180, y - 4 - onda * 0.4)]
    sa, sb = catmull(sombra_capa(0)), catmull(sombra_capa(16))
    def dobra(onda):
        x, y = preso
        return [(x - 10, y + 4), (x - 76, y - 4 - onda * 0.5), (x - 150, y - 8 - onda * 0.8), (x - 214, y - 10 - onda * 1.2)]
    da, db = catmull(dobra(0), False), catmull(dobra(16), False)
    p.append(f'<path d="{ca}" fill="{VERM}" stroke="{TINTA}" stroke-width="2.3" stroke-linejoin="round">{anim_d([ca, cb, ca], "0.9s")}</path>')
    p.append(f'<path d="{sa}" fill="{VERM_S}">{anim_d([sa, sb, sa], "0.9s")}</path>')
    p.append(f'<path d="{da}" fill="none" stroke="{VERM_S}" stroke-width="2.6" stroke-linecap="round">{anim_d([da, db, da], "0.9s")}</path>')
    p.append(f'<path d="{ca}" fill="none" stroke="{TINTA}" stroke-width="2.3" stroke-linejoin="round">{anim_d([ca, cb, ca], "0.9s")}</path>')

    # --- perna de trás
    p.append(membro_svg(Membro([q_t, joelho_t, tornozelo_t], [(0, 38), (0.28, 36), (0.5, 23), (0.64, 26), (1, 15)]), AZUL_L, AZUL_LS))
    bota_t = Membro([entre(joelho_t, tornozelo_t, 0.5), tornozelo_t, ponta_t], [(0, 25), (0.45, 16), (0.6, 16), (1, 7)])
    p.append(membro_svg(bota_t, VERM_L, VERM_LS))

    # --- braço de trás e luva
    p.append(membro_svg(Membro([o_t, cotovelo_t, punho_t], [(0, 27), (0.25, 28), (0.5, 19), (0.62, 21), (1, 15)]), AZUL_L, AZUL_LS))
    p.append(membro_svg(Membro([entre(cotovelo_t, punho_t, 0.45), punho_t], [(0, 24), (1, 17)], ponta_redonda=False), VERM_L, VERM_LS))
    p.append(mao(punho_t, VERM_L, VERM_LS, VERM_LUZ))

    # --- tronco: peito largo em cima, cintura fina
    tronco = Membro([quadril, meio, ombro], [(0, 42), (0.33, 38), (0.66, 62), (0.88, 62), (1, 54)], amostras=10)
    p.append(membro_svg(tronco, AZUL, AZUL_S, AZUL_LUZ, fracao=0.4))
    # peitoral
    pe1, pe2 = mais(mais(ombro, EIXO, -0.5 * H), FRENTE, 4), mais(mais(ombro, EIXO, -0.9 * H), FRENTE, 18)
    p.append(linha([mais(ombro, FRENTE, 6), pe1, pe2], TINTA, 1.6, 0.85))
    # cinto
    c1, c2 = mais(quadril, EIXO, 0.2 * H), mais(quadril, EIXO, 0.5 * H)
    cinto = [mais(c1, FRENTE, -20), mais(c2, FRENTE, -19), mais(c2, FRENTE, 19), mais(c1, FRENTE, 20)]
    p.append(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in cinto)} Z" fill="{AMARELO}" stroke="{TINTA}" stroke-width="2" stroke-linejoin="round" />')

    # --- perna da frente
    p.append(membro_svg(Membro([q_f, joelho_f, tornozelo_f], [(0, 39), (0.28, 37), (0.5, 23), (0.64, 27), (1, 15)]), AZUL, AZUL_S, AZUL_LUZ))
    bota_f = Membro([entre(joelho_f, tornozelo_f, 0.5), tornozelo_f, ponta_f], [(0, 26), (0.45, 16), (0.6, 16), (1, 7)])
    p.append(membro_svg(bota_f, VERM, VERM_S, VERM_LUZ))

    # --- emblema no peito
    em = mais(mais(ombro, EIXO, -0.75 * H), FRENTE, 12)
    p.append(f'<circle cx="{f(em[0])}" cy="{f(em[1])}" r="{f(0.36 * H)}" fill="{AMARELO}" stroke="{TINTA}" stroke-width="2" />')
    r = 0.36 * H
    raio = [(0.15, -0.8), (-0.4, 0.1), (0.0, 0.1), (-0.2, 0.75), (0.4, -0.15), (0.02, -0.15)]
    p.append(f'<path d="M{" L".join(f"{f(em[0] + x * r)} {f(em[1] + y * r)}" for x, y in raio)} Z" fill="{TINTA}" />')

    # --- pescoço e cabeça
    p.append(membro_svg(Membro([base_pescoco, mais(centro_cabeca, EIXO, -0.2 * H)], [(0, 24), (1, 20)]), PELE, PELE_S))
    p.append(cabeca_svg(centro_cabeca))

    # --- ombro (deltoide) e braço da frente por cima de tudo
    p.append(membro_svg(Membro([mais(o_f, (-1, 0), 4), mais(o_f, (1, 0), 10)], [(0, 38), (1, 31)]), AZUL, AZUL_S, AZUL_LUZ))
    p.append(membro_svg(Membro([o_f, cotovelo_f, punho_f], [(0, 28), (0.25, 29), (0.5, 20), (0.62, 22), (1, 16)]), AZUL, AZUL_S, AZUL_LUZ))
    p.append(membro_svg(Membro([entre(cotovelo_f, punho_f, 0.45), punho_f], [(0, 25), (1, 18)], ponta_redonda=False), VERM, VERM_S, VERM_LUZ))
    p.append(mao(punho_f, VERM, VERM_S, VERM_LUZ))

    # onda de choque das palmas no cartão
    xm = max(punho_t[0], punho_f[0]) + 0.66 * H + 4
    ondas = ''.join(
        f'<path d="M{f(xm + k * 7)} {f(punho_t[1] - 34 - k * 5)} Q{f(xm + 12 + k * 8)} {f((punho_t[1] + punho_f[1]) / 2 - 6)} {f(xm + k * 7)} {f(punho_f[1] + 14 + k * 5)}" fill="none" stroke="{TINTA}" stroke-width="{2.4 - k * 0.6}" stroke-linecap="round" />'
        for k in range(3)
    )
    p.append(f'<g opacity="0.7">{ondas}<animate attributeName="opacity" values="0.15;0.8;0.15" dur="0.5s" repeatCount="indefinite" /></g>')

    corpo = '\n  '.join(p)
    return f'''<svg class="personagem personagem--heroi" viewBox="0 0 420 300" width="420" height="300" aria-hidden="true" focusable="false">
  {corpo}
</svg>''', (punho_t, punho_f)


# ============================================================ vilão


PRETO, PRETO_LUZ = '#07050f', '#191433'
BORDA = '#000000'
INDIGO = '#7b6cf0'
CARMIM, CARMIM_ESC = '#e01e37', '#8f0b20'
OURO = '#c9992f'
FUNDO_DOBRA = '#020106'


def f_forma(pontos, cor, borda=True, largura=1.8):
    traco = f' stroke="{BORDA}" stroke-width="{largura}" stroke-linejoin="round"' if borda else ''
    return f'<path d="{catmull(pontos)}" fill="{cor}"{traco} />'


def anim(valores, dur, atraso='0s'):
    return (
        f'<animate attributeName="d" dur="{dur}" begin="{atraso}" repeatCount="indefinite" calcMode="spline" '
        f'keyTimes="0;0.5;1" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" values="{";".join(valores)}" />'
    )


def garra():
    """Mão em garra no tamanho de uma mão de verdade: palma e quatro dedos longos que afinam
    até a ponta, apontando para o cartão. (Escalada em volta do punho.)"""
    centro, escala = (210, 92), 0.55

    def e(pt):
        return (centro[0] + (pt[0] - centro[0]) * escala, centro[1] + (pt[1] - centro[1]) * escala)

    partes = []
    palma = [e(q) for q in [(212, 86), (200, 78), (190, 84), (186, 96), (194, 106), (208, 104)]]
    dedos = [
        [(198, 80), (182, 66), (166, 58), (152, 58)],
        [(192, 86), (172, 80), (152, 80), (136, 84)],
        [(190, 94), (172, 98), (154, 106), (142, 116)],
        [(194, 102), (182, 114), (172, 126), (166, 138)],
    ]
    for pts, w in zip(dedos, [6.5, 7, 6.5, 6]):
        m = Membro([e(q) for q in pts], [(0, w), (0.55, w * 0.8), (1, 1)], amostras=6, ponta_redonda=False)
        partes.append(f_forma(m.contorno(), PRETO, largura=1.5))
        partes.append(linha(m.luz(0.1, 0.75, 1.2), INDIGO, 1.1, 0.85))
    partes.append(f_forma(palma, PRETO, largura=1.5))
    c = e((196, 92))
    partes.append(
        f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="4" fill="{CARMIM}" filter="url(#v-brilho)" opacity="0.9">'
        '<animate attributeName="r" values="3.5;5.5;3.5" dur="1.4s" repeatCount="indefinite" /></circle>'
    )
    return (chr(10) + '  ').join(partes)


OLHOS = '<g filter="url(#v-brilho)" fill="#ff2a44"><path d="M270 62 C274 59 280 58 283 60 L281 66 C277 66 273 65 270 62 Z" /><path d="M300 62 C296 59 290 58 287 60 L289 66 C293 66 297 65 300 62 Z" /><animate attributeName="opacity" values="1;0.6;1;1;0.15;1" keyTimes="0;0.2;0.4;0.86;0.9;1" dur="3.6s" repeatCount="indefinite" /></g>'


NUCLEO_OLHOS = '<g fill="#ffd3da"><path d="M274 62.2 C277 60.6 280 60.4 281.6 61.4 L280.8 63.8 C278.4 63.8 276 63.4 274 62.2 Z" /><path d="M296 62.2 C293 60.6 290 60.4 288.4 61.4 L289.2 63.8 C291.6 63.8 294 63.4 296 62.2 Z" /><animate attributeName="opacity" values="1;0.6;1;1;0.15;1" keyTimes="0;0.2;0.4;0.86;0.9;1" dur="3.6s" repeatCount="indefinite" /></g>'


def tentaculos_svg():
    saida = []
    for i, (segs, w0, w1, amp) in enumerate(TENTACULOS):
        var = [segs, deslocar(segs, amp), segs, deslocar(segs, -amp * 0.75), segs]
        pts = [amostrar(v, 10) for v in var]
        corpo = [afinado(p, w0, w1, 0.9, ponta_redonda=False) for p in pts]
        luz = [paralela(p, w0 * 0.3, 0.04, 0.86) for p in pts]
        brasa = [paralela(p, -w0 * 0.33, 0.02, 0.6) for p in pts]
        suc = [ventosas(p, w0, w1, 6, 0.16, 0.66) for p in pts]
        dur, atr = f'{1.8 + i * 0.27:.2f}s', f'{-i * 0.37:.2f}s'
        saida.append(
            '    <g class="tentaculo">\n'
            f'      <path d="{corpo[0]}" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.4" stroke-linejoin="round">{animar_tentaculo(corpo, dur, atr)}</path>\n'
            f'      <path d="{suc[0]}" fill="#2b2560" opacity="0.85">{animar_tentaculo(suc, dur, atr)}</path>\n'
            f'      <path d="{brasa[0]}" fill="none" stroke="{CARMIM}" stroke-width="1.8" stroke-linecap="round" opacity="0.75">{animar_tentaculo(brasa, dur, atr)}</path>\n'
            f'      <path d="{luz[0]}" fill="none" stroke="{INDIGO}" stroke-width="1.6" stroke-linecap="round" opacity="0.9">{animar_tentaculo(luz, dur, atr)}</path>\n'
            '    </g>'
        )
    return '\n'.join(saida)


def fumaca():
    """Fiapos de fumaça subindo da barra e sumindo."""
    fiapos = []
    for i, (cx, r, cor, dur) in enumerate([(236, 10, '#4a3fa0', 3.0), (268, 13, '#2b2560', 3.6), (300, 9, '#e01e37', 2.8), (322, 11, '#4a3fa0', 3.3)]):
        fiapos.append(
            f'<ellipse cx="{cx}" cy="292" rx="{r}" ry="{r * 0.7:.1f}" fill="{cor}">'
            f'<animate attributeName="cy" values="296;246" dur="{dur}s" begin="{-i * 0.9:.1f}s" repeatCount="indefinite" />'
            f'<animate attributeName="opacity" values="0.7;0" dur="{dur}s" begin="{-i * 0.9:.1f}s" repeatCount="indefinite" />'
            f'<animate attributeName="rx" values="{r};{r * 2.2:.1f}" dur="{dur}s" begin="{-i * 0.9:.1f}s" repeatCount="indefinite" />'
            '</ellipse>'
        )
    return f'<g filter="url(#v-fumaca)" opacity="0.8">{"".join(fiapos)}</g>'


def vilao():
    p = []
    # tentáculos nascem de uma massa sob o sobretudo
    p.append(f_forma([(226, 120), (216, 154), (220, 190), (236, 212), (254, 202), (258, 160), (246, 122)], PRETO))
    p.append(f'<g class="tentaculos">\n{tentaculos_svg()}\n  </g>')

    # abas de trás do sobretudo, esvoaçando para o lado do cartão
    aba_a = [(238, 130), (222, 178), (204, 222), (178, 258), (196, 256), (186, 276), (214, 266), (230, 250)]
    aba_b = [(238, 130), (218, 180), (194, 222), (162, 252), (182, 254), (170, 270), (208, 266), (230, 250)]
    a, b = catmull(aba_a), catmull(aba_b)
    p.append(f'<path d="{a}" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.8" stroke-linejoin="round">{anim([a, b, a], "1.1s")}</path>')
    ra, rb = catmull(aba_a[:5], False), catmull(aba_b[:5], False)
    p.append(f'<path d="{ra}" fill="none" stroke="{CARMIM}" stroke-width="1.8" opacity="0.7">{anim([ra, rb, ra], "1.1s")}</path>')

    # sobretudo: laterais curvas, barra rasgada em pontas
    # O eixo do corpo passa por x=285 (centro da cabeça): ombros, lapelas e botões são simétricos a ele.
    esquerda = [(285, 94), (262, 96), (248, 102), (241, 116), (238, 144), (232, 196), (222, 250), (212, 280)]
    barra = [(228, 266), (238, 292), (252, 270), (264, 296), (278, 272), (292, 300), (306, 276), (320, 294), (331, 270)]
    direita = [(331, 270), (327, 210), (325, 150), (326, 118), (322, 104), (308, 96), (285, 94)]
    d_casaco = catmull(esquerda, False) + ' L' + ' L'.join(f'{x} {y}' for x, y in barra) + ' L' + catmull(direita, False)[1:] + ' Z'
    p.append(f'<path d="{d_casaco}" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.8" stroke-linejoin="round" />')
    # plano iluminado pela luz fria: o painel de cima do peito, entre o ombro e a abertura
    p.append(f_forma([(252, 110), (246, 146), (244, 196), (262, 194), (268, 150), (270, 128)], PRETO_LUZ, borda=False))
    # abertura do sobretudo: desce do V das lapelas, passa pelo cinto e chega à barra
    p.append(f'<path d="M271 130 C272 150 273 168 274 184 C276 214 277 244 278 272" fill="none" stroke="{FUNDO_DOBRA}" stroke-width="4" stroke-linecap="round" />')
    p.append(f'<path d="M274 132 C275 152 276 168 277 186 C279 216 280 244 281 268" fill="none" stroke="#2b2560" stroke-width="1.4" stroke-linecap="round" />')
    # dobras: sombra funda em cunha descendo até as pontas da barra, com filete de luz ao lado
    for (x_topo, y_topo), (x_pe, y_pe) in [((254, 198), (252, 270)), ((302, 196), (306, 276))]:
        p.append(f'<path d="M{x_topo} {y_topo} L{x_pe - 5} {y_pe} L{x_pe + 5} {y_pe} Z" fill="{FUNDO_DOBRA}" />')
        p.append(f'<path d="M{x_topo + 2} {y_topo + 6} L{x_pe + 7} {y_pe - 2}" stroke="#2b2560" stroke-width="1.6" stroke-linecap="round" />')
    # lapelas em V, uma de cada lado do eixo, encontrando-se no primeiro botão
    p.append(f'<path d="M276 96 L262 100 L256 108 L285 134 Z" fill="{PRETO_LUZ}" stroke="{BORDA}" stroke-width="1.4" stroke-linejoin="round" />')
    p.append(f'<path d="M294 96 L308 100 L314 108 L285 134 Z" fill="{PRETO_LUZ}" stroke="{BORDA}" stroke-width="1.4" stroke-linejoin="round" />')
    p.append(f'<path d="M310 104 L288 130" stroke="{INDIGO}" stroke-width="1.6" stroke-linecap="round" />')
    p.append(f'<path d="M262 104 L282 128" stroke="#2b2560" stroke-width="1.4" stroke-linecap="round" />')
    # recortes de luz: índigo na borda direita, brasa carmim embaixo à esquerda
    p.append(linha([(326, 186), (328, 226), (329, 262)], INDIGO, 2.2, 0.95))
    p.append(linha([(232, 200), (224, 246), (215, 274)], CARMIM, 2.4, 0.85))
    p.append(linha([(242, 140), (236, 190), (228, 246)], CARMIM_ESC, 3))
    # cinto com fivela no eixo e duas fileiras de botões, simétricas ao eixo
    p.append(f'<path d="M232 168 C262 172 296 171 326 166 L327 179 C296 184 262 186 231 182 Z" fill="#0d0a1c" stroke="{BORDA}" stroke-width="1.6" />')
    p.append(f'<rect x="278" y="169.5" width="14" height="14" rx="1.5" fill="none" stroke="{OURO}" stroke-width="2.6" />')
    p.append(f'<path d="M281 172.5 L289 180.5" stroke="{OURO}" stroke-width="1.2" opacity="0.6" />')
    for y in (142, 158):
        p.append(f'<circle cx="276" cy="{y}" r="2.6" fill="{OURO}" /><circle cx="294" cy="{y}" r="2.6" fill="{OURO}" />')

    # braço de trás, caído junto ao corpo: dá largura ao ombro direito
    caido = Membro([(318, 106), (326, 136), (328, 166)], [(0, 22), (1, 18)], amostras=8)
    p.append(f_forma(caido.contorno(), PRETO))
    p.append(linha([(330, 110), (336, 136), (337, 162)], INDIGO, 2, 0.9))
    p.append(f_forma([(320, 166), (336, 166), (335, 178), (322, 178)], '#0d0a1c'))
    p.append(linha([(320, 167), (336, 167)], CARMIM, 1.4, 0.6))

    # braço erguido: nasce no ombro esquerdo (não no peito) e vai até a garra
    p.append(f_forma([(240, 104), (254, 98), (262, 106), (256, 122), (242, 124)], PRETO))
    manga = Membro([(250, 112), (232, 104), (210, 94)], [(0, 26), (0.5, 23), (1, 21)], amostras=8)
    p.append(f_forma(manga.contorno(), PRETO))
    p.append(linha(manga.luz(0.05, 0.9, 2.2), INDIGO, 2, 0.9))
    p.append(linha([(246, 124), (228, 114), (214, 104)], CARMIM, 1.6, 0.6))
    p.append(f_forma([(216, 84), (222, 100), (210, 103), (206, 88)], CARMIM_ESC))
    p.append(garra())

    # gola alta em lâminas
    p.append(f'<path d="M258 104 C250 92 244 82 242 72 C244 58 248 48 252 38 C258 52 266 66 276 94 Z" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.8" stroke-linejoin="round" />')
    p.append(f'<path d="M312 104 C320 92 326 82 328 72 C326 58 322 48 318 38 C312 52 304 66 294 94 Z" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.8" stroke-linejoin="round" />')
    p.append(f'<path d="M313 101 C320 90 326 80 327 72 C325 58 321 48 318 40" fill="none" stroke="{INDIGO}" stroke-width="2" stroke-linecap="round" />')
    p.append(f'<path d="M256 100 C250 90 246 82 244 72" fill="none" stroke="{CARMIM}" stroke-width="1.6" stroke-linecap="round" opacity="0.7" />')
    # rosto: escuridão; olhos com halo vermelho e núcleo quente
    p.append('<ellipse cx="285" cy="66" rx="22" ry="15" fill="#000" />')
    p.append(OLHOS)
    p.append(NUCLEO_OLHOS)

    # chapéu de feltro
    p.append('<g transform="rotate(-8 285 48)">')
    p.append(f'<path d="M258 50 C256 32 260 18 272 14 C280 12 290 12 298 14 C310 18 314 32 312 50 Z" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.8" stroke-linejoin="round" />')
    p.append('<path d="M258 42 C276 46 296 46 312 41 L312 50 C296 53 276 53 258 50 Z" fill="#b3122b" />')
    p.append('<path d="M262 44.5 C278 47.5 296 47.5 310 43.5" fill="none" stroke="#ff5a6e" stroke-width="1" opacity="0.7" />')
    p.append('<path d="M270 18 C278 22 290 22 300 18" fill="none" stroke="#2b2560" stroke-width="2" stroke-linecap="round" />')
    p.append(f'<path d="M222 58 C238 46 268 42 286 42 C306 42 334 45 348 55 C332 62 306 61 286 61 C264 61 238 62 222 58 Z" fill="{PRETO}" stroke="{BORDA}" stroke-width="1.8" stroke-linejoin="round" />')
    p.append(linha([(246, 47), (286, 44), (326, 47), (342, 53)], INDIGO, 2, 0.95))
    p.append(f'<path d="M228 59.5 C252 62.5 304 62.5 342 57" fill="none" stroke="{CARMIM}" stroke-width="1.6" stroke-linecap="round" opacity="0.7" />')
    p.append(f'<path d="M304 14 C312 20 314 32 312 48" fill="none" stroke="{INDIGO}" stroke-width="1.8" stroke-linecap="round" />')
    p.append('</g>')

    corpo = '\n  '.join(p)
    return f'''<svg class="personagem personagem--vilao" viewBox="0 0 350 310" width="350" height="310" aria-hidden="true" focusable="false">
  <defs>
    <radialGradient id="v-aura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#e01e37" stop-opacity="0.5" />
      <stop offset="60%" stop-color="#e01e37" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#e01e37" stop-opacity="0" />
    </radialGradient>
    <filter id="v-brilho" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="2.4" result="b" />
      <feMerge><feMergeNode in="b" /><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <filter id="v-fumaca" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6" /></filter>
  </defs>
  <ellipse cx="270" cy="170" rx="96" ry="136" fill="url(#v-aura)" />
  {fumaca()}
  {corpo}
</svg>'''


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    for nome, svg in (('heroi.svg', heroi()[0]), ('vilao.svg', vilao())):
        with open(os.path.join(SAIDA, nome), 'w', encoding='utf-8', newline=chr(10)) as arq:
            arq.write(svg)
        print(f'{nome}: {len(svg)} caracteres')
