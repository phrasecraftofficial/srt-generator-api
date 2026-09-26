import spaces  # <--- IMPORTANTE: Deve ser o primeiro import
import os
import torch
import gradio as gr
from transformers import pipeline
from moviepy.editor import VideoFileClip
import yt_dlp

# Configura o modelo Whisper do Hugging Face
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Carregando modelo Whisper no dispositivo: {device}")
transcriber = pipeline(
    "automatic-speech-recognition", 
    model="openai/whisper-small", 
    device=device
)

# O decorador @spaces.GPU aloca a placa de vídeo sob demanda para esta função
@spaces.GPU
def processar_video_por_url(url_video):
    if not url_video:
        return "Por favor, envie uma URL válida."
    
    video_path = "video_baixado.mp4"
    audio_path = "audio_extraido.mp3"
    
    try:
        print(f"Baixando vídeo da URL: {url_video}")
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': video_path,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_video])
            
        print("Extraindo MP3...")
        video_clip = VideoFileClip(video_path)
        if video_clip.audio is None:
            return "Erro: O vídeo não possui faixa de áudio."
        
        video_clip.audio.write_audiofile(audio_path, logger=None)
        video_clip.close()
        
        print("Gerando legenda com IA...")
        resultado = transcriber(
            audio_path, 
            return_timestamps=True, 
            generate_kwargs={"language": "portuguese"}
        )
        
        texto_legenda = resultado["text"]
        
        # Limpa os arquivos temporários após o uso
        for p in [video_path, audio_path]:
            if os.path.exists(p):
                os.remove(p)
                
        return texto_legenda

    except Exception as e:
        # Garante a limpeza em caso de erro
        for p in [video_path, audio_path]:
            if os.path.exists(p):
                os.remove(p)
        return f"Ocorreu um erro ao processar o vídeo: {str(e)}"

# Interface visual do Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🎬 Gerador de Legendas por URL (Hugging Face)")
    gr.Markdown("Cole a URL de um vídeo para extrair o áudio e gerar a transcrição em texto.")
    
    with gr.Row():
        url_input = gr.Textbox(label="URL do Vídeo (Instagram, Facebook, etc)", placeholder="Cole o link aqui...")
        btn = gr.Button("Gerar Legenda", variant="primary")
        
    output_text = gr.Textbox(label="Legenda Gerada", lines=10)
    
    btn.click(fn=processar_video_por_url, inputs=url_input, outputs=output_text, api_name="predict")

# O launch não precisa da porta 7860 explícita no Hugging Face, mas funciona com ela
demo.launch(server_name="0.0.0.0", server_port=7860)
