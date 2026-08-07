# ============================================================
#  Baixa o FFmpeg durante o deploy do Vercel e copia os
#  binários para a pasta do projeto (vão junto no deploy)
# ============================================================
import os
import shutil

import static_ffmpeg

print("⬇️  Baixando FFmpeg/FFprobe...")
static_ffmpeg.add_paths(verbose=True)

destino = 'static-ffmpeg-cache'
os.makedirs(destino, exist_ok=True)

candidatos = [
    os.path.expanduser('~/.cache/static-ffmpeg'),
    os.path.expanduser('~/.static_ffmpeg'),
    '/tmp/static-ffmpeg',
]

encontrado = False
for base in candidatos:
    if not os.path.exists(base):
        continue
    for dirpath, dirnames, filenames in os.walk(base):
        if 'ffmpeg' in filenames and 'ffprobe' in filenames:
            for nome in ('ffmpeg', 'ffprobe'):
                origem = os.path.join(dirpath, nome)
                shutil.copy(origem, os.path.join(destino, nome))
                os.chmod(os.path.join(destino, nome), 0o755)
            print(f'✅ FFmpeg copiado de {dirpath} para ./{destino}')
            encontrado = True
            break
    if encontrado:
        break

if not encontrado:
    print('⚠️  Não encontrei os binários do FFmpeg — as conversões vão falhar.')
