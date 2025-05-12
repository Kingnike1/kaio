import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import yt_dlp
import os

def interpretar_erro(e):
    mensagem = str(e).lower()
    if "video unavailable" in mensagem or "this video is private" in mensagem:
        return "⚠️ O vídeo está indisponível ou é privado."
    elif "geo restricted" in mensagem or "not available in your country" in mensagem:
        return "🌍 O vídeo está bloqueado na sua região."
    elif "unsupported url" in mensagem:
        return "❌ URL inválida ou não suportada."
    elif "too many requests" in mensagem or "rate limit" in mensagem:
        return "🚫 Muitas requisições. Tente novamente mais tarde."
    elif "signature extraction" in mensagem:
        return "🔐 Erro ao decodificar a assinatura do vídeo."
    elif "unable to extract" in mensagem:
        return "⚠️ Não foi possível extrair informações do vídeo."
    elif "http error" in mensagem:
        return "🌐 Problema de conexão ou vídeo removido."
    else:
        return f"❌ Erro desconhecido: {e}"

def baixar_conteudo(urls, path, is_playlist, baixar_video, log_callback, update_progress):
    if not os.path.exists(path):
        os.makedirs(path)

    formato = (
        'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
        if baixar_video else
        'bestaudio[ext=m4a]'
    )

    ydl_opts = {
        'format': formato,
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4' if baixar_video else 'm4a'
    }

    total = len(urls)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for index, url in enumerate(urls, 1):
            try:
                log_callback(f"🔗 Baixando ({index}/{total}): {url}")
                ydl.download([url])
                log_callback(f"✅ Sucesso: {url}\n")
            except Exception as e:
                erro_msg = interpretar_erro(e)
                log_callback(f"❌ Falha: {erro_msg} ({url})\n")
            update_progress(index, total)

def selecionar_arquivo(entry):
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
    if caminho:
        entry.delete(0, tk.END)
        entry.insert(0, caminho)

def selecionar_pasta(entry):
    caminho = filedialog.askdirectory()
    if caminho:
        entry.delete(0, tk.END)
        entry.insert(0, caminho)

def iniciar_download():
    links_texto = link_input.get("1.0", tk.END).strip()
    arquivo_links = entry_arquivo.get().strip()
    caminho_destino = entry_destino.get().strip() or os.path.expanduser("~/Downloads")
    is_playlist = var_playlist.get()
    baixar_video = var_video.get()

    urls = []
    if links_texto:
        for linha in links_texto.splitlines():
            if ',' in linha:
                urls.extend(link.strip() for link in linha.split(',') if link.strip())
            else:
                urls.append(linha.strip())
    elif arquivo_links:
        try:
            with open(arquivo_links, 'r', encoding='utf-8') as f:
                urls = [linha.strip() for linha in f if linha.strip()]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo: {e}")
            return
    else:
        messagebox.showwarning("Aviso", "Forneça os links manualmente ou carregue um arquivo .txt.")
        return

    if not urls:
        messagebox.showwarning("Aviso", "Nenhum link válido encontrado.")
        return

    log_output.delete("1.0", tk.END)
    progress_bar["value"] = 0
    progress_bar["maximum"] = len(urls)

    def log(msg):
        log_output.insert(tk.END, msg + "\n")
        log_output.see(tk.END)

    def atualizar_barra(atual, total):
        progress_bar["value"] = atual
        root.update_idletasks()

    baixar_conteudo(urls, caminho_destino, is_playlist, baixar_video, log, atualizar_barra)
    log_output.insert(tk.END, "\n🏁 Concluído!\n")

# GUI
root = tk.Tk()
root.title("Downloader YouTube (Áudio/Vídeo)")
root.geometry("700x640")

# Frame dos links
tk.Label(root, text="Links (1 por linha ou separados por vírgula):").pack(anchor="w", padx=10)
link_input = scrolledtext.ScrolledText(root, height=6)
link_input.pack(fill="x", padx=10, pady=5)

# Ou carregar de arquivo
frame_file = tk.Frame(root)
frame_file.pack(fill="x", padx=10, pady=5)
tk.Label(frame_file, text="Ou carregar links de arquivo (.txt):").pack(anchor="w")
entry_arquivo = tk.Entry(frame_file)
entry_arquivo.pack(side="left", fill="x", expand=True)
tk.Button(frame_file, text="Selecionar Arquivo", command=lambda: selecionar_arquivo(entry_arquivo)).pack(side="left", padx=5)

# Pasta de destino
frame_destino = tk.Frame(root)
frame_destino.pack(fill="x", padx=10, pady=5)
tk.Label(frame_destino, text="Pasta de destino:").pack(anchor="w")
entry_destino = tk.Entry(frame_destino)
entry_destino.pack(side="left", fill="x", expand=True)
tk.Button(frame_destino, text="Selecionar Pasta", command=lambda: selecionar_pasta(entry_destino)).pack(side="left", padx=5)

# Opções
frame_opts = tk.Frame(root)
frame_opts.pack(fill="x", padx=10, pady=5)

var_playlist = tk.BooleanVar()
var_video = tk.BooleanVar()

tk.Checkbutton(frame_opts, text="É playlist", variable=var_playlist).pack(side="left", padx=5)
tk.Checkbutton(frame_opts, text="Baixar vídeo completo (.mp4)", variable=var_video).pack(side="left", padx=5)

# Botão de download
tk.Button(root, text="📥 Iniciar Download", command=iniciar_download, bg="green", fg="white").pack(pady=10)

# Barra de progresso
progress_bar = ttk.Progressbar(root, length=500, mode='determinate')
progress_bar.pack(pady=5)

# Área de log
tk.Label(root, text="Log de status:").pack(anchor="w", padx=10)
log_output = scrolledtext.ScrolledText(root, height=15)
log_output.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
