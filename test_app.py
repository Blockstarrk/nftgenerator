import sys
sys.path.append('.')

from flask import Flask, render_template, request, jsonify, send_from_directory
from generate_nfts import generate_unique_nft, categories
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'test-secret-key'  # Change in production (different from normal)

@app.route('/nfts/<path:filename>')
def serve_nft(filename):
    return send_from_directory('generated_nfts', filename)

@app.route('/')
def index():
    return render_template('index.html', has_generated=False, host_type='test')

@app.route('/generate_nft', methods=['POST'])
def generate_nft():
    image_path, metadata = generate_unique_nft(categories)
    
    if image_path and metadata:
        traits = [attr['value'] for attr in metadata['attributes']]
        filename = os.path.basename(image_path)
        image_url = f'/nfts/{filename}'

        return jsonify({
            'success': True,
            'image_url': image_url,
            'traits': traits
        })
    else:
        return jsonify({'success': False, 'error': 'Failed to generate NFT'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)