import sys
sys.path.append('.')

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from generate_nfts import generate_unique_nft, categories
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'normal-secret-key'  # Change in production

@app.route('/nfts/<path:filename>')
def serve_nft(filename):
    return send_from_directory('generated_nfts', filename)

@app.route('/')
def index():
    if 'has_generated' not in session:
        session['has_generated'] = False
    return render_template('index.html', has_generated=session['has_generated'], host_type='normal')

@app.route('/generate_nft', methods=['POST'])
def generate_nft():
    if session.get('has_generated', False):
        return jsonify({'success': False, 'error': 'You have already generated an NFT. Only one NFT per user is allowed.'})

    image_path, metadata = generate_unique_nft(categories)
    
    if image_path and metadata:
        traits = [attr['value'] for attr in metadata['attributes']]
        filename = os.path.basename(image_path)
        image_url = f'/nfts/{filename}'

        session['has_generated'] = True

        return jsonify({
            'success': True,
            'image_url': image_url,
            'traits': traits
        })
    else:
        return jsonify({'success': False, 'error': 'Failed to generate NFT'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)