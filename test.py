from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt

olaylar = sb.events(match_id=3943043)
sutlar = olaylar[olaylar['type'] == 'Shot'].copy()

pitch = Pitch(pitch_color='#1a1a2e', line_color='white')
fig, ax = pitch.draw(figsize=(14, 9))
fig.set_facecolor('#1a1a2e')

for _, sut in sutlar.iterrows():
    x = sut['location'][0]
    y = sut['location'][1]
    xg = sut['shot_statsbomb_xg']
    sonuc = sut['shot_outcome']
    takim = sut['team']
    oyuncu = sut['player'].split()[-1]  # Sadece soyisim

    # Takıma göre renk
    if takim == 'Spain':
        renk = '#FF0000'  # Kırmızı - İspanya
    else:
        renk = '#FFFFFF'  # Beyaz - İngiltere

    # Gol ise yıldız, değilse daire
    marker = '*' if sonuc == 'Goal' else 'o'
    boyut = xg * 2000 if sonuc == 'Goal' else xg * 800

    pitch.scatter(x, y, ax=ax, s=boyut, color=renk, 
                  alpha=0.9, marker=marker, edgecolors='yellow' if sonuc == 'Goal' else 'gray', linewidth=1.5)

    # Gol ise isim yaz
    if sonuc == 'Goal':
        ax.text(x, y + 3, oyuncu, color='yellow', fontsize=9, 
                ha='center', fontweight='bold')

plt.title('Euro 2024 Finali — Shot Map\n🔴 İspanya  ⚪ İngiltere  ⭐ Gol', 
          color='white', fontsize=14, pad=15)

plt.savefig('shotmap_v2.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
ispanya_xg = sutlar[sutlar['team'] == 'Spain']['shot_statsbomb_xg'].sum()
ingiltere_xg = sutlar[sutlar['team'] == 'England']['shot_statsbomb_xg'].sum()

fig.text(0.5, 0.02, 
         f'İspanya xG: {ispanya_xg:.2f}    |    İngiltere xG: {ingiltere_xg:.2f}',
         color='white', fontsize=12, ha='center',
         bbox=dict(boxstyle='round', facecolor='#2d2d4e', alpha=0.8))
plt.show()
