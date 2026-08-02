const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const loader = document.getElementById("loader");
const form = document.getElementById("uploadForm");

// Click upload box
uploadBox.addEventListener("click", () => {
    fileInput.click();
});

// Show selected file name
fileInput.addEventListener("change", () => {

    if(fileInput.files.length > 0){
        fileName.textContent = "Selected File: " + fileInput.files[0].name;
    }

});

// Drag over
uploadBox.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadBox.style.background="#eef2ff";
});

// Drag leave
uploadBox.addEventListener("dragleave", () => {
    uploadBox.style.background="white";
});

// Drop file
uploadBox.addEventListener("drop", (e) => {

    e.preventDefault();

    const files = e.dataTransfer.files;

    if(files.length > 0){

        fileInput.files = files;

        fileName.textContent = "Selected File: " + files[0].name;
    }

    uploadBox.style.background="white";

});

// Show loader on submit
form.addEventListener("submit", () => {
    loader.style.display="block";
});