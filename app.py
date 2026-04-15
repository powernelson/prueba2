from rembg import remove
from PIL import Image
from flask import Flask, render_template, request, send_file
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def home():
    
    imagen_para_html = None
    
    
    if request.method == 'POST':
        if 'imagen' not in request.files:
            return 'No se subió ninguna imagen', 400
        
        file = request.files['imagen'] # aqui tomamos los bytes 
        
        if file.filename == '':
            return 'No seleccionaste ningún archivo', 400
        input_image  =  Image.open(file.stream) # aaui esos bytes transformamos a  la imagen 
        
        remove_imagen = remove(input_image) # AHORA REMOVEMOS EL FONDO
        
        
        # ahora para devolver la imagen 
        img_io = io.BytesIO()
        remove_imagen.save(img_io, 'PNG')
        img_io.seek(0)
        
        # enviamos la imagen al html 
        #return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='sin_fondo.png')
        # Esto transforma la imagen en un string tipo "iVBORw0KGgo..."
        imagen_para_html = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
    return render_template('index.html' , imagen_b64 = imagen_para_html)

if __name__ == '__main__':
    app.run(debug=True)
        
        
        
        
        