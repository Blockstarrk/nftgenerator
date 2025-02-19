document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');

    // Add click event listener
    generateBtn.addEventListener('click', generateNFT);

    // Check if button should be disabled (only for normal host)
    if (window.location.port === '5000') { // Normal host
        if (document.getElementById('generateBtn').classList.contains('disabled')) {
            generateBtn.title = "You have already generated an NFT";
            generateBtn.classList.add('disabled'); // Ensure disabled class is applied
            generateBtn.removeEventListener('click', generateNFT); // Prevent further clicks
        }
    }
});

function generateNFT() {
    const generateBtn = document.getElementById('generateBtn');

    // Only check for restriction on normal host
    if (window.location.port === '5000' && generateBtn.classList.contains('disabled')) {
        alert('You have already generated an NFT. Only one NFT per user is allowed.');
        return;
    }

    fetch('/generate_nft', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('nftImage').src = data.image_url;
                document.getElementById('nftImage').style.display = 'block';

                const traitsList = document.getElementById('Traits').querySelector('ul');
                traitsList.innerHTML = '';
                data.traits.forEach(trait => {
                    const li = document.createElement('li');
                    li.textContent = trait;
                    traitsList.appendChild(li);
                });

                // Disable button only on normal host after generation
                if (window.location.port === '5000') {
                    generateBtn.classList.add('disabled');
                    generateBtn.removeEventListener('click', generateNFT);
                }
            } else {
                alert(data.error);
            }
        })
        .catch(error => console.error('Fetch error:', error)); // Log error for debugging
}