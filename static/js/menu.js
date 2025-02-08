function showMenuModal(event) {
    event.preventDefault();
    document.getElementById('menuModal').style.display = 'block';
}

document.querySelector('.close-modal').addEventListener('click', function() {
    document.getElementById('menuModal').style.display = 'none';
});

document.getElementById('menuModal').addEventListener('click', function(e) {
    if (e.target === this) {
        this.style.display = 'none';
    }
});