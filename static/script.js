const input = document.getElementById('image-input');
const preview = document.querySelector('.preview');

if (input) {
  input.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    preview.innerHTML = `<img src="${url}" alt="preview" />`;
  });
}