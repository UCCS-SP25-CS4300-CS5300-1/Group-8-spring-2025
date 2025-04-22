const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture');
const uploadBtn = document.getElementById('upload');
const retakeBtn = document.getElementById('retake');
const launchCameraBtn = document.getElementById('launchCameraBtn');
const captureErrorMessage = document.getElementById('captureErrorMessage');

let cameraStream = null;

// Request access to the camera
function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } } })
        .then(stream => {
            cameraStream = stream;
            video.srcObject = stream;
        })
        .catch(error => {
            console.error('Camera access denied:', error);
            captureErrorMessage.style.display = 'block';
        });
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
}

retakeBtn.addEventListener('click', function() {
    canvas.style.display = 'none';
    video.style.display = 'block';
    uploadBtn.style.display = 'none';
    retakeBtn.style.display = 'none';
    captureBtn.style.display = 'block';

    startCamera();
});

launchCameraBtn.addEventListener('click', function() {
    canvas.style.display = 'none';
    video.style.display = 'block';
    uploadBtn.style.display = 'none';
    retakeBtn.style.display = 'none';
    captureBtn.style.display = 'block';

    startCamera();
});

captureBtn.addEventListener('click', function () {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to a data URL and create a file object
    canvas.toBlob(blob => {
        const file = new File([blob], "captured_image.jpg", { type: "image/jpeg" });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.getElementById('image').files = dataTransfer.files;
        uploadBtn.style.display = 'block'; // Show upload button
        
        canvas.style.display = 'block';
        video.style.display = 'none';
        retakeBtn.style.display = 'block';
        uploadBtn.style.display = 'block';
        captureBtn.style.display = 'none';

        stopCamera();
    }, "image/jpeg");
});

const captureModal = document.getElementById('captureModal');
captureModal.addEventListener('hidden.bs.modal', () => {
    stopCamera();
});