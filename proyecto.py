#ggs
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de AI", page_icon="icono,jpg", layout= "centered")

st.title("Mi primera app de st")

nombre = st.text_input("¿Cual es su nombre?")

if st.button("saludar"):
    st.write(f"¡Hola {nombre}, Bienvenido a mi chat!")

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
modelname= ['LLaMa 8 (para tareas generales)', 'LLaMa 70 (para tareas complejas)', 'Mistral (compresión)']
def config():
    st.title("LLaMA")
    st.sidebar.title("Configurar AI")
    elegirModelName=st.sidebar.selectbox("Elegi un modelo", options=modelname,index=0)
    elegirModelo=modelos[modelname.index(elegirModelName)]
    return elegirModelo


#Clase 7
def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model= modelo,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )



#clase 8
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role":rol, "content":contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])
def area_chat():
    contenedorDelChat=st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes=[]



#clase 9











def generar_respuesta(chat_completo):
      respuesta_completa = ""
      for frase in chat_completo:
          if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
      return respuesta_completa
def main():
    modelo = config()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribí tu mensaje:")
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
    
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")

                st.rerun()

if __name__ == "__main__":
    main()