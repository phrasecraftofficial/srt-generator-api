# srt-generator-api
Using HuggingFace

Aqui está o **fluxo resumido, completo e seguro** da sua arquitetura moderna, sem dependências de plataformas instáveis e com tudo no seu devido lugar:

---

### 🔄 Fluxo de Funcionamento (Passo a Passo)

1. **Apresentação (Front-end):**
* O seu site fica hospedado de graça na **Vercel** ou **Netlify**.
* O usuário entra no site e envia o link de um Short, Reels ou vídeo.


2. **Orquestração (Hugging Face Spaces):**
* O site envia o link para a API do seu Space no **Hugging Face** (rodando via Docker).
* O Hugging Face baixa o vídeo, extrai o **áudio** e gera o arquivo de legenda **`.srt`**.


3. **Armazenamento de Mídia (Backblaze B2):**
* O Hugging Face faz o upload do **áudio** e do **`.srt`** gerados diretamente para o seu bucket no **Backblaze B2**.
* O B2 devolve os links públicos desses arquivos.


4. **Banco de Dados & Realtime (PocketBase):**
* O Hugging Face salva as referências (URLs do B2, status, etc.) fazendo um `POST` no **PocketBase** (hospedado no Fly.io / Render, com volume persistente).
* O PocketBase avisa instantaneamente o seu site via **Realtime (WebSockets)**.
* O site na Vercel recebe a atualização na hora e exibe o resultado pronto para o usuário.


5. **Segurança e Backups:**
* O **código-fonte** do projeto fica versionado e seguro no **GitHub**.
* O arquivo do banco de dados do PocketBase (`data.db`) tem seus **backups salvos automaticamente no Backblaze B2** (evitando o limite de tamanho e riscos do GitHub).
